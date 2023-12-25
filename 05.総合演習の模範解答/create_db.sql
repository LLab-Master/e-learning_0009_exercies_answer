.open test.db
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE user (
	id INTEGER NOT NULL, 
	name VARCHAR(80), 
	password VARCHAR(10) NOT NULL, 
	age INTEGER, 
	address VARCHAR(100), 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO user VALUES(1,'Taro','abc',30,'Tokyo');
INSERT INTO user VALUES(2,'Jiro','def',23,'Osaka');
INSERT INTO user VALUES(3,'Hanako','hij',44,'Yokohama');
INSERT INTO user VALUES(4,'Ken','klm',35,'Nagoya');
INSERT INTO user VALUES(5,'Tom','xzy',33,'Sapporo');
CREATE TABLE category (
	id INTEGER NOT NULL, 
	name VARCHAR(256), 
	PRIMARY KEY (id)
);
INSERT INTO category VALUES(1,'Book');
INSERT INTO category VALUES(2,'CD');
INSERT INTO category VALUES(3,'DVD');
CREATE TABLE product (
	id INTEGER NOT NULL, 
	name VARCHAR(256), 
	price INTEGER,
        category_id INTEGER,
	PRIMARY KEY (id),
        FOREIGN KEY (category_id) REFERENCES category(id)
);
INSERT INTO product VALUES(1,'CD1',1250,2);
INSERT INTO product VALUES(2,'CD2',1000,2);
INSERT INTO product VALUES(3,'DVD2',5000,3);
INSERT INTO product VALUES(4,'Book1',1000,1);
INSERT INTO product VALUES(7,'DVD1',500,3);
INSERT INTO product VALUES(8,'Book2',9000,1);
COMMIT;
.quit

