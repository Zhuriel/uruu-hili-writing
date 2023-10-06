import cairo
import re
import argh

import uruu
import hili


unitsize_default = 100


def parse_word(in_str: str) -> list((uruu.UruuSyl, hili.HiliSyl)):
    ret = []
    if "-" in in_str:
        (uruu_str, hili_str) = in_str.split("-")
        while (len(uruu_str) > 0 or len(hili_str) > 0):
            (usyl, uruu_str) = uruu.parse_syl(uruu_str)
            (hsyl, hili_str) = hili.parse_syl(hili_str)
            ret.append((usyl, hsyl))
    else:
        return ("", "")
    return ret


def parse_line(in_str: str) -> list(list((uruu.UruuSyl, hili.HiliSyl))):
    words = in_str.split(" ")
    return list(map(parse_word, words))


def parse_str(in_str: str) -> list(list(list((uruu.UruuSyl, hili.HiliSyl)))):
    lines = in_str.split("\\")
    return list(map(parse_line, lines))


def draw_str(lines: list(list(list((uruu.UruuSyl, hili.HiliSyl))))):
    pass


if __name__ == "__main__":
    print(parse_str("uruu-hili"))
    print(parse_str("ontuuqa-arkjes'ti"))
    print(parse_str("boor-yit eeñraat-sken'hy"))