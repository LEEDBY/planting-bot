-- database/init_db.sql

CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    language_code VARCHAR(5) DEFAULT 'en',
    referrer_id BIGINT,
    referral_count INTEGER DEFAULT 0,
    donated BOOLEAN DEFAULT FALSE,
    balance NUMERIC DEFAULT 0.0,
    FOREIGN KEY (referrer_id) REFERENCES users (user_id)
);
