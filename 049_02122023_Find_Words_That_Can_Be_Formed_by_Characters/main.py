def countCharacters(words, chars):
    def _build_dict_chars(string):
        result = {}
        for s in string:
            if s in result:
                result[s] += 1
            else:
                result[s] = 1
        return result
    dict_chars = _build_dict_chars(chars)
    result = 0
    for word in words:
        dict_word = _build_dict_chars(word)
        is_valid_word = True
        for key, value in dict_word.items():
            if key not in dict_chars:
                is_valid_word = False
                break
            else:
                if value > dict_chars[key]:
                    is_valid_word = False
                    break
        if is_valid_word:
            result += len(word)
    
    return result

def countCharacters_2(words, chars):
    sum_word_valid = []
    for word in words:
        for char in word:
            if word.count(char) > chars.count(char):
                break
        else:
            sum_word_valid.append(len(word))
    return sum(sum_word_valid)

words = ["hello","world","leetcode"] 
chars = "welldonehoneyr"
print(countCharacters_2(words, chars))