const express = require('express');
const router = express.Router();

// Service status endpoint
router.get('/status', (req, res) => {
  res.json({
    services: [
      { name: 'file-indexer', status: 'active', port: 8010 },
      { name: 'learning-journal', status: 'active', port: 8011 },
      { name: 'notification', status: 'active', port: 8012 },
      { name: 'session-manager', status: 'active', port: 8013 },
      { name: 'voice-processor', status: 'active', port: 8014 }
    ],
    timestamp: new Date().toISOString()
  });
});

// File indexer service endpoint
router.post('/file-indexer/index', (req, res) => {
  res.json({
    message: 'File indexing request received',
    data: req.body,
    timestamp: new Date().toISOString()
  });
});

// Learning journal service endpoint
router.post('/learning-journal/log', (req, res) => {
  res.json({
    message: 'Learning journal log request received',
    data: req.body,
    timestamp: new Date().toISOString()
  });
});

// Notification service endpoint
router.post('/notification/send', (req, res) => {
  res.json({
    message: 'Notification send request received',
    data: req.body,
    timestamp: new Date().toISOString()
  });
});

module.exports = router;
