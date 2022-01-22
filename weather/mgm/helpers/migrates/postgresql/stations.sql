BEGIN;
create schema if not exists mgm;
create table if not exists mgm.stations(
    id serial not null,
    "istNo" int null,
    "istAd" varchar null,
    enlem numeric null,
    boylam numeric null,
    yukseklik int null,
    "ilPlaka" int null,
    il varchar null,
    ilce varchar null,
    "BirimId" int null,
    "Indikator" varchar,
    "BasincSensor" int2 null,
    "NemSensor" int2 null,
    "RuzgarSensor" int2 null,
    "SicaklikSensor" int2 null,
    "ToprakSicSensor" int2 null,
    "HaliHazirHavaSensor" int2 null,
    "OmgiGrupAdi" varchar null,
    "YagisSensor" int2 null,
    "KarSensor" int2 null,
    created timestamp without time zone NULL DEFAULT current_timestamp,
    updated timestamp without time zone null,
    CONSTRAINT stations_pk PRIMARY KEY (id),
    CONSTRAINT stations_key UNIQUE ("ilPlaka","istNo")
);
CREATE INDEX IF NOT EXISTS stations_idx ON mgm.stations ("ilPlaka","istNo");
COMMIT;