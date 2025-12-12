from hangman import update_status

def test_update_status():
    test_list = ["_"]*5
    updates, new_test_list = update_status("camel", test_list, "d")
    assert updates == 0
    assert new_test_list == test_list

    test_list = ["_"]*6
    updates, new_test_list = update_status("baboon", test_list, "b")
    assert updates == 2
    assert new_test_list == ["b", "_", "b", "_", "_", "_"]