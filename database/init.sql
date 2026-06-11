CREATE TABLE IF NOT EXISTS api_clients (
  id SERIAL PRIMARY KEY,
  name VARCHAR(80) NOT NULL,
  api_key VARCHAR(120) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);

INSERT INTO api_clients (name, api_key)
VALUES ('demo', 'demo-key')
ON CONFLICT (api_key) DO NOTHING;

CREATE TABLE IF NOT EXISTS subscriptions (
  id SERIAL PRIMARY KEY,
  client_id INTEGER REFERENCES api_clients(id),
  base VARCHAR(3) NOT NULL,
  quote VARCHAR(3) NOT NULL,
  target_rate DOUBLE PRECISION NOT NULL,
  direction VARCHAR(4) NOT NULL DEFAULT 'both',
  notify_url VARCHAR(300) NOT NULL,
  email VARCHAR(120) DEFAULT '',
  active BOOLEAN DEFAULT TRUE
);

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name='subscriptions' AND column_name='direction'
  ) THEN
    ALTER TABLE subscriptions ADD COLUMN direction VARCHAR(4) NOT NULL DEFAULT 'both';
  END IF;
END $$;
