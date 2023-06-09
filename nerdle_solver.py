# This file is part of the nerdle_solver distribution
# (https://github.com/nerdle_solver or http://nerdle_solver.github.io).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from itertools import permutations
from re import findall

FIRST = ['9', '-', '1', '0', '/', '5', '=', '7']
SECOND = ['4', '*', '6', '+', '8', '=', '3', '2']
SIZE = 8

OPS = {'+': lambda a, b: a + b, '-': lambda a, b: a - b, '*': lambda a, b: a * b, '/': lambda a, b: a / b}


def get_values() -> tuple[list[str], list[str], list[list[str]]]:
    print('FIRST PUT TO NERDLE THE FOLLOWING COMBINATIONS')
    print('THEN INTRODUCE: - IF GREY | g IF GREEN | p IF PURPLE')

    # reads strings
    while True:
        print(''.join(FIRST))
        first_got: list[str] = [*input()]
        print(''.join(SECOND))
        second_got: list[str] = [*input()]

        if ''.join(first_got).strip('-pg') or ''.join(second_got).strip('-pg') or \
                len(first_got) != SIZE or len(second_got) != SIZE:
            print('WRONG INPUT\n')

        else:
            break

    # use chars
    _has: list[str] = list(set([FIRST[i] for i in range(SIZE) if first_got[i] != '-'] +
                               [SECOND[i] for i in range(SIZE) if second_got[i] != '-']))

    # has positions
    _has_pos: list[str] = [FIRST[i] if first_got[i] == 'g' else SECOND[i] if second_got[i] == 'g' else ''
                           for i in range(SIZE)]

    # has not positions
    _has_pos_not: list[list[str]] = []
    for i, p in enumerate(zip(first_got, second_got)):
        _has_pos_not.append([])
        if p[0] == 'p':
            _has_pos_not[-1].append(FIRST[i])
        if p[1] == 'p':
            _has_pos_not[-1].append(SECOND[i])

    return _has, _has_pos, _has_pos_not


def print_solutions(sol: list[tuple[str]]) -> None:  # prints every solution
    for s in sol:
        print('FOUND A POSSIBLE SOLUTION', ' '.join(s))


def get_solutions(_has: list[str], _has_pos: list[str], _has_pos_not: list[list[str]]) -> list[tuple[str]]:
    if len(_has) < SIZE:  # fill with permutations
        to_find = [_has.copy() + list(tf) for tf in permutations(_has, SIZE - len(_has)) if tf.count('=') == 0]
    else:  # enough
        to_find = [_has]

    sol = []
    for tf in to_find: # get all solutions possible
        tmp_sol = find_in(tf, _has_pos, _has_pos_not)
        if tmp_sol:
            sol += tmp_sol
    return list(set(sol))  # returns all solutions found


def check_has_pos(lp: list[str], _has_pos: list[str]) -> bool:
    return 0 not in [0 if _has_pos[i] and lp[i] != _has_pos[i] else 1 for i in range(SIZE)]


def check_has_pos_not(lp, _has_pos_not) -> bool:
    return 0 not in [0 if _has_pos_not[i] != [''] and lp[i] in _has_pos_not[i] else 1 for i in range(SIZE)]


def regex_filter(no_regex_list: list[str]) -> bool:
    # is supposed that on every side of operations are numbers
    str_p: str = ''.join(no_regex_list)

    if findall('[-+*/=][-+*/=]', str_p):  # two joined symbols
        return False

    if findall(r'^[-+*/=]|[-+*/=]$', str_p):  # no starts or ends with symbols
        return False

    if findall(r'/0+[-+*/=]|/0+$', str_p):  # no zero division
        return False

    if findall(r'=.+[-+*/].+', str_p):  # no operations other side of equal
        return False

    return True


def merge_nums(no_merge_nums_list) -> list[str]:
    # merge all nums
    merge_nums_list: list[str] = ['0']
    for c in no_merge_nums_list:
        if c.isdigit() and merge_nums_list[-1].isdigit():
            merge_nums_list[-1] += c
        else:
            merge_nums_list.append(c)
    return [str(int(c)) if c.isdigit() else c for c in merge_nums_list]


def operate(operate_list: list[str]) -> float:
    # operates following the hierarchy of operations
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
        op: str = operate_list.pop(i_op)
        op_b = operate_list.pop(i_op)
        operate_list.insert(i_op, OPS[op](float(op_a), float(op_b)))
        operate(operate_list)

    return float(operate_list[0])


def check_sol(res_a: float, res_b: float) -> bool:
    # check if is a solution
    return int(res_a) == int(res_b) if res_a.is_integer() and res_b.is_integer() else False


def find_in(to_find, _has_pos, _has_pos_not) -> list[tuple[str]]:
    all_solutions: list[tuple[str]] = []

    for p in permutations(to_find):  # for every permutation
        lp: list[str] = list(p)

        # if positions not mach or no correct regex
        if not check_has_pos(lp, _has_pos) or not check_has_pos_not(lp, _has_pos_not) or not regex_filter(lp):
            continue

        merged_lp: list[str] = merge_nums(lp)  # merge nums

        result: float = operate(merged_lp[:merged_lp.index('=')])  # operate

        # if is a solution and not in solution list
        if check_sol(result, float(merged_lp[-1])) and p not in all_solutions:
            all_solutions.append(p)

    return all_solutions


if __name__ == '__main__':
    print_solutions(get_solutions(*get_values()))
