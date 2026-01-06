CREATE TABLE
  pokemon (
    id INTEGER,
    name TEXT NOT NULL,
    date_added TEXT NOT NULL,
    PRIMARY KEY (id)
  );

CREATE TABLE
  abilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
  );

CREATE TABLE
  pokemon_abilities (
    pokemon_id INTEGER,
    ability_id INTEGER,
    PRIMARY KEY (pokemon_id, ability_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon (id),
    FOREIGN KEY (ability_id) REFERENCES abilities (id)
  );

CREATE TABLE
  types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
  );

CREATE TABLE
  pokemon_types (
    pokemon_id INTEGER,
    type_id INTEGER,
    PRIMARY KEY (pokemon_id, type_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon (id),
    FOREIGN KEY (type_id) REFERENCES types (id)
  );

CREATE TABLE
  specifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    weight INTEGER NOT NULL,
    height TEXT NOT NULL
  );

CREATE TABLE
  pokemon_specifications (
    pokemon_id INTEGER,
    specifications_id INTEGER,
    PRIMARY KEY (pokemon_id, specifications_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon (id),
    FOREIGN KEY (specifications_id) REFERENCES specifications (id)
  );

CREATE TABLE
  evolution_chain (
    id INTEGER,
    base TEXT,
    first_evolution TEXT,
    second_evolution TEXT,
    PRIMARY KEY (id)
  );

CREATE TABLE
  pokemon_evolutions (
    pokemon_id INTEGER,
    evolutions_id INTEGER,
    PRIMARY KEY (pokemon_id, evolutions_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon (id),
    FOREIGN KEY (evolutions_id) REFERENCES evolution_chain (id)
  );

CREATE VIEW
  pokemon_info AS
SELECT
  pokemon.id,
  pokemon.name,
  pokemon.date_added,
  abilities.name AS ability,
  types.name AS type,
  specifications.weight,
  specifications.height,
  evolution_chain.base,
  evolution_chain.first_evolution,
  evolution_chain.second_evolution
FROM
  pokemon
  LEFT JOIN pokemon_abilities ON pokemon.id = pokemon_abilities.pokemon_id
  LEFT JOIN abilities ON pokemon_abilities.ability_id = abilities.id
  LEFT JOIN pokemon_types ON pokemon.id = pokemon_types.pokemon_id
  LEFT JOIN types ON pokemon_types.type_id = types.id
  LEFT JOIN pokemon_specifications ON pokemon.id = pokemon_specifications.pokemon_id
  LEFT JOIN specifications ON pokemon_specifications.specifications_id = specifications.id
  LEFT JOIN pokemon_evolutions ON pokemon.id = pokemon_evolutions.pokemon_id
  LEFT JOIN evolution_chain ON pokemon_evolutions.evolutions_id = evolution_chain.id;