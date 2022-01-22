BEGIN;
create schema if not exists mgm;
create table if not exists mgm.cities(
    id serial not null,
    "ilPlaka" int2 null,
    il varchar null,
    ilce varchar null,
    oncelik int2 null,
    yukseklik numeric null,
    boylam numeric null,
    enlem numeric null,
    aciklama varchar null,
    "sondurumIstNo" int null,
    "saatlikTahminIstNo" int null,
    "gunlukTahminIstNo" int null,
    "alternatifHadiseIstNo" int null,
    "merkezId" int null,
    "modelId" int null,
    gps int2 null,
    created timestamp without time zone NULL DEFAULT current_timestamp,
    updated timestamp without time zone null,
    CONSTRAINT cities_pk PRIMARY KEY (id),
    CONSTRAINT cities_key UNIQUE ("ilPlaka")
);
CREATE INDEX IF NOT EXISTS cities_idx ON mgm.cities ("ilPlaka");
COMMIT;