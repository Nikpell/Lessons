class MaxPooling:
    def __init__(self, step=(2, 2), size=(2, 2)):
        self.step = step
        self.size = size

    def mp(self, matrix):
        for i in range(len(matrix)):
            if len(matrix) != len(matrix[i]):
                raise ValueError("Неверный формат для первого параметра matrix.")
            for j in range(len(matrix[i])):
                if type(matrix[i][j]) not in (int, float):
                    raise ValueError("Неверный формат для первого параметра matrix.")
        new_matrix_size = 0
        remainer = len(matrix)
        while remainer - self.size[0] >= 0:
            remainer -= self.step[0]
            new_matrix_size += 1
        new_matrix = [[0] * new_matrix_size for i in range(new_matrix_size)]
        for i in range(len(new_matrix)):
            for j in range(len(new_matrix[i])):
                new_matrix[i][j] = max([max(matrix[k][j * self.step[0]:j * self.step[0] + self.size[0]])
                                        for k in range(i * self.step[0], i * self.step[0] + self.size[0])])
        return new_matrix

    def __call__(self, matrix, *args, **kwargs):
        return self.mp(matrix)


mp = MaxPooling(step=(2, 2), size=(2, 2))
m1 = [[1, 10, 10], [5, 10, 0], [0, 1, 2]]
m2 = [[1, 10, 10, 12], [5, 10, 0, -5], [0, 1, 2, 300], [40, -100, 0, 54.5]]
res1 = mp(m1)
res2 = mp(m2)

assert res1 == [[10]], "неверный результат операции MaxPooling"
assert res2 == [[10, 12], [40, 300]], "неверный результат операции MaxPooling"

mp = MaxPooling(step=(3, 3), size=(2, 2))
m3 = [[1, 12, 14, 12], [5, 10, 0, -5], [0, 1, 2, 300], [40, -100, 0, 54.5]]
res3 = mp(m3)
assert res3 == [[12]], "неверный результат операции при MaxPooling(step=(3, 3), size=(2,2))"

try:
    res = mp([[1, 2], [3, 4, 5]])
except ValueError:
    assert True
else:
    assert False, "некорректо отработала проверка (или она отсутствует) на не прямоугольную матрицу"

try:
    res = mp([[1, 2], [3, '4']])
except ValueError:
    assert True
else:
    assert False, "некорректо отработала проверка (или она отсутствует) на не числовые значения в матрице"

mp = MaxPooling(step=(1, 1), size=(5, 5))
res = mp([[5, 0, 88, 2, 7, 65],
          [1, 33, 7, 45, 0, 1],
          [54, 8, 2, 38, 22, 7],
          [73, 23, 6, 1, 15, 0],
          [4, 12, 9, 1, 76, 6],
          [0, 15, 10, 8, 11, 78]])  # [[88, 88], [76, 78]]
print(res)

# assert res == [[88, 88], [76, 78]], "неверный результат операции MaxPooling(step=(1, 1), size=(5, 5))"


