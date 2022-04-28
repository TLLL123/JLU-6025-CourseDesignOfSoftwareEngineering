"""
Predict set inference
"""
import copy
import operator


class Rule:
    def __init__(self, left, right):
        """
        文法规则
            left：非终极符
            right：左侧推导文法
            predict：每条文法的predict集
        """
        self.left = left
        self.right = right
        self.predict = set()


class Generator:
    def __init__(self, file):
        """
        从文件读入SNL语法规则，推导文法Predict集
            get_rules(file)：从文件读入字符串生成文法规则
            get_non_terminators()：返回非终极符集合，便于后续判断
            get_firstset()：推导First集
            get_followset()：推导Follow集
            get_predictset()：推导Predict集
        """
        self.rules = self.get_rules(file)
        self.non_terminators = self.get_non_terminators()
        self.firstset = self.get_firstset()
        self.followset = self.get_followset()
        self.get_predictset()

    def get_rules(self, file):
        """
        从文件读入SNL文法，预处理字符串，生成104条文法规则
            return：list[Rule]
        """
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
        """
        返回非终极符集合，便于后续做判断
            return：set()
        """
        non_terminators = set()
        for rule in self.rules:
            non_terminators.add(rule.left)
        return non_terminators

    def get_firstset(self):
        """
        求所有非终极符的firt集
            return：dict[非终极符, set{首字符集}]
        """
        firstset = {}
        for non_terminator in iter(self.non_terminators):
            firstset[non_terminator] = set()
        completedset = set()
        for non_terminator in iter(self.non_terminators):
            firstset, completedset = \
                self.get_oneword_firstset(non_terminator, firstset, completedset)
        return firstset

    def get_oneword_firstset(self, word, firstset, completedset):
        """
        递归(dfs)求单个非终极符的firt集
            firstset：dict[非终极符, set{首字符集}]
            completedset:记录已经求过First集的所有非终极符
        """
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
        """
        求所有非终极符的follow集，当follow集不再更新时表示全部求完
            return：dict[非终极符, set{跟随符集}]
        """
        followset = {}
        for non_terminator in iter(self.non_terminators):
            followset[non_terminator] = set()
        start_word = copy.deepcopy(self.non_terminators)
        for rule in self.rules:
            for word in rule.right:
                start_word.discard(word)
        assert len(start_word) == 1, \
            'There is more than one grammar start symbol, please check the given grammar productions.'
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
        """
        根据First集和Follow集对每条文法求Predict集
        每条文法的Predict集和对应左、右部记录在一个数据结构中
        """
        for rule in self.rules:
            predict = self.First(rule.right)
            if 'ε' in predict:
                predict.remove('ε')
                predict |= self.followset[rule.left]
            rule.predict = predict

    def First(self, list):
        """
        求一串符号序列的first集
            return：set{首字符集}
        """
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
        """
        打印显示程序读入的文法规则
        """
        for rule in self.rules:
            print(rule.left, "=>", end='')
            for x in rule.right:
                print(' {}'.format(x), end='')
            print()

    def save_predictset(self, path, visible=False):
        """
        predict集存盘
            path：存盘路径
            visible：为True打印输出
        """
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
        """
        是否属于非终极符？
            return：True:False
        """
        if word not in self.non_terminators:
            return True
        return False


def strip_blank(str):
    """
    字符串预处理，使从文件读入的字符串更工整易于处理
        return：str
    """
    str = list(str.strip(" "))
    res = ''
    for i in range(len(str)):
        if str[i] == " " and str[i + 1] == " ":
            continue
        res += str[i]
    return res


if __name__ == '__main__':
    generator = Generator("SNL文法")  # 初始化并推导Predict集
    generator.save_predictset('predict', visible=True)  # 存盘并打印显示
