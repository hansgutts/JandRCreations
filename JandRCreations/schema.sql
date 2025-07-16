DROP TABLE IF EXISTS prod_design;
DROP TABLE IF EXISTS prod_type;
DROP TABLE IF EXISTS prod;
DROP TABLE IF EXISTS custom;
DROP TABLE IF EXISTS options;

CREATE TABLE prod_design (
    prod_design_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prod_design TEXT NOT NULL
);

CREATE TABLE prod_type (
    prod_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prod_type TEXT NOT NULL,
    prod_type_description TEXT NOT NULL,
    prod_design_id TEXT NOT NULL,
    FOREIGN KEY (prod_design_id) REFERENCES prod_design (prod_design_id)
);

CREATE TABLE prod (
    prod_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prod_type_id INTEGER,
    prod_name TEXT NOT NULL,
    prod_description TEXT NOT NULL,
    prod_price REAL NOT NULL,
    prod_cost REAL NOT NULL,
    prod_sold BOOLEAN NOT NULL,
    FOREIGN KEY (prod_type_id) REFERENCES prod_type (prod_type_id)
);

CREATE TABLE custom (
    custom_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prod_id INTEGER NOT NULL,
    custom TEXT NOT NULL,
    custom_desc TEXT NOT NULL,
    exclusive BOOLEAN NOT NULL,
    require BOOLEAN NOT NULL,
    FOREIGN KEY (prod_id) REFERENCES prod (prod_id)
);

CREATE TABLE options (
    options_id INTEGER PRIMARY KEY AUTOINCREMENT,
    custom_id INTEGER NOT NULL,
    cost_change REAL NOT NULL,
    option_name TEXT NOT NULL,
    FOREIGN KEY (custom_id) REFERENCES custom (custom_id)
);



INSERT INTO prod_design (prod_design) VALUES ('custom');
INSERT INTO prod_design (prod_design) VALUES ('premade');

INSERT INTO prod_type (prod_type, prod_design_id, prod_type_description) VALUES ('wreaths', 1, 'get wreath');
INSERT INTO prod_type (prod_type, prod_design_id, prod_type_description) VALUES ('yarn crafts', 1, 'get bracelet');
INSERT INTO prod_type (prod_type, prod_design_id, prod_type_description) VALUES ('woodburning', 1, 'get wood');

INSERT INTO prod_type (prod_type, prod_design_id, prod_type_description) VALUES ('safety keychains', 2, 'keep safe');
INSERT INTO prod_type (prod_type, prod_design_id, prod_type_description) VALUES ('airtags', 2, 'help keep others safe');
INSERT INTO prod_type (prod_type, prod_design_id, prod_type_description) VALUES ('other', 2, 'other things dont fall into a clear category');

INSERT INTO prod (prod_type_id, prod_name, prod_description, prod_price, prod_cost, prod_sold) VALUES ('1', 'Hol_Wreath', 'A holiday wreath', 5, 5, FALSE);
INSERT INTO prod (prod_type_id, prod_name, prod_description, prod_price, prod_cost, prod_sold) VALUES ('2', 'Hol_Wreath', 'A holiday wreath', 5, 5, FALSE);
INSERT INTO prod (prod_type_id, prod_name, prod_description, prod_price, prod_cost, prod_sold) VALUES ('3', 'Hol_Wreath', 'A holiday wreath', 5, 5, FALSE);
INSERT INTO prod (prod_type_id, prod_name, prod_description, prod_price, prod_cost, prod_sold) VALUES ('4', 'Hol_Wreath', 'A holiday wreath', 5, 5, FALSE);
INSERT INTO prod (prod_type_id, prod_name, prod_description, prod_price, prod_cost, prod_sold) VALUES ('5', 'Hol_Wreath', 'A holiday wreath', 5, 5, FALSE);
INSERT INTO prod (prod_type_id, prod_name, prod_description, prod_price, prod_cost, prod_sold) VALUES ('6', 'Hol_Wreath', 'A holiday wreath', 5, 5, FALSE);

INSERT INTO custom (custom_id, prod_id, custom, custom_desc, exclusive, require) VALUES (1, 1, 'Color', 'Choose your color', TRUE, TRUE);
INSERT INTO custom (custom_id, prod_id, custom, custom_desc, exclusive, require) VALUES (2, 1, 'Color', 'Choose your color', TRUE, TRUE);

INSERT INTO options (options_id, custom_id, cost_change, option_name) VALUES (1, 1, 2.50, 'Blue');
INSERT INTO options (options_id, custom_id, cost_change, option_name) VALUES (2, 1, 2.50, 'Red');
INSERT INTO options (options_id, custom_id, cost_change, option_name) VALUES (3, 1, 2.50, 'orange');
INSERT INTO options (options_id, custom_id, cost_change, option_name) VALUES (4, 1, 2.50, 'green');

INSERT INTO options (options_id, custom_id, cost_change, option_name) VALUES (5, 2, 2.50, 'Blue');
INSERT INTO options (options_id, custom_id, cost_change, option_name) VALUES (6, 2, 2.50, 'Red');
INSERT INTO options (options_id, custom_id, cost_change, option_name) VALUES (7, 2, 2.50, 'orange');
INSERT INTO options (options_id, custom_id, cost_change, option_name) VALUES (8, 2, 2.50, 'green');