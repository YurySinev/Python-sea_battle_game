
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

