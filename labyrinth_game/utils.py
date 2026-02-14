import math
from labyrinth_game.constants import ROOMS

def describe_current_room(game_state):
    """ описание текущей комнаты."""
    room_id = game_state['current_room']
    room = ROOMS[room_id]

    # Название комнаты заглавными
    print(f"\n== {room_id.upper()} ==\n")
    # Описание
    print(room['description'])

    # Предметы
    if room['items']:
        print("Заметные предметы:", ", ".join(room['items']))

    # Выходы
    if room['exits']:
        exits_str = ", ".join(room['exits'].keys())
        print("Выходы:", exits_str)

    # Загадка
    if room['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state):
    """Обработка решения загадки в текущей комнате."""
    
    from labyrinth_game.player_actions import get_input
    room_id = game_state['current_room']
    room = ROOMS[room_id]

    if not room['puzzle']:
        print("Загадок здесь нет.")
        return

    question, correct_answer = room['puzzle']
    print(f"\nЗагадка: {question}")
    user_answer = get_input("Ваш ответ: ")

    if user_answer == correct_answer:
        print("Верно! Загадка решена.")
        # Убираем загадку, чтобы нельзя было решить повторно
        room['puzzle'] = None
        # Можно добавить награду (например, случайный предмет или очки)
        print("Вы получили немного опыта.")
        # Здесь можно добавить выдачу предмета, если нужно
    else:
        print("Неверно. Попробуйте снова.")

def attempt_open_treasure(game_state):
    """
    Логика для открытия сундука в сокровищнице.
    Вызывается только в комнате 'treasure_room'.
    """
    from labyrinth_game.player_actions import get_input
    room = ROOMS['treasure_room']
    inventory = game_state['player_inventory']

    # Проверяем, есть ли ключ
    if 'treasure_key' in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        # Удаляем сундук из комнаты
        if 'treasure_chest' in room['items']:
            room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return

    # Ключа нет, предлагаем ввести код
    print("Сундук заперт на кодовый замок.")
    answer = get_input("Хотите попробовать ввести код? (да/нет): ").lower()
    if answer == 'да':
        code = get_input("Введите код: ")
        # Правильный ответ из загадки комнаты
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
    """
    Генерирует псевдослучайное число на основе seed (целое) и modulo.
    Использует формулу на основе синуса.
    Возвращает целое число от 0 до modulo-1.
    """
    # Большие дробные множители для "размазывания"
    a = 12.9898
    b = 43758.5453
    # Синус от seed * a, затем умножаем на b
    x = math.sin(seed * a) * b
    # Берём дробную часть
    frac = x - math.floor(x)
    # Масштабируем и возвращаем целое
    return int(frac * modulo)

def trigger_trap(game_state):
    """
    Имитирует срабатывание ловушки.
    Если у игрока есть предметы — теряет один случайный.
    Если инвентарь пуст — возможна смерть.
    """
    print("\nЛовушка активирована! Пол стал дрожать...")
    inventory = game_state['player_inventory']
    steps = game_state['steps_taken']

    if inventory:
        # Выбираем случайный индекс предмета
        idx = pseudo_random(steps, len(inventory))
        lost_item = inventory.pop(idx)
        print(f"Вы потеряли: {lost_item}")
    else:
        # Инвентарь пуст — проверяем на смерть
        luck = pseudo_random(steps, 10)
        if luck < 3:
            print("Вы не удержались и провалились в яму... Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вам чудом удалось уцелеть!")

def random_event(game_state):
    """
    Генерирует случайное событие после перемещения.
    Вызывается только если событие происходит (вероятность 1/10).
    """
    steps = game_state['steps_taken']
    # Определяем, произойдёт ли событие (seed = steps, modulo = 10)
    if pseudo_random(steps, 10) != 0:
        return  # событие не происходит

    # Выбираем тип события (0, 1, 2)
    event_type = pseudo_random(steps + 1, 3)  # смещаем seed для разнообразия

    if event_type == 0:
        # Находка
        print("\nВы заметили что-то блестящее на полу. Это монетка!")
        current_room = game_state['current_room']
        ROOMS[current_room]['items'].append('coin')

    elif event_type == 1:
        # Испуг
        print("\nВы слышите шорох за спиной...")
        if 'sword' in game_state['player_inventory']:
            print("Вы хватаетесь за меч, и шорох затихает. Существо отпугнуто.")

    else:  # event_type == 2
        # Проверка на ловушку в trap_room
        if game_state['current_room'] == 'trap_room' and 'torch' not in game_state['player_inventory']:
            print("\nВы чувствуете, как пол под ногами начинает проваливаться!")
            trigger_trap(game_state)
        else:
            # Если условия не совпали, ничего не происходит (можно просто проигнорировать)
            pass

def show_help():
    print("\nДоступные команды:")
    print(" go <direction> - перейти в направлении (north/south/east/west)")
    print(" look - осмотреть текущую комнату")
    print(" take <item> - поднять предмет")
    print(" use <item> - использовать предмет из инвентаря")
    print(" inventory - показать инвентарь")
    print(" solve - попытаться решить загадку в комнате")
    print(" quit - выйти из игры")
    print(" help - показать это сообщение")