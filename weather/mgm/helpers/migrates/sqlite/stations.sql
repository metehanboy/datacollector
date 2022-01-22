BEGIN;
create table if not exists stations(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    istNo INTEGER,
    istAd TEXT,
    enlem NUMERIC,
    boylam NUMERIC,
    yukseklik INTEGER,
    ilPlaka INTEGER,
    il TEXT,
    ilce TEXT,
    BirimId INTEGER,
    Indikator TEXT,
    BasincSensor INTEGER,
    NemSensor INTEGER,
    RuzgarSensor INTEGER,
    SicaklikSensor INTEGER,
    ToprakSicSensor INTEGER,
    HaliHazirHavaSensor INTEGER,
    OmgiGrupAdi TEXT,
    YagisSensor INTEGER,
    KarSensor INTEGER,
    created REAL DEFAULT (datetime('now', 'localtime')),
    updated REAL);
CREATE INDEX if not exists stations_idx ON stations(ilPlaka,istNo);
CREATE UNIQUE INDEX if not exists stations_key ON stations(ilPlaka,istNo);
COMMIT;

