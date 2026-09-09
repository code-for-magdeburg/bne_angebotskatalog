export type Institution = {
    id: number;
    institution_type: "kita_vorschule" | "grundschule" | "schule" | "universität" | "verein" | "privates_unternehmen" | "städtisches_unternehmen" | "stiftung" | "städtische_organisation" | "amt" | "ministerium" | "pflegeheim";
    name: string;
    description: string;
    address: Address;
    links: Link[];
    logo_url: string;
}

type Link = {
    link_type: "website" | "instagram" | "mastodon" | "facebook" | "twitter";
    value: string;
}

type Agent = {
    id: number;
    institution_id: number;
    first_name: string;
    last_name: string;
    phone?: string;
    email: string;
    links?: Link[];
}

type Address = {
    recipient: string;
    recipient_addition?: string;
    street: string;
    zip_code: string;
    city: string;
    accessible: boolean;
}

/**
 * an offer can be booked by a school (it must contain tangible information)
 */
type Offer = {
    id: number;
    institution_id: number;
    offer_type: "workshop" | "exkursion" | "mentoring" | "podiumsdiskussion" | "ausstellung" | "infostand" | "projekttag" | "projektwoche" | "kino" | "fortbildung" | "ausleihbares_lernmaterial" | "beratung" | "wettbewerb" | "führung" | "seminar" | "vortrag" | "ag" | "schülerfirma";
    name: string;
    image_url?: string;
    description: string;
    location: ("bei_euch" | "bei_uns" | "dritter_ort" | "online")[];
    location_address?: Address;
    timeframe: Timeframe;
    cost: Cost;
    agents: Agent[];
    links?: Link[];
    topics: string[];
    target_groups: ("vorschulkinder" | "grundschulkinder" | "unterstufe" | "oberstufe" | "studierende" | "lehrkräfte" | "auszubildende" | "fachkräfte" | "familien" | "ehrenamtliche" | "senioren" | "pädagogen" | "hausmeister" | "schulleitung" | "für_alle")[];
    min_participants: number;
    max_participants: number;
    sdgs: (1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17)[]
}

type Cost =
    | { cost_type: "free"; note?: string }
    | { cost_type: "paid"; amount: number; currency: "EUR"; unit?: string; note?: string };

type Timeframe = {
    duration_minutes: number;
    recurrence?: {
        interval: number;
        unit: "woche" | "monat" | "jahr";
    };
    note?: string; // freeform fallback, e.g. "nach Absprache"
};