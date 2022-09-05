b = 2
c = 3.141592 + b


def inline_inside_me():
    def in_here_too(d: float) -> float:
        return 3.141592 + b + c + d

    print(3.141592 + in_here_too(3.141592))


def and_in_me():
    p = 4 + 3.141592
    return p + 3.141592
