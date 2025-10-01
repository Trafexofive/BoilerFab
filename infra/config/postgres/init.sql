-- BoilerFab PostgreSQL Initialization Script
-- Create tables for advanced features (when database profile is enabled)

-- Extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Templates table for advanced template management
CREATE TABLE IF NOT EXISTS templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    version VARCHAR(50) DEFAULT '1.0.0',
    author VARCHAR(255),
    license VARCHAR(100),
    tags TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    active BOOLEAN DEFAULT true
);

-- Template parameters table
CREATE TABLE IF NOT EXISTS template_parameters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    template_id UUID REFERENCES templates(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    description TEXT,
    required BOOLEAN DEFAULT false,
    default_value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Generation history table
CREATE TABLE IF NOT EXISTS generation_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    template_name VARCHAR(255) NOT NULL,
    project_name VARCHAR(255) NOT NULL,
    parameters JSONB,
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    client_ip INET,
    success BOOLEAN DEFAULT true,
    error_message TEXT
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_templates_name ON templates(name);
CREATE INDEX IF NOT EXISTS idx_templates_active ON templates(active);
CREATE INDEX IF NOT EXISTS idx_template_parameters_template_id ON template_parameters(template_id);
CREATE INDEX IF NOT EXISTS idx_generation_history_template ON generation_history(template_name);
CREATE INDEX IF NOT EXISTS idx_generation_history_generated_at ON generation_history(generated_at);

-- Insert default templates metadata (optional)
INSERT INTO templates (name, description, author, tags) VALUES
  ('fastapi-minimal', 'A minimal FastAPI project template', 'BoilerFab', ARRAY['python', 'fastapi', 'api']),
  ('flask-api', 'Modern Flask REST API', 'BoilerFab', ARRAY['python', 'flask', 'api']),
  ('universal-makefile', 'Universal Docker Compose Makefile', 'BoilerFab', ARRAY['makefile', 'docker', 'devops'])
ON CONFLICT (name) DO NOTHING;