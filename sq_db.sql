CREATE TABLE IF NOT EXISTS log (
    id SERIAL PRIMARY KEY,
    date_order TEXT NOT NULL,
    name_customer TEXT NOT NULL,
    brand_car TEXT NOT NULL,
    year_car TEXT NOT NULL,
    number_car TEXT NOT NULL,
    text_order TEXT NOT NULL,
    id_act INTEGER DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS act (
    id SERIAL PRIMARY KEY,
    id_act INTEGER NOT NULL,
    date_act TEXT NOT NULL,
    name_work TEXT NOT NULL,
    price_work INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS stock_plus (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
quantity INTEGER NOT NULL,
price_unit INTEGER NOT NULL
);

CREATE TABLE stock_minus (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price_unit INTEGER NOT NULL,
    id_act INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS employees (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
profession TEXT NOT NULL
);



