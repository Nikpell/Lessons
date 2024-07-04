from collections import Counter


class NewList:
    def __init__(self, lst=None):
        self._lst = lst[:] if lst and type(lst) == list else []

    def __sub__(self, other):
        if not isinstance(other, (list, NewList)):
            raise ArithmeticError("Правый операнд должен быть типом list")
        else:
            if isinstance(other, list):
                lst_sub = other
            else:
                lst_sub = other.get_list()
            return NewList(self.__diff_list__(self._lst, lst_sub))
    def __rsub__(self, other):
        if isinstance(other, list):
            lst1 = other
        else:
            lst1 = other.get_list()
        return NewList(self.__diff_list__(lst1, self._lst))
    @staticmethod
    def __diff_list__(lst1, lst2):
        count = Counter(list(map(lambda x: str(x), lst2)))
        sub_lst = []
        for item in lst1:
            if count[str(item)] == 0:
                sub_lst.append(item)
            else:
                count[str(item)] -= 1
        return sub_lst

    def get_list(self):
        return self._lst


lst1 = NewList([1, 2, -4, 6, 10, 11, 15, False, True])
lst2 = NewList([0, 1, 2, 3, True])
res_1 = lst1 - lst2  # NewList: [-4, 6, 10, 11, 15, False]
lst1 -= lst2  # NewList: [-4, 6, 10, 11, 15, False]
res_2 = lst2 - [0, True]  # NewList: [1, 2, 3]
res_3 = [1, 2, 3, 4.5] - res_2  # NewList: [4.5]
print(res_3.get_list())
a = NewList([2, 3])
res_4 = [1, 2, 2, 3] - a # NewList: [1, 2]
print(res_4.get_list())
