class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):  # для проверки точек на равенство
        return self.x == other.x and self.y == other.y

    def __repr__(self): # возвращает кортеж из координат
        return f"Dot({self.x}, {self.y})"


if __name__ == "__main__":
    a = Dot(1, 1)
    b = Dot(1, 2)
    c = Dot(1, 1)
    print(a == c)
    print(a, b, c)
    aa = [Dot(2,5),Dot(3,4),Dot(6,7),Dot(8,5),Dot(6,7),Dot(2,3),Dot(1,2),Dot(1,2),Dot(1,2),Dot(1,1)]
    print(a in aa)      # True
    print(aa.count(a)) # 1