BEGIN;
create table if not exists districts(
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
CREATE INDEX if not exists districts_idx ON districts(ilPlaka,ilce);
CREATE UNIQUE INDEX if not exists districts_key ON districts(ilPlaka,ilce);
COMMIT;
