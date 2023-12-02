import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  TextField,
  Box,
  Skeleton,
  createTheme,
  ThemeProvider,
  CssBaseline,
  FormControlLabel,
  Switch
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
  const [isStreaming, setIsStreaming] = useState(true); // Add a state to control streaming

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
      setResponse(prev => prev + event.data); // Append new data
      // setResponse(prev => prev + marked.parse(event.data)); // Append new data
      // setResponse(marked.parse(event.data));
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
      const message = JSON.stringify({ query: question, is_streaming: isStreaming });
      websocket.send(message);
    }
  };

  const handleToggleStreaming = (e) => {
    setIsStreaming(e.target.checked)
    console.log(isStreaming)
  }

  const renderedResponse = marked.parse(response);
  // Add UI control for setting streaming mode (if desired)

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            AI Assistant 🤓 v0.0.2.1
          </Typography>
          <div style={{display:'flex', flexDirection:'column', marginBottom:'15px'}} >
            <FormControlLabel control={<Switch defaultChecked onChange={handleToggleStreaming} />} label="Stream Response" />
            <FormControlLabel control={<Switch defaultChecked />} label="Use Context" />
          </div>
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
          {/* Optionally add a switch or button to toggle isStreaming */}
        </Box>
        {!response && loading && (
          <>
            <Skeleton />
            <Skeleton animation="wave" />
            <Skeleton animation={false} />
          </>
        )}
        {response && <div dangerouslySetInnerHTML={{ __html: renderedResponse }} />}
      </Container>
    </ThemeProvider>
  );
}

export default App;