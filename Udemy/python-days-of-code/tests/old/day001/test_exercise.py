import day001.src.exercise as e

def test_concat():
    assert e.concat(4, "test") == "4test"


def test_print_n():
    assert e.print_n("Hello", 3) == "HelloHelloHello"

def test_swap():
    assert e.swap(4, "the") == ("the", 4)
    assert e.swap(None, (1, 2, 3)) == ((1, 2, 3), None)