import re
import sys
from collections import deque

sys.setrecursionlimit(10000)


class SplayTreeException(Exception):
    pass


class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

        self.parent = None
        self.r_child = None
        self.l_child = None

    def has_right_child(self):
        return self.r_child is not None

    def has_left_child(self):
        return self.l_child is not None


class SplayTree:
    def __init__(self):
        self.root = None

    def print(self, out=sys.stdout):
        if self.root is None:
            out.write('_\n')
            return

        height = self.height(self.root)
        nodes_queue = deque()
        pos_queue = deque()

        out.write(f'[{self.root.key} {self.root.value}]\n')

        if self.root.l_child is not None:
            nodes_queue.append(self.root.l_child)
            pos_queue.append(0)

        if self.root.r_child is not None:
            nodes_queue.append(self.root.r_child)
            pos_queue.append(1)

        nums_of_nodes = len(pos_queue)

        if nums_of_nodes == 0:
            return

        curr = pos_queue.popleft()

        for layer in range(1, height):
            curr_pos = 0
            layer_width = 2 ** layer

            while nums_of_nodes != 0:
                if curr_pos == curr:
                    nums_of_nodes -= 1
                    node = nodes_queue.popleft()

                    if curr != layer_width - 1:
                        out.write(f'[{node.key} {node.value} {node.parent.key}] ')
                    else:
                        out.write(f'[{node.key} {node.value} {node.parent.key}]')

                    if node.l_child is not None:
                        nodes_queue.append(node.l_child)
                        pos_queue.append(2 * (curr + 1) - 2)

                    if node.r_child is not None:
                        nodes_queue.append(node.r_child)
                        pos_queue.append(2 * (curr + 1) - 1)

                    curr_pos = curr + 1

                    if len(pos_queue) != 0:
                        curr = pos_queue.popleft()

                elif curr - curr_pos != 0:
                    out.write('_ ' * (curr - curr_pos))
                    curr_pos = curr

                if nums_of_nodes == 0:
                    out.write('_ ' * (layer_width - curr_pos - 1))
                    if curr_pos != layer_width:
                        out.write('_')

            nums_of_nodes = len(pos_queue) + 1
            out.write('\n')

    def height(self, node):
        if node is None:
            return 0

        return 1 + max(self.height(node.l_child), self.height(node.r_child))

    def right_rotate(self, node=Node()):
        left_child = node.l_child
        node.l_child = left_child.r_child

        if left_child.has_right_child():
            left_child.r_child.parent = node

        left_child.parent = node.parent

        if node.parent is None:
            self.root = left_child
        elif node.parent.r_child == node:
            node.parent.r_child = left_child
        else:
            node.parent.l_child = left_child

        left_child.r_child = node
        node.parent = left_child

    def left_rotate(self, node=Node()):
        right_child = node.r_child
        node.r_child = right_child.l_child

        if right_child.has_left_child():
            right_child.l_child.parent = node

        right_child.parent = node.parent

        if node.parent is None:
            self.root = right_child
        elif node.parent.l_child == node:
            node.parent.l_child = right_child
        else:
            node.parent.r_child = right_child

        right_child.l_child = node
        node.parent = right_child

    def splay(self, node=Node()):
        if node is None:
            return

        while node.parent is not None:
            if node.parent != self.root:
                parent = node.parent
                gr_parent = node.parent.parent
                # zig-zig
                if node.parent.l_child == node and parent.parent.l_child == parent:
                    self.right_rotate(gr_parent)
                    self.right_rotate(parent)
                # zig-zag
                elif node.parent.l_child == node and parent.parent.r_child == parent:
                    self.right_rotate(parent)
                    self.left_rotate(gr_parent)
                # zag-zig
                elif node.parent.r_child == node and parent.parent.l_child == parent:
                    self.left_rotate(parent)
                    self.right_rotate(gr_parent)
                # zag-zag
                elif node.parent.r_child == node and parent.parent.r_child == parent:
                    self.left_rotate(gr_parent)
                    self.left_rotate(parent)
            else:
                # zig
                if node.parent.l_child == node:
                    self.right_rotate(node.parent)
                # zag
                else:
                    self.left_rotate(node.parent)

    def add(self, key=None, value=None):
        if key is None or value is None:
            raise SplayTreeException('error')

        parent_node = SplayTree.find(self.root, key)

        if parent_node is None:
            self.root = Node(key, value)
            return

        if parent_node.key == key:
            self.splay(parent_node)
            raise SplayTreeException('error')
        elif parent_node.key > key:
            node_to_add = parent_node.l_child = Node(key, value)
        else:
            node_to_add = parent_node.r_child = Node(key, value)

        node_to_add.parent = parent_node
        self.splay(node_to_add)

    def delete(self, key):
        if key is None:
            raise SplayTreeException('error')

        node_to_delete = SplayTree.find(self.root, key)
        self.splay(node_to_delete)

        if node_to_delete is None or node_to_delete.key != key:
            raise SplayTreeException('error')

        if node_to_delete.l_child is None and node_to_delete.r_child is None:
            self.root = None

        elif not node_to_delete.has_left_child():
            self.root = node_to_delete.r_child
            self.root.parent = None

        elif not node_to_delete.has_right_child():
            self.root = node_to_delete.l_child
            self.root.parent = None

        else:
            temp_node = node_to_delete.l_child
            while temp_node.has_right_child():
                temp_node = temp_node.r_child
            new_root = temp_node
            self.splay(new_root)
            new_root.r_child = node_to_delete.r_child

            if new_root.has_right_child():
                new_root.r_child.parent = new_root

    def search(self, key):
        if key is None:
            raise SplayTreeException('error')

        node_to_search = SplayTree.find(self.root, key)
        self.splay(node_to_search)

        if not node_to_search or node_to_search.key != key:
            return None

        return self.root.value

    def set(self, key, value):
        if key is None or value is None:
            raise SplayTreeException('error')

        node_to_set = SplayTree.find(self.root, key)
        self.splay(node_to_set)

        if node_to_set is None or node_to_set.key != key:
            raise SplayTreeException('error')

        self.root.value = value

    def maximum(self):
        if self.root is None:
            raise SplayTreeException('error')

        temp_node = self.root
        while temp_node.has_right_child():
            temp_node = temp_node.r_child
        max_node = temp_node
        self.splay(max_node)

        return max_node.key, max_node.value

    def minimum(self):
        if self.root is None:
            raise SplayTreeException('error')

        temp_node = self.root
        while temp_node.has_left_child():
            temp_node = temp_node.l_child
        min_node = temp_node
        self.splay(min_node)

        return min_node.key, min_node.value

    @staticmethod
    def find(root=Node(), key=None):
        if root is None:
            return None

        prev_node = None
        temp_node = root

        while temp_node is not None:
            prev_node = temp_node
            if key == temp_node.key:
                return temp_node
            elif key < temp_node.key:
                temp_node = temp_node.l_child
            else:
                temp_node = temp_node.r_child

        return prev_node


if __name__ == '__main__':
    splay_tree = SplayTree()

    for line in sys.stdin:
        if line == '\n':
            continue
        try:
            line = line[:-1]
            cmd = line.split(' ')

            if re.match(re.compile(r'(add -?\d+ \S*$)'), line):
                splay_tree.add(int(cmd[1]), cmd[2])

            elif re.match(re.compile(r'(set -?\d+ \S*$)'), line):
                splay_tree.set(int(cmd[1]), cmd[2])

            elif re.match(re.compile(r'(delete -?\d+$)'), line):
                splay_tree.delete(int(cmd[1]))

            elif re.match(re.compile(r'(search -?\d+$)'), line):
                value = splay_tree.search(int(cmd[1]))
                if value is not None:
                    print(f'1 {value}')
                else:
                    print('0')

            elif re.match(re.compile(r'(min)$'), line):
                key, value = splay_tree.minimum()
                print(f'{key} {value}')

            elif re.match(re.compile(r'(max)$'), line):
                key, value = splay_tree.maximum()
                print(f'{key} {value}')

            elif re.match(re.compile(r'(print)$'), line):
                splay_tree.print()
            else:
                print("error")
        except SplayTreeException as st_error:
            print(st_error)