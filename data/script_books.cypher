:auto USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM "http://localhost:11001/project-f1a57a82-eafa-4113-9afc-38d6c0ff708d/book.csv" AS row FIELDTERMINATOR ','
WITH row, row.Title AS title, row.Genre AS genre
MERGE (s:book {title:title, genre:genre});

:auto USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM "http://localhost:11001/project-f1a57a82-eafa-4113-9afc-38d6c0ff708d/people.csv" AS row FIELDTERMINATOR ','
WITH row, toInteger(row.id) AS id, row.name AS name
MERGE (s:User{id:id, name:name});

WITH range(5,35) as userRange
MATCH (u:User)
WITH collect(u) as users, userRange
MATCH (b:book)
WITH b, apoc.coll.randomItems(users, apoc.coll.randomItem(userRange)) as users, toInteger(rand()*5) as score
FOREACH (user in users | CREATE (user)-[:rates{score:score}]->(b));