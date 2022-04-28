"""
Utilities
"""
from graphviz import Digraph


class FormatTransformer:
    """
    格式转换工具
    """
    def tokenListTransf(self, tokenlist):
        """
        token序列单词大小写转换，便于程序输入输出对接
            return：list[token序列]
        """
        res = []
        for i, aa in enumerate(tokenlist):
            if aa[1] != 'ID' and aa[1] != 'CONST':
                token = (aa[0], aa[1], aa[2].upper())
                res.append(token)
            else:
                res.append(aa)
        return res


def drawTree(root, matchTags):
    dot = Digraph(comment='Tree')
    def connectNode(node):
        if(len(node.children)>0):
            for child in node.children:
                if(child.tag in matchTags):
                    dot.node(str(child.tag), child.data+'---'+str(child.word), shape='plaintext',fontcolor='crimson')
                else:
                    dot.node(str(child.tag),child.data,shape='plaintext')
                dot.edge(str(node.tag),str(child.tag),arrowshape='none')
                connectNode(child)#递归
    dot.node(str(root.tag),root.data,shape='plaintext')
    connectNode(root)
    dot.render('SyntaxTree-output/SyntaxTree.gv', view=True)


def draw():
    g = Digraph('G', filename='hello.gv')
    g.edge_attr.update(arrowhead='vee', arrowsize='2')  # edge 的样式
    g.graph_attr['rankdir'] = 'LR'
    g.node('node1', label='Hello', shape='star')
    g.node('node2', label='World', shape='egg')
    g.edge('node1', 'node2')
    g.view()

    f = Digraph('finite_state_machine', filename='fsm.gv')
    f.attr(rankdir='LR', size='20,5')
    # 单独定义的 node 会有双圆结构
    f.attr('node', shape='doublecircle')
    f.node('LR_0')
    f.node('LR_3')
    f.node('LR_4')
    f.node('LR_8')
    f.attr('node', shape='circle')
    f.edge('LR_0', 'LR_2', label='SS(B)')
    f.edge('LR_0', 'LR_1', label='SS(S)')
    f.edge('LR_1', 'LR_3', label='S($end)')
    f.edge('LR_2', 'LR_6', label='SS(b)')
    f.edge('LR_2', 'LR_5', label='SS(a)')
    f.edge('LR_2', 'LR_4', label='S(A)')
    f.edge('LR_5', 'LR_7', label='S(b)')
    f.edge('LR_5', 'LR_5', label='S(a)')
    f.edge('LR_6', 'LR_6', label='S(b)')
    f.edge('LR_6', 'LR_5', label='S(a)')
    f.edge('LR_7', 'LR_8', label='S(b)')
    f.edge('LR_7', 'LR_5', label='S(a)')
    f.edge('LR_8', 'LR_6', label='S(b)')
    f.edge('LR_8', 'LR_5', label='S(a)')
    f.view()

    graph = Digraph(name='SyntaxTree', filename='Syntax Tree.gv')
    g.attr(rankdir='LR', size='20,5')
    g.edge_attr.update(arrowhead='vee', arrowsize='1')  # edge 的样式

# D1(){   //非终极符D1递归下降程序
#     if token 属于 集合1
#         D2();       //调用非终极符D2递归下降程序
#         match(x);   //匹配终极符x
#     elif token 属于 集合2
#         match(y);   //匹配终极符x
#         D3();       //调用非终极符D3递归下降程序
#         D4();       //调用非终极符D4递归下降程序
#     elif token 属于 集合3
#         skip();     //空语句
#     else
#         error();    //出错
#     fi
# }