import sys


class BlockSystem:
    def __init__(self, attempts_count, period, block_time, max_block_time, curr_time):
        self.attempts_count = attempts_count
        self.period = period
        self.block_time = block_time
        self.max_block_time = max_block_time
        self.curr_time = curr_time

        self.next_attempt = self.last_attempt = -1

        self.start_time = curr_time - 2 * max_block_time
        self.end_time = 0

    def block_user(self, attempts):
        self.end_time = self.block_time + attempts[self.next_attempt]
        self.block_time *= 2
        if self.block_time > self.max_block_time:
            self.block_time = self.max_block_time
        self.last_attempt = self.next_attempt = -1


if __name__ == '__main__':
    [attempts_count, period, block_time, max_block_time, curr_time] = [int(arg) for arg in input().split()]
    attempts = [int(line[:-1]) for line in sys.stdin if line != '\n']
    attempts.sort()

    BS = BlockSystem(attempts_count, period, block_time, max_block_time, curr_time)

    for attempt in attempts:
        if BS.start_time > attempt:
            continue
        elif BS.next_attempt == BS.last_attempt == -1:
            BS.next_attempt = BS.last_attempt = attempts.index(attempt)
            if BS.attempts_count == 1:
                BS.block_user(attempts)
            continue

        if attempt - attempts[BS.last_attempt] > BS.period:
            BS.next_attempt += 1
            BS.last_attempt += 1
            continue
        else:
            BS.next_attempt += 1

        if BS.next_attempt - BS.last_attempt + 1 == BS.attempts_count:
            BS.block_user(attempts)

    print(BS.end_time) if BS.curr_time <= BS.end_time else print('ok')