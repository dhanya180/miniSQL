CREATE TABLE users (id INT, name TEXT, age INT);
INSERT INTO users VALUES (1, Alice, 22);
INSERT INTO users VALUES (2, Bob, 17);
INSERT INTO users VALUES (3, Carol, 30);
SELECT name FROM users WHERE age > 18;