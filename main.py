from random import randint


class Dot:  # Объекты класса Точка будут возвращать кортежи с координатами вида Dot(x, y)
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):  # проверка точек на равенство
        return self.x == other.x and self.y == other.y

    def __repr__(self):  # возвращает кортеж из координат
        return f"Dot({self.x}, {self.y})"


# классы исключений:
class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы стреляете за пределы поля!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Уже стреляли по этой клетке!"


class BoardWrongShipException(BoardException):
    pass


class Ship:  # класс Корабль:
    def __init__(self, bow, l, o):
        self.bow = bow  # координаты носа корабля: кортеж типа Dot(x,y)
        self.l = l  # длина
        self.o = o  # направление, boolean: 0 - горизонтально, 1 - вертик (или наоборот, неважно)
        self.lives = l  # количество жизней, совпадает с длиной

    @property
    def dots(self):
        ship_dots = []  # список точек-координат корабля
        for i in range(self.l):  # перебор значений в зависим. от длины корабля
            cur_x = self.bow.x  # устанавливается точка x
            cur_y = self.bow.y  # y
            if self.o == 0:  # направление, по которому будут приращиваться значения:
                cur_x += i  # либо по горизонтали
            elif self.o == 1:
                cur_y += i  # либо по вертикали
            ship_dots.append(Dot(cur_x, cur_y))  # добавляем пару точек в список

        return ship_dots  # передаем список кому нужно

    def shooten(self, shot):  # проверка, попал ли выстрел по координатам корабля
        return shot in self.dots  # ответ: True - False


class Board:  # класс для игрового поля:
    def __init__(self, hid=False, size=6):
        self.hid = hid  # видимость/скрытость поля
        self.size = size  # размер

        self.count = 0  # счетчик пораженных кораблей
        # матрица игр.поля size*size (6*6), заполненная нулями:
        self.field = [["0"] * size for _ in range(size)]

        self.busy = []  # занятые точки (либо корабль, либо куда стреляли)
        self.ships = []  # список кораблей на поле

    def __str__(self):  # возвращает многострочную переменную
        res = ''  # с "картинкой" ситуации на поле
        res += '  | 1 | 2 | 3 | 4 | 5 | 6 |'  # добавляем первую строку
        for i, row in enumerate(self.field):  # добавляем следующие строки
            # со скорректир.номерами, разделителями и инфо из строк матрицы field:
            res += f"\n{i + 1} | " + " | ".join(row) + " | "

        if self.hid:  # если параметр hid=True, то символы корабля будут заменены
            res = res.replace("■", "O")  # на нолики (на вражеской доске)

        return res  # готовая "картинка" с ситуацией

    def out(self, d):  # True - если точка вне пределов игр.поля
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):  # определить точки вокруг корабля
        near = [  # список точек со сдвигом, окружающих точку (0,0)
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:  # подсчет точек, куда нельзя будет ставить др.корабль
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                # если точка не выходит за границы поля и не занята:
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."  # помечаем ее на поле
                    self.busy.append(cur)  # и добавляем в список занятых

    def add_ship(self, ship):  # добавление корабля на поле
        for d in ship.dots:
            # если точка за полем или занята:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException  # выбрасывается исключение
        for d in ship.dots:  # если все ОК:
            self.field[d.x][d.y] = "■"  # точка помечается
            self.busy.append(d)  # и заносится в список занятых

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):  # выстрел
        if self.out(d):  # не выходит ли точка за границы поля?
            raise BoardOutException
        if d in self.busy:  # не использована ли уже эта точка?
            raise BoardUsedException
        self.busy.append(d)  # если ОК, добавить точку
        for ship in self.ships:  # проходимся по списку кораблей
            if ship.shooten(d):  # вычисляем точку попадания и последствия для корабля
                ship.lives -= 1  # уменьшаем количество "жизней"
                self.field[d.x][d.y] = "X"  # помечаем подбитую точку
                if ship.lives == 0:  # если количество жизней корабля 0
                    self.count += 1  # увеличиваем счетчик уничтоженных кораблей
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:  # если корабль ранен
                    print("Корабль подбит!")
                    return True
        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False

    def begin(self):  # обнуляем список busy. До начала игры он использовался
        self.busy = []  # для расстановки кораблей, а сейчас понадобится для
        # записи точек, куда производились выстрелы. Можно была завести еще один список,
        # но метод contour получился универсальным: и для расстановки, и для самой игры

    def defeat(self):
        return self.count == len(self.ships)


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


class Game:  # класс Игра:
    def __init__(self, size=6):  # конструктор игры
        self.size = size  # задаем размер поля
        pl = self.random_board()  # создаем доску для игрока
        pc = self.random_board()  # создаем доску для компьютера
        pc.hid = True  # скрываем корабли с доски для компьютера

        self.ai = AI(pc, pl)  # объект класса AI(свое поле, поле противника)
        self.us = User(pl, pc)  # объект класса User(свое поле, поле противника)

    def try_board(self):  # генерирование игрового поля
        lens = [3, 2, 2, 1, 1, 1, 1]  # список длин кораблей
        board = Board(size=self.size)  # создание игрового поля
        attempts = 0  # количество попыток
        for l in lens:  # создание кораблей и расстановка их по полю
            while True:
                attempts += 1
                if attempts > 2000:  # максимальное количество попыток
                    return None  # если не получится - сброс и сначала
                # создание корабля cо случайными координатами и ориентацией:
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)  # попытка добавить корабль на поле
                    break  # если все ОК, то бесконечый цикл закончится
                except BoardWrongShipException:  # если не получилось
                    pass

        board.begin()  # активизация созданного поля с кораблями
        return board  # передача объекта в игру

    def random_board(self):  # создание случайного поля с кораблями
        board = None  # иозначально поле отсутствует
        while board is None:  # бесконечные попытки создания поля
            board = self.try_board()
            return board  # пока не завершится успехом

    def greeting(self):  # приветствие перед началом игры
        print("--------------------------")
        print("    Классическая игра     ")
        print("       МОРСКОЙ БОЙ        ")
        print("--------------------------")
        print(" Формат ввода: x y Enter  ")
        print("  где  x - номер строки   ")
        print("       y - номер столбца  ")

    def loop(self):  # игровой цикл
        num = 0
        while True:
            print("-" * 20)
            print("Доска игрока: ")
            print(self.us.board)
            print("Доска компьютера: ")
            print(self.ai.board)
            print("-" * 20)

            if num % 2 == 0:
                print("-" * 20)
                print("Ваш ход!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()

            if repeat:  # при попадании можно повторить ход, для чего
                num -= 1  # num просто уменьшается на единицу
            # проверка, что количество пораженных кораблей равно количеству кораблей на доске:
            # if self.ai.count == len(self.ai.board.ships):
            if self.ai.board.defeat(): # другой вариант
                print("-" * 20)
                print("ВЫ ВЫИГРАЛИ!")
                break
            # либо проще - количество пораженных кораблей равно 7:
            # if self.us.count == 7:
            if self.us.board.defeat():
                print("-" * 20)
                print("ВЫИГРАЛ КОМПЬЮТЕР!")
                break

            num += 1
    def start(self):
        self.greeting()
        self.loop()


if __name__ == '__main__':
    # ship1 = Ship(Dot(3, 4), 3, 0)
    # print(ship1.dots)
    # shoot = ship1.shooten(Dot(5, 4))
    # print(shoot)
    # b = Board()
    # b.add_ship(Ship(Dot(1, 2), 4, 0))
    # b.add_ship(Ship(Dot(0, 0), 2, 0))
    # print(b)
    # print(b.busy)
    g = Game()
    # g.size = 6
    # # print(g.try_board())
    # print(g.random_board())
    g.start()
