def add(b: int, c: int) -> int:
    return b + c


def example() -> int:
    inline_me = add(1, 2) + add(3, 4)
    return inline_me + 4
