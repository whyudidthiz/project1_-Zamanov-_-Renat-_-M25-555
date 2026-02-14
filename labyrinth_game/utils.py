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
