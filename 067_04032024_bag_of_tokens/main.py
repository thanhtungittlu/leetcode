# def bagOfTokensScore(tokens: list, power: int) -> int:
#     score = 0
#     tokens.sort()
#     while len(tokens) > 1:
#         list_pop = []
#         for i in range(len(tokens)):
#             if power >= tokens[i]:
#                 power -= tokens[i]
#                 list_pop.append(i)
#                 score += 1
#         tokens = [value for index, value in enumerate(tokens) if index not in list_pop]
#         if len(tokens) <= 1:
#             break
#         if score == 0: #Dùng power để mua
#             if power < tokens[0]:
#                 break
#             else:
#                 power -= tokens[0]
#                 tokens.pop(0)
#                 score += 1
#         power += tokens[-1]
#         tokens.pop(-1)
#         score -= 1
    
#     if len(tokens) == 0:
#         return score
#     if len(tokens) == 1:
#         return score if tokens[0] > power else score + 1
#     return score
    
def bagOfTokensScore(tokens: list, power: int) -> int:
    tokens.sort()
    score = 0
    i, j = 0, len(tokens) - 1
    while i <= j:
        if power >= tokens[i]:
            power -= tokens[i]
            score += 1
            i += 1
        elif score and j > i + 1:
            power += tokens[j]
            score -= 1
            j -= 1
        else:
            break
    return score

tokens = [100,200,300,5,500,150,400]
power = 50
print(bagOfTokensScore(tokens,power))



