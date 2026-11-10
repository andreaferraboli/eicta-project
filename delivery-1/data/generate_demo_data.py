"""Deterministic DEMO data generator for the Euphoric Events schema.

THIS IS A FALLBACK FOR LOCAL TESTING ONLY. It is NOT evidence for task 4 of the
first delivery, which requires the data to be generated with Mockaroo
(see delivery-1/mockaroo/README.md).

The data shape is chosen so that the later deliveries can reuse it without
violating their constraints:
- every festival has >= 2 stages and >= 2 stands
- every stage has >= 2 performances
- every performance has >= 2 artists
- every stand sells >= 2 products
  (delivery 3 requires at least two elements per array of sub-documents)

Usage:  python generate_demo_data.py [output.sql]
Stdlib only. Same output on every run (fixed seed).
"""

import random
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

SEED = 20251002
N_FESTIVALS = 25
STAGES_PER_FESTIVAL = 2
PERFORMANCES_PER_STAGE = 2
STANDS_PER_FESTIVAL = 2
N_MUSICIANS = 30
N_BANDS = 25
N_PERSONS = 40

FESTIVAL_WORDS = ["Aurora", "Solstice", "Echo", "Neon", "Riverside", "Horizon", "Velvet", "Lunar",
                  "Summit", "Harbor", "Prism", "Wild", "Golden", "Electric", "Coral"]
CITIES = ["Milano", "Torino", "Bologna", "Roma", "Napoli", "Firenze", "Verona", "Genova",
          "Bari", "Palermo", "Trento", "Padova", "Rimini", "Cagliari", "Lecce"]
GENRES = ["rock", "jazz", "electronic", "pop", "hip hop", "indie", "metal", "folk", "techno", "soul"]
COUNTRIES = ["Italy", "France", "Germany", "Spain", "UK", "USA", "Sweden", "Brazil", "Japan", "Nigeria"]
NATIONALITIES = {"Italy": "Italian", "France": "French", "Germany": "German", "Spain": "Spanish",
                 "UK": "British", "USA": "American", "Sweden": "Swedish", "Brazil": "Brazilian",
                 "Japan": "Japanese", "Nigeria": "Nigerian"}
INSTRUMENTS = ["guitar", "bass", "drums", "piano", "vocals", "synthesizer", "saxophone", "violin", "trumpet", "turntables"]
FIRST = ["Luca", "Giulia", "Marco", "Sara", "Andrea", "Elena", "Paolo", "Chiara", "Davide", "Marta",
         "Noah", "Emma", "Liam", "Mia", "Hugo", "Lea", "Kenji", "Ada", "Tom", "Ines"]
LAST = ["Rossi", "Bianchi", "Ferrari", "Russo", "Romano", "Gallo", "Costa", "Fontana", "Conti", "Greco",
        "Martin", "Smith", "Muller", "Garcia", "Silva", "Sato", "Okafor", "Berg", "Dubois", "Lopez"]
SPONSORS = ["Acme Drinks", "Nordic Bikes", "Sunny Foods", "Pixel Telecom", "Blue Bank", "Green Energy",
            "Urban Wear", "Fresh Market", "Sound Gear", "Cloud Coffee"]
PAYMENT_METHODS = ["credit card", "debit card", "cash", "PayPal", "Apple Pay"]
TICKET_TYPES = [("regular", 59.0), ("day pass", 35.0), ("VIP", 149.0)]
FOODS = [("Veggie Burger", "vegetarian"), ("Falafel Wrap", "vegan"), ("Margherita Slice", "vegetarian"),
         ("Pulled Pork Bun", "meat"), ("Fish Tacos", "fish"), ("Gluten-free Pasta", "gluten-free"),
         ("Tofu Bowl", "vegan"), ("Chicken Skewers", "meat"), ("Caprese Panino", "vegetarian"),
         ("Poke Bowl", "fish"), ("Arancino", "vegetarian"), ("Hot Dog", "meat")]
DRINKS = ["Craft IPA", "Lager Pint", "Lemon Soda", "Still Water", "Sparkling Water", "Iced Tea",
          "Cola", "Orange Juice", "Spritz", "Cold Brew", "Ginger Beer", "Energy Drink"]
MERCH = ["Festival T-shirt", "Logo Cap", "Tote Bag", "Poster", "Wristband", "Hoodie",
         "Sticker Pack", "Bandana", "Water Bottle", "Enamel Pin", "Vinyl Sampler", "Rain Poncho"]


def q(value):
    """SQL literal."""
    if value is None:
        return "NULL"
    if isinstance(value, (int, float)):
        return repr(value)
    return "'" + str(value).replace("'", "''") + "'"


def insert(table, rows):
    cols = list(rows[0].keys())
    lines = [f"INSERT INTO {table} ({', '.join(cols)}) VALUES"]
    lines.append(",\n".join("  (" + ", ".join(q(r[c]) for c in cols) + ")" for r in rows) + ";")
    return "\n".join(lines)


def generate():
    rnd = random.Random(SEED)
    data = {}

    # Festivals: one per week from 2026-05-01, 3 to 4 days each.
    festivals = []
    for i in range(N_FESTIVALS):
        start = date(2026, 5, 1) + timedelta(days=7 * i)
        end = start + timedelta(days=rnd.choice([2, 3]))
        suffix = ["Fest", "Sound Days"][i // len(FESTIVAL_WORDS)]
        festivals.append({"Name": f"{FESTIVAL_WORDS[i % len(FESTIVAL_WORDS)]} {suffix} {start.year}",
                          "Location": CITIES[i % len(CITIES)],
                          "StartDate": start.isoformat(), "EndDate": end.isoformat()})
    data["Festival"] = festivals

    stages = []
    for fi, f in enumerate(festivals):
        for s in range(STAGES_PER_FESTIVAL):
            stages.append({"Code": f"ST{fi + 1:02d}{chr(65 + s)}",
                           "Name": ["Main Stage", "Forest Stage", "Lake Stage", "Dome"][(fi + s) % 4],
                           "MaxCapacity": rnd.choice([800, 1500, 2500, 5000, 12000]),
                           "LocationDescription": ["north field", "near the main entrance", "by the lake",
                                                   "inside the pavilion", "south lawn"][(fi + 2 * s) % 5],
                           "FestivalName": f["Name"]})
    data["Stage"] = stages
    festival_by_name = {f["Name"]: f for f in festivals}

    # Artists (ISA): musicians first, then bands.
    musicians, artists = [], []
    for i in range(N_MUSICIANS):
        country = COUNTRIES[i % len(COUNTRIES)]
        full = f"{FIRST[i % len(FIRST)]} {LAST[(i * 7) % len(LAST)]}"
        stage_name = f"{FIRST[i % len(FIRST)][0]}{LAST[(i * 7) % len(LAST)]} {['Jr', 'Lux', 'Nova', 'X', 'Blue', 'Ray'][i % 6]}"
        artists.append({"StageName": stage_name, "Country": country,
                        "MainGenre": GENRES[i % len(GENRES)], "ArtistType": "musician"})
        musicians.append({"StageName": stage_name, "FullName": full,
                          "Nationality": NATIONALITIES[country],
                          "MainInstrument": INSTRUMENTS[(i * 3) % len(INSTRUMENTS)]})
    band_words = ["Wolves", "Satellites", "Mirrors", "Comets", "Lanterns", "Owls", "Tides", "Engines",
                  "Rivers", "Ghosts", "Pilots", "Gardens", "Signals"]
    bands = []
    for i in range(N_BANDS):
        name = f"The {['Silver', 'Midnight', 'Paper', 'Crystal', 'Velvet'][i % 5]} {band_words[i % len(band_words)]}"
        artists.append({"StageName": name, "Country": COUNTRIES[(i * 3) % len(COUNTRIES)],
                        "MainGenre": GENRES[(i * 7) % len(GENRES)], "ArtistType": "band"})
        bands.append({"StageName": name, "FormationYear": 1985 + (i * 13) % 38})
    data["Artist"], data["Musician"], data["Band"] = artists, musicians, bands

    members = []
    for i, b in enumerate(bands):
        chosen = rnd.sample(musicians, 2 + i % 3)  # 2 to 4 members
        members += [{"BandName": b["StageName"], "MusicianName": m["StageName"]} for m in chosen]
    data["BandMember"] = members

    performances, perf_artists = [], []
    pid = 1
    for st in stages:
        f = festival_by_name[st["FestivalName"]]
        day0 = date.fromisoformat(f["StartDate"])
        for k in range(PERFORMANCES_PER_STAGE):
            day = day0 + timedelta(days=k % 2)
            start = datetime(day.year, day.month, day.day, 18 + 2 * k, 0)
            genre = GENRES[(pid * 3) % len(GENRES)]
            performances.append({"PerformanceID": pid,
                                 "Title": f"{genre.title()} Night #{pid}",
                                 "Genre": genre,
                                 "StartTime": start.isoformat(sep=" ", timespec="minutes"),
                                 "EndTime": (start + timedelta(minutes=90)).isoformat(sep=" ", timespec="minutes"),
                                 "StageCode": st["Code"]})
            for a in rnd.sample(artists, 2 + pid % 2):  # 2 or 3 artists
                perf_artists.append({"PerformanceID": pid, "ArtistStageName": a["StageName"]})
            pid += 1
    data["Performance"], data["PerformanceArtist"] = performances, perf_artists

    stands = []
    for fi, f in enumerate(festivals):
        for s in range(STANDS_PER_FESTIVAL):
            stands.append({"Name": f"{['Food Court', 'Bar', 'Merch Corner', 'Snack Point'][(fi + s) % 4]} {fi + 1:02d}{chr(65 + s)}",
                           "Sponsor": SPONSORS[(fi * 2 + s) % len(SPONSORS)],
                           "FestivalName": f["Name"]})
    data["Stand"] = stands

    products = []
    for i, (name, ftype) in enumerate(FOODS):
        products.append({"Name": name, "Price": round(6 + (i * 1.5) % 9, 2), "Category": "food",
                         "ExpirationDate": (date(2026, 9, 1) + timedelta(days=i * 5)).isoformat(), "FoodType": ftype})
    for i, name in enumerate(DRINKS):
        products.append({"Name": name, "Price": round(2.5 + (i * 0.75) % 6, 2), "Category": "drink",
                         "ExpirationDate": (date(2027, 1, 1) + timedelta(days=i * 20)).isoformat(), "FoodType": None})
    for i, name in enumerate(MERCH):
        products.append({"Name": name, "Price": round(5 + (i * 4) % 40, 2), "Category": "merchandise",
                         "ExpirationDate": None, "FoodType": None})
    data["Product"] = products

    sells = []
    for i, st in enumerate(stands):
        # products[i % n] guarantees every product is sold by at least one stand
        chosen = [products[i % len(products)]]
        chosen += rnd.sample([p for p in products if p is not chosen[0]], 2)
        sells += [{"StandName": st["Name"], "ProductName": p["Name"]} for p in chosen]
    data["Sells"] = sells

    persons = []
    for i in range(N_PERSONS):
        fn, ln = FIRST[(i * 3) % len(FIRST)], LAST[(i * 11) % len(LAST)]
        persons.append({"Email": f"{fn.lower()}.{ln.lower()}{i + 1}@example.com",
                        "FullName": f"{fn} {ln}", "Phone": f"+39 3{rnd.randint(10, 99)} {rnd.randint(1000000, 9999999)}"})
    data["Person"] = persons

    purchases, tickets, items = [], [], []
    stands_by_festival = {}
    for st in stands:
        stands_by_festival.setdefault(st["FestivalName"], []).append(st)
    sells_by_stand = {}
    for s in sells:
        sells_by_stand.setdefault(s["StandName"], []).append(s["ProductName"])

    purchase_id, ticket_id = 1, 1
    # Ticket purchases: one per person, 1 or 2 tickets each, bought before the festival.
    for i, person in enumerate(persons):
        f = festivals[i % len(festivals)]
        start, end = date.fromisoformat(f["StartDate"]), date.fromisoformat(f["EndDate"])
        purchases.append({"PurchaseID": purchase_id,
                          "PurchaseDate": (start - timedelta(days=10 + i)).isoformat(),
                          "PaymentMethod": PAYMENT_METHODS[i % len(PAYMENT_METHODS)],
                          "PersonEmail": person["Email"]})
        for _ in range(1 + i % 2):
            ttype, price = TICKET_TYPES[ticket_id % len(TICKET_TYPES)]
            valid_to = start if ttype == "day pass" else end
            tickets.append({"TicketID": ticket_id, "Type": ttype, "Price": price,
                            "ValidFrom": start.isoformat(), "ValidTo": valid_to.isoformat(),
                            "FestivalName": f["Name"], "PurchaseID": purchase_id})
            ticket_id += 1
        purchase_id += 1
    # Shop purchases: during the festival the person holds a ticket for, 1 to 3 items each.
    for i, person in enumerate(persons):
        f = festivals[i % len(festivals)]
        purchases.append({"PurchaseID": purchase_id,
                          "PurchaseDate": f["StartDate"],
                          "PaymentMethod": PAYMENT_METHODS[(i + 2) % len(PAYMENT_METHODS)],
                          "PersonEmail": person["Email"]})
        stand = stands_by_festival[f["Name"]][i % STANDS_PER_FESTIVAL]
        for prod in sells_by_stand[stand["Name"]][: 1 + i % 3]:
            items.append({"PurchaseID": purchase_id, "StandName": stand["Name"], "ProductName": prod})
        purchase_id += 1
    data["Purchase"], data["Ticket"], data["PurchaseItem"] = purchases, tickets, items
    return data


ORDER = ["Festival", "Stage", "Artist", "Musician", "Band", "BandMember", "Performance",
         "PerformanceArtist", "Stand", "Product", "Sells", "Person", "Purchase", "Ticket", "PurchaseItem"]


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("demo") / "seed_demo.sql"
    out.parent.mkdir(parents=True, exist_ok=True)
    data = generate()
    parts = ["-- DEMO DATA generated by generate_demo_data.py (deterministic fallback).",
             "-- NOT generated with Mockaroo: not valid as evidence for task 4 of delivery 1.",
             "PRAGMA foreign_keys = ON;", "BEGIN TRANSACTION;"]
    parts += [insert(t, data[t]) for t in ORDER]
    parts.append("COMMIT;")
    out.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    print(f"wrote {out} ({', '.join(f'{t}={len(data[t])}' for t in ORDER)})")


if __name__ == "__main__":
    main()
