import numpy as np
from collections import defaultdict
from itertools import combinations

class Apriori:
    def __init__(self, data, min_sup_rate = 0.2):
        self.data = data
        self.size = len(data)
        self.min_sup_value = min_sup_rate * self.size

    def first_scan(self):
        freqDict = defaultdict(int)
        for p in self.data:
            for item in p:
                freqDict[item] += 1
        f1 = []
        for item in freqDict:
            if freqDict[item] >= self.min_sup_value:
                f1.append([item])
        return f1

    def prune(self, c, fn, n):
        subset = list(combinations(c, n-1))
        for each in subset:
            each = list(each)
            if each not in fn:
                return True
        return False

    def join(self, fn):
        n = len(fn[0]) + 1
        candidate = []
        for item1 in fn:
            for item2 in fn:
                stop = False
                for i in range(n-2):
                    if item1[i] != item2[i]:
                        stop = True
                        break
                if stop:
                    continue
                if item1[n-2] < item2[n-2]:
                    c = item1 + [item2[n-2]]
                else:
                    continue
                if self.prune(c, fn, n):
                    continue
                else:
                    candidate.append(c)
        return candidate

    def run(self):
        fn = self.first_scan()
        f = fn
        while fn:
            candidate = self.join(fn)
            freqDict = defaultdict(int)
            for p in self.data:
                for c in candidate:
                    if set(c) <= set(p):
                        freqDict[tuple(c)] += 1
            fk = []
            for c in freqDict:
                if freqDict[c] >= self.min_sup_value:
                    fk.append(list(c))
            fn = fk
            f += fk
        return f

def data_loader(file_path='associationruletestdata.txt'):
    '''
    :return: [['G1_Up', ..., disease name], ...]
    '''
    file = open(file_path, 'r')
    raw_data = []
    for line in file.readlines():
        line = line.strip().split('\t')
        tmp_data = []
        for index, item in enumerate(line):
            if item == 'Up' or item == 'Down':
                tmp_data.append('G%s_%s'%(str(index+1), item))
            else:
                tmp_data.append(item)
        raw_data.append(tmp_data)
    return raw_data



if __name__ == '__main__':
    data = data_loader()
    a = Apriori(data=data, min_sup_rate=0.5)
    print(len(a.run()))
