-- DELETE FROM cities; -- (for testing script all over again)
-- sql script that creates a database about cities of the world and their population

-- creating table
CREATE TABLE "cities" ( 
	"id" INTEGER NOT NULL,
	"name" TEXT NOT NULL,
	"population" INTEGER NOT NULL,
	"country" TEXT NOT NULL,
	PRIMARY KEY("id") 
);

-- inserting first set of values
INSERT INTO cities(id, name, population, country)
VALUES
('1', 'Los Angeles', '3,849,000', 'USA'),
('2', 'Frankfurt am Main', '753,056', 'Germany'),
('3', 'Amsterdam', '821,752', 'Netherlands'),
('4', 'Barcelona', '1,620,000', 'Spain'),
('5', 'Medellin', '2,569,000', 'Colombia'),
('6', 'New York', '8,468,000', 'USA'),
('7', 'Bad Hersfeld', '29,984', 'Germany'),
('8', 'Toronto', '2,930,000', 'Canada'),
('9', 'Alajuela', '42,975', 'Costa Rica'),
('10', 'Mannheim', '315,554', 'Germany'),
('11', 'Marrakesh', '928,850', 'Morocco'),
('12', 'Liverpool', '500,500', 'England');

-- selecting all cities from the table
SELECT name FROM cities;

-- selecting all cities from Germany
SELECT name FROM cities WHERE country = 'Germany';

-- updating population of Bad Hersfeld
UPDATE cities
SET population = '32,725'
WHERE name = 'Bad Hersfeld';

-- deleting Amsterdam from Table
DELETE FROM cities 
WHERE name = 'Amsterdam';

-- printing whole table (not required)
SELECT * FROM cities;

