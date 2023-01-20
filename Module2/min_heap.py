import sys
import re


class MinHeapException(Exception):
    pass


class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value


class MinHeap:
    def __init__(self):
        self.nodes_list = list()
        self.heap_indices = dict()

    @staticmethod
    def sift_up(indices, arr, idx):
        if idx != 0:
            parent_idx = (idx - 1) // 2
            if arr[idx].key < arr[parent_idx].key:
                indices[arr[idx].key] = parent_idx
                indices[arr[parent_idx].key] = idx

                arr[idx], arr[parent_idx] = arr[parent_idx], arr[idx]
                MinHeap.sift_up(indices, arr, parent_idx)

    @staticmethod
    def sift_down(indices, arr, idx):
        min_idx = idx
        left_idx = 2 * idx + 1
        right_idx = 2 * idx + 2

        if left_idx < len(arr) and arr[left_idx].key < arr[min_idx].key:
            min_idx = left_idx

        if right_idx < len(arr) and arr[right_idx].key < arr[min_idx].key:
            min_idx = right_idx

        if min_idx != idx:
            indices[arr[idx].key] = min_idx
            indices[arr[min_idx].key] = idx

            arr[idx], arr[min_idx] = arr[min_idx], arr[idx]
            MinHeap.sift_down(indices, arr, min_idx)

    def print(self, output):
        if self.heap_size() == 0:
            output.write('_\n')
            return

        output.write(f'[{self.nodes_list[0].key} {self.nodes_list[0].value}]\n')

        if self.heap_size() == 1:
            return

        layer = 1
        curr_idx = 1

        while True:
            width = 2 ** layer

            for node in range(width):
                if node + curr_idx > self.heap_size() - 1:
                    output.write('_ ' * (width - node - 1))
                    output.write('_')
                    break

                parent = ((curr_idx + node) - 1) // 2
                output.write(f'[{self.nodes_list[curr_idx + node].key} '
                             f'{self.nodes_list[curr_idx + node].value} '
                             f'{self.nodes_list[parent].key}]')

                if node != width - 1:
                    output.write(' ')

            output.write('\n')
            curr_idx += width
            layer += 1

            if curr_idx > self.heap_size() - 1:
                break

    def heap_size(self):
        return len(self.nodes_list)

    def add_node(self, key=None, value=None):
        if key is None or value is None or key in self.heap_indices:
            raise MinHeapException('error')

        if not self.nodes_list:
            self.nodes_list.append(Node(key, value))
            self.heap_indices[key] = 0
        else:
            self.nodes_list.append(Node(key, value))
            self.heap_indices[key] = self.heap_size() - 1
            self.sift_up(self.heap_indices, self.nodes_list, self.heap_size() - 1)

    def set_node(self, key=None, value=None):
        if key is None or value is None or key not in self.heap_indices:
            raise MinHeapException('error')

        idx = self.heap_indices[key]
        self.nodes_list[idx].value = value

    def del_node(self, key=None):
        if key is None or key not in self.heap_indices:
            raise MinHeapException('error')

        size = self.heap_size()
        idx = self.heap_indices[key]

        if size > 1 and idx < size - 1:
            del self.heap_indices[key]
            self.heap_indices[self.nodes_list[-1].key] = idx
            self.nodes_list[idx] = self.nodes_list[-1]
            self.nodes_list.pop()

            parent_idx = (idx - 1) // 2

            if not idx or self.nodes_list[idx].key > self.nodes_list[parent_idx].key:
                MinHeap.sift_down(self.heap_indices, self.nodes_list, idx)
            else:
                MinHeap.sift_up(self.heap_indices, self.nodes_list, idx)
        else:
            del self.heap_indices[key]
            self.nodes_list.pop()

    def extract_node(self):
        if not self.nodes_list:
            raise Exception('error')

        node_to_extract = self.nodes_list[0]

        self.heap_indices.pop(self.nodes_list[0].key)
        self.nodes_list[0] = self.nodes_list[-1]
        self.nodes_list.pop()

        if self.heap_size() == 0:
            return node_to_extract

        self.heap_indices[self.nodes_list[0].key] = 0
        self.sift_down(self.heap_indices, self.nodes_list, 0)

        return node_to_extract

    def search_node(self, key):
        if key is None:
            raise MinHeapException('error')

        if key not in self.heap_indices:
            return None

        return self.heap_indices[key]

    def min(self):
        if not self.nodes_list:
            raise MinHeapException('error')

        return self.nodes_list[0]

    def max(self):
        if not self.nodes_list:
            raise MinHeapException('error')

        max_node = self.nodes_list[0]
        nodes_count = self.heap_size()

        for curr_idx in range(nodes_count // 2, nodes_count):
            if self.nodes_list[curr_idx].key > max_node.key:
                max_node = self.nodes_list[curr_idx]

        return max_node


if __name__ == '__main__':
    min_heap = MinHeap()
    output = sys.stdout

    for line in sys.stdin:
        if line == '\n':
            continue
        try:
            line = line[:-1]
            cmd = line.split(' ')

            if re.match(re.compile(r'(add -?\d+ \S*$)'), line):
                min_heap.add_node(int(cmd[1]), cmd[2])

            elif re.match(re.compile(r'(set -?\d+ \S*$)'), line):
                min_heap.set_node(int(cmd[1]), cmd[2])

            elif re.match(re.compile(r'(delete -?\d+$)'), line):
                min_heap.del_node(int(cmd[1]))

            elif re.match(re.compile(r'(search -?\d+$)'), line):
                idx = min_heap.search_node(int(cmd[1]))
                if idx is not None:
                    print(f'1 {idx} {min_heap.nodes_list[idx].value}')
                else:
                    print('0')

            elif re.match(re.compile(r'(extract)$'), line):
                extracted_node = min_heap.extract_node()
                print(f'{extracted_node.key} {extracted_node.value}')

            elif re.match(re.compile(r'(min)$'), line):
                min_node = min_heap.min()
                print(f'{min_node.key} {min_heap.heap_indices[min_node.key]} {min_node.value}')

            elif re.match(re.compile(r'(max)$'), line):
                max_node = min_heap.max()
                print(f'{max_node.key} {min_heap.heap_indices[max_node.key]} {max_node.value}')

            elif re.match(re.compile(r'(print)$'), line):
                min_heap.print(output)

            else:
                print('error')

        except MinHeapException as mh_error:
            print(mh_error)