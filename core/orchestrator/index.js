const express = require('express');
const cors = require('cors');
const helmet = require('helmet');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    service: 'orchestrator',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Orchestrator status endpoint
app.get('/api/status', (req, res) => {
  res.json({
    message: 'ZombieCoder Orchestrator is running',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    activeTasks: 0,
    queuedTasks: 0
  });
});

// Task management endpoints
app.post('/api/tasks/create', (req, res) => {
  const { taskType, data, priority = 'normal' } = req.body;
  
  res.json({
    message: 'Task created successfully',
    taskId: `task_${Date.now()}`,
    taskType,
    data,
    priority,
    status: 'queued',
    timestamp: new Date().toISOString()
  });
});

app.get('/api/tasks/:taskId', (req, res) => {
  const { taskId } = req.params;
  
  res.json({
    taskId,
    status: 'completed',
    result: 'Task completed successfully',
    timestamp: new Date().toISOString()
  });
});

// Agent coordination endpoints
app.post('/api/agents/coordinate', (req, res) => {
  const { agents, task } = req.body;
  
  res.json({
    message: 'Agent coordination initiated',
    coordinationId: `coord_${Date.now()}`,
    agents,
    task,
    status: 'active',
    timestamp: new Date().toISOString()
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({
    error: 'Internal Server Error',
    message: err.message
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Not Found',
    message: 'The requested resource was not found'
  });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`🎯 Orchestrator server running on port ${PORT}`);
  console.log(`📊 Health check: http://localhost:${PORT}/health`);
  console.log(`🔌 API status: http://localhost:${PORT}/api/status`);
});

module.exports = app;
