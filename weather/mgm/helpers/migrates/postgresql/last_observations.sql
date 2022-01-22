BEGIN;
create schema if not exists mgm;
create table if not exists mgm.last_observations(
        id serial not null,
        "istNo" int null,
        "veriZamani" timestamp without time zone null,
        "denizVeriZamani" timestamp without time zone null,
        sicaklik numeric null,
        "aktuelBasinc" numeric null,
        "denizSicaklik" numeric null,
        "denizeIndirgenmisBasinc" numeric null,
        gorus numeric null,
        "hadiseKodu" varchar null,
        kapalilik numeric null,
        "karYukseklik" numeric null,
        nem numeric null,
        "rasatMetar" varchar null,
        "rasatSinoptik" varchar null,
        "rasatTaf" varchar null,
        "ruzgarHiz" numeric null,
        "ruzgarYon" numeric null,
        "yagis00Now" numeric null,
        "yagis10Dk" numeric null,
        "yagis12Saat" numeric null,
        "yagis1Saat" numeric null,
        "yagis24Saat" numeric null,
        "yagis6Saat" numeric null,
        counter int DEFAULT 0,
        created timestamp without time zone NULL DEFAULT current_timestamp,
        updated timestamp without time zone null,
        CONSTRAINT last_observations_pk PRIMARY KEY (id),
        CONSTRAINT last_observations_key UNIQUE ("istNo","veriZamani")
);
CREATE INDEX IF NOT EXISTS last_observations_idx ON mgm.last_observations ("istNo","veriZamani","denizVeriZamani",created);
COMMIT;