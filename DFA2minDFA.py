from turtle import shape
from graphviz import Digraph
from RE2RET import REToRPN
from collections import deque

class NFA_State:
    def __init__(self, id=0, accepted=False) -> None:
        self.id = id
        self.accept = accepted
        self.next = []


class NFA_Transition:
    def __init__(self, source_state=None, target_state=None, char='') -> None:
        self.source_state = source_state
        self.target_state = target_state
        self.char = char

class DFA_State:
    def __init__(self, id=0, accepted=False) -> None:
        self.id = id
        self.accepted = accepted
        self.next = []

class DFA_Transition:
    def __init__(self, source_state=None, target_state=None, char='') -> None:
        self.source_state = source_state
        self.target_state = target_state
        self.char = char

end_state_id = -1
entre = {} # 建立节点序号与DFA节点地址的映射
def RE2NFA(re, draw=True):
    mp = {} # 记录头节点和尾节点的映射关系
    global end_state_id
    nfa_id = 0
    rpn = REToRPN(re)
    print(rpn)
    stack = []
    dots = Digraph(comment='RE to NFA')
    for i, c in enumerate(rpn):
        if c.isalpha():
            start = NFA_State(id=nfa_id)
            if draw:
                dots.node(str(nfa_id), str(nfa_id))
            nfa_id += 1
            end = NFA_State(id=nfa_id)
            if i == len(rpn) - 1:
                end_state_id = nfa_id
            if draw:
                dots.node(str(nfa_id), str(nfa_id))
            nfa_id += 1
            mp[start] = end
            edge = NFA_Transition(start, end, c)
            if draw:
                dots.edge(str(start.id), str(end.id), c)
            start.next.append(edge)
            stack.append(start)
            
        elif c == '*':
            head = stack[-1]
            stack.pop()
            tail = mp[head]
            tail2head = NFA_Transition(tail, head, '_')
            if draw:
                dots.edge(str(tail.id), str(head.id), 'ε')
            tail.next.append(tail2head)
            state_start = NFA_State(id=nfa_id)
            if draw:
                dots.node(str(nfa_id), str(nfa_id))
            nfa_id += 1
            start2head = NFA_Transition(state_start, head, '_')
            if draw:
                dots.edge(str(state_start.id), str(head.id), 'ε')
            state_start.next.append(start2head)
            state_end = NFA_State(id=nfa_id)
            if i == len(rpn) - 1:
                end_state_id = nfa_id
                if draw:
                    dots.node(str(nfa_id), str(nfa_id), shape="doublecircle")
                state_end.accept = True
            else:
                if draw:
                    dots.node(str(nfa_id), str(nfa_id))
            nfa_id += 1
            start2end = NFA_Transition(state_start, state_end, '_')
            if draw:
                dots.edge(str(state_start.id), str(state_end.id), 'ε')
            state_start.next.append(start2end)
            tail2end = NFA_Transition(tail, state_end, '_')
            if draw:
                dots.edge(str(tail.id), str(state_end.id), 'ε')
            tail.next.append(tail2end)
            mp[state_start] = state_end
            stack.append(state_start)

        elif c == '.':
            right_head = stack[-1]
            right_tail = mp[right_head]
            stack.pop()
            left_head = stack[-1]
            left_tail = mp[left_head]
            stack.pop()
            state_start = NFA_State(id=nfa_id)
            if draw:
                dots.node(str(nfa_id), str(nfa_id))
            nfa_id += 1
            start2left_head = NFA_Transition(state_start, left_head, '_')
            if draw:
                dots.edge(str(state_start.id), str(left_head.id), 'ε')
            state_start.next.append(start2left_head)
            left_tail2right_head = NFA_Transition(left_tail, right_head, '_')
            if draw:
                dots.edge(str(left_tail.id), str(right_head.id), 'ε')
            left_tail.next.append(left_tail2right_head)
            state_end = NFA_State(id=nfa_id)
            if i == len(rpn) - 1:
                end_state_id = nfa_id
                if draw:
                    dots.node(str(nfa_id), str(nfa_id), shape="doublecircle")
                state_end.accept = True
            else:
                if draw:
                    dots.node(str(nfa_id), str(nfa_id))
            nfa_id += 1
            right_tail2state_end = NFA_Transition(right_tail, state_end, '_')
            if draw:
                dots.edge(str(right_tail.id), str(state_end.id), 'ε')
            right_tail.next.append(right_tail2state_end)
            mp[state_start] = state_end
            stack.append(state_start)

        elif c == '|':
            up_head = stack[-1]
            up_tail = mp[up_head]
            stack.pop()
            low_head = stack[-1]
            low_tail = mp[low_head]
            stack.pop()
            state_start = NFA_State(nfa_id)
            if draw:
                dots.node(str(nfa_id), str(nfa_id))
            nfa_id += 1
            start2up_head = NFA_Transition(state_start, up_head, '_')
            if draw:
                dots.edge(str(state_start.id), str(up_head.id), 'ε')
            state_start.next.append(start2up_head)
            start2low_head = NFA_Transition(state_start, low_head, '_')
            if draw:
                dots.edge(str(state_start.id), str(low_head.id), 'ε')
            state_start.next.append(start2low_head)
            state_end = NFA_State(nfa_id)
            if i == len(rpn) - 1:
                end_state_id = nfa_id
                if draw:
                    dots.node(str(nfa_id), str(nfa_id), shape="doublecircle")
                state_end.accept = True
            else:
                if draw:
                    dots.node(str(nfa_id), str(nfa_id))
            nfa_id += 1
            up_tail2end = NFA_Transition(up_tail, state_end, '_')
            dots.edge(str(up_tail.id), str(state_end.id), 'ε')
            up_tail.next.append(up_tail2end)
            low_tail2end = NFA_Transition(low_tail, state_end, '_')
            dots.edge(str(low_tail.id), str(state_end.id), 'ε')
            low_tail.next.append(low_tail2end)
            mp[state_start] = state_end
            stack.append(state_start)
        else:
            print('Invalid character!')
            exit(0)
    if draw:
        dots.view()
        # print(dots.source)
    return stack[-1]



def NFA2DFA(head, alpha_list, draw=True):
    # 获取s(初始状态)
    dfa = Digraph(comment='DFA')
    s = list()
    p = head
    stack = [p]
    dfa_id = 0
    node_list = [] 
    dfa_list = []   # 已经出现过的dfa节点编号
    while stack:
        t = stack[-1]
        s.append(str(t.id))
        node_list.append(t)
        stack.pop()
        for edge in t.next:
            if edge.char == '_' and edge.target_state.id not in s:
                stack.append(edge.target_state)
    s = sorted(s)
    s = ' '.join(s)  # 因列表无法hash 把key转为string
    dfa_list.append(s)
    accepted = True if str(end_state_id) in s else False
    start = DFA_State(dfa_id, accepted)
    entre[dfa_id] = start   # 为最小化dfa准备
    if draw:
        if accepted:
            dfa.node(str(dfa_id), str(dfa_id), shape='doublecircle')
        else:
            dfa.node(str(dfa_id), str(dfa_id))
    dfa_id += 1
    que = deque([node_list])
    mp = {} # 从节点编号映射到DFA_State节点地址
    mp[s] = start
    while que:
        pre_node_list = que.popleft()
        pre_s = []
        for node in pre_node_list:
            pre_s.append(str(node.id))
        pre_s = sorted(pre_s) # 还原初始状态对应的编号
        pre_s = ' '.join(pre_s)
        pre_dfa_node = mp[pre_s] # 这行初始节点对应的dfa节点
        for c in alpha_list:
            cur_node_list = []
            new_s = []
            temp = pre_node_list[:]
            while temp:
                node = temp[-1]
                temp.pop()
                for edge in node.next:
                    if edge.char == c and str(edge.target_state.id) not in new_s:
                        cur_node_list.append(edge.target_state)
                        new_s.append(str(edge.target_state.id))
                        temp.append(edge.target_state)
            # cur_node_list要合并
            temp = cur_node_list[:]
            while temp:
                node = temp[-1]
                temp.pop()
                for edge in node.next:
                    if edge.char == '_' and str(edge.target_state.id) not in new_s:
                        cur_node_list.append(edge.target_state)
                        new_s.append(str(edge.target_state.id))
                        temp.append(edge.target_state)
            new_s = sorted(new_s)
            new_s = ' '.join(new_s)
            if new_s:   # 非空
                if new_s not in dfa_list:   # 第一次出现的新状态
                    dfa_list.append(new_s)
                    accepted = True if str(end_state_id) in new_s else False
                    new_dfa_node = DFA_State(dfa_id, accepted)
                    entre[dfa_id] = new_dfa_node
                    if accepted:
                        if draw:
                            dfa.node(str(dfa_id), str(dfa_id), shape='doublecircle')
                    else:
                        if draw:
                            dfa.node(str(dfa_id), str(dfa_id))
                    dfa_id += 1
                    mp[new_s] = new_dfa_node
                    edge = DFA_Transition(pre_dfa_node, new_dfa_node, c)
                    pre_dfa_node.next.append(edge)
                    if draw:
                        dfa.edge(str(pre_dfa_node.id), str(new_dfa_node.id), c)
                    que.append(cur_node_list)
                else:
                    this_dfa_node = mp[new_s]
                    edge = DFA_Transition(pre_dfa_node, this_dfa_node, c)
                    pre_dfa_node.next.append(edge)
                    if draw:
                        dfa.edge(str(pre_dfa_node.id), str(this_dfa_node.id), c)
    if draw:
        dfa.view()

def DFA2minDFA(alpha_list):
    n = len(entre)
    m = len(alpha_list)
    new_list = [0 for _ in range(n)]
    for i in range(n):
        new_list[i] = 2 if entre[i].accepted else 1
    array = [[-1 for _ in range(m)] for __ in range(n)]
    # while pre_list != new_list:
    pre_list = [0 for _ in range(n)]
    while new_list != pre_list:
        pre_list = new_list[:]
        for i in range(n):
            for j in range(m):
                # i节点 alpha_list[j]的字母
                for edge in entre[i].next:
                    if edge.char == alpha_list[j]:
                        idx = edge.target_state.id
                        array[i][j] = pre_list[idx]
        temp = []
        idx = 1
        for i in range(n):
            new_line = [pre_list[i]]
            new_line += array[i][:]
            if new_line not in temp:
                temp.append(new_line)
                new_list[i] = idx
                idx += 1
            else:
                for j, line in enumerate(temp):
                    if line == new_line:
                        new_list[i] = j + 1
                        break
    minDFA = Digraph(comment='min DFA')
    drawed = [] # 记录画过的节点编号
    group_drawed = [] # 记录画过的出发点编号
    end_status = []
    for i in range(n):
        if entre[i].accepted and new_list[i] not in end_status:
            end_status.append(new_list[i])
    for i in range(n):
        if new_list[i] in group_drawed: # 这组画过了
            continue
        if new_list[i] not in drawed:
            if new_list[i] in end_status:
                minDFA.node(str(new_list[i]), str(new_list[i]), shape='doublecircle')
            else:
                minDFA.node(str(new_list[i]), str(new_list[i]))
            drawed.append(new_list[i])        

        group_drawed.append(new_list[i])
        for j in range(m):
            to = array[i][j]
            if to == -1:
                continue
            if to not in drawed:    # 如果这个节点没有被画过
                if to in end_status:
                    if to in end_status:
                         minDFA.node(str(to), str(to), shape='doublecircle')
                    else:
                        minDFA.node(str(to), str(to))
                drawed.append(to)
            minDFA.edge(str(new_list[i]), str(to), alpha_list[j])

    minDFA.node('start', 'start')
    minDFA.edge('start', '1')
    minDFA.view()


# FIXME: 结束状态出错
# (a|b)*ab(a*|b)
re = '(a|b)*ab(a*|b)'
alpha_list = [] # 正则表达式中出现的字母表
for char in re:
    if char.isalpha() and char not in alpha_list:
        alpha_list.append(char)
alpha_list = sorted(alpha_list)
head = RE2NFA(re, False)
NFA2DFA(head, alpha_list, False)
DFA2minDFA(alpha_list)