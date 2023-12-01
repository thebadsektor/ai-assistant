import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  TextField,
  Box,
  Skeleton,
  createTheme,
  ThemeProvider,
  CssBaseline
} from '@mui/material';
import { marked } from 'marked';

const theme = createTheme({
  palette: {
    mode: 'dark',
  },
});

const WS_URL = "ws://localhost:8000/ws";
const RECONNECT_INTERVAL = 2000; // 2 seconds for reconnection attempts

function App() {
  const [response, setResponse] = useState("");
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [websocket, setWebsocket] = useState(null);

  useEffect(() => {
    connectWebSocket();

    return () => {
      if (websocket) websocket.close();
    };
  }, []);

  const connectWebSocket = () => {
    const ws = new WebSocket(WS_URL);

    ws.onopen = () => {
      console.log("WebSocket Connected");
    };

    ws.onmessage = (event) => {
      setLoading(false);
      setResponse(marked.parse(event.data));
    };

    ws.onclose = () => {
      console.log("WebSocket Disconnected. Attempting to reconnect...");
      setTimeout(connectWebSocket, RECONNECT_INTERVAL);
    };

    ws.onerror = (error) => {
      console.error("WebSocket Error:", error);
    };

    setWebsocket(ws);
  };

  const handleKeyUp = (e) => {
    if (e.key === "Enter" && websocket && websocket.readyState === WebSocket.OPEN) {
      setResponse('');
      setLoading(true);
      websocket.send(question);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            AI Assistant 🤓 v0.0.2
          </Typography>
          <TextField
            id="outlined-basic"
            label="Ask me Anything"
            variant="outlined"
            style={{ width: '100%' }}
            value={question}
            disabled={loading}
            onChange={e => setQuestion(e.target.value)}
            onKeyUp={handleKeyUp}
          />
        </Box>
        {!response && loading && (
          <>
            <Skeleton />
            <Skeleton animation="wave" />
            <Skeleton animation={false} />
          </>
        )}
        {response && <div dangerouslySetInnerHTML={{ __html: response }} />}
      </Container>
    </ThemeProvider>
  );
}

export default App;
