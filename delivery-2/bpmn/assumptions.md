# BPMN assumptions (DRAFT)

## Store&Store

| ID | Assumption |
|---|---|
| B-01 | Three pools: Customer (expanded, the text describes the customer's actions), Store&Store with lanes Customer Service, Inventory Management and Logistics, External Supplier (collapsed: its internal process is not described). |
| B-02 | Availability is checked product by product with a loop ("checks the availability of each product"): check, decide, package, then "All products packaged?" returns to the next product. |
| B-03 | When a product is not in stock, the customer service notifies the customer and waits for the updated shopping list; the check then restarts from the loop entry. |
| B-04 | The low-stock rule (fewer than 10 items) is evaluated only for available products, and the supplier order is a message to the External Supplier pool; the process does not wait for the supply ("before continuing with the order preparation" = the order is placed, then preparation continues). |
| B-05 | The physical shipment by Logistics is modelled as a message flow "shipment" to the customer. |
| B-06 | After shipping, an event-based gateway waits for either a return (message) or one week (timer, P7D). Return: report written, end. Timer: order recorded, end. |
| B-07 | The customer decides whether some items are defective; if not, the customer's process ends without returning items. |

## Euphoric Events (artist booking)

| ID | Assumption |
|---|---|
| B-10 | External actor: the artist (or their management), expanded pool. |
| B-11 | The RDBMS of delivery 1 is a dedicated lane "Festival RDBMS" with service tasks and a data store reference "Euphoric Events DB" (read: stages and free slots; write: Performance and PerformanceArtist rows, schedule update). |
| B-12 | The booking office waits 5 days for an answer (timer, P5D); a decline or the timeout moves to the next shortlisted artist; if none is left, the process ends without booking. |
| B-13 | "Publish line-up update" is a collapsed sub-process (website, social media), not detailed. |
| B-14 | The process starts with a timer event (line-up planning period opens). |
