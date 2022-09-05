b = 2
a = 3.141592
c = a + b


def inline_inside_me():
    def in_here_too(d: float) -> float:
        return a + b + c + d

    print(a + in_here_too(a))


def and_in_me():
    p = 4 + a
    return p + a
