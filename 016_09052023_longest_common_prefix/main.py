def longestCommonPrefix(strs):
    """
    :type strs: List[str]
    :rtype: str
    """
    if not strs:
        return ""
    prefix = strs[0]
    for ele in strs[1:]:
        while prefix != ele[0:len(prefix)]:
            prefix = prefix[:-1]  # Bỏ đi 1 đơn vị
            if not prefix:
                return ""
    return prefix


print(longestCommonPrefix(["flower", "flow", "flight"]))
