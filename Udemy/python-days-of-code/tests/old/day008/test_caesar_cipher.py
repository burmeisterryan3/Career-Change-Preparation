from caesar_cipher import caesar


def test_caeser():
    assert caesar("hello", 5, "encode") == "mjqqt"
    assert caesar("Hello World!", 9, "encode") == "qnuux gxbum!"
    assert caesar("mjqqt", 5, "decode") == "hello"
    assert caesar("qnuux gxbum!", 9, "decode") == "hello world!"
