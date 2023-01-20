from collections import defaultdict
import sys

# Статья про автомат Левенштейна (habr): https://habr.com/ru/post/275937/
# Статья с википедии: https://en.wikipedia.org/wiki/Levenshtein_automaton


class State:
    def __init__(self, node=None, word_idx=0, final_word_idx=0, dist=0):
        self.node = node                        # Текущий узел (указатель на него).
        self.word_idx = word_idx                # Индекс проверяемого слова.
        self.final_word_idx = final_word_idx    # Индекс слова, по которому происходит проверка.
        self.distance = dist                    # Коррекционное расстояние
        self.symbol = ''                        # Предыдущий символ, для проверки транспозиции


class SpellChecker:
    def __init__(self):
        self.result = dict()        # Словарь, в котором: ключ - коррекционное расстояние,
                                    #                     значение - set() из слов (из дерева) с данным расстоянием).

        self.state_stack = list()   # Стек состояний автомата Левенштейна.

    # Добавление состояния, где метод коррекции - удаление символа.
    def add_deletion_state(self, stack_item):
        self.state_stack.append(State(node=stack_item.node, word_idx=stack_item.word_idx + 1,
                                      final_word_idx=stack_item.final_word_idx, dist=1))

    # Добавление состояния, где метод коррекции - вставка символа.
    def add_insertion_state(self, stack_item):
        self.state_stack.append(State(node=stack_item.node, word_idx=stack_item.word_idx,
                                      final_word_idx=stack_item.final_word_idx + 1, dist=1))

    # Добавление состояния, где метод коррекции - изменение символа.
    def add_modification_state(self, stack_item, distance):
        self.state_stack.append(State(node=stack_item.node, word_idx=stack_item.word_idx + 1,
                                      final_word_idx=stack_item.final_word_idx + 1, dist=distance))

    # Добавление состояния, где метод коррекции - транспозиция символов.
    def add_transposition_state(self, stack_item, symbol, distance):
        new_item = State(node=stack_item.node, word_idx=stack_item.word_idx + 1,
                         final_word_idx=stack_item.final_word_idx + 1, dist=distance)
        new_item.symbol = symbol
        self.state_stack.append(new_item)

    # Метод добавление детей текущего состояния.
    def add_new_states(self, stack_item):
        for child in stack_item.node.children.values():
            new_state = State(node=child, word_idx=stack_item.word_idx,
                              final_word_idx=0, dist=stack_item.distance)
            new_state.symbol = stack_item.symbol
            self.state_stack.append(new_state)

    # Метод проверки правописания.
    # Сложность данного метода определяется длиной искомого слова n
    # и мощностью алфавита k=const, таким образом в худшем случаем
    # мы имеем сложность O(k * n)
    def check_spell(self, trie, word):
        # Заносим всех детей корня дерева в качестве состояний автомата.
        for child in trie.root.children.values():
            self.state_stack.append(State(node=child))

        while len(self.state_stack) != 0:
            # Изымаем состояние из стека состояний.
            stack_item = self.state_stack.pop(len(self.state_stack) - 1)

            # Полное совпадение префиксов -> слово найдено -> надо добавить его в словарь.
            if stack_item.node.is_word:
                # Нашли искомое слово.
                if stack_item.word_idx == len(word) and stack_item.final_word_idx == len(
                        stack_item.node.node_key) and stack_item.distance == 0:
                    if self.result.get("0") is None:
                        self.result["0"] = stack_item.node.final_word

                # Где-то был совершен переход в новое состояние (вставка, удаление, транспозиция).
                elif stack_item.word_idx == len(word) and stack_item.final_word_idx == len(
                        stack_item.node.node_key) and stack_item.distance == 1:
                    if self.result.get("1") is None:
                        self.result["1"] = set()
                    self.result["1"].add(stack_item.node.final_word)

                # Искомое слово включает префикс который мы обрабатываем.
                elif stack_item.word_idx == len(word) - 1 and stack_item.final_word_idx == len(
                        stack_item.node.node_key) and stack_item.distance == 0:
                    if self.result.get("1") is None:
                        self.result["1"] = set()
                    self.result["1"].add(stack_item.node.final_word)

                # Префикс включает искомое слово.
                elif stack_item.word_idx == len(word) and stack_item.final_word_idx == len(
                        stack_item.node.node_key) - 1 and stack_item.distance == 0:
                    if self.result.get("1") is None:
                        self.result["1"] = set()
                    self.result["1"].add(stack_item.node.final_word)

            # Добавляем детей текущего состояния.
            if stack_item.final_word_idx == len(stack_item.node.node_key):
                self.add_new_states(stack_item)
                continue

            # Дошли до конца исходного слова.
            if stack_item.word_idx == len(word):
                continue

            # Проверяем транспозицию.
            if stack_item.symbol != '':
                # Если транспозиция применялась:
                if word[stack_item.word_idx - 1] == stack_item.node.node_key[stack_item.final_word_idx] and \
                        word[stack_item.word_idx] == stack_item.symbol:
                    self.add_transposition_state(stack_item, '', stack_item.distance)

            # Не было транспозиции -> символы совпали.
            elif stack_item.node.node_key[stack_item.final_word_idx] == word[stack_item.word_idx]:
                self.add_modification_state(stack_item, stack_item.distance)

            # Если символы не совпали, добавляем новые состояния.
            else:
                if stack_item.distance == 0:
                    self.add_deletion_state(stack_item)
                    self.add_insertion_state(stack_item)
                    self.add_modification_state(stack_item, 1)
                    self.add_transposition_state(stack_item, stack_item.node.node_key[stack_item.final_word_idx], 1)

        return self.result


class TrieNode:
    def __init__(self, is_word=False, keys=None, final_word='', node_key=''):
        self.final_word = final_word                             # Итоговое слово.
        self.is_word = is_word                                   # Индикатор конца слова.
        self.children = keys if keys else defaultdict(TrieNode)  # Указатели на детей узла.
        self.node_key = node_key                                 # Ключ узла.


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        self.inner_insert(self.root, word, word)

    @staticmethod
    # Метод проверки совпадения слова и ключа.
    # На выходе получаем: префикс ключа, суффикс ключа и слово без префикса.
    # Сложность функции: O(min(n, k)), где n - длина слова, k - длина ключа.
    def match(key, word):
        idx = 0

        for k, w in zip(key, word):
            if k != w:
                break
            idx += 1

        return key[:idx], key[idx:], word[idx:]

    @staticmethod
    # Функция вставки в дерево.
    # Сложность функции вставки определяется длиной префикса k;
    # При этом на каждом узле, то есть каждая буква префикса -
    # это узел, необходимо делать проверку, которая, поскольку
    # я использую defaultdict(=dict), занимает O(1), таких проверок будет k.
    # Учитывая мощность алфавита (n), получим сложность вставки O(n * k).
    def inner_insert(node=None, word='', final_word=''):
        for key, child in node.children.items():
            prefix, suffix, word_part = Trie.match(key, word)

            # Полное совпадение ключа.
            if not suffix:
                if not word_part:
                    # Совпало само слово.
                    child.is_word = True
                    return True
                else:
                    # Совпала часть слова (слово без префикса)
                    return Trie.inner_insert(node=child, word=word_part, final_word=final_word)

            # Случай частичного совпадения ключа -> нужно разбить текущий узел.
            if prefix:
                child.node_key = suffix
                new_node = TrieNode(is_word=not word_part, keys={suffix: child}, node_key=prefix, final_word=final_word)
                node.children[prefix] = new_node
                del node.children[key]
                return Trie.inner_insert(node=new_node, word=word_part, final_word=final_word)

        node.children[word] = TrieNode(is_word=True, node_key=word, final_word=final_word)


if __name__ == '__main__':
    trie = Trie()
    dict_size = int(input())

    for i in range(dict_size):
        trie.insert(input().lower())

    for line in sys.stdin:
        if line == "\n":
            continue

        line = line[:-1]

        checker = SpellChecker()
        result = checker.check_spell(trie, line.lower())

        if result.get("0"):
            print(f"{line} - ok")
        elif result.get("1"):
            words = result.get("1")
            print(f"{line} -> {', '.join(sorted(words))}")
        else:
            print(f"{line} -?")