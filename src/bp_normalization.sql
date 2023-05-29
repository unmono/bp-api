PRAGMA foreign_keys = OFF;

-- CREATING TABLES
-- ----------------------------
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
-- Table to hold every mentioned part number in the pricelist
-- and related flags
CREATE TABLE partnum (
    part_no TEXT UNIQUE,
    discontinued INT,
    new_release INT
);
-- Junction table to reference related partnumbers
CREATE TABLE refers (
    predecessor INT REFERENCES partnum(rowid),
    successor INT REFERENCES partnum(rowid),
    PRIMARY KEY(predecessor, successor)
);
-- Empty unrequired tables in case of their absence in the price release
CREATE TABLE IF NOT EXISTS refs (predecessor TEXT, successor TEXT);
CREATE TABLE IF NOT EXISTS newrelease (part_no TEXT);
CREATE TABLE IF NOT EXISTS masterdata (part_no TEXT);
CREATE TABLE IF NOT EXISTS discontinued (part_no TEXT);

-- ADDING COLUMNS
-- ----------------------------
-- Subsub foreign key
ALTER TABLE pricelist
ADD COLUMN subsub_id INT REFERENCES subsub(id);
-- Partnum relation column
ALTER TABLE pricelist
ADD COLUMN partnum_id INT REFERENCES partnum(rowid);
-- Partnum relation column
ALTER TABLE masterdata
ADD COLUMN partnum_id INT REFERENCES partnum(rowid);

-- MOVING DATA AROUND
-- ----------------------------
BEGIN TRANSACTION;
    -- Section table
    -- String, that holds section number and title is like:
    -- 1. Section title
    -- The number of section becomes an id
    WITH sect_dividers AS(
        SELECT instr(sect, '.') AS dotindex, sect
        FROM (SELECT DISTINCT sect FROM pricelist)
    ) INSERT INTO sect
        SELECT
            -- sqlite counts chars from 1 and instr returns the number of given char
            -- in a string. Counting from 0 here has effect of python-like behavior.
            substr(sect, 0, dotindex) AS id,
            substr(sect, dotindex + 2) AS title
        FROM sect_dividers;

    -- Subsection table
    -- Now we have numbers of section and subsection
    -- 1.1 Subsection title
    -- First number becomes fk to sections
    -- Then first is multiplied by 100 and adds to second, thus we get 101.
    -- And it becomes a pk of subsection.
    -- By 100 because the maximum number of subsections in bp is 99.
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

    -- Sub-subsection table
    -- The same way in subsub string we have:
    -- 1.1.1 Subsub title
    -- First and second characters forms a 101 like in subsection table
    -- Don't need predefined pk here, but the initial string has to be saved
    -- to relate pricelist entries.
    WITH subsub_dividers AS(
        SELECT
            instr(subsub, ' ') AS spaceindex,
            instr(subsub, '.') AS first_dotindex,
            subsub
        -- In one release there were strings that contain unbreakable spaces.
        -- Replace them to normal ones.
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

    -- Populating partnum table from all provided tables along with flags
    -- UNION for some reason messes up with the flags, no matter what order
    -- of tables used
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

    -- Populating junction table for referencing related part numbers
    INSERT OR IGNORE INTO refers
        SELECT
            p.rowid AS predecessor,
            s.rowid AS successor
        FROM refs
        INNER JOIN partnum p ON refs.predecessor = p.part_no
        INNER JOIN partnum s ON refs.successor = s.part_no

        UNION

        SELECT
            s.rowid AS predecessor,
            p.rowid AS successor
        FROM refs
        INNER JOIN partnum p ON refs.predecessor = p.part_no
        INNER JOIN partnum s ON refs.successor = s.part_no;


    -- Relating pricelist entries to sub-subsections
    -- And rounding prices by the way
    UPDATE pricelist
    SET subsub_id = s.rowid, price = round(price, 2)
    FROM subsub AS s
    WHERE pricelist.subsub = s.raw_subsub;

    CREATE UNIQUE INDEX idx_partnum ON partnum(part_no);

    -- Relating pricelist entries to part numbers table
    UPDATE pricelist
    SET partnum_id = (
        SELECT rowid from partnum where part_no = pricelist.part_no
    );

    -- Relating masterdata entries to part numbers table
    UPDATE masterdata
    SET partnum_id = (
        SELECT rowid from partnum where part_no = masterdata.part_no
    );
COMMIT TRANSACTION;


-- DELETING REDUNDAND DATA
-- ----------------------------
ALTER TABLE pricelist DROP COLUMN part_no;
ALTER TABLE pricelist DROP COLUMN sect;
ALTER TABLE pricelist DROP COLUMN subsect;
ALTER TABLE pricelist DROP COLUMN subsub;
ALTER TABLE subsub DROP COLUMN raw_subsub;

ALTER TABLE masterdata DROP COLUMN part_no;

DROP TABLE newrelease;
DROP TABLE discontinued;
DROP TABLE refs;

-- todo: Delete duplicats!