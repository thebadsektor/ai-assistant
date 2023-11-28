import React, { useState, useEffect, useMemo } from 'react';
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

function App() {
  const [response, setResponse] = useState("");
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  // useMemo to initialize WebSocket
  const WS = useMemo(() => new WebSocket("ws://localhost:8000/ws"), []);

  useEffect(() => {
    WS.onmessage = (event) => {
      setLoading(false);
      setResponse(marked.parse(event.data));
    };

    return () => {
      WS.close();
    };
  }, [WS]); // Dependency array now correctly references the memoized WS

  const handleKeyUp = (e) => {
    if (e.key === "Enter") {
      setResponse('');
      setLoading(true);
      WS.send(question);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            AI Assistant 🤓
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
        {/* {!response && loading && <Typography>Loading...</Typography>} */}
        {!response && loading && (<>
                        <Skeleton />
                        <Skeleton animation="wave" />
                        <Skeleton animation={false} /></>)}
        {response && <div dangerouslySetInnerHTML={{ __html: response }} />}
      </Container>
    </ThemeProvider>
  );
}

export default App;