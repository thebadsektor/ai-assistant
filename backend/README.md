## Environment Setup

Copy the `.env.template` file to `.env` and fill in the necessary environment variables.

- `git add .env.template`
- `git commit -m "Add .env template"`

## Websocket Handling

### Backend

#### src/routes/websocket.py

1. Handle Connection Acceptance and Disconnection:
   - When a client connects, accept the connection and add it to a list of active connections.
   - When a client disconnects, remove it from the list of active connections.
2. Error Handling:
   - Catch exceptions that may occur during message handling.
   - Log errors for debugging purposes.
3. Graceful Closure:
   - Ensure that when the WebSocket connection is closed, it is removed from the list of active connections.
   - Handle client disconnections gracefully.

### React Frontend

#### src/App.js

1. Reconnection Logic:
   - Implement a strategy to automatically try to reconnect when the WebSocket connection is lost.
   - Use a backoff strategy to avoid overwhelming the server with reconnection attempts.
2. Connection Monitoring:
   - Monitor the WebSocket connection status (open, close, error) and take appropriate actions.
   - Inform the user when the WebSocket connection is lost and when it's trying to reconnect.
3. Graceful Shutdown:
   - Ensure that the WebSocket connection is closed properly when the user leaves the page or when the component is unmounted.
