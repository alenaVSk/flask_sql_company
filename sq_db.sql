CREATE TABLE IF NOT EXISTS log (
id integer PRIMARY KEY AUTOINCREMENT,
date_order text NOT NULL,
name_customer text NOT NULL,
brand_car text NOT NULL,
year_car text NOT NULL,
number_car text NOT NULL,
text_order text NOT NULL,
id_act integer
FOREIGN KEY (id_act) REFERENCES act (id)
);


CREATE TABLE IF NOT EXISTS stock_plus (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
quantity integer NOT NULL,
price_unit integer NOT NULL
);


CREATE TABLE stock_minus (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
quantity INTEGER NOT NULL,
price_unit INTEGER NOT NULL,
id_act INTEGER NOT NULL,
FOREIGN KEY (id_act) REFERENCES act(id)
);

CREATE TABLE IF NOT EXISTS employees (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
profession text NOT NULL
);

CREATE TABLE IF NOT EXISTS act (
id integer PRIMARY KEY AUTOINCREMENT,
date_act text NOT NULL,
name_work text NOT NULL,
price_work integer NOT NULL
);

