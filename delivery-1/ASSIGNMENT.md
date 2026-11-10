# EICTA: First Project Delivery, ER and SQL

> Transcribed from the course PDF "1st Project Delivery" (2025/26). Dates are reported as they appear in the document.

## Problem statement

The Euphoric Events company asked you to design a database for the management of their music festivals.

A festival is characterized by a name, a location, a start date, and an end date. Each festival is divided into multiple stages, characterized by an identification code, a name, a maximum capacity, and a description about its location within the festival. At each stage, different musical performances can be held. A performance has a unique identifier, a title, a genre (e.g., rock, jazz, electronic), and start/end times. Performances are given by one or more artists, which may be solo musicians or bands (i.e., at least two musicians). The system should store for each artist their stage name, country, and main musical genre. In addition to this, musicians should provide their full name, nationality and main instrument, whereas bands must register their formation year.

Alongside music, festivals can host several stands where people can buy food, drinks and merchandise. Each stand has a name, a sponsor, and can sell either of the three aforementioned products. A product is described by a name and a price; furthermore, food and drinks have an expiration date, and only food items have a type (e.g., vegetarian).

To enter a festival, people must buy tickets, which have a type (e.g., regular, day pass, VIP), a price, and a validity period. To buy tickets, a person must state their full name, e-mail address, and phone number. A person can buy multiple tickets, and they can also purchase shop items during the festival. Whenever a purchase happens, the system should store the date and the payment method used.

### Additional notes

- a. You can introduce unique IDs only if no attribute defined in the text can be a primary key.
- b. Mark a sample reading direction for the cardinalities.
- c. Always mark the type of ISA hierarchies if present.

## Tasks

1. Design an ER Model for the given problem. In addition to the ER Diagram, please specify all assumptions, important reasoning and design choices made on the text. Remember that you are not allowed to contradict the text in any way!
2. From the ER Model, define the Logical Model, describing all relationships, attributes, primary and foreign keys, etc.
3. From the Logical Model, write and describe the SQL code to define each table.
4. Populate the database using Mockaroo, creating at least 25 tuples for each table. Please provide a screenshot with the inserted data for each table.
5. For each of the following combinations of SQL statements, write and describe at least one query, run it on your database instance and report its outcome.
   - a. WHERE
   - b. WHERE, LIMIT, LIKE
   - c. WHERE, IN, Nested Query
   - d. GROUP BY, 1 JOIN, AS
   - e. WHERE, GROUP BY
   - f. GROUP BY, HAVING, AS
   - g. WHERE, GROUP BY, HAVING, AS
   - h. WHERE, Nested Query, GROUP BY
   - i. WHERE, GROUP BY, HAVING, 1 JOIN
   - j. WHERE, GROUP BY, HAVING, 2 JOINs

   For each combination, define a meaningful query, give it a title based on its objective, report the SQL code, describe how the query works and what it does, and finally provide a screenshot of the query results (try to have at least one tuple as output).

## Tools and templates

- [Draw.io](https://app.diagrams.net/)
- [Mockaroo](https://www.mockaroo.com/)
- [SQLite Online](https://sqliteonline.com/)
- [MySQL Installer](https://dev.mysql.com/downloads/installer/)
- [Report Template (MS Word)](https://polimi365-my.sharepoint.com/:w:/g/personal/10582370_polimi_it/EaKcBpADx2NLgDwAWahK_PQBofiS3nwT0jeCwAvtCwbqfA?e=rLhzRP)
- [Report Template (LaTeX)](https://polimi365-my.sharepoint.com/:u:/g/personal/10582370_polimi_it/EUuSzgxsgjFPn1PATBqPo4sBqx48IF0rKqPJS3rRn-pRcA?e=NgA3TV)
- [Overleaf](https://it.overleaf.com/)

## Deadline and delivery

- Register your group at [this link](https://polimi365-my.sharepoint.com/:x:/g/personal/10582370_polimi_it/EUA5BYpf5hlNo335tmseoccBVfsYgB_wda06mgfJjES3Ug?e=BgPIhl) until October 9 at 23:59.
- The deadline for submitting your project is October 23 at 23:59. Any late delivery will not be evaluated and no points will be assigned, regardless of the motivations provided.
- The project must be delivered on WeBeep using the "Assignments" section ("Consegne" in Italian).

The final delivery must contain the following items in a zipped folder:

- **A self-contained dump of your database**
  - i.e., ensure that the dump you deliver contains not only the database schema, but also the data you inserted in it.
  - For SQLite users, the `.db` file should contain everything for the delivery when exported. For MySQL users, you must select the option "Self-Contained Dump" when exporting the database as a `.sql` file.
- **The `.pdf` file with the report**
  - You can write it using either MS Word or LaTeX through Overleaf (LaTeX highly recommended). If you use Word, remember to deliver a `.pdf` file.
  - The report must include:
    - A first page with the title of your project, the group number, the names of the group members and the academic year.
    - An index of the contents of the document.
    - An introduction chapter where you enter the text of the delivery.
    - A text analysis chapter where you include all entities and relationships identified, the attributes, and the assumptions made on the text if needed.
    - One chapter for each of the requests previously defined.
    - A simple caption for each figure you include in the delivery.
  - Keep in mind that the structure and the clarity of your report is part of the evaluation, so please use the provided templates and follow the guidelines.
- **A folder with high-resolution images**, one for each figure in your report (e.g., ER Diagram, Mockaroo screenshots, query results).
