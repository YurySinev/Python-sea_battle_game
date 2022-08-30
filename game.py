from random import randint
from board import Board
from dots import Dot
from game_exceptions import *
from player import *
from ship import Ship

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
    g = Game()
    g.start()
