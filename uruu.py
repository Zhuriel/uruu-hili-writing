
uruu_vowels = "uoea"
uruu_consonants = "ptkqbdgmnrñ"


class UruuSyl:
    def __init__(self, ons: str, nuc: str, coda: str):
        self.onset = ons
        self.nucleus = nuc
        self.coda = coda

    def __repr__(self) -> str:
        return f"{self.onset} {self.nucleus} {self.coda}"

    def length(self) -> int:
        return cons_length(onset) + cons_length(coda) + 8
        


def parse_syl(in_str: str) -> (UruuSyl, str):
    initial = ""
    coda = ""
    if in_str == "":
        return ("", "")
    work_str = in_str
    # initial
    if (work_str[0] in uruu_consonants):
        initial = work_str[0]
        work_str = work_str[1:]
    # vowel
    if (work_str[0] not in uruu_vowels):
        print(f"invalid syllable in {in_str}")
        exit(1)
    nucleus = work_str[0]
    work_str = work_str[1:]
    # double vowel
    if (len(work_str) > 0 and work_str[0] == nucleus[0]):
        nucleus += work_str[0]
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

        coda = work_str[0]
        work_str = work_str[1:]
    #explicitly separated case
    if (len(work_str) >= 2 and 
        work_str[0] in uruu_consonants and
        work_str[1] == "'"):

        coda = work_str[0]
        work_str = work_str[2:] 
    return (UruuSyl(initial, nucleus, coda), work_str)


def cons_length(ch: str) -> int:
    match ch:
        case "": return 0
        case "r": return 2
        case _: return 5