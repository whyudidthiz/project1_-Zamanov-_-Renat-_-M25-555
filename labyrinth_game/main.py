#!/usr/bin/env python3
from labyrinth_game.constants import ROOMS
from labyrinth_game import utils, player_actions

game_state = {
    'player_inventory': [],
    'current_room': 'entrance',
    'game_over': False,
    'steps_taken': 0
}

def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    utils.describe_current_room(game_state)

    # Игровой цикл
    while not game_state['game_over']:
        command = player_actions.get_input()
        if command == "quit":
            print("Игра завершена.")
            break
        elif command == "":
            continue
        elif command == "inventory" or command == "inv":
            player_actions.show_inventory(game_state)
        elif command == "look":
            utils.describe_current_room(game_state)
        else:
            print("Неизвестная команда. Попробуйте: look, inventory, solve, go <направление>")

if __name__ == "__main__":
    main()
