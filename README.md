# Design Document

By Rossi Lucas

Video overview: <URL [HERE](https://studio.youtube.com/video/cKws74EyS7Y/edit)>

## Scope

In this section you should answer the following questions:

* What is the purpose of your database? The purpose of this database is to store Pokémon and allow users to access essential information about each one through a dynamic console interface. Users will be able to add Pokémon manually and interact with their stored data in a simple and intuitive way.
* Which people, places, things, etc. are you including in the scope of your database?
The database will include the following information about each Pokémon:

The official Pokémon ID

The Pokémon’s name

Its type or types

Its weight

Its main ability or abilities

Its evolution chain

This information represents the minimum data necessary for interacting with the Pokémon through the project’s console-based interface.
* Which people, places, things, etc. are *outside* the scope of your database? 
The database will not include more complex or extensive Pokémon attributes, such as:

All possible abilities from the games

Game-specific locations where the Pokémon can be found

Biome information

Colors, shiny variations, or visual data

Any other secondary attributes

These details are outside the scope of the project and will not be stored in the database.

## Functional Requirements

In this section you should answer the following questions:

* What should a user be able to do with your database? 
Users should be able to:

Add new Pokémon to the database

Remove an existing Pokémon

Search or filter to look for all of one pokemon

See al pokemons

All of these actions will be performed through a dynamic console interface using numbered menu options.
* What's beyond the scope of what a user should be able to do with your database?
Users will not be able to perform actions that require data not included in the database. For example:

Accessing extended information like all abilities or game-specific details

Viewing shiny forms, colors, or other visual attributes

Handling any Pokémon attributes not explicitly stored in the database

These features are intentionally excluded to maintain the project’s scope and complexity at an appropriate level.

## Representation

### Entities

In this section you should answer the following questions:

* Which entities will you choose to represent in your database?
Pokémon

This entity contains all the essential information needed for the console application to function. Since the scope of the project focuses on storing and managing manually added Pokémon, a single, well-structured Pokémon entity is sufficient.

* What attributes will those entities have?
The attributes they will have are:
Official pokemon Id
Pokemon name
Pokemon type 1
Pokemon type 2 if it have
Pokemon Weight
Pokemon main abiliti
Pokemon Secondary ability if it have
Pokemon evolution chain, like the base pokemon, if it have their first evolution and if it have too the second one

* Why did you choose the types you did?
Because these are the basic things you want to know about a pokemon, exept for the id, every table in sql have an id so i use that to my favor
* Why did you choose the constraints you did?
I use in majority NOT NULL because some things like the name or pokemon id can't be null, it will make imposible to look it on the other relations


### Relationships

[text](https://www.mermaidchart.com/d/f05afc7a-6d84-4751-8bbe-6b2ff83c3ff7)

## Optimizations

In this section you should answer the following questions:

* Which optimizations (e.g., indexes, views) did you create? Why?
I crate a view to look for all the things a pokemon have like in the pokedex, i want to create anindex but in the videos says the primary keys in sqlite already have some weird index created but if i want to crate a index it will by the pokemon id index

## Limitations

In this section you should answer the following questions:

* What are the limitations of your design?: Cant filter pokemon, like the plant types, cant order by heaviest for example
* What might your database not be able to represent very well?: The pokemon output because i made a many to many relationship and i find very hard to made a correct and stylized output of all the pokemon things like the pokedes but it's possible
