# main.py

from gardarika.character.character import Character
from gardarika.lore.world import get_world_description

def main():
    """Главная функция для демонстрации."""

    print("Добро пожаловать в мир Гардарики!")
    print("="*30)
    print(get_world_description())
    print("="*30)

    try:
        # Создаем персонажа
        player_name = "Святозар"
        player_class = "воин"
        player_faction = "kiev"

        player = Character(player_name, player_class, player_faction)

        print("Создан новый персонаж:")
        print(player)

    except ValueError as e:
        print(f"Ошибка при создании персонажа: {e}")

if __name__ == "__main__":
    main()
