
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


if __name__ == '__main__':
    ship1 = Ship((3, 5), 4, 1)
    print(ship1.bow)
    print(ship1.l)
    print(ship1.o)

