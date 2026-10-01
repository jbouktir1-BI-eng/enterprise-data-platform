# PostgreSQL Source V2

## Purpose

Provide the relational operational source model used by TP1 ingestion.

## Validation Snapshot

- 23 relational tables
- 41 foreign-key relationships
- 0 detected business-rule errors during the validated database audit

## Major Relationships

Customer -> Account Assignment
Customer -> Contract
Customer -> Opportunity
Opportunity -> Quote
Quote -> Order
Order -> Order Line
Order -> Invoice
Invoice -> Payment
Order/Product -> Shipment
Customer/Order/Product -> Support Ticket
Supplier/Product -> Purchase Order
Plant/Product -> Production Order

## Migration

The V2 model was created in the separate `source_v2` PostgreSQL schema.

The original V1 tables were preserved during migration and validation.
This enabled parallel validation and safe rollback.
