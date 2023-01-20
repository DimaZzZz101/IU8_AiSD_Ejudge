import math
import sys


class PItem:
    def __init__(self, p_weight, p_cost, nums):
        self.p_weight = p_weight
        self.p_cost = p_cost
        self.nums = nums


class Item:
    def __init__(self, weight, cost):
        self.weight = weight
        self.cost = cost


class Knapsack:
    def __init__(self, precision, max_capacity, items):
        self.precision = precision
        self.max_capacity = max_capacity
        self.orig_costs = [item.cost for item in items]
        self.items_count = len(items)

        self.costs = [item.cost for item in items]
        self.weights = [item.weight for item in items]

        self.max_cost = max(self.costs)

    def compute_sum(self):
        costs_sum = 0
        for cost in self.costs:
            costs_sum += cost
        return costs_sum

    def make_precision_items(self):
        coefficient = 1
        if self.precision != 0:
            coefficient = self.items_count / self.precision / self.max_cost
        if coefficient < 1:
            for i in range(self.items_count):
                self.costs[i] = math.floor(coefficient * self.costs[i])

        p_items = [PItem(0, 0, set())]
        for _ in range(self.compute_sum() + 1):
            p_items.append(PItem(self.max_capacity + 1, 0, set()))

        return p_items

    def solve_problem(self):
        p_items = self.make_precision_items()

        for i in range(self.items_count):
            j = self.compute_sum()
            while j >= self.costs[i]:
                pos = j - self.costs[i]
                if p_items[pos].p_weight + self.weights[i] < p_items[j].p_weight:
                    p_items[j].nums = p_items[pos].nums.copy()
                    p_items[j].nums.add(i)

                    p_items[j].p_weight = p_items[pos].p_weight + self.weights[i]
                    p_items[j].p_cost = p_items[pos].p_cost + self.orig_costs[i]
                j -= 1

        idx = 0
        for i in range(len(p_items) - 1, -1, -1):
            if p_items[i].p_weight <= self.max_capacity:
                idx = i
                break

        print(p_items[idx].p_weight, p_items[idx].p_cost)
        for num in p_items[idx].nums:
            print(num + 1)


if __name__ == '__main__':
    precision = float(input())
    capacity = int(input())
    items = list()

    for line in sys.stdin:
        if line == '\n':
            continue
        line = line[:-1].split()
        items.append(Item(int(line[0]), int(line[1])))

    knapsack = Knapsack(precision, capacity, items)
    knapsack.solve_problem()