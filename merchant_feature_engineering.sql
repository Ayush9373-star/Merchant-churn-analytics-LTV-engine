USE fintech_churn_db;

SELECT 
    merchant_id,
    
    -- 1. MONETARY VALUE: Total transaction volume processed through our gateway
    ROUND(SUM(quantity * unit_price), 2) AS total_processing_volume,
    
    -- 2. FREQUENCY: Number of unique checkout settlement events executed
    COUNT(DISTINCT transaction_id) AS total_transaction_count,
    
    -- 3. RECENCY: Days elapsed between the system's latest date and the merchant's last activity
    DATEDIFF(
        (SELECT MAX(transaction_time) FROM merchant_transactions), 
        MAX(transaction_time)
    ) AS days_since_last_active,
    
    -- 4. AVERAGE TICKET SIZE: Average value per transaction line (helps ML isolate high vs low-tier merchants)
    ROUND(AVG(quantity * unit_price), 2) AS avg_transaction_value,
    
    -- 5. MERCHANT TENURE (DAYS): Lifespan length of active engagement on our platform
    DATEDIFF(MAX(transaction_time), MIN(transaction_time)) AS merchant_tenure_days

FROM merchant_transactions
GROUP BY merchant_id;
