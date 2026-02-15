from labyrinth_game.constants import ROOMS


def show_inventory(game_state):
    """ Содержимое инвентаря игрока."""
    inv = game_state['player_inventory']
    if inv:
        print("Ваш инвентарь:", ", ".join(inv))
    else:
        print("Инвентарь пуст.")

def get_input(prompt="> "):
    """Запрашивает ввод пользователя, обрабатывает Ctrl+C и Ctrl+D."""
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state, direction):
    """Перемещает игрока в указанном направлении, если выход существует  
    и комната доступна."""
    from labyrinth_game.utils import describe_current_room, random_event

    current_room = game_state['current_room']
    room = ROOMS[current_room]

    if direction not in room['exits']:
        print("Нельзя пойти в этом направлении.")
        return

    next_room = room['exits'][direction]

    if next_room == 'treasure_room':
        if 'rusty_key' in game_state['player_inventory']:
            print("Вы используете найденный ключ, чтобы открыть путь в комнату " \
            "сокровищ.")
        else:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return  

    game_state['current_room'] = next_room
    game_state['steps_taken'] += 1
    print(f"\nВы переместились {direction}.\n")
    describe_current_room(game_state)
    random_event(game_state)

def take_item(game_state, item_name):
    """Подбирает предмет из текущей комнаты, если он там есть."""
    current_room = game_state['current_room']
    room = ROOMS[current_room]

    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item_name in room['items']:
        game_state['player_inventory'].append(item_name)
        room['items'].remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    """Использует предмет из инвентаря, выполняя уникальные действия."""
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return

    if item_name == "torch":
        print("Вы зажгли факел. Вокруг стало светлее.")
    elif item_name == "sword":
        print("Вы чувствуете уверенность, сжимая меч.")
    elif item_name == "bronze_box":
        if "rusty_key" not in game_state['player_inventory']:
            game_state['player_inventory'].append("rusty_key")
            print("Вы открыли бронзовую шкатулку и нашли ржавый ключ!" \
            " Он добавлен в инвентарь.")
        else:
            print("Шкатулка уже открыта, внутри пусто.")
    else:
        print("Вы не знаете, как использовать этот предмет.")