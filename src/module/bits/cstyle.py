def cstyle_arr32(l: list, _hex: bool = True):
    result = "unsigned int v[] = {"
    for i, v in enumerate(l):
        v &= 0xffffffff
        s = str(hex(v) if _hex else v)
        result += s
        if i != len(l) - 1:
            result += ", "
            if i % 8 == 7:
                result += '\n                    '
    result += "};"
    return result