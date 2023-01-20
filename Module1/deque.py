import sys
import re


class DequeException(Exception):
    pass


class Deque:
    def __init__(self):
        self.deque = None
        self.size = 0
        self.capacity = 0
        self.head = 0
        self.tail = 0

    def push_back(self, element):
        if self.deque is None:
            raise DequeException('error')
        if self.size == self.capacity:
            raise DequeException('overflow')

        self.deque[self.tail] = element
        self.size += 1
        self.tail += 1

        if self.tail == self.capacity:
            self.tail = 0

    def pop_back(self):
        if self.deque is None:
            raise DequeException('error')
        if self.size == 0:
            raise DequeException('underflow')
        if self.tail == 0:
            self.tail = self.capacity

        self.tail -= 1
        self.size -= 1
        element = self.deque[self.tail]

        return element

    def push_front(self, element):
        if self.deque is None:
            raise DequeException('error')
        if self.size == self.capacity:
            raise DequeException('overflow')
        if self.head == 0:
            self.head = self.capacity

        self.head -= 1
        self.size += 1

        self.deque[self.head] = element

    def pop_front(self):
        if self.deque is None:
            raise DequeException('error')
        if self.size == 0:
            raise DequeException('underflow')

        element = self.deque[self.head]

        self.head += 1
        self.size -= 1

        if self.head == self.capacity:
            self.head = 0

        return element

    def print(self):
        if self.deque is None:
            raise DequeException('error')
        if self.size == 0:
            print('empty')
            return

        element_pos = self.head

        for i in range(self.size):
            print(self.deque[element_pos], end=' ') if i != (self.size - 1) else print(self.deque[element_pos])
            element_pos += 1
            if element_pos == self.capacity:
                element_pos = 0

    def set_size(self, n):
        if self.deque is not None:
            raise DequeException('error')

        self.deque = [None] * n
        self.capacity = n


if __name__ == '__main__':
    deque = Deque()

    for line in sys.stdin:
        line = line.replace('\n', '')
        cmd = line.split()

        try:
            if re.match(re.compile('(pushb|pushf) ([\\S]+)$'), line):
                element = cmd[1]
                if cmd[0] == 'pushb':
                    deque.push_back(element)
                elif cmd[0] == 'pushf':
                    deque.push_front(element)
            elif re.match(re.compile('(popb|popf)$'), line):
                if cmd[0] == 'popb':
                    print(deque.pop_back())
                elif cmd[0] == 'popf':
                    print(deque.pop_front())
            elif re.match(re.compile('set_size ([\\d]+)$'), line):
                element = cmd[1]
                deque.set_size(int(element))
            elif re.match(re.compile('(print)$'), line):
                deque.print()
            elif line != "":
                print('error')

        except DequeException as DE:
            print(DE)