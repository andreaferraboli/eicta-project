-- Euphoric Events: relational schema (SQLite)
-- STATUS: DRAFT to be reviewed by the group. Derived from the draft ER model in
-- delivery-1/analysis/text-analysis.md. Every choice is listed in docs/assumptions.md.
--
-- Artificial IDs (note a of the PDF): only Ticket.TicketID and Purchase.PurchaseID,
-- because no attribute in the text can identify a ticket or a purchase.
-- Performance.PerformanceID is NOT artificial: the text says "a performance has a unique identifier".
-- Stage.Code is NOT artificial: the text says "an identification code".

PRAGMA foreign_keys = ON;

CREATE TABLE Festival (
    Name        TEXT PRIMARY KEY,
    Location    TEXT NOT NULL,
    StartDate   DATE NOT NULL,
    EndDate     DATE NOT NULL,
    CHECK (EndDate >= StartDate)
);

CREATE TABLE Stage (
    Code                TEXT PRIMARY KEY,
    Name                TEXT NOT NULL,
    MaxCapacity         INTEGER NOT NULL CHECK (MaxCapacity > 0),
    LocationDescription TEXT NOT NULL,
    FestivalName        TEXT NOT NULL REFERENCES Festival(Name) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Performance (
    PerformanceID INTEGER PRIMARY KEY,
    Title         TEXT NOT NULL,
    Genre         TEXT NOT NULL,
    StartTime     DATETIME NOT NULL,
    EndTime       DATETIME NOT NULL,
    StageCode     TEXT NOT NULL REFERENCES Stage(Code) ON UPDATE CASCADE ON DELETE CASCADE,
    CHECK (EndTime > StartTime)
);

-- ISA Artist -> {Musician, Band}: total, disjoint. Translated as parent + child tables.
-- ArtistType is the discriminator that makes disjointness checkable.
CREATE TABLE Artist (
    StageName  TEXT PRIMARY KEY,
    Country    TEXT NOT NULL,
    MainGenre  TEXT NOT NULL,
    ArtistType TEXT NOT NULL CHECK (ArtistType IN ('musician', 'band'))
);

CREATE TABLE Musician (
    StageName      TEXT PRIMARY KEY REFERENCES Artist(StageName) ON UPDATE CASCADE ON DELETE CASCADE,
    FullName       TEXT NOT NULL,
    Nationality    TEXT NOT NULL,
    MainInstrument TEXT NOT NULL
);

CREATE TABLE Band (
    StageName     TEXT PRIMARY KEY REFERENCES Artist(StageName) ON UPDATE CASCADE ON DELETE CASCADE,
    FormationYear INTEGER NOT NULL CHECK (FormationYear BETWEEN 1900 AND 2100)
);

-- A band is made of at least two musicians (checked in checks.sql, not expressible as a CHECK).
CREATE TABLE BandMember (
    BandName     TEXT NOT NULL REFERENCES Band(StageName) ON UPDATE CASCADE ON DELETE CASCADE,
    MusicianName TEXT NOT NULL REFERENCES Musician(StageName) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (BandName, MusicianName)
);

-- A performance is given by one or more artists.
CREATE TABLE PerformanceArtist (
    PerformanceID   INTEGER NOT NULL REFERENCES Performance(PerformanceID) ON UPDATE CASCADE ON DELETE CASCADE,
    ArtistStageName TEXT NOT NULL REFERENCES Artist(StageName) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (PerformanceID, ArtistStageName)
);

CREATE TABLE Stand (
    Name         TEXT PRIMARY KEY,
    Sponsor      TEXT NOT NULL,
    FestivalName TEXT NOT NULL REFERENCES Festival(Name) ON UPDATE CASCADE ON DELETE CASCADE
);

-- ISA Product -> {Food, Drink, Merchandise}: total, disjoint.
-- Translated by collapsing the children into the parent (single table + discriminator),
-- because Merchandise has no own attribute and Food/Drink share ExpirationDate.
-- The CHECK constraints enforce which attributes each category may/must have.
CREATE TABLE Product (
    Name           TEXT PRIMARY KEY,
    Price          NUMERIC NOT NULL CHECK (Price > 0),
    Category       TEXT NOT NULL CHECK (Category IN ('food', 'drink', 'merchandise')),
    ExpirationDate DATE,
    FoodType       TEXT,
    CHECK ((Category IN ('food', 'drink')) = (ExpirationDate IS NOT NULL)),
    CHECK ((Category = 'food') = (FoodType IS NOT NULL))
);

CREATE TABLE Sells (
    StandName   TEXT NOT NULL REFERENCES Stand(Name) ON UPDATE CASCADE ON DELETE CASCADE,
    ProductName TEXT NOT NULL REFERENCES Product(Name) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (StandName, ProductName)
);

CREATE TABLE Person (
    Email    TEXT PRIMARY KEY,
    FullName TEXT NOT NULL,
    Phone    TEXT NOT NULL
);

-- "Whenever a purchase happens, the system should store the date and the payment method used."
CREATE TABLE Purchase (
    PurchaseID    INTEGER PRIMARY KEY,
    PurchaseDate  DATE NOT NULL,
    PaymentMethod TEXT NOT NULL,
    PersonEmail   TEXT NOT NULL REFERENCES Person(Email) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Ticket (
    TicketID     INTEGER PRIMARY KEY,
    Type         TEXT NOT NULL,
    Price        NUMERIC NOT NULL CHECK (Price >= 0),
    ValidFrom    DATE NOT NULL,
    ValidTo      DATE NOT NULL,
    FestivalName TEXT NOT NULL REFERENCES Festival(Name) ON UPDATE CASCADE ON DELETE CASCADE,
    PurchaseID   INTEGER NOT NULL REFERENCES Purchase(PurchaseID) ON UPDATE CASCADE ON DELETE CASCADE,
    CHECK (ValidTo >= ValidFrom)
);

-- Shop items bought in a purchase, at a stand that sells them.
CREATE TABLE PurchaseItem (
    PurchaseID  INTEGER NOT NULL REFERENCES Purchase(PurchaseID) ON UPDATE CASCADE ON DELETE CASCADE,
    StandName   TEXT NOT NULL,
    ProductName TEXT NOT NULL,
    PRIMARY KEY (PurchaseID, StandName, ProductName),
    FOREIGN KEY (StandName, ProductName) REFERENCES Sells(StandName, ProductName) ON UPDATE CASCADE ON DELETE CASCADE
);
