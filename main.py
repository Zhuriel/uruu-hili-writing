import cairo
import re
import argh


unitsize_default = 100

uruu_vowels = "uoea"
uruu_consonants = "ptkqbdgmnrñ"
hili_vowels = "ieay"
hili_diph = ["ai", "ia", "ei", "ie", "yi"]
hili_consonants = "tknrshjl"


def parse_uruu_syl(in_str: str) -> (str, str):
    if in_str == "":
        return ("", "")
    work_str = in_str
    out_str = ""
    # initial
    if (work_str[0] in uruu_consonants):
        out_str += work_str[0]
        work_str = work_str[1:]
    # vowel
    if (work_str[0] not in uruu_vowels):
        print(f"invalid syllable in {in_str}")
        exit(1)
    out_str += work_str[0]
    work_str = work_str[1:]
    # double vowel
    if (len(work_str) > 0 and work_str[0] == out_str[-1]):
        out_str += work_str[0]
        work_str = work_str[1:]
    # no vowel sequences
    if (len(work_str) > 0 and work_str[0] in uruu_vowels):
        print(f"invalid syllable in {in_str}")
        exit(1)
    # coda consonant
    if ((len(work_str) >= 2 and 
         work_str[0] in uruu_consonants and 
         work_str[1] in uruu_consonants) or
        (len(work_str) == 1 and work_str[0] in uruu_consonants)):

        out_str += work_str[0]
        work_str = work_str[1:]
    #explicitly separated case
    if (len(work_str) >= 2 and 
        work_str[0] in uruu_consonants and
        work_str[1] == "'"):

        out_str += work_str[0]
        work_str = work_str[2:] 
    return (out_str, work_str)

    

def parse_hili_syl(in_str: str) -> (str, str):
    if in_str == "":
        return ("", "")
    work_str = in_str
    out_str = ""
    # initial consonants
    for _ in range(2):
        if (work_str[0] in hili_consonants):
            out_str += work_str[0]
            work_str = work_str[1:]
    # vowels
    if (work_str[0] not in hili_vowels):
        print(f"invalid syllable in {in_str} (no vowel)")
        exit(1)
    if (len(work_str) >= 2 and work_str[0:2] in hili_diph):
        out_str += work_str[0:2]
        work_str = work_str[2:]
    else:
        out_str += work_str[0]
        work_str = work_str[1:]
    # no vowel sequences
    if (len(work_str) > 0 and work_str[0] in hili_vowels):
        print(f"invalid syllable in {in_str} (invalid vowel sequence)")
        exit(1)
    # coda consonant
    if ((len(work_str) >= 3 and 
         work_str[0] in hili_consonants and 
         work_str[1] in hili_consonants and
         work_str[2] in hili_consonants) or
        (len(work_str) == 1 and work_str[0] in hili_consonants)):

        out_str += work_str[0]
        work_str = work_str[1:] 
    #explicitly separated case
    if (len(work_str) >= 2 and 
        work_str[0] in hili_consonants and
        work_str[1] == "'"):

        out_str += work_str[0]
        work_str = work_str[2:] 
    return (out_str, work_str)



def parse_word(in_str: str) -> list((str, str)):
    ret = []
    if "-" in in_str:
        (uruu, hili) = in_str.split("-")
        while (len(uruu) > 0 or len(hili) > 0):
            (usyl, uruu) = parse_uruu_syl(uruu)
            (hsyl, hili) = parse_hili_syl(hili)
            ret.append((usyl, hsyl))
    else:
        return ("", "")
    return ret


def parse_str(in_str: str) -> list(list((str, str))):
    words = in_str.split(" ")
    return list(map(parse_word, words))


if __name__ == "__main__":
    print(parse_str("uruu-hili"))
    print(parse_str("ontuuqa-arkjesti"))
    print(parse_str("boor-yit eeñraat-sken'hy"))