BEGIN;
create schema if not exists mgm;
create table if not exists mgm.districts(
    id serial not null,
    "ilPlaka" int2 null,
    il varchar null,
    ilce varchar null,
    oncelik int2 null,
    yukseklik int null,
    boylam numeric null,
    enlem numeric null,
    aciklama varchar null,
    "sondurumIstNo" int null,
    "saatlikTahminIstNo" int null,
    "gunlukTahminIstNo" int null,
    "alternatifHadiseIstNo" int null,
    "merkezId" int null,
    "modelId" int null,
    gps int null,
    created timestamp without time zone NULL DEFAULT current_timestamp,
    updated timestamp without time zone null,
    CONSTRAINT districts_pk PRIMARY KEY (id),
    CONSTRAINT districts_key UNIQUE ("ilPlaka",ilce)
);
CREATE INDEX IF NOT EXISTS districts_idx ON mgm.districts ("ilPlaka",il,ilce);
COMMIT;