from dots import Dot
from ship import Ship


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

