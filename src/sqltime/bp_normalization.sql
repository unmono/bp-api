PRAGMA foreign_keys = OFF;

-- Sections/subsections tables:
CREATE TABLE IF NOT EXISTS sect(id INT PRIMARY KEY, title TEXT);
CREATE TABLE subsect(
    id INT PRIMARY KEY,
    sect_id INT,
    title TEXT,
    FOREIGN KEY(sect_id) REFERENCES sects(id)
);
CREATE TABLE IF NOT EXISTS subsub(
    subsect_id INT,
    title TEXT,
    raw_subsub TEXT,
    FOREIGN KEY(subsect_id) REFERENCES subsect(id)
);

WITH sect_dividers AS(
    SELECT instr(sect, '.') AS dotindex, sect
    FROM (SELECT DISTINCT sect FROM pricelist)
) INSERT INTO sect
    SELECT
        substr(sect, 0, dotindex) AS id,
        substr(sect, dotindex + 2) AS title
    FROM sect_dividers;

WITH subsect_dividers AS(
    SELECT
        instr(subsect, '.') AS dotindex,
        instr(subsect, ' ') AS spaceindex,
        subsect
    FROM (SELECT DISTINCT subsect FROM pricelist)
) INSERT INTO subsect
    SELECT
        substr(subsect, 0, dotindex) * 100 + substr(subsect, dotindex + 1, spaceindex - dotindex) AS id,
        substr(subsect, 0, dotindex) AS sect_id,
        substr(subsect, spaceindex + 1) AS title
    FROM subsect_dividers;

WITH subsub_dividers AS(
    SELECT
        instr(subsub, ' ') AS spaceindex,
        instr(subsub, '.') AS first_dotindex,
        subsub
    FROM (SELECT DISTINCT replace(subsub, x'c2a0', x'20') as subsub FROM pricelist)
), subsub_splits AS(
    SELECT
        substr(subsub, spaceindex + 1) AS title,
        substr(subsub, 0, spaceindex) AS numbers,
        spaceindex,
        first_dotindex,
        instr(substr(subsub, first_dotindex + 1, spaceindex), '.') + first_dotindex AS second_dotindex,
        subsub AS raw_subsub
    FROM
        subsub_dividers
) INSERT INTO subsub
    SELECT
        substr(numbers, 0, first_dotindex) * 100
        +
        substr(numbers, first_dotindex + 1, second_dotindex - first_dotindex - 1) AS subsect_id,
        title,
        raw_subsub

    FROM subsub_splits;

ALTER TABLE pricelist
ADD COLUMN subsub_id INT REFERENCES subsub(id);

UPDATE pricelist
SET subsub_id = s.rowid, price = round(price, 2)
FROM subsub AS s
WHERE pricelist.subsub = s.raw_subsub;

ALTER TABLE pricelist DROP COLUMN sect;
ALTER TABLE pricelist DROP COLUMN subsect;
ALTER TABLE pricelist DROP COLUMN subsub;
ALTER TABLE subsub DROP COLUMN raw_subsub;

CREATE TABLE IF NOT EXISTS refs (predecessor TEXT, successor TEXT);
CREATE TABLE IF NOT EXISTS newrelease (part_no TEXT);
CREATE TABLE IF NOT EXISTS masterdata (part_no TEXT);
CREATE TABLE IF NOT EXISTS discontinued (part_no TEXT);

CREATE TABLE partnum (
    part_no TEXT UNIQUE,
    discontinued INT,
    new_release INT
);

INSERT OR IGNORE INTO partnum
    SELECT part_no, 0, 1 FROM newrelease
    UNION ALL
    SELECT part_no, 1, 0 FROM discontinued
    UNION ALL
    SELECT part_no, 0, 0 FROM pricelist
    UNION ALL
    SELECT predecessor, 0, 0 FROM refs
    UNION ALL
    SELECT successor, 0, 0 FROM refs;

CREATE TABLE refers (
    predecessor INT REFERENCES partnum(rowid),
    successor INT REFERENCES partnum(rowid)
);
INSERT INTO refers
    SELECT
        p.rowid AS predecessor,
        s.rowid AS successor
    FROM refs
    INNER JOIN partnum p ON refs.predecessor = p.part_no
    INNER JOIN partnum s ON refs.successor = s.part_no;

ALTER TABLE pricelist
ADD COLUMN partnum_id INT REFERENCES partnum(rowid);

UPDATE pricelist
SET partnum_id = (
    SELECT rowid from partnum where part_no = pricelist.part_no
);

ALTER TABLE pricelist DROP COLUMN part_no;

ALTER TABLE masterdata
ADD COLUMN partnum_id INT REFERENCES partnum(rowid);

UPDATE masterdata
SET partnum_id = (
    SELECT rowid from partnum where part_no = masterdata.part_no
);

ALTER TABLE masterdata DROP COLUMN part_no;

DROP TABLE newrelease;
DROP TABLE discontinued;
DROP TABLE refs;

CREATE INDEX idx_partnum ON partnum(part_no);