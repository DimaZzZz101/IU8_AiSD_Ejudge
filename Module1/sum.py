import sys


def calc_sum() -> int:
    summ = 0
    next_num = 0
    sign = 1
    for symbol in sys.stdin.read():
        if symbol == '-':
            summ += sign * next_num
            sign = -1
            next_num = 0
        elif symbol.isdigit():
            next_num = next_num * 10 + ord(symbol) - 48
        else:
            summ += sign * next_num
            next_num = 0
            sign = 1

    return summ


if __name__ == '__main__':
    print(calc_sum())