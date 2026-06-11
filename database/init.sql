CREATE TABLE IF NOT EXISTS api_clients (
  id SERIAL PRIMARY KEY,
  name VARCHAR(80) NOT NULL,
  api_key VARCHAR(120) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);

INSERT INTO api_clients (name, api_key)
VALUES ('demo', 'demo-key')
ON CONFLICT (api_key) DO NOTHING;
