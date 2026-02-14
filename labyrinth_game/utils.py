from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import get_input

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