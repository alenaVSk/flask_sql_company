CREATE TABLE IF NOT EXISTS act_foreign_key (
id integer PRIMARY KEY AUTOINCREMENT,
date_order text NOT NULL,
date_act text NOT NULL,
number_car text NOT NULL
);


CREATE TABLE IF NOT EXISTS act_work (
id integer PRIMARY KEY AUTOINCREMENT,
act_id int NOT NULL,
work_completed text NOT NULL,
name_work text NOT NULL,
price_work int NOT NULL,
FOREIGN KEY (act_id) REFERENCES act_foreign_key (id)
);


CREATE TABLE IF NOT EXISTS act_materials (
id integer PRIMARY KEY AUTOINCREMENT,
act_id int NOT NULL,
materials text NOT NULL,
price_materials int NOT NULL,
quantity int NOT NULL,
FOREIGN KEY (act_id) REFERENCES act_foreign_key (id)