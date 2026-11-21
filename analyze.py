from typing import List, Dict

from main import text_list, get_first_char, get_last_char


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


def main():
    result = classify(text_list)

    print("=" * 60)
    print(f"対象: {len(text_list)}匹")
    print("=" * 60)

    for label, names in result.items():
        print(f"{label}: {len(names)}匹")
        print("  " + ", ".join(names))
        print()

    first_chars = {get_first_char(name) for name in text_list}
    no_next = [name for name in text_list if get_last_char(name) not in first_chars]
    end_with_n = [name for name in no_next if get_last_char(name) == 'ン']

    print("=" * 60)
    print(f"後ろにつながらない: {len(no_next)}匹（うち「ン」で終わる: {len(end_with_n)}匹）")
    print("=" * 60)


if __name__ == "__main__":
    main()
