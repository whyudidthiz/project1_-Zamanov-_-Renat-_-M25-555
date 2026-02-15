import math

from labyrinth_game.constants import ROOMS


def describe_current_room(game_state):
    room_id = game_state['current_room']
    room = ROOMS[room_id]

    print(f"\n== {room_id.upper()} ==\n")
    print(room['description'])

    if room['items']:
        print("Заметные предметы:", ", ".join(room['items']))

    if room['exits']:
        exits_str = ", ".join(room['exits'].keys())
        print("Выходы:", exits_str)

    if room['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state):
    from labyrinth_game.player_actions import get_input
    room_id = game_state['current_room']
    room = ROOMS[room_id]

    if not room['puzzle']:
        print("Загадок здесь нет.")
        return

    question, correct_answer = room['puzzle']
    print(f"\nЗагадка: {question}")
    user_answer = get_input("Ваш ответ: ").strip().lower()

    def is_correct(user, correct):
        aliases = {
            '10': ['10', 'десять'],
            '4': ['4', 'четыре'],
            'марс': ['марс'],
            'шаг шаг шаг': ['шаг шаг шаг'],
            'резонанс': ['резонанс']
        }
        if correct in aliases:
            return user in aliases[correct]
        return user == correct

    if is_correct(user_answer, correct_answer):
        print("Верно! Загадка решена.")
        room['puzzle'] = None 

        if room_id == 'library':
            print("Вы нашли древний свиток с подсказкой! (никчему, но приятно)")
        elif room_id == 'crypt':
            print("Из саркофага выпала серебряная монета.")
            room['items'].append('silver_coin')
        elif room_id == 'observatory':
            print("Телескоп показывает новую звезду. Вы чувствуете вдохновение.")
        else:
            print("Вы получили немного опыта.")
    else:
        print("Неверно. Попробуйте снова.")
        if room_id == 'trap_room':
            print("Ваша ошибка активировала скрытый механизм!")
            trigger_trap(game_state)

def attempt_open_treasure(game_state):
    """
    Логика для открытия сундука в сокровищнице.
    Вызывается только в комнате 'treasure_room'.
    """
    from labyrinth_game.player_actions import get_input
    room = ROOMS['treasure_room']
    inventory = game_state['player_inventory']

    if 'treasure_key' in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        if 'treasure_chest' in room['items']:
            room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return

    print("Сундук заперт на кодовый замок.")
    answer = get_input("Хотите попробовать ввести код? (да/нет): ").lower()
    if answer == 'да':
        code = get_input("Введите код: ")
        correct_code = room['puzzle'][1] if room['puzzle'] else None
        if code == correct_code:
            print("Код принят! Замок открыт.")
            if 'treasure_chest' in room['items']:
                room['items'].remove('treasure_chest')
            print("В сундуке сокровище! Вы победили!")
            game_state['game_over'] = True
        else:
            print("Неверный код. Замок остаётся закрытым.")
    else:
        print("Вы отступаете от сундука.")

def pseudo_random(seed, modulo):
    
    a = 12.9898
    b = 43758.5453
    x = math.sin(seed * a) * b

    frac = x - math.floor(x)

    return int(frac * modulo)

def trigger_trap(game_state):
    """
    Имитирует срабатывание ловушки.
    Если у игрока есть предметы — теряет один случайный предмет.
    Если инвентарь пуст — возможна смерть.
    """
    print("\nЛовушка активирована! Пол стал дрожать...")
    inventory = game_state['player_inventory']
    steps = game_state['steps_taken']

    if inventory:
        idx = pseudo_random(steps, len(inventory))
        lost_item = inventory.pop(idx)
        print(f"Вы потеряли: {lost_item}")
    else:
        luck = pseudo_random(steps, 10)
        if luck < 3:
            print("Вы не удержались и провалились в яму... Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вам чудом удалось уцелеть!")

def random_event(game_state):
    """
    Генерирует случайное событие после перемещения.
    Вызывается только если событие происходит (вероятность 0.1).
    """
    steps = game_state['steps_taken']
    
    if pseudo_random(steps, 10) != 0:
        return  

    event_type = pseudo_random(steps + 1, 3)  

    if event_type == 0:
        print("\nВы заметили что-то блестящее на полу. Это монетка!")
        current_room = game_state['current_room']
        ROOMS[current_room]['items'].append('coin')

    elif event_type == 1:
        print("\nВы слышите шорох за спиной...")
        if 'sword' in game_state['player_inventory']:
            print("Вы хватаетесь за меч, и шорох затихает. Существо отпугнуто.")

    else:  
        if (game_state['current_room'] == 'trap_room'
            and 'torch' not in game_state['player_inventory']):
                print("\nВы чувствуете, как пол под ногами начинает проваливаться!")
                trigger_trap(game_state)
        else:
            pass

def show_help(commands):
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f" {cmd:<16} {desc}")