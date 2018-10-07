/* User is a keyword in sql, using customer instead  */

CREATE TABLE Customer(
    customer_id INTEGER  PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) NOT NULL UNIQUE,
    /* 320 is usually used */
    first_name VARCHAR(20) NOT NULL,
    middle_name VARCHAR(20) NULL,
    last_name VARCHAR(20) NOT NULL,
    phone_number CHAR(10) DEFAULT '0000000000',
    /* Default was added just for testing purposes, no need to keep inventing phone numbers */
    pwd VARCHAR(100) NOT NULL
    /* 255 is usually used */
);