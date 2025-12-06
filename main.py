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
    # 'ブーバー', 'カイロス', 'ケンタロス', 'コイキング', 'ギャラドス',
    # 'ラプラス', 'メタモン', 'イーブイ', 'シャワーズ', 'サンダース',
    # 'ブースター', 'ポリゴン', 'オムナイト', 'オムスター', 'カブト',
    # 'カブトプス', 'プテラ', 'カビゴン', 'フリーザー', 'サンダー', 'ファイヤー',
    # 'ミニリュウ', 'ハクリュー', 'カイリュー', 'ミュウツー', 'ミュウ'
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

def find_longest_path(names: List[str]) -> List[str]:
    """最長のしりとり経路を見つける"""
    graph = build_graph(names)
    n = len(names)

    max_path = []

    def dfs(current_text: str, used: Set[int], path: List[str]):
        nonlocal max_path

        # 現在のパスの方が長ければ更新
        if len(path) > len(max_path):
            max_path = path.copy()

        # 次に続けられるテキストを探す
        last_char = get_last_char(current_text)

        if last_char not in graph:
            return

        for idx, next_name in graph[last_char]:
            if idx not in used:
                used.add(idx)
                path.append(next_name)
                dfs(next_name, used, path)
                path.pop()
                used.remove(idx)

    # 探索を開始
    for start_idx, start_name in enumerate(names):
        print(f"探索中: {start_idx + 1}/{n} ({start_name})...")
        used = {start_idx}
        path = [start_name]
        dfs(start_name, used, path)

    return max_path

def main():
    print("=" * 60)

    print("最長経路を探索中...")
    print("-" * 60)

    # 探索処理の時間計測
    search_start_time = time.time()
    longest_path = find_longest_path(text_list)
    search_end_time = time.time()
    search_duration = search_end_time - search_start_time

    print()
    print("=" * 60)
    print("結果")
    print("=" * 60)
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