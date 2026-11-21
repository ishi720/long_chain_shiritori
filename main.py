import argparse
import sys
import time
from typing import List, Dict, Set, Tuple

# テキストリスト
text_list = [
    'フシギダネ', 'フシギソウ', 'フシギバナ', 'ヒトカゲ', 'リザード',
    'リザードン', 'ゼニガメ', 'カメール', 'カメックス', 'キャタピー',
    'トランセル', 'バタフリー', 'ビードル', 'コクーン', 'スピアー',
    'ポッポ', 'ピジョン', 'ピジョット', 'コラッタ', 'ラッタ',
    'オニスズメ', 'オニドリル', 'アーボ', 'アーボック', 'ピカチュウ',
    'ライチュウ', 'サンド', 'サンドパン', 'ニドラン♀', 'ニドリーナ',
    'ニドクイン', 'ニドラン♂', 'ニドリーノ', 'ニドキング', 'ピッピ',
    'ピクシー', 'ロコン', 'キュウコン', 'プリン', 'プクリン',
    'ズバット', 'ゴルバット', 'ナゾノクサ', 'クサイハナ', 'ラフレシア',
    'パラス', 'パラセクト', 'コンパン', 'モルフォン', 'ディグダ',
    'ダグトリオ', 'ニャース', 'ペルシアン', 'コダック', 'ゴルダック',
    'マンキー', 'オコリザル', 'ガーディ', 'ウインディ', 'ニョロモ',
    'ニョロゾ', 'ニョロボン', 'ケーシィ', 'ユンゲラー', 'フーディン',
    'ワンリキー', 'ゴーリキー', 'カイリキー', 'マダツボミ', 'ウツドン',
    'ウツボット', 'メノクラゲ', 'ドククラゲ', 'イシツブテ', 'ゴローン',
    'ゴローニャ', 'ポニータ', 'ギャロップ', 'ヤドン', 'ヤドラン',
    'コイル', 'レアコイル', 'カモネギ', 'ドードー', 'ドードリオ',
    'パウワウ', 'ジュゴン', 'ベトベター', 'ベトベトン', 'シェルダー',
    'パルシェン', 'ゴース', 'ゴースト', 'ゲンガー', 'イワーク',
    'スリープ', 'スリーパー', 'クラブ', 'キングラー', 'ビリリダマ',
    'マルマイン', 'タマタマ', 'ナッシー', 'カラカラ', 'ガラガラ',
    'サワムラー', 'エビワラー', 'ベロリンガ', 'ドガース', 'マタドガス',
    'サイホーン', 'サイドン', 'ラッキー', 'モンジャラ', 'ガルーラ',
    'タッツー', 'シードラ', 'トサキント', 'アズマオウ', 'ヒトデマン',
    'スターミー', 'バリヤード', 'ストライク', 'ルージュラ', 'エレブー',
    'ブーバー', 'カイロス', 'ケンタロス', 'コイキング', 'ギャラドス',
    'ラプラス', 'メタモン', 'イーブイ', 'シャワーズ', 'サンダース',
    'ブースター', 'ポリゴン', 'オムナイト', 'オムスター', 'カブト',
    'カブトプス', 'プテラ', 'カビゴン', 'フリーザー', 'サンダー', 'ファイヤー',
    'ミニリュウ', 'ハクリュー', 'カイリュー', 'ミュウツー', 'ミュウ'
]

def normalize_char(char: str) -> str:
    """文字を正規化（小文字→大文字、濁点半濁点を除去）"""
    # 小文字を大文字に変換
    small_to_large = {
        'ァ': 'ア', 'ィ': 'イ', 'ゥ': 'ウ', 'ェ': 'エ', 'ォ': 'オ',
        'ャ': 'ヤ', 'ュ': 'ユ', 'ョ': 'ヨ', 'ッ': 'ツ', 'ヮ': 'ワ'
    }
    char = small_to_large.get(char, char)

    # 濁点半濁点を除去
    # dakuten_map = {
    #     'ガ': 'カ', 'ギ': 'キ', 'グ': 'ク', 'ゲ': 'ケ', 'ゴ': 'コ',
    #     'ザ': 'サ', 'ジ': 'シ', 'ズ': 'ス', 'ゼ': 'セ', 'ゾ': 'ソ',
    #     'ダ': 'タ', 'ヂ': 'チ', 'ヅ': 'ツ', 'デ': 'テ', 'ド': 'ト',
    #     'バ': 'ハ', 'ビ': 'ヒ', 'ブ': 'フ', 'ベ': 'ヘ', 'ボ': 'ホ',
    #     'パ': 'ハ', 'ピ': 'ヒ', 'プ': 'フ', 'ペ': 'ヘ', 'ポ': 'ホ',
    #     'ヴ': 'ウ'
    # }
    # char = dakuten_map.get(char, char)

    return char

def get_last_char(name: str) -> str:
    """しりとりで使う最後の文字を取得"""
    last = name[-1]

    # 伸ばし棒の場合は一つ前の文字
    if last == 'ー' or last == '♀' or last == '♂':
        # 一つ前の文字を取得
        if len(name) >= 2:
            last = name[-2]

    # 正規化して返す
    return normalize_char(last)

def get_first_char(name: str) -> str:
    """しりとりで使う最初の文字を取得"""
    return normalize_char(name[0])

def build_graph(names: List[str]) -> Dict[str, List[Tuple[int, str]]]:
    """しりとりグラフを構築（文字 -> [(インデックス, テキスト), ...]）"""
    graph = {}

    for idx, name in enumerate(names):
        first_char = get_first_char(name)
        if first_char not in graph:
            graph[first_char] = []
        graph[first_char].append((idx, name))

    return graph

def classify(names: List[str]) -> Dict[str, List[str]]:
    """前後につながるかどうかで分類する"""
    first_chars = {get_first_char(name) for name in names}
    last_chars = {get_last_char(name) for name in names}

    result = {
        '前にも後ろにもつながらない': [],
        '最初にしか置けない': [],
        '最後にしか置けない': [],
        '途中に置ける': [],
    }

    for name in names:
        has_prev = get_first_char(name) in last_chars
        has_next = get_last_char(name) in first_chars

        if not has_prev and not has_next:
            result['前にも後ろにもつながらない'].append(name)
        elif not has_prev:
            result['最初にしか置けない'].append(name)
        elif not has_next:
            result['最後にしか置けない'].append(name)
        else:
            result['途中に置ける'].append(name)

    return result

def find_longest_path(names: List[str]) -> List[str]:
    """最長のしりとり経路を見つける"""
    if not names:
        return []

    # つながらないテキストを探索の対象から外す
    groups = classify(names)
    middle = groups['途中に置ける']

    # 最初にしか置けないテキストは先頭に、最後にしか置けないテキストは末尾に1つだけ付ける
    head_by_last_char = {}
    for name in groups['最初にしか置けない']:
        head_by_last_char.setdefault(get_last_char(name), name)

    tail_by_first_char = {}
    for name in groups['最後にしか置けない']:
        tail_by_first_char.setdefault(get_first_char(name), name)

    graph = build_graph(middle)
    n = len(middle)

    # 途中に置けるテキストを使わない並び
    max_path = [names[0]]
    for name in groups['最初にしか置けない']:
        tail = tail_by_first_char.get(get_last_char(name))
        if tail is not None:
            max_path = [name, tail]
            break

    def upper_bound(start_char: str, used: Set[int]) -> int:
        """この先つなげられるテキスト数の上限を見積もる"""
        # 今の文字からたどり着ける未使用のテキストを集める
        out_count = {}
        in_count = {}
        visited = {start_char}
        stack = [start_char]
        while stack:
            char = stack.pop()
            for idx, name in graph.get(char, []):
                if idx in used:
                    continue
                out_count[char] = out_count.get(char, 0) + 1
                last_char = get_last_char(name)
                in_count[last_char] = in_count.get(last_char, 0) + 1
                if last_char not in visited:
                    visited.add(last_char)
                    stack.append(last_char)

        # しりとりでは、文字ごとに「出ていく数」は「入ってくる数」を超えられない（出発する文字だけは1つ多くてよい）
        bound = 0
        for char, out in out_count.items():
            bound += min(out, in_count.get(char, 0) + (1 if char == start_char else 0))
        return bound

    def dfs(current_text: str, used: Set[int], path: List[str], head: str):
        nonlocal max_path

        # 先頭と末尾を付けた長さの方が長ければ更新
        tail = tail_by_first_char.get(get_last_char(current_text))
        length = len(path) + (head is not None) + (tail is not None)
        if length > len(max_path):
            max_path = ([head] if head is not None else []) + path + ([tail] if tail is not None else [])

        # 次に続けられるテキストを探す
        last_char = get_last_char(current_text)

        if last_char not in graph:
            return

        # 枝刈り：この先どれだけつなげても最長を超えられないなら戻る
        limit = len(path) + (head is not None) + upper_bound(last_char, used) + (1 if tail_by_first_char else 0)
        if limit <= len(max_path):
            return

        for idx, next_name in graph[last_char]:
            if idx not in used:
                used.add(idx)
                path.append(next_name)
                dfs(next_name, used, path, head)
                path.pop()
                used.remove(idx)

    # 探索を開始
    for start_idx, start_name in enumerate(middle):
        print(f"探索中: {start_idx + 1}/{n} ({start_name})...")
        head = head_by_last_char.get(get_first_char(start_name))
        used = {start_idx}
        path = [start_name]
        dfs(start_name, used, path, head)

    return max_path

def main():
    # 引数で匹数を指定する（省略したときは全部）
    parser = argparse.ArgumentParser(description="深さ優先探索で最長のしりとりを探す")
    parser.add_argument("count", nargs="?", type=int, default=len(text_list),
                        help=f"先頭から何匹を対象にするか（1〜{len(text_list)}、省略時は{len(text_list)}）")
    args = parser.parse_args()
    if not 1 <= args.count <= len(text_list):
        parser.error(f"匹数は1〜{len(text_list)}で指定してください")
    names = text_list[:args.count]

    print("=" * 60)

    print("最長経路を探索中...")
    print("-" * 60)

    # 探索処理の時間計測
    search_start_time = time.time()
    longest_path = find_longest_path(names)
    search_end_time = time.time()
    search_duration = search_end_time - search_start_time

    print()
    print("=" * 60)
    print("結果")
    print("=" * 60)
    print(f"対象: {len(names)}匹（{names[0]}〜{names[-1]}）")
    print(f"最長のしりとり: {len(longest_path)}匹")
    print()

    print("しりとりの順番:")
    for i, name in enumerate(longest_path, 1):
        last_char = get_last_char(name) if i < len(longest_path) else ""
        next_info = f" → {last_char}" if i < len(longest_path) else ""
        print(f"{i:3d}. {name}{next_info}")

    print()
    print("=" * 60)
    print(f"探索時間: {search_duration:.2f}秒")
    print("=" * 60)
    



if __name__ == "__main__":
    main()