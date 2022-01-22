BEGIN;
create table if not exists cities(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alternatifHadiseIstNo INTEGER,
    boylam NUMERIC,
    enlem NUMERIC,
    gunlukTahminIstNo INTEGER,
    il TEXT,
    ilPlaka INTEGER,
    ilce TEXT,
    merkezId INTEGER,
    oncelik INTEGER,
    saatlikTahminIstNo INTEGER,
    sondurumIstNo INTEGER,
    yukseklik INTEGER,
    aciklama TEXT,
    modelId INTEGER,
    gps INTEGER,
    created REAL DEFAULT (datetime('now', 'localtime')),
    updated REAL);
CREATE INDEX if not exists cities_idx ON cities(ilPlaka);
CREATE UNIQUE INDEX if not exists cities_key ON cities(ilPlaka);
COMMIT;