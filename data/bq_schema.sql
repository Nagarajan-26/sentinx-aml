-- Create core dataset if not exists
CREATE SCHEMA IF NOT EXISTS `aml_forensics_ledger`
OPTIONS(location="asia-southeast1");

-- 1. Entities: Bank accounts, individuals, and corporate registries
CREATE OR REPLACE TABLE `aml_forensics_ledger.entities` (
    entity_id STRING OPTIONS(description="Unique ID for bank account or corporate entity"),
    legal_name STRING,
    jurisdiction STRING OPTIONS(description="ISO 3-letter country code: IND, SGP, HKG, USA"),
    entity_type STRING OPTIONS(description="INDIVIDUAL, SHELL_CORP, FINTECH_NEOBANK, CASINO, TRUST"),
    incorporation_date DATE,
    risk_rating STRING OPTIONS(description="LOW, MEDIUM, HIGH, PEP"),
    created_at TIMESTAMP
)
CLUSTER BY entity_type, jurisdiction;

-- 2. Transaction Ledger: Graph edges across payment rails
CREATE OR REPLACE TABLE `aml_forensics_ledger.transactions` (
    transaction_id STRING,
    source_entity_id STRING,
    destination_entity_id STRING,
    amount NUMERIC,
    currency STRING,
    rail_type STRING OPTIONS(description="UPI, IMPS, SWIFT, NEFT, RTGS"),
    transaction_timestamp TIMESTAMP,
    declared_purpose STRING,
    is_structuring_flag BOOL OPTIONS(description="Benchmark ground truth flag")
)
PARTITION BY DATE(transaction_timestamp)
CLUSTER BY source_entity_id, destination_entity_id;

-- 3. Velocity View: Automated detection of pass-through mule hops (<24 hours dwell)
CREATE OR REPLACE VIEW `aml_forensics_ledger.v_rapid_pass_through` AS
SELECT 
    t1.source_entity_id AS originator,
    t1.destination_entity_id AS intermediate_mule,
    t2.destination_entity_id AS ultimate_beneficiary,
    t1.amount AS inbound_amount,
    t2.amount AS outbound_amount,
    TIMESTAMP_DIFF(t2.transaction_timestamp, t1.transaction_timestamp, MINUTE) AS retention_minutes
FROM `aml_forensics_ledger.transactions` t1
JOIN `aml_forensics_ledger.transactions` t2 
    ON t1.destination_entity_id = t2.source_entity_id
WHERE t2.transaction_timestamp >= t1.transaction_timestamp
  AND TIMESTAMP_DIFF(t2.transaction_timestamp, t1.transaction_timestamp, HOUR) <= 24
  AND ABS(t1.amount - t2.amount) / t1.amount <= 0.05;