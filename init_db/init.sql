-- Создаем таблицу tickers
CREATE TABLE tickers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Создаем таблицу prices
CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    price DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ticker_id INTEGER REFERENCES tickers(id)
);

-- Создаем таблицу news
CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(50) NOT NULL,
    source VARCHAR(255) NOT NULL,
    summary_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создаем таблицу users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создаем индексы для улучшения производительности
CREATE INDEX idx_tickers_name ON tickers(name);
CREATE INDEX idx_news_ticker ON news(ticker);
CREATE INDEX idx_news_created_at ON news(created_at);
CREATE INDEX idx_users_email ON users(email);