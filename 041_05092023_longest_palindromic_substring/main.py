
def longestPalindrome(s):
    """
    :type s: str
    :rtype: str
    """
    if len(s) < 2:
        return s

    def expand_around_center(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]

    longest = ""
    for i in range(len(s)):
        # Trường hợp chuỗi palindrome có độ dài là số lẻ
        palindrome1 = expand_around_center(i, i)
        if len(palindrome1) > len(longest):
            longest = palindrome1

        # Trường hợp chuỗi palindrome có độ dài là số chẵn
        palindrome2 = expand_around_center(i, i + 1)
        if len(palindrome2) > len(longest):
            longest = palindrome2

    return longest


# s ="jaliztdispcppzgzjxnjxwbhhtbjrijyibqwrhwuscmokylygielwssuyretqnoiglvsltmhetvdoliwibrnwmdtauczcswuqxxokaykslfzgxovphdptgtrbbozdkdgawcegemkumgbyqzjrzurkdaibfwwvcxfcstvixisrcfxvnlzizlbnacxssetlsxrvcaqvzmbnzdfmtskmxmjblzgpdsjvhqhrihiajvwxbmjsncjhmilercbdbzyncrnlyrxrefaeuttkscfttqnedzvqisclbremuxmngrpgqjqkijpizkixkrgaarpknivrrirbkeddkulvlfuetbdnugzodbfufqhrpkyufhrhnnnzsenkvqsuhlbaimniusuxsnmavqbilzgsfxjykrxdkkpnneikwlucdghnikojythrpgwyzoqgraycavrivsbfuaonssmryhcykooivrxmeeowllsfeyxrznvkdpobohpzolnpbxjjxbpnlozphobopdkvnzrxyefsllwoeemxrviookychyrmssnoaufbsvirvacyargqozywgprhtyjokinhgdculwkiennpkkdxrkyjxfsgzlibqvamnsxusuinmiablhusqvknesznnnhrhfuykprhqfufbdozgundbteuflvlukddekbrirrvinkpraagrkxikzipjikqjqgprgnmxumerblcsiqvzdenqttfcskttueaferxrylnrcnyzbdbcrelimhjcnsjmbxwvjaihirhqhvjsdpgzlbjmxmkstmfdznbmzvqacvrxsltessxcanblzizlnvxfcrsixivtscfxcvwwfbiadkruzrjzqybgmukmegecwagdkdzobbrtgtpdhpvoxgzflskyakoxxquwsczcuatdmwnrbiwilodvtehmtlsvlgionqteryusswleigylykomcsuwhrwqbiyjirjbthhbwxjnxjzgzppcpsidtzilaj"
s = 'aact'
print(longestPalindrome(s))
