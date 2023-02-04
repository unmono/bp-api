CREATE TEMPORARY VIEW v_sect
    AS
    SELECT DISTINCT sect FROM pricelist;

CREATE TEMPORARY VIEW v_subsect
    AS
    SELECT DISTINCT subsect FROM pricelist;

CREATE TEMPORARY VIEW v_subsub
    AS
    SELECT DISTINCT replace(subsub, x'c2a0', x'20') as subsub
    FROM pricelist;

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
    FOREIGN KEY(subsect_id) REFERENCES subsect(id)
);

WITH sect_dividers AS(
    SELECT instr(sect, '.') AS dotindex, sect
    FROM v_sect
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
    FROM v_subsect
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
    FROM v_subsub
), subsub_splits AS(
    SELECT
        substr(subsub, spaceindex + 1) AS title,
        substr(subsub, 0, spaceindex) AS numbers,
        spaceindex,
        first_dotindex,
        instr(substr(subsub, first_dotindex + 1, spaceindex), '.') + first_dotindex AS second_dotindex
    FROM
        subsub_dividers
) INSERT INTO subsub
    SELECT
        substr(numbers, 0, first_dotindex) * 100
        +
        substr(numbers, first_dotindex + 1, second_dotindex - first_dotindex -1) AS subsect_id,
        title
    FROM subsub_splits;
