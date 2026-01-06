-- In this SQL file, write (and comment!) the typical SQL queries users will run on your database

-- The queries shoulde be to add pokemons but all of that is managed by the app.py file --

SELECT * FROM pokemon WHERE id = 1; -- bulbasaur if it is in the DB
SELECT * FROM pokemon_info WHERE name = "charmander" -- Show all the charmander things like in the pokedex if it is in the DB