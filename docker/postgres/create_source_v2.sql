-- Technology: PostgreSQL 16
-- Technique : Parallel schema migration
-- Purpose   : Create validated V2 enterprise source model.

DROP SCHEMA IF EXISTS source_v2 CASCADE;
CREATE SCHEMA source_v2;

CREATE TABLE source_v2.customers (
    customer_id VARCHAR(30) PRIMARY KEY,
    customer_name TEXT NOT NULL,
    customer_segment TEXT NOT NULL,
    industry TEXT,
    commercial_value_tier TEXT,
    employee_count INTEGER,
    region TEXT,
    sales_organization TEXT,
    account_type TEXT,
    credit_rating TEXT,
    credit_limit NUMERIC(18,2),
    default_payment_terms TEXT,
    preferred_currency VARCHAR(10),
    contract_required BOOLEAN,
    eligible_portfolios TEXT,
    customer_status TEXT,
    data_classification TEXT,
    source_provider TEXT
);

CREATE TABLE source_v2.products (
    product_id VARCHAR(30) PRIMARY KEY,
    portfolio TEXT,
    category TEXT,
    product_family TEXT,
    product_line TEXT,
    product_name TEXT NOT NULL,
    offering_type TEXT,
    solution_type TEXT,
    workload TEXT,
    minimum_customer_tier TEXT,
    consumption_model TEXT,
    license_model TEXT,
    lifecycle TEXT,
    data_classification TEXT,
    source_provider TEXT
);

CREATE TABLE source_v2.employees (
    employee_id VARCHAR(30) PRIMARY KEY,
    employee_name TEXT,
    department TEXT,
    role TEXT,
    region TEXT,
    sales_organization TEXT,
    employment_status TEXT,
    data_classification TEXT
);

CREATE TABLE source_v2.orders (
    order_id VARCHAR(30) PRIMARY KEY,
    customer_id VARCHAR(30) REFERENCES source_v2.customers,
    employee_id VARCHAR(30) REFERENCES source_v2.employees,
    contract_id VARCHAR(30),
    order_date DATE NOT NULL,
    customer_segment TEXT,
    sales_organization TEXT,
    region TEXT,
    currency VARCHAR(10),
    status TEXT,
    data_classification TEXT,
    opportunity_id VARCHAR(30),
    quote_id VARCHAR(30),
    project_order_sequence INTEGER
);

CREATE TABLE source_v2.order_lines (
    order_id VARCHAR(30) REFERENCES source_v2.orders,
    line_number INTEGER,
    product_id VARCHAR(30) REFERENCES source_v2.products,
    portfolio TEXT,
    workload TEXT,
    quantity INTEGER,
    unit_price NUMERIC(18,2),
    discount_pct NUMERIC(8,2),
    gross_amount NUMERIC(18,2),
    net_amount NUMERIC(18,2),
    data_classification TEXT,
    PRIMARY KEY (order_id, line_number)
);

CREATE INDEX idx_v2_orders_customer
ON source_v2.orders(customer_id);

CREATE INDEX idx_v2_lines_product
ON source_v2.order_lines(product_id);
