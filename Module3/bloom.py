import re
import sys
import math

MERSENNE_NUMBER = 2 ** 31 - 1


class BitArray:
    def __init__(self, size):
        self.array = bytearray(math.ceil(size / 8))

    def set_value(self, bit):
        self.array[bit // 8] |= 2 ** (bit % 8)

    def get_value(self, bit):
        return self.array[bit // 8] & (2 ** (bit % 8))


class BloomFilter:
    def __init__(self, n, p):
        if round(-math.log2(p)) < 1:
            raise ValueError

        self.m = round(-n * math.log2(p) / math.log(2))
        self.k = round(-math.log2(p))

        self.primes = self.list_of_primes(self.k)
        self.bit_array = BitArray(self.m)

    @staticmethod
    def list_of_primes(size):
        primes = list()
        count = 2
        while len(primes) < size:
            for i in range(2, int(math.sqrt(count)) + 1):
                if count % i == 0:
                    break
            else:
                primes.append(count)
            count += 1
        return primes

    def add(self, key):
        for i in range(self.k):
            self.bit_array.set_value(self.compute_hash(i, key))

    def search(self, key):
        for i in range(self.k):
            if not self.bit_array.get_value(self.compute_hash(i, key)):
                return False
        return True

    def compute_hash(self, i, key):
        return (((i + 1) * key + self.primes[i]) % MERSENNE_NUMBER) % self.m

    def get_stats(self):
        return self.m, self.k

    def print(self, out=sys.stdout):
        for i in range(0, self.m):
            if self.bit_array.get_value(i):
                out.write('1')
            else:
                out.write('0')
        out.write('\n')


if __name__ == '__main__':
    bloom_filter = None

    while bloom_filter is None:
        for line in sys.stdin:
            line = line.rstrip('\n')
            if line == '':
                continue

            if not re.match(re.compile(r'(^set \d+ (1|0|(0\.\d+))$)'), line):
                print('error')
            else:
                set_params = line.split()
                n = int(set_params[1])
                p = float(set_params[2])

                if n == 0 or p >= 1 or p <= 0:
                    print('error')
                    continue
                try:
                    bloom_filter = BloomFilter(int(n), float(p))
                except ValueError:
                    print('error')
                    continue

                stats = bloom_filter.get_stats()
                print(f'{stats[0]} {stats[1]}')
                break
        else:
            sys.exit()

    for line in sys.stdin:
        line = line.rstrip('\n')
        if line == '':
            continue

        if re.match(re.compile(r'(^add \d+$)'), line):
            bloom_filter.add(int(line.split()[1]))

        elif re.match(re.compile(r'(^search \d+$)'), line):
            if bloom_filter.search(int(line.split()[1])):
                print(1)
            else:
                print(0)

        elif re.match(re.compile(r'(^print$)'), line):
            bloom_filter.print()

        else:
            print('error')