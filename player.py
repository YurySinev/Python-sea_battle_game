
class Player:  # класс Игрок:
    def __init__(self, board, enemy):  # аргументы - две доски
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):  # класс игрока ИИ:
    def ask(self):  # ход ПК
        d = Dot(randint(0, 5), randint(0, 5))  # получает два случайных числа между 0 и 5
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")  # показывает ход с коррекцией цифр
        return d  # передает программе свой ход


class User(Player):  # класс игрока-человека:
    def ask(self):  # ход человека
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:  # проверка, что введено 2 значения координат
                print("Введите 2 координаты...")
                continue

            x, y = cords  # передача этих значений в переменные x и y

            if not (x.isdigit()) or not (y.isdigit()):  # проверка, что
                print("Введите числа...")  # x и y - числа
                continue

            x, y = int(x), int(y)  # приведение к типу integer

            return Dot(x - 1, y - 1)  # кортеж со скорректированными координатами

