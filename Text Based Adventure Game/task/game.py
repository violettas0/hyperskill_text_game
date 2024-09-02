import json
import sys
import os

commands = ['/h', '/q', '/i', '/c', '/s']
user_name = ''
inventory = []
difficulty = ''
n_of_lives = 0

formating = {
    'name' : '',
    'species' : '',
    'gender' : '',
    'snack' : '',
    'weapon' : '',
    'tool' : ''
}


def menu():
    print('***Welcome to the Pupa\'s World***')
    print('1. Start a new game (START)')
    print('2. Load your progress (LOAD)')
    print('3. Quit the game (QUIT)')

    option = input().lower()

    if option in ['1', 'start']:
        print('Starting a new game...')
        starting_game()
    elif option in ['2', 'load']:
        load_game()
    elif option in ['3', 'quit']:
        print('Goodbye')
    else:
        print('Unknown input! Please enter a valid one.')
        menu()


def load_game():
    global inventory, difficulty, n_of_lives, user_name, formating
    while True:
        print('Choose username (/b - back):')
        directory_path = 'data\\saves'
        files = os.listdir(directory_path)
        json_files = [file for file in files if file.endswith('.json')]
        for jsonf in json_files:
            print(os.path.splitext(jsonf)[0])
        user_name_load = input()
        if user_name_load.lower() == '/b':
            menu()
            return
        elif f'{user_name_load.lower()}.json' in json_files:

            with open(f'data\\saves\\{user_name_load}.json', 'r') as f:
                load_data = json.load(f)
            formating = {
                'name': load_data['character']['name'],
                'species': load_data['character']['species'],
                'gender': load_data['character']['gender'],
                'snack': load_data['inventory']['snack_name'],
                'weapon': load_data['inventory']['weapon_name'],
                'tool': load_data['inventory']['tool_name']
            }
            inventory = [*load_data['inventory']['content']]
            n_of_lives = load_data['lives']
            difficulty = load_data['difficulty']
            user_name = user_name_load

            print('Loading your progress...')
            print(f'Level {load_data["progress"]["level"].strip("level")}')

            game(int(load_data['progress']['level'].strip('level')), load_data['progress']['scene'])

            break
        else:
            print('Unknown input! Please enter a valid one.')
            load_game()
            break
    return formating, inventory, n_of_lives, difficulty


def starting_game():
    global inventory, difficulty, n_of_lives, user_name
    difficulties = {'1': 'easy', '2': 'medium', '3': 'hard'}
    lives = {'easy' : 5, 'medium' : 3, 'hard' : 1}

    while True:
        user_name = input('Enter a username (\'/b\' to go back):')
        if user_name.lower() == '/b':
            menu()
            return
        else:
            break

    print('Create your character:')
    formating['name'] = input('Name:')
    formating['species'] = input('Species:')
    formating['gender']= input('Gender:')
    print('Pack your bag for the journey:')
    formating['snack'] = input('Snack:')
    formating['weapon'] = input('Weapon:')
    formating['tool'] = input('Tool:')
    inventory_values = ['snack', 'tool', 'weapon']
    inventory = list(map(formating.get, inventory_values))

    while True:
        print('Choose your difficulty:')
        print('1. Easy\n2. Medium\n3. Hard')
        difficulty_option = input().lower()
        if difficulty_option in difficulties or difficulty_option in difficulties.values():
            if difficulty_option in difficulties:
                difficulty = difficulties[difficulty_option]
            else:
                difficulty = difficulty_option
            n_of_lives = lives[difficulty]

            break
        else:
            print('Unknown input! Please enter a valid one.')

    print(f'Good luck on your journey, {user_name}!')
    print(f'Your character: {formating["name"]}, {formating["species"]}, {formating["gender"]}')
    print(f'Your inventory: {formating["snack"]}, {formating["weapon"]}, {formating["tool"]}')
    print(f'Difficulty: {difficulty}')
    print(f'Number of lives: {n_of_lives}')
    game(1)

def game(level, starting_scene_n = 'scene1'):
    global inventory, difficulty, n_of_lives, user_name

    path = 'data\\story.json'

    with open(path, 'r') as f:
        data = json.load(f)

    level_str = f'level{level}'
    starting_scene = data[level_str]['scenes'][starting_scene_n]['text']
    starting_options = data[level_str]['scenes'][starting_scene_n]['options']
    counter = 0
    dict_opt = {}

    print(starting_scene)

    for keys in starting_options:
        counter += 1
        print(f'{counter}. {keys["option_text"]}'.format(**formating))
        dict_opt[counter] = keys

    option = option_handle(dict_opt, starting_scene_n, level_str)

    while True:
        counter = 0
        scene = dict_opt[int(option)]['next']
        if dict_opt[int(option)]['next'] == 'end':
            level += 1
            print(f'Level {level}')
            break
        next = data[level_str]['scenes'][scene]['text']
        options = data[level_str]['scenes'][scene]['options']

        print(next.format(**formating))

        for keys in options:
            counter += 1
            print(f'{counter}. {keys["option_text"]}'.format(**formating))
            dict_opt[counter] = keys
        print(scene)
        option = option_handle(dict_opt, scene, level_str)


    #sys.exit()
    game(level)

def commands_logic(option, scene, level_str):
    global inventory, difficulty, n_of_lives, user_name
    if option.lower() == '/h':
        print('Type the number of the option you want to choose.\nCommands you can use:\n/i => Shows inventory.\n/q => Exits the game.\n/c => Shows the character traits.\n/h => Shows help.\n/s => Save the game.')
        return
    elif option.lower() == '/c':
        print(f'Your character: {formating["name"]}, {formating["species"]}, {formating["gender"]}.\nLives remaining: {n_of_lives}')
        return
    elif option.lower() == '/i':
        print(f'Inventory: {", ".join(inventory)}')
        return
    elif option.lower() == '/s':
        print(user_name)
        path_data = f'data\\saves\\{user_name}.json'
        if os.path.exists(path_data):
            with open(f'data\\saves\\{user_name}.json', "r") as f:
                old_data = json.load(f)
                f.close()
            user_data = {
                "character": {
                    "name": formating["name"],
                    "species": formating["species"],
                    "gender": formating["gender"]
                },
                "inventory": {
                    "snack_name": formating["snack"],
                    "weapon_name": formating["weapon"],
                    "tool_name": formating["tool"],
                    "content": inventory
                },
                "progress": {
                    "level": level_str,
                    "scene": scene
                },
                "lives": n_of_lives,
                "difficulty": difficulty
            }
            try:
                with open(path_data, "w") as file:
                    json.dump(user_data, file)  # This handles JSON serialization and writing
                    file.flush()  # Explicitly flush to ensure data is written

                print('Game saved!')
            except Exception as e:
                print(f"An error occurred while saving the game: {e}")

        else:
            with open(f'data\\saves\\{user_name}.json', "w") as file:
                user_data = {
                    "character": {
                        "name": formating["name"],
                        "species": formating["species"],
                        "gender": formating["gender"]
                    },
                    "inventory": {
                        "snack_name": formating["snack"],
                        "weapon_name": formating["weapon"],
                        "tool_name": formating["tool"],
                        "content": inventory
                    },
                    "progress": {
                        "level": level_str,
                        "scene": scene
                    },
                    "lives": n_of_lives,
                    "difficulty": difficulty
                }
                file.write(json.dumps(user_data))
                file.close()
                print('Game saved!')

        return

    elif option.lower() == '/q':
        print('Thanks for playing!')
        sys.exit()

def option_handle(dict_opt, scene, level_str):
    global inventory, difficulty, n_of_lives
    option = input()
    if option.lower() in commands:
        commands_logic(option, scene, level_str)
        return option_handle(dict_opt, scene, level_str)
    else:
        result = dict_opt[int(option)]['result_text']
        actions = dict_opt[int(option)]['actions']
        for action in actions:
            if action == 'hit':
                n_of_lives -= 1
                if n_of_lives == 0:
                    print('You died')
                    game(1)
                    return
                print(f'Lives remaining: {n_of_lives}')
            elif action == 'heal':
                n_of_lives += 1
                print(f'Lives remaining: {n_of_lives}')
            elif action.startswith('-'):
                item = formating[action.strip('-{}')]
                inventory.remove(item)
                print(f'Item removed: {action.strip("-").format(**formating)}')
            elif action.startswith('+'):
                formating[action.strip('+{}')] = action.strip('+{}')
                inventory.append(action.strip('+'))
                print(f'Item added: {action.strip("+").format(**formating)}')

        print(result.format(**formating))
        return option

menu()