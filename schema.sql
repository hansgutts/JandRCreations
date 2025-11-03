/*drop the tables*/
DROP TABLE IF EXISTS options;
DROP TABLE IF EXISTS custom;
DROP TABLE IF EXISTS prod;
DROP TABLE IF EXISTS prod_type;
DROP TABLE IF EXISTS prod_design;
DROP TABLE IF EXISTS user;

/*initialize the tables*/
CREATE TABLE prod_design (
    prod_design_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prod_design TEXT UNIQUE NOT NULL
);

CREATE TABLE prod_type (
    prod_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prod_type TEXT UNIQUE NOT NULL,
    prod_type_description TEXT NOT NULL,
    prod_type_image TEXT NOT NULL,
    prod_design_id INTEGER NOT NULL,
    FOREIGN KEY (prod_design_id) REFERENCES prod_design (prod_design_id) ON DELETE CASCADE
);

CREATE TABLE prod (
    prod_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prod_type_id INTEGER NOT NULL,
    prod_name TEXT UNIQUE NOT NULL,
    prod_description TEXT NOT NULL,
    prod_price REAL NOT NULL,
    prod_cost REAL NOT NULL,
    prod_sold BOOLEAN NOT NULL,
    prod_image TEXT NOT NULL,
    FOREIGN KEY (prod_type_id) REFERENCES prod_type (prod_type_id) ON DELETE CASCADE
);

CREATE TABLE custom (
    custom_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prod_id INTEGER NOT NULL,
    custom TEXT NOT NULL,
    custom_desc TEXT NOT NULL,
    require BOOLEAN NOT NULL,
    FOREIGN KEY (prod_id) REFERENCES prod (prod_id) ON DELETE CASCADE
);

CREATE TABLE options (
    options_id INTEGER PRIMARY KEY AUTOINCREMENT,
    custom_id INTEGER NOT NULL,
    cost_change REAL NOT NULL,
    option_name TEXT NOT NULL,
    FOREIGN KEY (custom_id) REFERENCES custom (custom_id) ON DELETE CASCADE
);

CREATE TABLE user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    userpassword TEXT NOT NULL
); 

INSERT INTO user (username, userpassword) VALUES ('rfleming115', 'scrypt:32768:8:1$cHG7j64o4QDN6hBK$0004dfc914326eca39b65461f7de4f3cb1a33172ea41f9a8daf3619d7b0ee3bb8b934bd0fcc8c7b3b4084c76420a8de01890eb8aca5baa7ec45b886295f589fd')