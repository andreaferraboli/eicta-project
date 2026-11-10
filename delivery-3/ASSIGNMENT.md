# EICTA: Third Project Delivery, MongoDB and Web

> Transcribed from the course PDF "3rd Project Delivery" (2025/26). Dates are reported as they appear in the document.

## MongoDB tasks

The 3rd Project Delivery is built starting from the 1st Project Delivery. In particular, we ask you to choose a set of **minimum 5 entities** from your ER Model and develop a MongoDB Database. Define **only one collection** and describe the basic structure of the documents (i.e., name, type, etc.) and the containment hierarchy (i.e., if a document representing an entity has an array of sub-documents representing an entity, describe the main document accordingly). You can re-use the data you created for the first delivery, although you'll have to reshape it to be coherent with the new MongoDB structure. Define **at least 10 documents** in your collection, and **at least two elements per array of sub-documents**. **Leave no empty arrays.**

1. Provide a description of the chosen document structure. It should include all attributes, their types and the containment hierarchy. You can refer to or copy-paste elements from the 1st delivery if needed.
2. Write the following queries:
   - A total of **5 create/update/delete queries** (at least one per type).
   - A total of **10 retrieval queries** with the following characteristics:
     - 2 queries with projections and logical query operators
     - 2 queries with limit, sort and comparison query operators
     - 1 query including element query operators
     - 1 query using the group operator
     - 1 query with an unwind and a group by
     - 1 query with an unwind, a group by, and followed by a filter
     - 1 query with two conditions evaluated separately on the sub-documents of an array
     - 1 query with two conditions evaluated simultaneously on the sub-documents of an array
   - For each query, provide a title, a short description and a screenshot of its results.

## Web tasks

### 1. Static promotional page

Design a promotional web page for Euphoric Events. In particular you need to create a page for promoting an instance of a festival. You may choose any type of event you wish to feature.

This task requires you to make a static page (i.e., no interaction with a server) using HTML, CSS, and optionally JavaScript for DOM manipulation. Try to make a page that looks nice (no pure HTML!). You are allowed to include images and videos obtained (or linked) from external sources.

In the project report, please provide a description about the web page's contents, a short discussion about the structure and styling of different parts of the page, and some screenshots.

### 2. Page with server and database

Design a simple web page interacting with a server and a database:

- The web page must contain a log-in form and a sign-in form.
- Each form must submit the form data to a Node.js + Express server which will process it, query an SQLite database, and return a response.
  - Use [SQLite Online](https://sqliteonline.com/) to create a basic SQLite database with a single user table containing the attributes required for signing and logging in (unique email, password, name, surname, ...). Passwords can be in plain text without having to hash them.
- In case of a successful operation, a message should be displayed on the web page welcoming the user.
- The client-side must perform validations for the form fields. The server must handle failed attempts of logging or signing in.
- Styling is optional (you can provide a pure HTML page).

In the project report, please provide a description about the implemented logic for signing and logging in.

## Tools and templates

For MongoDB:

- [MongoDB Atlas](https://www.mongodb.com/products/platform/atlas-database)
- For installation refer to "E06 - Register and Connect to MongoDB Atlas" in the Exercise Session folder on WeBeep.

For Web:

- [Node.js Installer](https://nodejs.org/en/download) (use the installer for the LTS version)

For the project report:

- [Report Template (MS Word)](https://polimi365-my.sharepoint.com/:w:/g/personal/10582370_polimi_it/EaKcBpADx2NLgDwAWahK_PQBofiS3nwT0jeCwAvtCwbqfA?e=rLhzRP)
- [Report Template (LaTeX)](https://polimi365-my.sharepoint.com/:u:/g/personal/10582370_polimi_it/EUuSzgxsgjFPn1PATBqPo4sBqx48IF0rKqPJS3rRn-pRcA?e=NgA3TV)
- [Overleaf](https://it.overleaf.com/)

## Deadline and delivery

- The deadline for submitting your project is December 9 at 23:59. Any late delivery will not be evaluated and no points will be assigned, regardless of the motivations provided.
- The project must be delivered on WeBeep using the "Assignments" section ("Consegne" in Italian).

The final delivery must contain the following items in a zipped folder:

- **A dump of your MongoDB database.**
- **One folder for each of the Web Tasks** containing the source code of your implementation.
- **A `.pdf` file with the report of at most 30 pages.**
  - You can write it using either MS Word or LaTeX through Overleaf (LaTeX highly recommended). If you use Word, remember to deliver a `.pdf` file.
  - The report must include:
    - A first page with the title of your project, the group number, the names of the group members and the academic year.
    - An index of the contents of the document.
    - One chapter for each of the requests previously defined.
    - A simple caption for each figure you include in the delivery.
    - (You can avoid including List of Figures and List of Tables.)
  - Keep in mind that the structure and the clarity of your report is part of the evaluation, so please use the provided templates and follow the guidelines.
  - Remember that you are writing a project report. It must be concise and complete.
- **A folder with high-resolution images**, one for each figure in your report.
