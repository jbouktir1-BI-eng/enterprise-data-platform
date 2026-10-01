# TP1 — Source Architecture

## Source Domains

| Domain | Source Type | Main Data | Shared Keys |
|---|---|---|---|
| Sales | PostgreSQL | orders, order_lines, quotes | customer_id, product_id, employee_id |
| CRM | REST API / JSON | customers, contacts, opportunities | customer_id, employee_id |
| Finance | Excel / CSV | invoices, payments, costs | customer_id, order_id |
| Product | PostgreSQL | products, families, lifecycle | product_id |
| Pricing | REST API / CSV | prices, discounts | product_id, partner_id |
| Supply Chain | CSV | inventory, warehouses, shipments | product_id, warehouse_id, order_id |
| Procurement | Excel / CSV | suppliers, purchase_orders | supplier_id, product_id |
| Manufacturing | CSV / JSON | plants, production_orders | plant_id, product_id |
| Partners & Alliances | REST API / JSON | partners, programs, rebates | partner_id, customer_id |
| Distribution | CSV | distributors, sell-in, sell-out | partner_id, product_id |
| Support | REST API | tickets, SLA | customer_id, product_id |
| HR | Excel | employees, roles, departments | employee_id |
| Marketing | REST API / CSV | campaigns, leads | customer_id, campaign_id |
| Geography | JSON | countries, regions, territories | geography_id |
| Targets & Forecast | Excel | targets, budgets, forecast | product_id, geography_id, employee_id |

## Enterprise Shared Keys

- customer_id
- product_id
- employee_id
- supplier_id
- partner_id
- order_id
- warehouse_id
- plant_id
- geography_id
- campaign_id

## TP1 Source Principle

Multiple independent source systems must feed one reusable ingestion framework.

Source -> Validation -> Raw/Bronze -> Metadata

Failed or invalid records:

Source -> Validation -> Quarantine

## Portability Dependency

Current:
WSL2 Ubuntu DEV

Future:
Ubuntu Server DEV -> Ubuntu Server PROD

TP1 prepares portability.
Server migration is implemented later.

## Future Dependencies

- TP2: Data Lake and Data Quality
- TP3: PySpark processing
- TP5: analytical modeling / warehouse
- TP6: Airflow orchestration
- TP7: Product Master
- TP9: BI / Executive Cockpit
- TP10: forecasting and ML
- TP11: PROD, security and monitoring

Only reusable contracts are prepared during TP1.
Future TP implementations are not duplicated here.
