CREATE DATABASE bank;
USE bank;

CREATE TABLE customer(
	account_no INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (account_no),
    cus_name VARCHAR(100),
    cus_surname VARCHAR(100),
    cus_email VARCHAR(100),
    cus_username VARCHAR(100),
    cus_password VARCHAR(100),
    cus_age INT
);

ALTER TABLE customer AUTO_INCREMENT=1000;

CREATE TABLE registration(
	account_no INT,
    PRIMARY KEY (account_no),
    accountType VARCHAR(100)
);


CREATE TABLE transactions(
	account_no INT,
    PRIMARY KEY (account_no),
    transaction_name VARCHAR(100),
    transaction_date DATE,
    amount FLOAT
);

CREATE TABLE account_types(
	currency_unit VARCHAR(10),
    account_type VARCHAR(50)
);

CREATE TABLE customer_balances(
	account_no INT,
    PRIMARY KEY (account_no),
	customer_balance FLOAT
);
