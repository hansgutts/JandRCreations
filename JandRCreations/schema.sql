DROP TABLE IF EXISTS prod_design;
DROP TABLE IF EXISTS prod_type;
DROP TABLE IF EXISTS prod;
DROP TABLE IF EXISTS custom;
DROP TABLE IF EXISTS options;
DROP TABLE IF EXISTS user;

CREATE TABLE prod_design (
    prod_design_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prod_design TEXT UNIQUE NOT NULL
);

CREATE TABLE prod_type (
    prod_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prod_type TEXT UNIQUE NOT NULL,
    prod_type_description TEXT NOT NULL,
    prod_type_image TEXT NOT NULL,
    prod_design_id TEXT NOT NULL,
    FOREIGN KEY (prod_design_id) REFERENCES prod_design (prod_design_id)
);

CREATE TABLE prod (
    prod_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prod_type_id INTEGER,
    prod_name TEXT UNIQUE NOT NULL,
    prod_description TEXT NOT NULL,
    prod_price REAL NOT NULL,
    prod_cost REAL NOT NULL,
    prod_sold BOOLEAN NOT NULL,
    prod_image TEXT NOT NULL,
    FOREIGN KEY (prod_type_id) REFERENCES prod_type (prod_type_id)
);

CREATE TABLE custom (
    custom_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prod_id INTEGER NOT NULL,
    custom TEXT NOT NULL,
    custom_desc TEXT NOT NULL,
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

CREATE TABLE user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    userpassword TEXT NOT NULL
); 
INSERT INTO user (username, userpassword) VALUES ('hansgutts', '1234');

/*
INSERT INTO prod_design (prod_design) VALUES ('custom');
INSERT INTO prod_design (prod_design) VALUES ('premade');

INSERT INTO prod_type (prod_type, prod_design_id, prod_type_description, prod_type_image) VALUES ('wreaths', 1, 'get wreath', 'wreaths.png');
INSERT INTO prod_type (prod_type, prod_design_id, prod_type_description, prod_type_image) VALUES ('yarn crafts', 1, 'get bracelet', 'yarn crafts.png');
INSERT INTO prod_type (prod_type, prod_design_id, prod_type_description, prod_type_image) VALUES ('woodburning', 1, 'get wood', 'woodburning.png');

INSERT INTO prod_type (prod_type, prod_design_id, prod_type_description, prod_type_image) VALUES ('safety keychains', 2, 'keep safe', 'safety keychains.png');
INSERT INTO prod_type (prod_type, prod_design_id, prod_type_description, prod_type_image) VALUES ('airtags', 2, 'help keep others safe', 'airtags.png');
INSERT INTO prod_type (prod_type, prod_design_id, prod_type_description, prod_type_image) VALUES ('other', 2, 'other things dont fall into a clear category', 'other.png');

INSERT INTO prod (prod_type_id, prod_name, prod_description, prod_price, prod_cost, prod_sold, prod_image) VALUES ('1', 'Hol_Wreath', 'A holiday wreath', 5, 5, False, 'Hol_Wreath.png');
INSERT INTO prod (prod_type_id, prod_name, prod_description, prod_price, prod_cost, prod_sold, prod_image) VALUES ('2', 'Hol_Wreath2', 'A holiday wreath', 5, 5, False, 'Hol_Wreath.png');
INSERT INTO prod (prod_type_id, prod_name, prod_description, prod_price, prod_cost, prod_sold, prod_image) VALUES ('3', 'Hol_Wreath3', 'A holiday wreath', 5, 5, False, 'Hol_Wreath.png');
INSERT INTO prod (prod_type_id, prod_name, prod_description, prod_price, prod_cost, prod_sold, prod_image) VALUES ('4', 'Hol_Wreath4', 'A holiday wreath', 5, 5, False, 'Hol_Wreath.png');
INSERT INTO prod (prod_type_id, prod_name, prod_description, prod_price, prod_cost, prod_sold, prod_image) VALUES ('5', 'Hol_Wreath5', 'A holiday wreath', 5, 5, False, 'Hol_Wreath.png');
INSERT INTO prod (prod_type_id, prod_name, prod_description, prod_price, prod_cost, prod_sold, prod_image) VALUES ('6', 'Hol_Wreath6', 'A holiday wreath', 5, 5, False, 'Hol_Wreath.png');

INSERT INTO custom (custom_id, prod_id, custom, custom_desc, require) VALUES (1, 1, 'Color1', 'Choose your color', False);
INSERT INTO custom (custom_id, prod_id, custom, custom_desc, require) VALUES (2, 1, 'Color2', 'Choose your color', False);

INSERT INTO options (options_id, custom_id, cost_change, option_name) VALUES (1, 1, 4.50, 'Blue');
INSERT INTO options (options_id, custom_id, cost_change, option_name) VALUES (2, 1, 4.50, 'Red');
INSERT INTO options (options_id, custom_id, cost_change, option_name) VALUES (3, 1, 4.50, 'orange');
INSERT INTO options (options_id, custom_id, cost_change, option_name) VALUES (4, 1, 4.50, 'green');

INSERT INTO options (options_id, custom_id, cost_change, option_name) VALUES (5, 2, 2.50, 'Blue');
INSERT INTO options (options_id, custom_id, cost_change, option_name) VALUES (6, 2, 2.50, 'Red');
INSERT INTO options (options_id, custom_id, cost_change, option_name) VALUES (7, 2, 2.50, 'orange');
INSERT INTO options (options_id, custom_id, cost_change, option_name) VALUES (8, 2, 2.50, 'green');
*/