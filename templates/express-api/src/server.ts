/**
 * {{PROJECT_NAME}} Express Server
 * A modern TypeScript Express API
 */

import express from 'express'
import cors from 'cors'
import helmet from 'helmet'
import morgan from 'morgan'
import compression from 'compression'
import { config } from './config/config'
import { errorHandler } from './middleware/errorHandler'
import { apiRoutes } from './routes/api'

const app = express()
const PORT = process.env.PORT || {{port}}

// Security middleware
app.use(helmet())
app.use(cors())
app.use(compression())

// Logging
app.use(morgan('combined'))

// Body parsing middleware
app.use(express.json({ limit: '10mb' }))
app.use(express.urlencoded({ extended: true }))

// Routes
app.get('/', (req, res) => {
  res.json({
    message: 'Welcome to {{PROJECT_NAME}} API!',
    version: '1.0.0',
    endpoints: {
      health: '/health',
      api: '/api/v1'
    }
  })
})

app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: '{{PROJECT_NAME}}',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  })
})

// API routes
app.use('/api/v1', apiRoutes)

// Error handling middleware (should be last)
app.use(errorHandler)

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Not Found',
    message: 'The requested resource was not found',
    path: req.originalUrl
  })
})

// Start server
app.listen(PORT, () => {
  console.log(`🚀 {{PROJECT_NAME}} server running on port ${PORT}`)
  console.log(`📚 Health check: http://localhost:${PORT}/health`)
  console.log(`🌐 API docs: http://localhost:${PORT}/api/v1`)
})

export default app