// Requirement: D2-QR-2
// Category: 2 nodes in MATCH + conditions (2/2)
// Title: Guitarists and drummers in bands formed before 2000
// Description: Musicians playing guitar or drums who are members of a band formed before 2000.
// Evidence to collect: delivery-2/report/figures/r02_match2_cond_band_members.png (Neo4j Browser, graph or table view)
MATCH (m:Musician)-[:MEMBER_OF]->(b:Band)
WHERE m.mainInstrument IN ['guitar', 'drums'] AND b.formationYear < 2000
RETURN m.stageName AS musician, m.mainInstrument AS instrument, b.stageName AS band, b.formationYear AS formed
ORDER BY formed;
