CREATE TABLE IF NOT EXISTS log (
id integer PRIMARY KEY AUTOINCREMENT,
date_order text NOT NULL,
name_customer text NOT NULL,
brand_car text NOT NULL,
year_car text NOT NULL,
number_car text NOT NULL,
text_order text NOT NULL
);


CREATE TABLE IF NOT EXISTS stock_plus (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
quantity integer NOT NULL,
price_unit integer NOT NULL
);


CREATE TABLE IF NOT EXISTS stock_minus (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
quantity integer NOT NULL,
price_unit integer NOT NULL
);


CREATE TABLE IF NOT EXISTS employees (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
profession text NOT NULL
);


