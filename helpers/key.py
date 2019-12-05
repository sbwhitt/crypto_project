def __parse_hex(key_raw):
    l = len(key_raw)
    for i in range(l):
        h = str(hex(i))
        if h[len(h)-1:] not in key_raw:
            print("Error - Invalid Key")
            return
    return "hex"

def __parse_alph(key_raw):
    return "alph"

def parse(key_str):
    try:
        key_hex = int(key_str, 16)
        return __parse_hex(key_str)
    except ValueError:
        return __parse_alph(key_str)
