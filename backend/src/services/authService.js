const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');
const db = require('../database');
const config = require('../config');

/**
 * Register a new user
 */
async function register(email, password, fullName, phoneNumber = null) {
  try {
    // Check if user already exists
    const existingUser = await db.query(
      'SELECT id FROM users WHERE email = $1',
      [email]
    );
    
    if (existingUser.rows.length > 0) {
      throw new Error('User already exists with this email');
    }
    
    // Hash password
    const passwordHash = await bcrypt.hash(password, 10);
    
    // Create user
    const result = await db.query(
      `INSERT INTO users (id, email, password_hash, full_name, phone_number, created_at, is_active)
       VALUES ($1, $2, $3, $4, $5, NOW(), true)
       RETURNING id, email, full_name, phone_number, created_at`,
      [uuidv4(), email, passwordHash, fullName, phoneNumber]
    );
    
    return result.rows[0];
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
}

/**
 * Login user and generate JWT tokens
 */
async function login(email, password) {
  try {
    // Find user
    const result = await db.query(
      'SELECT id, email, password_hash, full_name, is_active FROM users WHERE email = $1',
      [email]
    );
    
    if (result.rows.length === 0) {
      throw new Error('Invalid email or password');
    }
    
    const user = result.rows[0];
    
    if (!user.is_active) {
      throw new Error('Account is inactive');
    }
    
    // Verify password
    const isValidPassword = await bcrypt.compare(password, user.password_hash);
    
    if (!isValidPassword) {
      throw new Error('Invalid email or password');
    }
    
    // Update last login
    await db.query(
      'UPDATE users SET last_login = NOW() WHERE id = $1',
      [user.id]
    );
    
    // Generate tokens
    const accessToken = generateAccessToken(user);
    const refreshToken = generateRefreshToken(user);
    
    // Store refresh token
    await storeRefreshToken(user.id, refreshToken);
    
    return {
      user: {
        id: user.id,
        email: user.email,
        fullName: user.full_name,
      },
      accessToken,
      refreshToken,
    };
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
}

/**
 * Generate access token
 */
function generateAccessToken(user) {
  return jwt.sign(
    { 
      userId: user.id, 
      email: user.email 
    },
    config.jwt.secret,
    { expiresIn: config.jwt.expiresIn }
  );
}

/**
 * Generate refresh token
 */
function generateRefreshToken(user) {
  return jwt.sign(
    { 
      userId: user.id,
      type: 'refresh'
    },
    config.jwt.secret,
    { expiresIn: config.jwt.refreshExpiresIn }
  );
}

/**
 * Store refresh token in database
 */
async function storeRefreshToken(userId, token) {
  const tokenHash = await bcrypt.hash(token, 10);
  const expiresAt = new Date();
  expiresAt.setDate(expiresAt.getDate() + 7); // 7 days
  
  await db.query(
    `INSERT INTO refresh_tokens (id, user_id, token_hash, expires_at, created_at)
     VALUES ($1, $2, $3, $4, NOW())`,
    [uuidv4(), userId, tokenHash, expiresAt]
  );
}

/**
 * Refresh access token
 */
async function refreshAccessToken(refreshToken) {
  try {
    // Verify refresh token
    const decoded = jwt.verify(refreshToken, config.jwt.secret);
    
    if (decoded.type !== 'refresh') {
      throw new Error('Invalid token type');
    }
    
    // Get user
    const result = await db.query(
      'SELECT id, email, full_name, is_active FROM users WHERE id = $1',
      [decoded.userId]
    );
    
    if (result.rows.length === 0 || !result.rows[0].is_active) {
      throw new Error('User not found or inactive');
    }
    
    const user = result.rows[0];
    
    // Generate new access token
    const accessToken = generateAccessToken(user);
    
    return {
      accessToken,
      user: {
        id: user.id,
        email: user.email,
        fullName: user.full_name,
      },
    };
  } catch (error) {
    console.error('Refresh token error:', error);
    throw error;
  }
}

/**
 * Verify JWT token
 */
function verifyToken(token) {
  try {
    return jwt.verify(token, config.jwt.secret);
  } catch (error) {
    throw new Error('Invalid or expired token');
  }
}

/**
 * Get user by ID
 */
async function getUserById(userId) {
  const result = await db.query(
    'SELECT id, email, full_name, phone_number, created_at FROM users WHERE id = $1 AND is_active = true',
    [userId]
  );
  
  return result.rows[0] || null;
}

module.exports = {
  register,
  login,
  refreshAccessToken,
  generateAccessToken,
  verifyToken,
  getUserById,
};
