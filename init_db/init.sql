CREATE TABLE tickers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    price DOUBLE PRECISION NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    ticker_id INTEGER REFERENCES tickers(id)
);

CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(50) NOT NULL,
    source VARCHAR(255) NOT NULL,
    summary_text TEXT NOT NULL,
    price_difference DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    login VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tickers_name ON tickers(name);
CREATE INDEX idx_news_ticker ON news(ticker);
CREATE INDEX idx_news_created_at ON news(created_at);
CREATE INDEX idx_users_email ON users(email);