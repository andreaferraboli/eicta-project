// Import the delivery-1 data exported as CSV by: python scripts/eicta.py export-csv
// Files are read from the Neo4j import directory (mounted from build/delivery-2/neo4j-import).
// Node types: Festival, Stage, Performance, Artist (ISA: Musician | Band), Stand,
// Product (ISA: Food | Drink | Merchandise), Person, Purchase, Ticket.

// ---- nodes
LOAD CSV WITH HEADERS FROM 'file:///festival.csv' AS row
CREATE (:Festival {name: row.Name, location: row.Location,
                   startDate: date(row.StartDate), endDate: date(row.EndDate)});

LOAD CSV WITH HEADERS FROM 'file:///stage.csv' AS row
MATCH (f:Festival {name: row.FestivalName})
CREATE (s:Stage {code: row.Code, name: row.Name, maxCapacity: toInteger(row.MaxCapacity),
                 locationDescription: row.LocationDescription})
CREATE (s)-[:PART_OF]->(f);

LOAD CSV WITH HEADERS FROM 'file:///performance.csv' AS row
MATCH (s:Stage {code: row.StageCode})
CREATE (p:Performance {performanceId: toInteger(row.PerformanceID), title: row.Title, genre: row.Genre,
                       startTime: localdatetime(replace(row.StartTime, ' ', 'T')),
                       endTime: localdatetime(replace(row.EndTime, ' ', 'T'))})
CREATE (p)-[:HELD_AT]->(s);

// ISA Artist (total, disjoint): every artist gets the Artist label plus exactly one child label.
LOAD CSV WITH HEADERS FROM 'file:///artistfull.csv' AS row
CREATE (a:Artist {stageName: row.StageName, country: row.Country, mainGenre: row.MainGenre})
FOREACH (_ IN CASE WHEN row.ArtistType = 'musician' THEN [1] ELSE [] END |
  SET a:Musician, a.fullName = row.FullName, a.nationality = row.Nationality, a.mainInstrument = row.MainInstrument)
FOREACH (_ IN CASE WHEN row.ArtistType = 'band' THEN [1] ELSE [] END |
  SET a:Band, a.formationYear = toInteger(row.FormationYear));

LOAD CSV WITH HEADERS FROM 'file:///stand.csv' AS row
MATCH (f:Festival {name: row.FestivalName})
CREATE (st:Stand {name: row.Name, sponsor: row.Sponsor})
CREATE (st)-[:LOCATED_AT]->(f);

// ISA Product (total, disjoint): the SQL discriminator becomes a child label.
LOAD CSV WITH HEADERS FROM 'file:///product.csv' AS row
CREATE (p:Product {name: row.Name, price: toFloat(row.Price)})
FOREACH (_ IN CASE WHEN row.Category = 'food' THEN [1] ELSE [] END |
  SET p:Food, p.expirationDate = date(row.ExpirationDate), p.foodType = row.FoodType)
FOREACH (_ IN CASE WHEN row.Category = 'drink' THEN [1] ELSE [] END |
  SET p:Drink, p.expirationDate = date(row.ExpirationDate))
FOREACH (_ IN CASE WHEN row.Category = 'merchandise' THEN [1] ELSE [] END |
  SET p:Merchandise);

LOAD CSV WITH HEADERS FROM 'file:///person.csv' AS row
CREATE (:Person {email: row.Email, fullName: row.FullName, phone: row.Phone});

LOAD CSV WITH HEADERS FROM 'file:///purchase.csv' AS row
MATCH (pe:Person {email: row.PersonEmail})
CREATE (pu:Purchase {purchaseId: toInteger(row.PurchaseID), date: date(row.PurchaseDate),
                     paymentMethod: row.PaymentMethod})
CREATE (pe)-[:MADE]->(pu);

LOAD CSV WITH HEADERS FROM 'file:///ticket.csv' AS row
MATCH (f:Festival {name: row.FestivalName})
MATCH (pu:Purchase {purchaseId: toInteger(row.PurchaseID)})
CREATE (t:Ticket {ticketId: toInteger(row.TicketID), type: row.Type, price: toFloat(row.Price),
                  validFrom: date(row.ValidFrom), validTo: date(row.ValidTo)})
CREATE (t)-[:VALID_FOR]->(f)
CREATE (pu)-[:INCLUDES]->(t);

// ---- relationships from the N:M tables
LOAD CSV WITH HEADERS FROM 'file:///bandmember.csv' AS row
MATCH (m:Musician {stageName: row.MusicianName}), (b:Band {stageName: row.BandName})
CREATE (m)-[:MEMBER_OF]->(b);

LOAD CSV WITH HEADERS FROM 'file:///performanceartist.csv' AS row
MATCH (a:Artist {stageName: row.ArtistStageName}), (p:Performance {performanceId: toInteger(row.PerformanceID)})
CREATE (a)-[:PERFORMS_IN]->(p);

LOAD CSV WITH HEADERS FROM 'file:///sells.csv' AS row
MATCH (st:Stand {name: row.StandName}), (p:Product {name: row.ProductName})
CREATE (st)-[:SELLS]->(p);

LOAD CSV WITH HEADERS FROM 'file:///purchaseitem.csv' AS row
MATCH (pu:Purchase {purchaseId: toInteger(row.PurchaseID)}), (p:Product {name: row.ProductName})
CREATE (pu)-[:INCLUDES_ITEM {standName: row.StandName}]->(p);
