# labyrinth_game/player_actions.py

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
