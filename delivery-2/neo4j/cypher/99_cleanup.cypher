// Removes every node and relationship (constraints are kept).
// DESTRUCTIVE: run only through "python scripts/eicta.py neo4j-load", which reloads the seed right after.
MATCH (n) CALL { WITH n DETACH DELETE n } IN TRANSACTIONS OF 1000 ROWS;
