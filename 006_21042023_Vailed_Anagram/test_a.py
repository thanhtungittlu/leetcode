from main import isAnagram


def test_1():
    assert isAnagram("rat", "car") == False


def test_2():
    assert isAnagram("anagbram", "nagaramb") == True


def test_3():
    assert isAnagram("anagram", "nagaram") == True


def test_4():
    assert isAnagram("ganagram", "vnagaram") == False
