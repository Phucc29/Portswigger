CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);
INSERT INTO users (username, password) VALUES ('administrator', 'password123');

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT
);
INSERT INTO products (name, description) VALUES ('Laptops', 'High performance laptop for engineers.');

CREATE TABLE stocks (
    product_id INTEGER,
    store_id INTEGER,
    count INTEGER
);
INSERT INTO stocks (product_id, store_id, count) VALUES (1, 1, 100), (1, 2, 55);