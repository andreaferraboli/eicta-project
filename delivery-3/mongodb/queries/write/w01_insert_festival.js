// Requirement: D3-QW-1
// Category: create
// Title: Insert a new festival document
// Description: Inserts a complete festival with 2 stages, 2 performances per stage, 2 artists per performance and 2 stands with 2 products each (no array has fewer than 2 elements).
// Evidence to collect: delivery-3/report/figures/w01_insert_festival.png (MongoDB Compass / Atlas / mongosh)
// Query as typed in mongosh (copy into the report):
/*
const res = db.festivals.insertOne(
  {
    _id: "Demo Winter Fest 2026",
    name: "Demo Winter Fest 2026",
    location: "Trento",
    startDate: ISODate("2026-12-10T00:00:00Z"),
    endDate: ISODate("2026-12-12T00:00:00Z"),
    stages: [
      { code: "STW01A", name: "Ice Dome", maxCapacity: 3000, locationDescription: "inside the arena",
        performances: [
          { performanceId: 9001, title: "Winter Opening", genre: "electronic",
            startTime: ISODate("2026-12-10T21:00:00Z"), endTime: ISODate("2026-12-10T22:30:00Z"),
            artists: [
              { stageName: "Demo DJ One", country: "Italy", mainGenre: "electronic", type: "musician",
                fullName: "Anna Demo", nationality: "Italian", mainInstrument: "turntables" },
              { stageName: "The Demo Band", country: "Austria", mainGenre: "rock", type: "band", formationYear: 2015 }
            ] },
          { performanceId: 9002, title: "Snow Jazz", genre: "jazz",
            startTime: ISODate("2026-12-11T20:00:00Z"), endTime: ISODate("2026-12-11T21:30:00Z"),
            artists: [
              { stageName: "Demo Sax", country: "France", mainGenre: "jazz", type: "musician",
                fullName: "Paul Demo", nationality: "French", mainInstrument: "saxophone" },
              { stageName: "The Demo Trio", country: "Italy", mainGenre: "jazz", type: "band", formationYear: 2009 }
            ] }
        ] },
      { code: "STW01B", name: "Chalet Stage", maxCapacity: 900, locationDescription: "near the slopes",
        performances: [
          { performanceId: 9003, title: "Folk by the Fire", genre: "folk",
            startTime: ISODate("2026-12-10T18:00:00Z"), endTime: ISODate("2026-12-10T19:00:00Z"),
            artists: [
              { stageName: "Demo Fiddle", country: "Ireland", mainGenre: "folk", type: "musician",
                fullName: "Ciara Demo", nationality: "Irish", mainInstrument: "violin" },
              { stageName: "The Demo Band", country: "Austria", mainGenre: "rock", type: "band", formationYear: 2015 }
            ] },
          { performanceId: 9004, title: "Acoustic Sunset", genre: "indie",
            startTime: ISODate("2026-12-11T17:00:00Z"), endTime: ISODate("2026-12-11T18:00:00Z"),
            artists: [
              { stageName: "Demo DJ One", country: "Italy", mainGenre: "electronic", type: "musician",
                fullName: "Anna Demo", nationality: "Italian", mainInstrument: "turntables" },
              { stageName: "Demo Fiddle", country: "Ireland", mainGenre: "folk", type: "musician",
                fullName: "Ciara Demo", nationality: "Irish", mainInstrument: "violin" }
            ] }
        ] }
    ],
    stands: [
      { name: "Demo Hot Drinks", sponsor: "Cloud Coffee",
        products: [
          { name: "Mulled Wine", price: 5.5, category: "drink", expirationDate: ISODate("2027-01-31T00:00:00Z") },
          { name: "Hot Chocolate", price: 4.0, category: "drink", expirationDate: ISODate("2027-01-31T00:00:00Z") }
        ] },
      { name: "Demo Merch Hut", sponsor: "Urban Wear",
        products: [
          { name: "Wool Beanie", price: 18.0, category: "merchandise" },
          { name: "Thermal Mug", price: 12.0, category: "merchandise" }
        ] }
    ]
  }
);
printjson(res);
*/
const res = db.festivals.insertOne(
  {
    _id: "Demo Winter Fest 2026",
    name: "Demo Winter Fest 2026",
    location: "Trento",
    startDate: ISODate("2026-12-10T00:00:00Z"),
    endDate: ISODate("2026-12-12T00:00:00Z"),
    stages: [
      { code: "STW01A", name: "Ice Dome", maxCapacity: 3000, locationDescription: "inside the arena",
        performances: [
          { performanceId: 9001, title: "Winter Opening", genre: "electronic",
            startTime: ISODate("2026-12-10T21:00:00Z"), endTime: ISODate("2026-12-10T22:30:00Z"),
            artists: [
              { stageName: "Demo DJ One", country: "Italy", mainGenre: "electronic", type: "musician",
                fullName: "Anna Demo", nationality: "Italian", mainInstrument: "turntables" },
              { stageName: "The Demo Band", country: "Austria", mainGenre: "rock", type: "band", formationYear: 2015 }
            ] },
          { performanceId: 9002, title: "Snow Jazz", genre: "jazz",
            startTime: ISODate("2026-12-11T20:00:00Z"), endTime: ISODate("2026-12-11T21:30:00Z"),
            artists: [
              { stageName: "Demo Sax", country: "France", mainGenre: "jazz", type: "musician",
                fullName: "Paul Demo", nationality: "French", mainInstrument: "saxophone" },
              { stageName: "The Demo Trio", country: "Italy", mainGenre: "jazz", type: "band", formationYear: 2009 }
            ] }
        ] },
      { code: "STW01B", name: "Chalet Stage", maxCapacity: 900, locationDescription: "near the slopes",
        performances: [
          { performanceId: 9003, title: "Folk by the Fire", genre: "folk",
            startTime: ISODate("2026-12-10T18:00:00Z"), endTime: ISODate("2026-12-10T19:00:00Z"),
            artists: [
              { stageName: "Demo Fiddle", country: "Ireland", mainGenre: "folk", type: "musician",
                fullName: "Ciara Demo", nationality: "Irish", mainInstrument: "violin" },
              { stageName: "The Demo Band", country: "Austria", mainGenre: "rock", type: "band", formationYear: 2015 }
            ] },
          { performanceId: 9004, title: "Acoustic Sunset", genre: "indie",
            startTime: ISODate("2026-12-11T17:00:00Z"), endTime: ISODate("2026-12-11T18:00:00Z"),
            artists: [
              { stageName: "Demo DJ One", country: "Italy", mainGenre: "electronic", type: "musician",
                fullName: "Anna Demo", nationality: "Italian", mainInstrument: "turntables" },
              { stageName: "Demo Fiddle", country: "Ireland", mainGenre: "folk", type: "musician",
                fullName: "Ciara Demo", nationality: "Irish", mainInstrument: "violin" }
            ] }
        ] }
    ],
    stands: [
      { name: "Demo Hot Drinks", sponsor: "Cloud Coffee",
        products: [
          { name: "Mulled Wine", price: 5.5, category: "drink", expirationDate: ISODate("2027-01-31T00:00:00Z") },
          { name: "Hot Chocolate", price: 4.0, category: "drink", expirationDate: ISODate("2027-01-31T00:00:00Z") }
        ] },
      { name: "Demo Merch Hut", sponsor: "Urban Wear",
        products: [
          { name: "Wool Beanie", price: 18.0, category: "merchandise" },
          { name: "Thermal Mug", price: 12.0, category: "merchandise" }
        ] }
    ]
  }
);
printjson(res);
