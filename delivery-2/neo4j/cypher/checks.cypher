// Quantitative and ISA checks. Output rows: kind, name, value.
// kind = count      -> value must be >= 10 (at least 10 instances per node type)
// kind = violation  -> value must be 0
UNWIND ['Festival', 'Stage', 'Performance', 'Artist', 'Musician', 'Band', 'Stand', 'Product',
        'Food', 'Drink', 'Merchandise', 'Person', 'Purchase', 'Ticket'] AS label
CALL { WITH label MATCH (n) WHERE label IN labels(n) RETURN count(n) AS c }
RETURN 'count' AS kind, label AS name, c AS value
UNION ALL
RETURN 'violation' AS kind, 'artist_isa_total_disjoint' AS name,
       COUNT { MATCH (a:Artist) WHERE NOT (a:Musician XOR a:Band) } AS value
UNION ALL
RETURN 'violation' AS kind, 'child_label_without_artist' AS name,
       COUNT { MATCH (a) WHERE (a:Musician OR a:Band) AND NOT a:Artist } AS value
UNION ALL
RETURN 'violation' AS kind, 'product_isa_total_disjoint' AS name,
       COUNT { MATCH (p:Product) WHERE size([l IN labels(p) WHERE l IN ['Food', 'Drink', 'Merchandise']]) <> 1 } AS value
UNION ALL
RETURN 'violation' AS kind, 'band_min_two_members' AS name,
       COUNT { MATCH (b:Band) WHERE COUNT { (:Musician)-[:MEMBER_OF]->(b) } < 2 } AS value
UNION ALL
RETURN 'violation' AS kind, 'performance_without_artist' AS name,
       COUNT { MATCH (p:Performance) WHERE NOT EXISTS { (:Artist)-[:PERFORMS_IN]->(p) } } AS value
UNION ALL
RETURN 'violation' AS kind, 'isolated_nodes' AS name,
       COUNT { MATCH (n) WHERE NOT EXISTS { (n)--() } } AS value;
