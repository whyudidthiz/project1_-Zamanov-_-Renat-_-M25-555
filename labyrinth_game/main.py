#!/usr/bin/env python3

from labyrinth_game.constants import ROOMS
from labyrinth_game import utils, player_actions
from labyrinth_game.constants import COMMANDS

game_state = {
    'player_inventory': [],
    'current_room': 'entrance',
    'game_over': False,
    'steps_taken': 0
}

def process_command(game_state, command):
    if not command:
        return

    parts = command.split()
    action = parts[0]

    # Односложные команды направления
    if action in ['north', 'south', 'east', 'west']:
        player_actions.move_player(game_state, action)
        return

    match action:
        case "quit" | "exit":
            print("Игра завершена.")
            game_state['game_over'] = True

        case "look":
            utils.describe_current_room(game_state)

        case "inventory" | "inv":
            player_actions.show_inventory(game_state)

        case "go":
            if len(parts) < 2:
                print("Укажите направление (например: go north)")
            else:
                direction = parts[1]
                player_actions.move_player(game_state, direction)

        case "take":
            if len(parts) < 2:
                print("Укажите предмет (например: take torch)")
            else:
                item_name = parts[1]
                player_actions.take_item(game_state, item_name)

        case "use":
            if len(parts) < 2:
                print("Укажите предмет (например: use torch)")
            else:
                item_name = parts[1]
                player_actions.use_item(game_state, item_name)

        case "solve":
            if game_state['current_room'] == 'treasure_room':
                utils.attempt_open_treasure(game_state)
            else:
                utils.solve_puzzle(game_state)

        case "help":
            utils.show_help(COMMANDS)

        case _:
            print("Неизвестная команда. Попробуйте: look, inventory, go <направление>, take <предмет>, use <предмет>, solve, help, quit")

def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    utils.describe_current_room(game_state)

    while not game_state['game_over']:
        command = player_actions.get_input()
        process_command(game_state, command)

if __name__ == "__main__":
    main()