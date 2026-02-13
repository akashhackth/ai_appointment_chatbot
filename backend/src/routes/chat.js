const express = require('express');
const { body, param, query } = require('express-validator');
const chatService = require('../services/chatService');
const authService = require('../services/authService');
const { authenticate } = require('../middleware/auth');
const { handleValidationErrors } = require('../middleware/validation');

const router = express.Router();

/**
 * POST /api/chat/message
 * Send a message to the chatbot
 */
router.post('/message',
  authenticate,
  [
    body('message').trim().notEmpty().withMessage('Message is required'),
    body('sessionId').optional().isUUID(),
  ],
  handleValidationErrors,
  async (req, res, next) => {
    try {
      const { message, sessionId } = req.body;
      const userId = req.userId;
      
      // Send message to AI service
      const response = await chatService.sendMessage(userId, message, sessionId);
      
      res.json({
        success: true,
        ...response,
      });
    } catch (error) {
      next(error);
    }
  }
);

/**
 * GET /api/chat/history/:sessionId
 * Get chat history for a session
 */
router.get('/history/:sessionId',
  authenticate,
  [
    param('sessionId').isUUID(),
    query('limit').optional().isInt({ min: 1, max: 100 }),
  ],
  handleValidationErrors,
  async (req, res, next) => {
    try {
      const { sessionId } = req.params;
      const limit = parseInt(req.query.limit) || 50;
      
      const messages = await chatService.getChatHistory(sessionId, limit);
      
      res.json({
        sessionId,
        messages,
      });
    } catch (error) {
      next(error);
    }
  }
);

/**
 * GET /api/chat/sessions
 * Get user's chat sessions
 */
router.get('/sessions',
  authenticate,
  async (req, res, next) => {
    try {
      const sessions = await chatService.getUserSessions(req.userId);
      
      res.json({
        sessions,
      });
    } catch (error) {
      next(error);
    }
  }
);

/**
 * POST /api/chat/session
 * Create a new chat session
 */
router.post('/session',
  authenticate,
  async (req, res, next) => {
    try {
      const sessionId = await chatService.createSession(req.userId);
      
      res.status(201).json({
        sessionId,
        message: 'Session created',
      });
    } catch (error) {
      next(error);
    }
  }
);

/**
 * DELETE /api/chat/session/:sessionId
 * End a chat session
 */
router.delete('/session/:sessionId',
  authenticate,
  [
    param('sessionId').isUUID(),
  ],
  handleValidationErrors,
  async (req, res, next) => {
    try {
      await chatService.endSession(req.params.sessionId, req.userId);
      
      res.json({
        message: 'Session ended',
      });
    } catch (error) {
      next(error);
    }
  }
);

/**
 * POST /api/chatbot/token
 * Generate short-lived chatbot access token
 */
router.post('/chatbot/token',
  authenticate,
  async (req, res, next) => {
    try {
      const user = await authService.getUserById(req.userId);
      
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }
      
      // Generate a short-lived token (5 minutes)
      const token = authService.generateAccessToken({
        id: user.id,
        email: user.email,
      });
      
      res.json({
        token,
        expiresIn: 300, // 5 minutes in seconds
        user: {
          id: user.id,
          email: user.email,
        },
      });
    } catch (error) {
      next(error);
    }
  }
);

module.exports = router;
