BEGIN;

CREATE TABLE address (
    id                          INTEGER PRIMARY KEY,
    address_recipient           TEXT,
    address_recipient_addition  TEXT,
    address_street              TEXT NOT NULL,
    address_city                TEXT NOT NULL,
    address_zip_code            TEXT NOT NULL,
    address_accessible          BOOLEAN NOT NULL CHECK (address_accessible IN (0, 1))
);

CREATE TABLE link (
    id          INTEGER PRIMARY KEY,
    link_type   TEXT NOT NULL CHECK (
        link_type IN ('website', 'instagram', 'mastodon', 'facebook', 'twitter')
    ),
    value       TEXT NOT NULL CHECK (length(trim(value)) > 0)
);

CREATE TABLE institution (
    id                  INTEGER PRIMARY KEY,
    institution_type    TEXT NOT NULL CHECK (
        institution_type IN (
            'kita_vorschule',
            'grundschule',
            'schule',
            'universität',
            'verein',
            'privates_unternehmen',
            'städtisches_unternehmen',
            'stiftung',
            'städtische_organisation',
            'amt',
            'ministerium',
            'pflegeheim'
        )
    ),
    name                TEXT NOT NULL CHECK (length(trim(name)) > 0),
    description         TEXT NOT NULL,
    address_id          INTEGER NOT NULL REFERENCES address(id)
                        ON UPDATE CASCADE
                        ON DELETE RESTRICT,
    logo_url            TEXT,
    link_id             INTEGER REFERENCES link(id)
                        ON UPDATE CASCADE
                        ON DELETE SET NULL
);

CREATE TABLE agent (
    id                  INTEGER PRIMARY KEY,
    institution_id      INTEGER NOT NULL REFERENCES institution(id)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE,
    first_name          TEXT NOT NULL CHECK (length(trim(first_name)) > 0),
    last_name           TEXT NOT NULL CHECK (length(trim(last_name)) > 0),
    phone               TEXT,
    email               TEXT NOT NULL CHECK (length(trim(email)) > 0),
    link_id             INTEGER REFERENCES link(id)
                        ON UPDATE CASCADE
                        ON DELETE SET NULL
);

CREATE TABLE offer (
    id                              INTEGER PRIMARY KEY,
    institution_id                  INTEGER NOT NULL REFERENCES institution(id)
                                    ON UPDATE CASCADE
                                    ON DELETE CASCADE,
    offer_type                      TEXT NOT NULL CHECK (
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
            'beratung',
            'arbeitsgruppe'
        )
    ),
    name                            TEXT NOT NULL CHECK (length(trim(name)) > 0),
    agent_id                        INTEGER REFERENCES agent(id)
                                    ON UPDATE CASCADE
                                    ON DELETE SET NULL,
    image_url                       TEXT,
    description                     TEXT NOT NULL,
    address_id                      INTEGER REFERENCES address(id)
                                    ON UPDATE CASCADE
                                    ON DELETE SET NULL,

    timeframe_duration_minutes      INTEGER NOT NULL CHECK (
        timeframe_duration_minutes > 0
    ),
    timeframe_recurrence_interval   INTEGER CHECK (
        timeframe_recurrence_interval IS NULL
        OR timeframe_recurrence_interval > 0
    ),
    timeframe_recurrence_unit       TEXT CHECK (
        timeframe_recurrence_unit IN ('woche', 'monat', 'jahr')
    ),
    timeframe_note                  TEXT,

    cost_type                       TEXT NOT NULL CHECK (
        cost_type IN ('free', 'paid')
    ),
    cost_amount                     REAL CHECK (
        cost_amount IS NULL OR cost_amount >= 0
    ),
    cost_currency                   TEXT NOT NULL DEFAULT 'EUR' CHECK (
        cost_currency = 'EUR'
    ),
    cost_unit                       TEXT,
    cost_note                       TEXT,

    min_participants                INTEGER NOT NULL CHECK (
        min_participants > 0
    ),
    max_participants                INTEGER NOT NULL CHECK (
        max_participants >= min_participants
    ),

    link_id                         INTEGER REFERENCES link(id)
                                    ON UPDATE CASCADE
                                    ON DELETE SET NULL,

    CHECK (
        (
            timeframe_recurrence_interval IS NULL
            AND timeframe_recurrence_unit IS NULL
        )
        OR
        (
            timeframe_recurrence_interval IS NOT NULL
            AND timeframe_recurrence_unit IS NOT NULL
        )
    ),

    CHECK (
        (cost_type = 'free' AND (cost_amount IS NULL OR cost_amount = 0))
        OR
        (cost_type = 'paid' AND cost_amount IS NOT NULL AND cost_amount > 0)
    )
);

CREATE TABLE offer_location (
    id		INTEGER PRIMARY KEY,
    offer_id    INTEGER NOT NULL REFERENCES offer(id)
                ON UPDATE CASCADE
                ON DELETE CASCADE,
    location    TEXT NOT NULL CHECK (
        location IN (
            'bei_euch',
            'bei_uns',
            'dritter_ort',
            'online'
        )
    )
);

CREATE TABLE offer_target_group (
    id          INTEGER PRIMARY KEY,
    offer_id        INTEGER NOT NULL REFERENCES offer(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
    target_group    TEXT NOT NULL CHECK (length(trim(target_group)) > 0)
);

CREATE TABLE offer_sdg (
    id          INTEGER PRIMARY KEY,
    offer_id    INTEGER NOT NULL REFERENCES offer(id)
                ON UPDATE CASCADE
                ON DELETE CASCADE,
    sdg         INTEGER NOT NULL CHECK (sdg BETWEEN 1 AND 17)
);

CREATE INDEX idx_institution_address_id
    ON institution(address_id);

CREATE INDEX idx_institution_link_id
    ON institution(link_id);

CREATE INDEX idx_agent_institution_id
    ON agent(institution_id);

CREATE INDEX idx_agent_link_id
    ON agent(link_id);

CREATE INDEX idx_offer_institution_id
    ON offer(institution_id);

CREATE INDEX idx_offer_agent_id
    ON offer(agent_id);

CREATE INDEX idx_offer_address_id
    ON offer(address_id);

CREATE INDEX idx_offer_link_id
    ON offer(link_id);

CREATE INDEX idx_offer_location_location
    ON offer_location(location);

CREATE INDEX idx_offer_target_group_target_group
    ON offer_target_group(target_group);

CREATE INDEX idx_offer_sdg_sdg
    ON offer_sdg(sdg);

COMMIT;
