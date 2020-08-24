#Created by Kevin Zheng, Aug 21, 2020

import copy

vars = list()
operators = ["AND", "OR", "NOT", "IMPLIES", "BI"]
parsed_str = []

def parse(string):
    tmp = set()

    string = string.replace("()", "")
    s = string.replace("(", "( ")
    s = s.replace(")", " )")
    l = [x.strip() for x in s.split()]
    p = []

    if l[0] in operators and l[0] != "NOT":
        raise Exception("Operator" + l[0] + " must have two sides")
    elif l[0] == "(":
        p.append("(")
    elif l[0] == ")":
        raise Exception("Bad parentheses")
    else:
        tmp.add(l[0])

    for i in range(1, len(l)):
        if l[i] == "NOT":
            if l[i-1] != "(":
                raise Exception("Input not fully parenthesized")
        elif l[i] in operators and (l[i-1] == "(" or l[i-1] in operators):
            raise Exception("Operator" + l[i] + " must have two sides")
        elif l[i] == "(":
            if l[i-1] not in operators and l[i-1] != "(":
                raise Exception("Bad parentheses at position " + str(i))
            else:
                p.append(")")
        elif l[i] == ")":
            if l[i-1] in operators:
                raise Exception("Operator" + l[i-1] + " must have two sides")
            elif len(p) == 0:
                raise Exception("Bad parentheses")
            else:
                p.pop()
        elif l[i] not in operators:
            tmp.add(l[i])

    if l[-1] in operators:
        raise Exception("Operator " + l[-1] + " must have a right side")
    if len(p) != 0:
        raise Exception("Bad parentheses")
    
    for term in tmp:
        vars.append(term)
    return l

def operate(v, s):
    if len(s) == 1:
        return v[s[0]]
    elif len(s) == 2 and s[0] == "NOT":
        return not v[s[1]]
    elif len(s) == 3:
        if s[1] == "AND":
            return v[s[0]] and v[s[2]]
        elif s[1] == "OR":
            return v[s[0]] or v[s[2]]
        elif s[1] == "IMPLIES":
            return (not v[s[0]]) or v[s[2]]
        elif s[1] == "BI":
            return ((not v[s[0]]) or v[s[2]]) and (v[s[0]] or (not v[s[2]]))

def calculate(values):
    stack = []
    eq = copy.deepcopy(parsed_str)
    i = 0
    while i < len(eq):
        if eq[i] == "(":
            stack.append(i)
        elif eq[i] == ")":
            left_bound = stack.pop()
            eq[left_bound] = operate(values, eq[left_bound+1:i])
            del eq[left_bound+1:i+1]
            i = left_bound
        i += 1
    return eq[0]

def print_res(values, res):
    for term in values.keys():
        if term == True or term == False:
            continue
        print(("T" if values[term] else "F").ljust(len(term)+1, ' '), end = '| ')
    print("T" if res else "F")

def recurse(values, i):
    if i == len(vars):
        res = calculate(values)
        print_res(values, res)
        return

    true_case = copy.deepcopy(values)
    false_case = copy.deepcopy(values)

    true_case[vars[i]] = True
    false_case[vars[i]] = False

    recurse(true_case, i+1)
    recurse(false_case, i+1)

original = input()
parsed_str = parse(original)
vars.sort()
val = {True: True, False: False}

print()
for term in vars:
    print(term, end = ' | ')
print(original)
recurse(val, 0)