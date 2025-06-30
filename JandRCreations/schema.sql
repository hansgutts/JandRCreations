DROP TABLE IF EXISTS prod_design;
DROP TABLE IF EXISTS prod_type;
DROP TABLE IF EXISTS prod;

CREATE TABLE prod_design (
    prod_design_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prod_design TEXT NOT NULL
);

CREATE TABLE prod_type (
    prod_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prod_type TEXT NOT NULL,
    prod_design_id TEXT NOT NULL,
    FOREIGN KEY (prod_design_id) REFERENCES prod_design (prod_design_id)
);

CREATE TABLE prod (
    prod_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prod_type_id INTEGER
    prod_name TEXT NOT NULL,
    prod_description TEXT NOT NULL,
    prod_price REAL NOT NULL,
    prod_cost REAL NOT NULL,
    prod_sold BOOLEAN NOT NULL,
    prod_path TEXT,
    FOREIGN KEY (prod_type_id) REFERENCES prod_type (prod_type_id)
);

INSERT INTO prod_design (prod_design) VALUES ('custom');
INSERT INTO prod_design (prod_design) VALUES ('premade');

INSERT INTO prod_type (prod_type, prod_design_id) VALUES ('wreath', 1);
INSERT INTO prod_type (prod_type, prod_design_id) VALUES ('bracelet', 1);
INSERT INTO prod_type (prod_type, prod_design_id) VALUES ('wood', 1);