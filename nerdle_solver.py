from itertools import permutations
import re

FIRST = ['1', '0', '/', '5', '=', '9', '-', '7', ]
SECOND = ['6', '*', '4', '+', '8', '=', '3', '2']
SIZE = 8

OPS = {'+': lambda a, b: a+b, '-': lambda a, b: a-b, '*': lambda a, b: a*b, '/': lambda a, b: a/b}


def get_values():
    print('FIRST PUT TO NERDLE THE FOLLOWING COMBINATIONS')
    print('THEN INTRODUCE: - IF GREY | g IF GREEN | p IF PURPLE')

    # reads strings
    while True:
        print(' '.join(FIRST))
        first_got = [*input()]
        print(' '.join(SECOND))
        second_got = [*input()]
        if not ''.join(first_got).strip('-pg') or not ''.join(second_got).strip('-pg') or \
                len(first_got) != SIZE or len(first_got) != SIZE:
            break
        print('WRONG INPUT')

    # use chars
    _has = list(set([FIRST[i] for i in range(SIZE) if first_got[i] != '-'] +
                    [SECOND[i] for i in range(SIZE) if second_got[i] != '-']))

    # has positions
    _has_pos = [FIRST[i] if first_got[i] == 'g' else SECOND[i] if second_got[i] == 'g' else '' for i in range(SIZE)]

    # has not positions
    _has_pos_not = []
    for i in range(SIZE):
        _has_pos_not.append([])
        if first_got[i] == 'p':
            _has_pos_not[-1].append(FIRST[i])
        if second_got[i] == 'p':
            _has_pos_not[-1].append(SECOND[i])

    return _has, _has_pos, _has_pos_not


def get_solutions(_has, _has_pos, _has_pos_not):
    if len(_has) < SIZE:  # fill with permutations
        to_find = [tf for tf in _has.copy() + permutations(_has, SIZE - len(_has)) if tf.count('=') == 1]
    else:  # enough
        to_find = [_has]

    for tf in to_find:  # find all
        find_in(tf, _has_pos, _has_pos_not)


def check_has_pos(lp, _has_pos):
    return 0 not in [0 if _has_pos[i] and lp[i] != _has_pos[i] else 1 for i in range(SIZE)]


def check_has_pos_not(lp, _has_pos_not):
    return 0 not in [0 if _has_pos_not[i] != [''] and lp[i] in _has_pos_not[i] else 1 for i in range(SIZE)]


def regex_filter(no_regex_list):
    # is supposed that on every side of operations are numbers
    str_p = ''.join(no_regex_list)

    if re.findall('[-+*/=][-+*/=]', str_p):  # two joined symbols
        return False

    if re.findall(r'^[-+*/=]', str_p) or re.findall(r'[-+*/=]$', str_p):  # no starts or ends with symbols
        return False

    if re.findall(r'/0+$', str_p) or re.findall(r'/0+[-+*/=]', str_p):  # no zero division
        return False

    if re.findall(r'^0', str_p):  # no zero start
        return False

    if re.findall(r'=.+[-+*/].+', str_p):  # no operations other side of equal
        return False

    return True


def merge_nums(no_merge_nums_list):
    # merge all nums
    merge_nums_list = ['0']
    for c in no_merge_nums_list:
        if c.isdigit() and merge_nums_list[-1].isdigit():
            merge_nums_list[-1] += c
        else:
            merge_nums_list.append(c)
    return [str(int(c)) if c.isdigit() else c for c in merge_nums_list]


def operate(operate_list):
    i_op = None

    for i in range(len(operate_list)):
        if operate_list[i] == '*' or operate_list[i] == '/':
            i_op = i - 1
            break

    if i_op is None:
        for i in range(len(operate_list)):
            if operate_list[i] == '+' or operate_list[i] == '-':
                i_op = i - 1
                break

    if i_op is not None:
        op_a = operate_list.pop(i_op)
        op = operate_list.pop(i_op)
        op_b = operate_list.pop(i_op)
        operate_list.insert(i_op, OPS[op](float(op_a), float(op_b)))
        operate(operate_list)

    return float(operate_list[0])


def check_sol(res_a, res_b):
    return int(res_a) == int(res_b) if res_a.is_integer() and res_b.is_integer() else False


def find_in(to_find, _has_pos, _has_pos_not):
    all_solutions = []
    for p in permutations(to_find):
        lp = list(p)

        if not check_has_pos(lp, _has_pos) or not check_has_pos_not(lp, _has_pos_not):
            continue

        if not regex_filter(lp):
            continue

        merged_lp = merge_nums(lp)

        result = operate(merged_lp[:merged_lp.index('=')])

        if check_sol(result, float(merged_lp[-1])):
            print('FOUND A POSSIBLE SOLUTION:', ' '.join(lp)) if p not in p else all_solutions.append(p)


if __name__ == '__main__':
    get_solutions(*get_values())
