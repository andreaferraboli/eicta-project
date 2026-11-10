-- Integrity checks for the Euphoric Events database.
-- Each query returns (check_name, violations). Every value must be 0.
-- Run by: python scripts/eicta.py sql-check
-- PRAGMA foreign_key_check and the ">= 25 tuples per table" check are run by the script itself.

-- ISA Artist: total (every artist is a musician or a band)
SELECT 'artist_isa_total', COUNT(*) FROM Artist a
WHERE NOT EXISTS (SELECT 1 FROM Musician m WHERE m.StageName = a.StageName)
  AND NOT EXISTS (SELECT 1 FROM Band b WHERE b.StageName = a.StageName);

-- ISA Artist: disjoint (no artist is both)
SELECT 'artist_isa_disjoint', COUNT(*) FROM Musician m JOIN Band b ON b.StageName = m.StageName;

-- Discriminator coherent with the child table
SELECT 'artist_type_matches_child', COUNT(*) FROM Artist a
WHERE (a.ArtistType = 'musician' AND a.StageName NOT IN (SELECT StageName FROM Musician))
   OR (a.ArtistType = 'band' AND a.StageName NOT IN (SELECT StageName FROM Band));

-- A band has at least two musicians
SELECT 'band_min_two_members', COUNT(*) FROM Band b
WHERE (SELECT COUNT(*) FROM BandMember bm WHERE bm.BandName = b.StageName) < 2;

-- A performance is given by one or more artists
SELECT 'performance_has_artist', COUNT(*) FROM Performance p
WHERE NOT EXISTS (SELECT 1 FROM PerformanceArtist pa WHERE pa.PerformanceID = p.PerformanceID);

-- A festival is divided into multiple stages (assumption: at least 2)
SELECT 'festival_multiple_stages', COUNT(*) FROM Festival f
WHERE (SELECT COUNT(*) FROM Stage s WHERE s.FestivalName = f.Name) < 2;

-- Performances fall within the festival dates
SELECT 'performance_within_festival', COUNT(*) FROM Performance p
JOIN Stage s ON s.Code = p.StageCode
JOIN Festival f ON f.Name = s.FestivalName
WHERE date(p.StartTime) < f.StartDate OR date(p.EndTime) > f.EndDate;

-- Ticket validity within the festival dates
SELECT 'ticket_within_festival', COUNT(*) FROM Ticket t
JOIN Festival f ON f.Name = t.FestivalName
WHERE t.ValidFrom < f.StartDate OR t.ValidTo > f.EndDate;

-- Shop items are bought during the festival of the stand
SELECT 'item_purchase_during_festival', COUNT(*) FROM PurchaseItem pi
JOIN Purchase pu ON pu.PurchaseID = pi.PurchaseID
JOIN Stand st ON st.Name = pi.StandName
JOIN Festival f ON f.Name = st.FestivalName
WHERE pu.PurchaseDate < f.StartDate OR pu.PurchaseDate > f.EndDate;

-- Every purchase contains at least one ticket or one shop item
SELECT 'purchase_not_empty', COUNT(*) FROM Purchase pu
WHERE NOT EXISTS (SELECT 1 FROM Ticket t WHERE t.PurchaseID = pu.PurchaseID)
  AND NOT EXISTS (SELECT 1 FROM PurchaseItem pi WHERE pi.PurchaseID = pu.PurchaseID);
