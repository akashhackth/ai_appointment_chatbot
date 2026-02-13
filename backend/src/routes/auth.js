const express = require('express');
const { body } = require('express-validator');
const authService = require('../services/authService');
const { handleValidationErrors } = require('../middleware/validation');

const router = express.Router();

/**
 * POST /api/auth/register
 * Register a new user
 */
router.post('/register',
  [
    body('email').isEmail().normalizeEmail(),
    body('password').isLength({ min: 8 }).withMessage('Password must be at least 8 characters'),
    body('fullName').trim().notEmpty().withMessage('Full name is required'),
    body('phoneNumber').optional().trim(),
  ],
  handleValidationErrors,
  async (req, res, next) => {
    try {
      const { email, password, fullName, phoneNumber } = req.body;
      
      const user = await authService.register(email, password, fullName, phoneNumber);
      
      res.status(201).json({
        message: 'User registered successfully',
        user: {
          id: user.id,
          email: user.email,
          fullName: user.full_name,
        },
      });
    } catch (error) {
      if (error.message.includes('already exists')) {
        return res.status(409).json({ error: error.message });
      }
      next(error);
    }
  }
);

/**
 * POST /api/auth/login
 * Login user and receive JWT tokens
 */
router.post('/login',
  [
    body('email').isEmail().normalizeEmail(),
    body('password').notEmpty(),
  ],
  handleValidationErrors,
  async (req, res, next) => {
    try {
      const { email, password } = req.body;
      
      const result = await authService.login(email, password);
      
      res.json({
        message: 'Login successful',
        ...result,
      });
    } catch (error) {
      if (error.message.includes('Invalid') || error.message.includes('inactive')) {
        return res.status(401).json({ error: error.message });
      }
      next(error);
    }
  }
);

/**
 * POST /api/auth/refresh
 * Refresh access token using refresh token
 */
router.post('/refresh',
  [
    body('refreshToken').notEmpty(),
  ],
  handleValidationErrors,
  async (req, res, next) => {
    try {
      const { refreshToken } = req.body;
      
      const result = await authService.refreshAccessToken(refreshToken);
      
      res.json({
        message: 'Token refreshed',
        ...result,
      });
    } catch (error) {
      return res.status(401).json({ error: 'Invalid or expired refresh token' });
    }
  }
);

/**
 * GET /api/auth/me
 * Get current user info (requires authentication)
 */
router.get('/me',
  require('../middleware/auth').authenticate,
  async (req, res, next) => {
    try {
      const user = await authService.getUserById(req.userId);
      
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }
      
      res.json({ user });
    } catch (error) {
      next(error);
    }
  }
);

module.exports = router;
