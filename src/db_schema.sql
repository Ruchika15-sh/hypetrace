CREATE TABLE brands (
    brand_id SERIAL PRIMARY KEY,
    brand_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE trend_metrics (
    id SERIAL PRIMARY KEY,
    brand_id INT REFERENCES brands(brand_id),
    date DATE NOT NULL,
    search_interest INT
);

CREATE TABLE stock_prices (
    id SERIAL PRIMARY KEY,
    brand_id INT REFERENCES brands(brand_id),
    date DATE NOT NULL,
    close_price NUMERIC
);

CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    brand_id INT REFERENCES brands(brand_id),
    celebrity VARCHAR(150),
    event_date DATE NOT NULL,
    event_type VARCHAR(50),
    occasion VARCHAR(200),
    description TEXT,
    source_link TEXT
);