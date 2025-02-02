import fileinput
from functools import lru_cache

txt = "".join(fileinput.input())
towels_s, patterns_s = txt.split("\n\n")

towels = towels_s.split(", ")
patterns = [line for line in patterns_s.splitlines()]

# trie node
class Node:
    def __init__(self):
        self.d = {}
        self.word = False

    def add(self, w):
        node = self
        for c in w:
            if c not in node.d:
                node.d[c] = Node()
            node = node.d[c]
        node.word = True

class Trie:
    def __init__(self, words):
        self.root = Node()
        self.add_words(words)

    def add_words(self, words):
        for w in words:
            self.root.add(w)
    
    def get_prefixes_indices(self, w):
        node = self.root
        res = []
        for i, c in enumerate(w):
            if c not in node.d:
                break
            node = node.d[c]
            if node.word:
                res.append(i)
        return res

def is_possible(pattern, towels):
    @lru_cache(None)
    def dp(i):
        if i == len(pattern):
            return True
        for j in range(i, len(pattern)):   
            if pattern[i:j + 1] in towels and dp(j + 1):
                return True
        return False
    return dp(0)

def part2(patterns, towels):
    trie = Trie(towels)

    @lru_cache(None)
    def dp(w):
        if not w:
            return 1
        indices = trie.get_prefixes_indices(w)
        if not indices:
            return 0
        res = 0
        for i in indices:
            res += dp(w[i + 1:])
        return res

    res = 0
    for pattern in patterns:
        res += dp(pattern)
    return res

def part1(patterns, towels):
    towels = set(towels)
    res = 0
    for p in patterns:
        res += is_possible(p, towels)
    return res

print(part1(patterns, towels))
print(part2(patterns, towels))
