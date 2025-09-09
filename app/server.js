import { WebSocketServer } from 'ws';

const PORT = 3000;
const wss = new WebSocketServer({ port: PORT });

wss.on('connection', (ws) => {
  console.log('Client connected');

  ws.on('message', (message) => {
    try {
      const data = JSON.parse(message);
      console.log('📡 Received data:', data);
    } catch (e) {
      console.error('❌ Failed to parse message:', message);
    }
  });

  ws.on('close', () => {
    console.log('🔌 Client disconnected');
  });
});

console.log(`🚀 WebSocket server listening on ws://localhost:${PORT}`);
