hili_vowels = "ieay"
hili_diph = ["ai", "ia", "ei", "ie", "yi"]
hili_consonants = "tknrshjl"


class HiliSyl:
    def __init__(self, ons: str, nuc: str, coda: str):
        self.onset = ons
        self.nucleus = nuc
        self.coda = coda

    def __repr__(self) -> str:
        return f"{self.onset} {self.nucleus} {self.coda}"

    def length(self) -> int:
        ret = 8
        if len(onset) == 2:
            ret += 4
        if len(coda) == 1:
            ret += 4


def parse_syl(in_str: str) -> (HiliSyl, str):
    if in_str == "":
        return ("", "")
    work_str = in_str

    onset = ""
    nucleus = ""
    coda = ""
    # initial consonants
    for _ in range(2):
        if (work_str[0] in hili_consonants):
            onset += work_str[0]
            work_str = work_str[1:]
    # vowels
    if (work_str[0] not in hili_vowels):
        print(f"invalid syllable in {in_str} (no vowel)")
        exit(1)
    if (len(work_str) >= 2 and work_str[0:2] in hili_diph):
        nucleus = work_str[0:2]
        work_str = work_str[2:]
    else:
        nucleus = work_str[0]
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

        coda = work_str[0]
        work_str = work_str[1:] 
    #explicitly separated case
    if (len(work_str) >= 2 and 
        work_str[0] in hili_consonants and
        work_str[1] == "'"):

        coda = work_str[0]
        work_str = work_str[2:] 
    return (HiliSyl(onset, nucleus, coda), work_str)


