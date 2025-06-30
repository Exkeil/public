import random



# Функция bubble_sort принимает список целых чисел
# data и сортирует его в порядке убывания элементов с
# помощью пузырьковой сортировки. Кроме того, функция
# должна посчитать количество операций (итераций цикла),
# которые выполняет алгоритм, и вернуть это число вызывающей
# стороне.
def bubble_sort(data):
    n=len(data)
    iteration = 0
    for i in range(n):
        for j in range(0, n - i - 1):
            iteration += 1
            if data[j] < data[j + 1]:def is_balanced(line):
    stack = []
    bracket_pairs = {')': '(', ']': '[', '}': '{'}
    for char in line:
        if char in bracket_pairs.values():
            stack.append(char)
        elif char in bracket_pairs.keys():
            if not stack or stack[-1] != bracket_pairs[char]:
                return False
            stack.pop()
    return not stack


def case_is_balanced():
    cases = {
        '()': True,
        '()[]{}': True,
        '(]': False,
        '({})': True,
    }
    for i, case in enumerate(cases.keys()):
        if is_balanced(case) == cases[case]:
            print(f'{i}: OK')
        else:
            print(f'{i}: Not OK')


def main():
    case_is_balanced()


if __name__ == '__main__':
    main()
                data[j], data[j + 1] = data[j + 1], data[j]
    return iteration



def test_sorted():
    data = [random.randint(0, 1000) for i in range(100)]
    data_to_sort = data.copy()
    bubble_sort(data_to_sort)
    if data_to_sort == sorted(data, reverse=True):
        print('OK')
    else:
        print('NOT OK')


def make_observations():
    size = 10
    results = []
    for i in range(100):
        data = [random.randint(0, 1000) for i in range(size)]
        iterations = bubble_sort(data)
        results.append((size, iterations))
        size += 10
    return results

def main():
    test_sorted()
    with open('bubble.csv', 'w') as file:
        file.write(f'size, iterations\n')
        for row in make_observations():
            file.write(f'{row[0]}, {row[1]}\n')
    print('Done!')


if __name__ == '__main__':
    main()



