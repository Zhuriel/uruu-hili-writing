import cairo
import math


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
        return cons_length(self.onset) + cons_length(self.coda) + 8

    def draw(self, ctx: cairo.Context):
        if self.nucleus == "":
            return
        print(f"drawing {self}")
        draw_cons(self.onset, ctx)
        ctx.translate(0, cons_length(self.onset))
        draw_vowel(self.nucleus, ctx)
        ctx.translate(0, 8)
        draw_cons(self.coda, ctx)
        ctx.translate(0, -cons_length(self.onset) - 8)


def cons_length(ch: str) -> int:
    match ch:
        case "": return 0
        case "r": return 2
        case "d" | "g": return 4
        case "b" | "ñ": return 6
        case _: return 5


def draw_cons(cons: str, ctx: cairo.Context):
    match cons:
        case "p":
            ctx.move_to(0, 0)
            ctx.line_to(8, 0)
            ctx.line_to(5, 3)
            ctx.stroke()
        case "t":
            ctx.move_to(0, 3)
            ctx.line_to(8, 3)
            ctx.line_to(5, 0)
            ctx.stroke()
        case "k":
            ctx.move_to(8, 3)
            ctx.line_to(0, 3)
            ctx.line_to(3, 0)
            ctx.stroke()
        case "q":
            ctx.move_to(8, 0)
            ctx.line_to(0, 0)
            ctx.line_to(3, 3)
            ctx.stroke()
        case "b":
            ctx.move_to(0, 2)
            ctx.line_to(8, 2)
            ctx.stroke()
            ctx.move_to(5, 0)
            ctx.line_to(5, 4)
            ctx.stroke()
        case "d":
            ctx.move_to(0, 2)
            ctx.line_to(8, 2)
            ctx.move_to(5, 2)
            ctx.line_to(5, 0)
            ctx.stroke()
        case "g":
            ctx.move_to(0, 0)
            ctx.line_to(8, 0)
            ctx.line_to(8, 2)
            ctx.line_to(5, 2)
            ctx.line_to(5, 0)
            ctx.stroke()
        case "n":
            ctx.move_to(0, 0)
            ctx.line_to(8, 0)
            ctx.line_to(8, 3)
            ctx.line_to(6, 3)
            ctx.stroke()
        case "m":
            ctx.move_to(0, 0)
            ctx.line_to(8, 0)
            ctx.line_to(8, 3)
            ctx.stroke()
        case "r":
            ctx.move_to(0, 0)
            ctx.line_to(8, 0)
            ctx.stroke()
        case "ñ":
            ctx.move_to(0, 2)
            ctx.line_to(4, 2)
            ctx.move_to(8, 0)
            ctx.line_to(4, 2)
            ctx.line_to(8, 4)


def draw_vowel(vow: str, ctx: cairo.Context):
    u_angle = 0.25
    a1 = 1 + u_angle
    a2 = 1 - u_angle
    match vow:
        case "u":
            startx = 5 + (3 * math.cos(a1 * math.pi))
            starty = 3 + (3 * math.sin(a1 * math.pi))
            ctx.move_to(startx, starty)
            ctx.arc(5, 3, 3, a1 * math.pi, a2 * math.pi)
            ctx.move_to(8, 0)
            ctx.line_to(8, 6)
            ctx.stroke()
        case "uu":
            startx = 5 + (3 * math.cos(a1 * math.pi))
            starty = 3 + (3 * math.sin(a1 * math.pi))
            ctx.move_to(startx, starty)
            ctx.arc(5, 3, 3, a1 * math.pi, a2 * math.pi)
            ctx.stroke()
        case "oo":
            ctx.move_to(8, 0)
            ctx.line_to(2, 0)
            ctx.line_to(2, 6)
            ctx.line_to(5, 0.5)
            ctx.stroke()
        case "o":
            ctx.move_to(8, 6)
            ctx.line_to(8, 0)
            ctx.line_to(2, 0)
            ctx.line_to(2, 6)
            ctx.line_to(5, 0.5)
            ctx.stroke()
        case "ee":
            ctx.move_to(8, 0)
            ctx.line_to(2, 3)
            ctx.line_to(8, 6)
            ctx.stroke()
        case "e":
            ctx.move_to(8, 0)
            ctx.line_to(2, 3)
            ctx.line_to(8, 6)
            ctx.close_path()
            ctx.stroke()
        case "aa":
            ctx.move_to(2, 0)
            ctx.line_to(8, 3)
            ctx.line_to(2, 6)
            ctx.stroke()
        case "a":
            ctx.move_to(2, 0)
            ctx.line_to(8, 3)
            ctx.line_to(2, 6)
            ctx.move_to(8, 0)
            ctx.line_to(8, 6)
            ctx.stroke()


def parse_syl(in_str: str) -> (UruuSyl, str):
    initial = ""
    coda = ""
    if in_str == "":
        return (UruuSyl("", "", ""), "")
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
    # explicitly separated case
    if (len(work_str) >= 2 and
            work_str[0] in uruu_consonants and
            work_str[1] == "'"):

        coda = work_str[0]
        work_str = work_str[2:]
    return (UruuSyl(initial, nucleus, coda), work_str)
