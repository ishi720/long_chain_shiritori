from main import text_list, get_first_char, get_last_char, classify


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
