BEGIN;
create table if not exists last_observations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        istNo INTEGER,
        veriZamani REAL,
        denizVeriZamani REAL,
        sicaklik NUMERIC,
        aktuelBasinc NUMERIC,
        denizSicaklik NUMERIC,
        denizeIndirgenmisBasinc NUMERIC,
        gorus NUMERIC,
        hadiseKodu TEXT,
        kapalilik NUMERIC,
        karYukseklik NUMERIC,
        nem NUMERIC,
        rasatMetar TEXT,
        rasatSinoptik TEXT,
        rasatTaf TEXT,
        ruzgarHiz NUMERIC,
        ruzgarYon NUMERIC,
        yagis00Now NUMERIC,
        yagis10Dk NUMERIC,
        yagis12Saat NUMERIC,
        yagis1Saat NUMERIC,
        yagis24Saat NUMERIC,
        yagis6Saat NUMERIC,
        counter INTEGER DEFAULT(0),
        created REAL DEFAULT (datetime('now', 'localtime')),
        updated REAL);
CREATE INDEX if not exists last_observations_idx ON last_observations(istNo,veriZamani,denizVeriZamani,created);
CREATE UNIQUE INDEX if not exists last_observations_key ON last_observations(istNo,veriZamani);
COMMIT;
