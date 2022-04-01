import copy
import operator


class Rule:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.predict = set()


class Generator:
    def __init__(self, file):
        self.rules = self.get_rules(file)
        self.non_terminators = self.get_non_terminators()
        self.firstset = self.get_firstset()
        self.followset = self.get_followset()
        self.get_predictset()

    def get_rules(self, file):
        rules = []
        with open(file, 'r', encoding='UTF-8') as f:
            lines = f.readlines()
        left = ''
        for line in lines:
            rule = line.strip('\n').split(')', 1)[-1]
            if '::=' in rule:
                left, right = rule.split('::=')
                left = left.strip(' ')
                right = right.strip(' ').split(' ')
            else:
                right = rule.split('|', 1)[-1].strip(' ').split(' ')
            rule = Rule(left, right)
            rules.append(rule)
        return rules

    def get_non_terminators(self):
        non_terminators = set()
        for rule in self.rules:
            non_terminators.add(rule.left)
        return non_terminators

    def get_firstset(self):
        firstset = {}
        for non_terminator in iter(self.non_terminators):
            firstset[non_terminator] = set()
        completedset = set()
        for non_terminator in iter(self.non_terminators):
            firstset, completedset = \
                self.get_oneword_firstset(non_terminator, firstset, completedset)
        return firstset

    def get_oneword_firstset(self, word, firstset, completedset):
        for rule in self.rules:
            if rule.left == word:
                for i, aa in enumerate(rule.right):
                    if self.is_terminators(aa):
                        firstset[word].add(aa)
                        break
                    elif word not in completedset:
                        firstset, completedset = \
                            self.get_oneword_firstset(aa, firstset, completedset)
                    add_set = copy.deepcopy(firstset[aa])
                    if 'ε' not in add_set:
                        firstset[word] |= add_set
                        break
                    if i + 1 != len(rule.right):
                        add_set.remove('ε')
                    firstset[word] |= add_set
        completedset.add(word)
        return firstset, completedset

    def get_followset(self):
        followset = {}
        for non_terminator in iter(self.non_terminators):
            followset[non_terminator] = set()
        start_word = copy.deepcopy(self.non_terminators)
        for rule in self.rules:
            for word in rule.right:
                start_word.discard(word)
        assert len(start_word) == 1, \
            'There is more than one grammar start symbol, please check the given grammar production.'
        followset[start_word.pop()].add('#')
        while True:
            save_set = copy.deepcopy(followset)
            for rule in self.rules:
                for i in range(len(rule.right)):
                    if not self.is_terminators(rule.right[i]):
                        if i + 1 == len(rule.right):
                            followset[rule.right[i]] |= followset[rule.left]
                        else:
                            add_set = self.First(rule.right[i + 1:])
                            if 'ε' in add_set:
                                add_set.remove('ε')
                                followset[rule.right[i]] |= (add_set | followset[rule.left])
                            else:
                                followset[rule.right[i]] |= add_set
            if operator.eq(save_set, followset):
                break
        return followset

    def get_predictset(self):
        for rule in self.rules:
            predict = self.First(rule.right)
            if 'ε' in predict:
                predict.remove('ε')
                predict |= self.followset[rule.left]
            rule.predict = predict

    def First(self, list):
        add_set = set()
        for i, aa in enumerate(list):
            if self.is_terminators(aa):
                add_set.add(aa)
                break
            ss = copy.deepcopy(self.firstset[aa])
            if 'ε' not in ss:
                add_set |= ss
                break
            if i + 1 != len(list):
                ss.remove('ε')
            add_set |= ss
        return add_set

    def show_rules(self):
        for rule in self.rules:
            print(rule.left, "=>", end='')
            for x in rule.right:
                print(' {}'.format(x), end='')
            print()

    def save_predictset(self, path, visible=False):
        with open(path, 'w', encoding='utf-8') as file:
            for i, rule in enumerate(self.rules):
                line = str(i + 1) + ')' + rule.left + '::='
                for x in rule.right:
                    line += x + ' '
                line += '{'
                for x in iter(rule.predict):
                    line += x + ' '
                line = line[::-1].replace(' ', '}', 1)[::-1]
                if visible:
                    print(line)
                line += '\n'
                file.write(line)

    def is_terminators(self, word):
        if word not in self.non_terminators:
            return True
        return False


def strip_blank(str):
    str = list(str.strip(" "))
    res = ''
    for i in range(len(str)):
        if str[i] == " " and str[i + 1] == " ":
            continue
        res += str[i]
    return res


if __name__ == '__main__':
    generator = Generator("SNL文法")
    generator.save_predictset('predict', visible=True)
