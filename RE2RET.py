# TODO: 输入正则表达式， 生成逆波兰
# ab|c(d*|a)

def REToRPN(re: str) -> str:
    re = addDots(re)
    stack = []
    s = []
    # 运算符优先级 * > . > |
    prio = {'|': 0, '.': 1, '*': 2}
    for c in re:
        if c.isalpha():
            s.append(c)
        else:
            if c == '(':
                stack.append(c)
            elif c == ')':
                while stack[-1] != '(':
                    s.append(stack[-1])
                    stack.pop()
                stack.pop()
            elif c == '*':
                s.append(c)
            else:
                if stack == []:
                    stack.append(c)
                    continue
                while stack != [] and stack[-1] != '(' and prio[stack[-1]] >= prio[c]:
                    s.append(stack[-1])
                    stack.pop()
                stack.append(c)
    while stack != []:
        s.append(stack[-1])
        stack.pop()
    return ''.join(s)


def addDots(re: str) -> str:
    # 字符之间 & 字符与() & ()与()
    s = list(re)
    for i in range(len(re) - 1, 0, -1):
        if s[i].isalpha() and s[i - 1].isalpha():
            s.insert(i, '.')
        elif s[i].isalpha() and s[i - 1] == ')':
            s.insert(i, '.')
        elif s[i] == '(' and s[i - 1].isalpha():
            s.insert(i, '.')
        elif s[i] == '(' and s[i - 1] == ')':
            s.insert(i, '.')
        elif s[i].isalpha() and s[i - 1] == '*':
            s.insert(i, '.')
    return ''.join(s)

# re = 'ab|b(d*|a)'
# re = '(a|b)*ab(a*|b)'
# re = "(a|b)*ab(a*|b)"
# print(REToRPN(re))