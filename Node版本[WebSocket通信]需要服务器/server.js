const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const { GoogleGenerativeAI } = require('@google/generative-ai');
const cors = require('cors');
const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

const genAI = new GoogleGenerativeAI("这里填API");

app.use(express.json());
app.use(cors());

app.use(express.static('public')); // Serve static files from the 'public' directory

wss.on('connection', (ws) => {
  console.log('Client connected');

  ws.on('message', async (message) => {
    try {
      const { prompt, imageParts } = JSON.parse(message);

      const model = genAI.getGenerativeModel({ model: 'gemini-pro' });
      const result = await model.generateContentStream([prompt, ...imageParts]);

      for await (const chunk of result.stream) {
        const chunkText = chunk.text();
        console.log(chunkText);
        ws.send(chunkText);
      }

      // 等待两秒钟再传递下一段
      setTimeout(() => {
        ws.send(''); // 发送一个空消息表示等待结束
      }, 2000);
    } catch (error) {
      console.error(error);
      ws.send(JSON.stringify({ error: 'Internal Server Error' }));
    }
  });
});

server.listen(process.env.PORT || 3000, () => {
  console.log(`Server is running on http://localhost:${server.address().port}`);
});

