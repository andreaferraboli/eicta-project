# EICTA 2024/25: previous-year deliveries (reference only)

> Transcribed from the 2024/25 course PDFs. Different problem (WellDressed fashion company) and different requirements: **do not use these as requirements** for the current project, which is described in `delivery-1/`, `delivery-2/`, `delivery-3/`.
>
> Main differences from 2025/26: Neo4j needed min 5 entities (now 8 with an ISA), query mix differs (3 MATCH queries, no variable-length path); MongoDB allowed multiple collections with 10 documents per entity and 20 embedded in total (now one collection, 10 documents, 2 elements per array); no Web tasks.

## First delivery: ER and SQL

"The WellDressed fashion company wants to create a database about its products and exhibitions. The company hires fashion models to partake in fashion exhibitions. Each model provides their personal data, including Personal ID, name, surname, birth date, phone number, height, and dress size (XS, S, M, L, XL, etc.). Models are assigned to a fashion designer. These are described by their Personal ID, name, surname, stage name (nome d'arte), phone number, and a brief description of their career. Fashion designers produce dresses for the models to wear in exhibitions. Each dress is worn by one model. Dresses are identified by a unique ID, size (XS, S, M, L, XL, etc.), colour, and production time. Dresses are made using fabrics described by a unique ID, price per square meter, name, and description of their properties. The amount of fabric used to produce a dress is also stored. Fabrics can be made from other fabrics. Models partake in exhibitions, described by a unique ID, duration (in minutes), title, location address, and description. Once a year, a fashion competition is held. The competition involves fashion designers submitting one of their dresses. The winning dress is marked as such. Dresses can be submitted to one competition only."

Requests:

- **ER**: ER Model of the problem, including all the necessary attributes, (potential) assumptions, important reasoning, etc. You're not allowed to contradict the text in any way.
- **LM**: Logical Model, describing all the entities, their attributes, primary and foreign keys, etc.
- **RM**: final Relational Model, describing all the tables with their attributes, primary and foreign keys, relationships, etc.
- **SQL1**: code to define each table.
- **SQL2**: populate the database using [Mockaroo](https://www.mockaroo.com), at least 25 tuples for each table, with a screenshot each.
- **SQL3**: at least one query (title, query, description, outcome) for each combination: WHERE; WHERE, LIMIT, LIKE; WHERE, IN, Nested Query; GROUP BY, 1 JOIN, AS; WHERE, GROUP BY; GROUP BY, HAVING, AS; WHERE, GROUP BY, HAVING, AS; WHERE, Nested Query, GROUP BY; WHERE, GROUP BY, HAVING, 1 JOIN; WHERE, GROUP BY, HAVING, 2 JOINs.

Delivery: self-contained MySQL dump; PDF report (first page with members' name, surname, personal code, title, academic year; index; introduction; text analysis; one chapter per request); folder with high-resolution pictures; a simple description below each figure. Deadline in the document: two weeks after assignment, by midnight. Oral examination at the end of the project, group evaluated as a whole.

## Second delivery: Neo4j and BPMN

Choose a minimum of 5 entities from your ER Model and develop a Neo4j Database (nodes in a relationship with each other). Reuse MySQL data via CSV ([import guide](https://neo4j.com/developer/guide-import-csv/)). At least 10 node instances for each node type.

- **DB**: schematic representation of the chosen nodes (no cardinalities needed).
- **Details**: attributes, types and description for each node and relationship.
- **Query**: 5 creation/update/delete queries (at least 1 per type); 10 queries: 3 with at least 2 nodes in MATCH and conditions; 2 with at least 2 nodes in MATCH, conditions and aggregation without WITH; 2 with at least 2 nodes in MATCH, conditions and a WITH; 2 with at least 3 nodes in MATCH, conditions and multiple WITH; 1 with the `shortestPath(...)` function.
- **BPMN**: models submit their CVs through the company's front desk. As soon as a CV is received, it is forwarded to the HR department, which checks it. If they deem the candidate suitable for a position, they forward the CV to the head of the company. Otherwise, the candidate is noticed, and the process terminates. The head of the company contacts the fashion designers (internals) who work for the company and submits the model's CV to them. Designers have three days to reply to the head (a response is mandatory, even if negative). If a designer is interested in working with the model, the head asks the front desk to contact the model to set up a meeting with them. If no designer is interested, the candidate is notified, and the process terminates. If the model answers affirmatively, the designer is contacted through the front desk, and they are asked to prepare a dress for the model. The dress is sent to the model, and then a meeting with the head is held. After the meeting, the head of the company provides their final decision through the front desk. They have at most 5 days to do so. Otherwise, the candidate is notified, and the process terminates.

Delivery: Neo4j dump; PDF report (first page, index, introduction, one chapter per request); folder with high-resolution pictures.

## Third delivery: MongoDB

Choose a minimum of 5 entities and develop a MongoDB Database. Define the basic structure of each document and the containment hierarchy. At least 10 documents for each entity; if an entity's document is contained in another entity, at least 20 of them in total (e.g., 2 for each of the 10 main documents). Leave no empty arrays.

- **DB**: schematic representation of the documents and containment hierarchy.
- **Query**: 5 creation/update/delete queries (at least 1 per type); 10 queries: 2 with projections and logical operators; 2 with limit, sort and comparison operators; 1 with element operators; 1 simple aggregation; 1 unwind and aggregation; 1 unwind, aggregation, then filter; 1 with two conditions evaluated separately on a sub-document of an array; 1 with two conditions evaluated simultaneously on a sub-document of an array.

Delivery: MongoDB dump; PDF report (first page, index, introduction, one chapter per request); folder with high-resolution pictures.
