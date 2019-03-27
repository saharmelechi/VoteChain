CREATE TABLE IF NOT EXISTS voters(
 voter_identification TEXT PRIMARY KEY
) WITHOUT ROWID;

INSERT INTO voters (voter_identification)
VALUES ('testing')