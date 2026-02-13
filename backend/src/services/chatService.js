const axios = require('axios');
const config = require('../config');
const db = require('../database');
const { v4: uuidv4 } = require('uuid');

const AI_SERVICE_URL = config.aiService.url;

/**
 * Send message to AI chatbot service
 */
async function sendMessage(userId, message, sessionId = null) {
  try {
    const response = await axios.post(`${AI_SERVICE_URL}/chat`, {
      user_id: userId,
      message: message,
      session_id: sessionId,
    });
    
    return response.data;
  } catch (error) {
    console.error('AI Service error:', error.message);
    throw new Error('Failed to communicate with AI service');
  }
}

/**
 * Get chat history for a session
 */
async function getChatHistory(sessionId, limit = 50) {
  try {
    const result = await db.query(
      `SELECT id, message_type, content, created_at, metadata
       FROM chat_messages
       WHERE session_id = $1
       ORDER BY created_at DESC
       LIMIT $2`,
      [sessionId, limit]
    );
    
    return result.rows.reverse(); // Return in chronological order
  } catch (error) {
    console.error('Get chat history error:', error);
    throw error;
  }
}

/**
 * Get user's active sessions
 */
async function getUserSessions(userId) {
  try {
    const result = await db.query(
      `SELECT id, started_at, ended_at, is_active, session_metadata
       FROM chat_sessions
       WHERE user_id = $1
       ORDER BY started_at DESC
       LIMIT 10`,
      [userId]
    );
    
    return result.rows;
  } catch (error) {
    console.error('Get user sessions error:', error);
    throw error;
  }
}

/**
 * Create a new chat session
 */
async function createSession(userId) {
  try {
    const sessionId = uuidv4();
    
    await db.query(
      `INSERT INTO chat_sessions (id, user_id, started_at, is_active)
       VALUES ($1, $2, NOW(), true)`,
      [sessionId, userId]
    );
    
    return sessionId;
  } catch (error) {
    console.error('Create session error:', error);
    throw error;
  }
}

/**
 * End a chat session
 */
async function endSession(sessionId, userId) {
  try {
    await db.query(
      `UPDATE chat_sessions
       SET ended_at = NOW(), is_active = false
       WHERE id = $1 AND user_id = $2`,
      [sessionId, userId]
    );
    
    return true;
  } catch (error) {
    console.error('End session error:', error);
    throw error;
  }
}

module.exports = {
  sendMessage,
  getChatHistory,
  getUserSessions,
  createSession,
  endSession,
};
