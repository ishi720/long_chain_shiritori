import time
from collections import defaultdict
from typing import List, Set

import pulp

from main import text_list, get_first_char, get_last_char


def find_components(edges: List[int], start: str, firsts: List[str], lasts: List[str]) -> List[Set[str]]:
    """最初の文字と、選ばれたテキストでつながっている文字のまとまりを求める"""
    parent = {start: start}

    def find(char: str) -> str:
        while parent[char] != char:
            parent[char] = parent[parent[char]]
            char = parent[char]
        return char

    for i in edges:
        for char in (firsts[i], lasts[i]):
            parent.setdefault(char, char)
        parent[find(firsts[i])] = find(lasts[i])

    groups = defaultdict(set)
    for char in parent:
        groups[find(char)].add(char)
    return list(groups.values())


def order_path(edges: List[int], start: str, firsts: List[str], lasts: List[str]) -> List[int]:
    """選ばれたテキストを、しりとりの順番に並べる（ヒルホルツァーのアルゴリズム）"""
    adj = defaultdict(list)
    for i in edges:
        adj[firsts[i]].append(i)

    stack = [(start, None)]
    order = []
    while stack:
        char, edge = stack[-1]
        if adj[char]:
            i = adj[char].pop()
            stack.append((lasts[i], i))
        else:
            stack.pop()
            if edge is not None:
                order.append(edge)

    order.reverse()
    return order


def find_longest_path_ilp(names: List[str]) -> List[str]:
    """整数計画法で最長のしりとり経路を見つける"""
    if not names:
        return []

    n = len(names)
    firsts = [get_first_char(name) for name in names]
    lasts = [get_last_char(name) for name in names]
    chars = sorted(set(firsts) | set(lasts))

    prob = pulp.LpProblem('shiritori', pulp.LpMaximize)

    # テキストごとに、使うなら1、使わないなら0
    x = [pulp.LpVariable(f'x_{i}', cat='Binary') for i in range(n)]
    # 文字ごとに、しりとりの最初の文字なら1、最後の文字なら1
    s = {c: pulp.LpVariable(f's_{k}', cat='Binary') for k, c in enumerate(chars)}
    t = {c: pulp.LpVariable(f't_{k}', cat='Binary') for k, c in enumerate(chars)}

    # 使うテキストの数をできるだけ多くする
    prob += pulp.lpSum(x)

    # 文字ごとに「その文字で終わる数」と「その文字で始まる数」を釣り合わせる（最初と最後の文字だけ1つずれる）
    for c in chars:
        incoming = pulp.lpSum(x[i] for i in range(n) if lasts[i] == c)
        outgoing = pulp.lpSum(x[i] for i in range(n) if firsts[i] == c)
        prob += incoming + s[c] == outgoing + t[c]

    prob += pulp.lpSum(s.values()) == 1
    prob += pulp.lpSum(t.values()) == 1

    while True:
        prob.solve(pulp.PULP_CBC_CMD(msg=False))
        if pulp.LpStatus[prob.status] != 'Optimal':
            raise RuntimeError(f"解が見つかりませんでした: {pulp.LpStatus[prob.status]}")

        chosen = [i for i in range(n) if x[i].value() > 0.5]
        start = next(c for c in chars if s[c].value() > 0.5)
        components = find_components(chosen, start, firsts, lasts)
        if len(components) <= 1:
            break

        # 1本につながっていないので、離れたまとまりを禁止する条件を足して解き直す
        for comp in components:
            inside = [i for i in range(n) if firsts[i] in comp and lasts[i] in comp]
            entering = [i for i in range(n) if firsts[i] not in comp and lasts[i] in comp]
            # まとまりの中のテキストを使うなら、外から入ってくるか、そこから始まる必要がある
            prob += pulp.lpSum(x[i] for i in inside) <= len(inside) * (
                pulp.lpSum(x[i] for i in entering) + pulp.lpSum(s[c] for c in comp)
            )

    return [names[i] for i in order_path(chosen, start, firsts, lasts)]


def main():
    print("=" * 60)
    print("整数計画法で最長経路を探索中...")
    print("-" * 60)

    search_start_time = time.time()
    longest_path = find_longest_path_ilp(text_list)
    search_duration = time.time() - search_start_time

    print()
    print("=" * 60)
    print("結果")
    print("=" * 60)
    print(f"対象: {len(text_list)}匹")
    print(f"最長のしりとり: {len(longest_path)}匹")
    print()

    print("しりとりの順番:")
    for i, name in enumerate(longest_path, 1):
        next_info = f" → {get_last_char(name)}" if i < len(longest_path) else ""
        print(f"{i:3d}. {name}{next_info}")

    print()
    print("=" * 60)
    print(f"探索時間: {search_duration:.2f}秒")
    print("=" * 60)


if __name__ == "__main__":
    main()
