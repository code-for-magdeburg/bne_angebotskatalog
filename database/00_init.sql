BEGIN;

CREATE TABLE institution (
    id                  INTEGER PRIMARY KEY,
    institution_type    TEXT NOT NULL CHECK(
        institution_type IN ('kita_vorschule','grundschule','schule','universität','verein','privates_unternehmen','städtisches_unternehmen','stiftung','städtische_organisation','amt','ministerium','pflegeheim')
    ),
    name                TEXT NOT NULL,
    description         TEXT NOT NULL,
    address_id          INTEGER NOT NULL REFERENCES address(id),
    logo_url             TEXT,
    link            INTEGER REFERENCES link(id)
);

CREATE TABLE address (
    id        INTEGER PRIMARY KEY,
    address_recipient TEXT NOT NULL,
    address_recipient_addition TEXT,
    address_street TEXT NOT NULL,
    address_city TEXT NOT NULL,
    address_zip_code TEXT NOT NULL,
    address_accessible     BOOLEAN NOT NULL
);

CREATE TABLE link (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    link_type   TEXT NOT NULL CHECK(
        link_type IN ('website','instagram','mastodon','facebook','twitter')
    ),
    value       TEXT NOT NULL
);

CREATE TABLE agent (
    id              INTEGER PRIMARY KEY,
    institution_id  INTEGER NOT NULL REFERENCES institution(id),
    first_name      TEXT NOT NULL,
    last_name       TEXT NOT NULL,
    phone           TEXT,
    email           TEXT NOT NULL,
    link	    INTEGER REFERENCES link(id)
);

CREATE TABLE offer (
    id INTEGER PRIMARY KEY,
    institution_id INTEGER NOT NULL REFERENCES institution(id),
    offer_type TEXT NOT NULL CHECK (
        offer_type IN (
            'workshop',
            'exkursion',
            'mentoring',
            'podiumsdiskussion',
            'ausstellung',
            'infostand',
            'projekttag',
            'projektwoche',
            'kino',
            'fortbildung',
            'ausleihbares_lernmaterial',
            'beratung'
        )
    ),
    name TEXT NOT NULL,
    agents INTEGER REFERENCES agent(id),
    image_url TEXT,
    description TEXT NOT NULL,
    address_id INTEGER REFERENCES address(id),
    timeframe_duration_minutes INTEGER NOT NULL,
    timeframe_recurrence_interval INTEGER,
    timeframe_recurrence_unit TEXT CHECK (
        timeframe_recurrence_unit IN ('woche', 'monat', 'jahr')
    ),
    timeframe_note TEXT,
    cost_type TEXT NOT NULL CHECK (cost_type IN ('free', 'paid')),
    cost_amount REAL,
    cost_currency TEXT CHECK (cost_currency IN ('EUR')) DEFAULT 'EUR',
    cost_unit TEXT,
    cost_note TEXT,
    min_participants INTEGER NOT NULL,
    max_participants INTEGER NOT NULL,
    link INTEGER REFERENCES link(id)
);

CREATE TABLE offer_location (
    offer_id INTEGER NOT NULL REFERENCES offer(id),
    location TEXT NOT NULL CHECK (
        location IN (
            'bei_euch',
            'bei_uns',
            'dritter_ort',
            'online'
        )
    ),
    PRIMARY KEY (offer_id, location)
);

CREATE TABLE offer_target_group (
    offer_id INTEGER NOT NULL REFERENCES offer(id),
    target_group TEXT NOT NULL,
    PRIMARY KEY (offer_id, target_group)
);

CREATE TABLE offer_sdg (
    offer_id INTEGER NOT NULL REFERENCES offer(id),
    sdg INTEGER NOT NULL CHECK (sdg BETWEEN 1 AND 17),
    PRIMARY KEY (offer_id, sdg)
);

COMMIT;

