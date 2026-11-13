CREATE DATABASE IF NOT EXISTS fintech_churn_db;
USE fintech_churn_db;
#DROP TABLE IF EXISTS merchant_transactions;

CREATE TABLE merchant_transactions (
    row_id INT AUTO_INCREMENT PRIMARY KEY ,
    merchant_id VARCHAR(50) NOT NULL,
    transaction_id VARCHAR(50) NOT NULL,
    transaction_time DATETIME NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 4) NOT NULL
);
USE fintech_churn_db;
SELECT COUNT(*) FROM merchant_transactions;
