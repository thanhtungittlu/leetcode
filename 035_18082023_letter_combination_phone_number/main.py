def letterCombinations(digits):
    """
    :type digits: str
    :rtype: List[str]
    """
    if not digits:
        return []

    phone_mapping = {
        '2': 'abc',
        '3': 'def',
        '4': 'ghi',
        '5': 'jkl',
        '6': 'mno',
        '7': 'pqrs',
        '8': 'tuv',
        '9': 'wxyz'
    }

    combinations = ['']

    for digit in digits:
        letters = phone_mapping[digit]
        new_combinations = []
        for combination in combinations:
            for letter in letters:
                new_combinations.append(combination + letter)
        combinations = new_combinations

    return combinations


print(letterCombinations("23"))