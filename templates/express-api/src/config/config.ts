/**
 * Configuration for {{PROJECT_NAME}}
 */

import dotenv from 'dotenv'

dotenv.config()

export const config = {
  port: process.env.PORT || {{port}},
  nodeEnv: process.env.NODE_ENV || 'development',
  
  // Database (example)
  database: {
    url: process.env.DATABASE_URL || 'sqlite://{{PROJECT_NAME}}.db'
  },
  
  // JWT (example)
  jwt: {
    secret: process.env.JWT_SECRET || 'your-secret-key-change-in-production',
    expiresIn: process.env.JWT_EXPIRES_IN || '24h'
  },
  
  // CORS
  cors: {
    origin: process.env.CORS_ORIGIN || '*',
    credentials: true
  },
  
  // Rate limiting
  rateLimit: {
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100 // limit each IP to 100 requests per windowMs
  }
}