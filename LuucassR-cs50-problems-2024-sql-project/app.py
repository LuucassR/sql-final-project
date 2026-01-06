import requests
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import datetime


def manageApp():

    pokemon_final_info = {
        "id": None,
        "name": None,
        "abilities": [],
        "types": [],
        "specifications": ["weight", "height"],
        "evolutions": [],
    }

    def getOption():
        print(
            "1. Add pokemon  2. Remove pokemon  3. See all pokemons  4. See all of a specific pokemon 5. quit"
        )
        pokemon_to_search_option = input("Option: ")
        print()
        options = ["1", "2", "3", "4", "5"]
        if pokemon_to_search_option not in options:
            print("Please select a valid option")
            return None
        return pokemon_to_search_option


    def get_pokemon_request(pokemon_name):
        try:
            pokemon_rq = requests.get(
                f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
            )
            pokemon_rq.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            return None
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: {e}")
            return None
        except requests.exceptions.Timeout as e:
            print(f"Timeout Error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"An unexpected error occurred: {e}")
            return None

        return pokemon_rq

    def get_evolution_chain(pokemon_name):
        poke_rq = get_pokemon_request(pokemon_name)
        if not poke_rq:
            return []

        data = poke_rq.json()
        pokemon_species_url = data.get("species")["url"]

        specie_rq = requests.get(pokemon_species_url)
        specie_data = specie_rq.json()

        evolution_chain_url = specie_data.get("evolution_chain")["url"]
        evolution_rq = requests.get(evolution_chain_url)
        evolution_data = evolution_rq.json()

        evolutions_list = []

        def print_evolutions(chain):
            species_name = chain["species"]["name"]
            evolutions_list.append(species_name)
            for evolves_to in chain.get("evolves_to", []):
                print_evolutions(evolves_to)

        print_evolutions(evolution_data["chain"])
        return evolutions_list

    def add_pokemon():
        pokemon_final_info = {
            "id": None,
            "name": None,
            "abilities": [],
            "types": [],
            "specifications": ["weight", "height"],
            "evolutions": [],
        }

        print("Provide the name of the pokemon you want to add to the Database")
        pokemon = input("Pokemon: ").lower().strip()
        poke_rq = get_pokemon_request(pokemon)

        if not poke_rq:
            print("Not pokemon request")
            return None

        data = poke_rq.json()

        # Pokemon id
        pokemon_final_info["id"] = data.get("id")

        # Pokemon name
        pokemon_final_info["name"] = pokemon

        # Abilities
        for ability in data.get("abilities", []):
            ability_name = ability["ability"]["name"]
            pokemon_final_info["abilities"].append(ability_name)

        # Types
        for type_info in data.get("types", []):
            type_name = type_info["type"]["name"]
            pokemon_final_info["types"].append(type_name)

        # Weight & Height (Specifications)
        pokemon_final_info["specifications"][0] = data.get("weight")
        pokemon_final_info["specifications"][1] = data.get("height")

        # Evolutions
        evolutions = get_evolution_chain(pokemon)
        pokemon_final_info["evolutions"] = evolutions

        engine = create_engine("sqlite+pysqlite:///pokemons.db")

        with engine.connect() as conn:
            conn.execute(
                text(
                    "INSERT INTO pokemon (id, name, date_added) VALUES (:id, :name, :date_added)"
                ),
                {
                    "id": pokemon_final_info["id"],
                    "name": pokemon_final_info["name"],
                    "date_added": datetime.datetime.now().strftime("%d-%m-%Y"),
                },
            )

            for ability_name in pokemon_final_info["abilities"]:
                conn.execute(
                    text("INSERT INTO abilities (name) VALUES (:name)"),
                    {"name": ability_name},
                )
                ability_id = conn.execute(
                    text("SELECT id FROM abilities WHERE name = :name"),
                    {"name": ability_name},
                ).fetchone()[0]
                conn.execute(
                    text(
                        "INSERT INTO pokemon_abilities (pokemon_id, ability_id) VALUES (:pid, :aid)"
                    ),
                    {"pid": pokemon_final_info["id"], "aid": ability_id},
                )

            for type_name in pokemon_final_info["types"]:
                conn.execute(
                    text("INSERT INTO types (name) VALUES (:name)"), {"name": type_name}
                )
                type_id = conn.execute(
                    text("SELECT id FROM types WHERE name = :name"), {"name": type_name}
                ).fetchone()[0]
                conn.execute(
                    text(
                        "INSERT INTO pokemon_types (pokemon_id, type_id) VALUES (:pid, :tid)"
                    ),
                    {"pid": pokemon_final_info["id"], "tid": type_id},
                )

            conn.execute(
                text("INSERT INTO specifications (weight, height) VALUES (:w, :h)"),
                {
                    "w": pokemon_final_info["specifications"][0],
                    "h": pokemon_final_info["specifications"][1],
                },
            )

            spec_id = conn.execute(
                text("SELECT id FROM specifications ORDER BY id DESC LIMIT 1")
            ).fetchone()[0]
            conn.execute(
                text(
                    "INSERT INTO pokemon_specifications (pokemon_id, specifications_id) VALUES (:pid, :sid)"
                ),
                {"pid": pokemon_final_info["id"], "sid": spec_id},
            )
            if evolutions:
                base = pokemon_final_info["evolutions"][0]
                first = (
                    pokemon_final_info["evolutions"][1] if len(evolutions) > 1 else None
                )
                second = (
                    pokemon_final_info["evolutions"][2] if len(evolutions) > 2 else None
                )
                conn.execute(
                    text(
                        "INSERT INTO evolution_chain (id, base, first_evolution, second_evolution) VALUES (:id, :base, :first, :second)"
                    ),
                    {
                        "id": pokemon_final_info["id"],
                        "base": base,
                        "first": first,
                        "second": second,
                    },
                )
                evol_id = pokemon_final_info["id"]
                conn.execute(
                    text(
                        "INSERT INTO pokemon_evolutions (pokemon_id, evolutions_id) VALUES (:pid, :eid)"
                    ),
                    {"pid": pokemon_final_info["id"], "eid": evol_id},
                )

            conn.commit()

    def remove_pokemon():
        # Prompt for pokemon
        print("What pokemon you want to remove fromthe Data Base")
        pokemon = input("Pokemon: ")

        # Get datadabse
        engine = create_engine("sqlite+pysqlite:///pokemons.db")

        # Connect database
        with engine.connect() as conn:
            try:
                # Get pokemon id
                pokemon_id = conn.execute(
                    text("SELECT id FROM pokemon WHERE name = :name"), {"name": pokemon}
                ).fetchone()

                if not pokemon_id:
                    return print("No such pokemon in the Data Base")

                pokemon_id = pokemon_id[0]

                conn.execute(text("DELETE FROM pokemon_abilities WHERE pokemon_id = :pid"), {"pid": pokemon_id})
                conn.execute(text("DELETE FROM pokemon_types WHERE pokemon_id = :pid"), {"pid": pokemon_id})
                conn.execute(text("DELETE FROM pokemon_specifications WHERE pokemon_id = :pid"), {"pid": pokemon_id})
                conn.execute(text("DELETE FROM pokemon_evolutions WHERE pokemon_id = :pid"), {"pid": pokemon_id})

                conn.execute(text("DELETE FROM pokemon WHERE id = :pid"), {"pid": pokemon_id})

                conn.execute(text("""
                    DELETE FROM abilities
                    WHERE id NOT IN (SELECT ability_id FROM pokemon_abilities)
                """))
                conn.execute(text("""
                    DELETE FROM types
                    WHERE id NOT IN (SELECT type_id FROM pokemon_types)
                """))
                conn.execute(text("""
                    DELETE FROM specifications
                    WHERE id NOT IN (SELECT specifications_id FROM pokemon_specifications)
                """))
                conn.execute(text("""
                    DELETE FROM evolution_chain
                    WHERE id NOT IN (SELECT evolutions_id FROM pokemon_evolutions)
                """))
                
                conn.commit()
                
                print(f"Pokemon '{pokemon}' removed.")

            except OperationalError as e:
                print("Database error:", e)
            except Exception as e:
                print("An error occurred:", e)

    def see_all_pokemons():
        engine = create_engine("sqlite+pysqlite:///pokemons.db")

        print("These are all the pokemons in the database")

        with engine.connect() as conn:
            for pokemon in conn.execute(text("SELECT name FROM pokemon")):
                print(pokemon[0])


    def see_pokemon():
        engine = create_engine("sqlite+pysqlite:///pokemons.db")

        see_all_pokemons()

        print("Which one you want to see")
        pokemon = input("Pokemon: ").strip()

        with engine.connect() as conn:
            rows = conn.execute(
                text("SELECT * FROM pokemon_info WHERE name = :pokemon"),
                {"pokemon": pokemon},
            ).fetchall()

            if not rows:
                print("No such pokemon in the Data Base")
                return

            for row in rows:
                print(row)


    while True:
        option = getOption()
        if (option == "5"):
            print("Quitting...")
            return None
        if option == "1":
            add_pokemon()
        elif option == "2":
            remove_pokemon()
        elif option == "3":
            see_all_pokemons()
        elif option == "4":
            see_pokemon()
        else:
            return print("Not a valid option")
    

    return pokemon_final_info


if __name__ == "__main__":
    manageApp()
