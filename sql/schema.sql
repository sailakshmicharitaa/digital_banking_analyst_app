CREATE TABLE digital_banking_metrics (
    customer_id VARCHAR(30) PRIMARY KEY,
    region VARCHAR(50),
    acquisition_channel VARCHAR(50),
    application_date DATE,
    verification_status VARCHAR(20),
    activation_status VARCHAR(20),
    activated_date DATE,
    age_band VARCHAR(20),
    product_type VARCHAR(30),
    monthly_transactions INTEGER,
    monthly_spend DECIMAL(12, 2),
    fraud_flag INTEGER,
    fraud_amount DECIMAL(12, 2),
    complaint_flag INTEGER,
    login_days_30 INTEGER,
    retention_risk VARCHAR(20)
);
