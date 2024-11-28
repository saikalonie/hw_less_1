
def binary_search(arr, target):
    """
    Реализация алгоритма бинарного поиска.
    Сложность: O(log n)

    :param arr: Отсортированный список элементов
    :param target: Элемент, который нужно найти
    :return: Индекс элемента или -1, если элемент не найден
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


if __name__ == "__main__":
    data = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    print("Массив:", data)

    target = 7
    result = binary_search(data, target)
    if result != -1:
        print(f"Элемент {target} найден на индексе {result}.")
    else:
        print(f"Элемент {target} не найден.")
