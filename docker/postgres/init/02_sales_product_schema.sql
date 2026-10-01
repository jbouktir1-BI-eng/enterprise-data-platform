CREATE TABLE IF NOT EXISTS products (
    product_id      VARCHAR(20) PRIMARY KEY,
    product_name    VARCHAR(150) NOT NULL,
    product_family  VARCHAR(100) NOT NULL,
    business_unit   VARCHAR(20) NOT NULL,
    list_price      NUMERIC(12,2) NOT NULL,
    lifecycle       VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id        VARCHAR(20) PRIMARY KEY,
    customer_id     VARCHAR(20) NOT NULL,
    employee_id     VARCHAR(20) NOT NULL,
    order_date      DATE NOT NULL,
    status          VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS order_lines (
    order_id        VARCHAR(20) NOT NULL REFERENCES orders(order_id),
    line_number     INTEGER NOT NULL,
    product_id      VARCHAR(20) NOT NULL REFERENCES products(product_id),
    quantity        INTEGER NOT NULL,
    discount_pct    NUMERIC(5,2) NOT NULL,
    PRIMARY KEY (order_id, line_number)
);

CREATE INDEX IF NOT EXISTS idx_orders_customer
    ON orders(customer_id);

CREATE INDEX IF NOT EXISTS idx_orders_employee
    ON orders(employee_id);

CREATE INDEX IF NOT EXISTS idx_order_lines_product
    ON order_lines(product_id);
