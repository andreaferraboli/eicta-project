# EICTA: Second Project Delivery, Neo4j and BPMN

> Transcribed from the course PDF "2nd Project Delivery" (2025/26). Dates are reported as they appear in the document.

## Neo4j tasks

The 2nd Project is built starting from the 1st Project. In particular, we ask you to choose a set of **minimum 8 entities** from your ER Model (**including at least one of the ISA hierarchies**) and develop a Neo4j Database, including nodes and relationships built using the chosen entities. For each node type (i.e., nodes representing the chosen entity), you should represent its attributes and relationships with the other chosen node types (be coherent with your ER diagram). Of course, choose nodes that are connected. You can reuse the same data you created for the MySQL/SQLite Database. To do so, export the data in a `.csv` format and follow [this guide](https://neo4j.com/docs/getting-started/data-import/csv-import/) to upload it into your Neo4j DB. Create **at least 10 node instances for each node type**.

1. Provide a schematic representation of the chosen nodes. This should highlight node types, relationship types and their properties. You can use draw.io for this task.
2. For each node and relationship, list their attributes and types with a very short description. You can also refer to (or copy-paste) sections of the 1st project if no changes were made to the attributes. If you need to make additional assumptions on the problem statement, list them in this section.
3. Write the following queries:
   - A total of **5 create/update/delete queries** (at least one per type).
   - A total of **10 retrieval queries** with the following characteristics:
     - 2 queries with at least two nodes in the MATCH statement and conditions
     - 2 queries with at least two nodes in the MATCH statement, conditions and aggregation without a WITH statement
     - 2 queries with at least two nodes in the MATCH statement, conditions and one WITH statement
     - 2 queries with at least three nodes in the MATCH statement, conditions and multiple WITH statements
     - 1 query with variable-length paths in the MATCH statement and conditions
     - 1 query that computes the shortest path
   - For each query, provide a title, a short description and a screenshot of its results (either in graph or in tabular format).

## BPMN tasks

### 1. Store&Store process

Given the following process, write the BPMN diagram representing it. If any assumptions beyond the problem statement are made, write them.

The Store&Store Company is interested in developing an e-commerce system for their electronic stores, and asked you to provide them with a BPMN diagram depicting the pipeline of interactions with the customer, and the preparation and shipping of an order.

The process starts with the customer asking for the available products. The customer service receives the request, and forwards it to the inventory management, which retrieves the list of available products. After receiving the list, the customer prepares its order and sends it to the customer service. The preparation of the order is handled by the inventory management, which checks the availability of each product and, when available, handles its packaging. If any product is not in stock, the customer service sends a notification to the customer, which is required to update the shopping list. Additionally, to allow better management of the warehouse stocks, when a product is running out (i.e., less than 10 items are available), the inventory management places an order to an external supplier before continuing with the order preparation. After all products of the shopping list have been packaged, the customer service notifies the customer that the order is ready for shipping, and then the order is physically sent by the logistics department. Since it is possible that an order may contain defective products, customers are allowed to return items to the customer service. If no item is returned within a week, the order is recorded and the process terminates. Otherwise, the customer service writes a report for the returned items and the process terminates.

### 2. Euphoric Events process

Design a process that involves the Euphoric Events company. Provide a textual statement for the modeled process and a BPMN diagram describing it. Such process must:

- Involve at least one external actor.
- Involve the RDBMS of the first project (use artifacts and a dedicated swim lane to this end).
- Showcase at least 10 steps (including activities, events, and sub-processes) before terminating.

## Tools and templates

For Neo4j:

- [Draw.io](https://app.diagrams.net/) (diagrams)
- [Neo4j Online tool or Desktop Installer](https://neo4j.com/download/)

For BPMN:

- [bpmn.io](https://demo.bpmn.io/)

For the project report:

- [Report Template (MS Word)](https://polimi365-my.sharepoint.com/:w:/g/personal/10582370_polimi_it/EaKcBpADx2NLgDwAWahK_PQBofiS3nwT0jeCwAvtCwbqfA?e=rLhzRP)
- [Report Template (LaTeX)](https://polimi365-my.sharepoint.com/:u:/g/personal/10582370_polimi_it/EUuSzgxsgjFPn1PATBqPo4sBqx48IF0rKqPJS3rRn-pRcA?e=NgA3TV)
- [Overleaf](https://it.overleaf.com/)

## Deadline and delivery

- The deadline for submitting your project is November 20 at 23:59. Any late delivery will not be evaluated and no points will be assigned, regardless of the motivations provided.
- The project must be delivered on WeBeep using the "Assignments" section ("Consegne" in Italian).

The final delivery must contain the following items in a zipped folder:

- **A dump of your Neo4j database.**
- **The `.pdf` file with the report of at most 30 pages.**
  - You can write it using either MS Word or LaTeX through Overleaf (LaTeX highly recommended). If you use Word, remember to deliver a `.pdf` file.
  - The report must include:
    - A first page with the title of your project, the group number, the names of the group members and the academic year.
    - An index of the contents of the document.
    - One chapter for each of the requests previously defined.
    - A simple caption for each figure you include in the delivery.
  - Keep in mind that the structure and the clarity of your report is part of the evaluation, so please use the provided templates and follow the guidelines.
  - Remember that you are writing a project report. It must be concise and complete.
- **A folder with high-resolution images**, one for each figure in your report (e.g., Neo4j schemata, query results, BPMN diagrams).
