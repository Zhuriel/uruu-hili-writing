import cairo
import math


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
        if len(self.onset) == 2:
            ret += 4
        if len(self.coda) == 1:
            ret += 4
        return ret

    def draw(self, ctx: cairo.Context):
        if self.nucleus == "":
            return
        print(f"drawing {self}")

        if len(self.onset) == 2:
            ctx.translate(0, 4)
            draw_cons(self.onset[0], ctx, False)
            draw_core(self.onset[1], ctx)
        else:
            draw_core(self.onset, ctx)
        draw_vowel(self.nucleus, ctx)
        ctx.translate(0, 6)
        draw_cons(self.coda, ctx, True)
        ctx.translate(0, -6)
        if len(self.onset) == 2:
            ctx.translate(0, -4)


def draw_core(cons: str, ctx: cairo.Context):
    match cons:
        case "":
            ctx.move_to(-8, 3)
            ctx.line_to(-2, 3)
            ctx.stroke()
        case "t":
            ctx.move_to(-5, 6)
            ctx.arc_negative(-5, 3, 3, 0.5 * math.pi, math.pi)
            ctx.stroke()
        case "k":
            ctx.move_to(-8, 3)
            ctx.line_to(-5, 0)
            ctx.line_to(-2, 3)
            ctx.line_to(-5, 6)
            ctx.close_path()
            ctx.stroke()
        case "n":
            ctx.move_to(-2, 3)
            ctx.line_to(-8, 3)
            ctx.line_to(-5, 0)
            ctx.line_to(-5, 5.8)
            ctx.stroke
        case "r":
            ctx.move_to(-5, 0.2)
            ctx.line_to(-5, 5.8)
            ctx.move_to(-3, 2)
            ctx.line_to(-3, 4)
            ctx.move_to(-7, 2)
            ctx.line_to(-7, 4)
            ctx.stroke()
        case "s":
            ctx.move_to(-5, 3)
            ctx.arc(-5, 1.5, 1.5, 0.5 * math.pi, 2.5 * math.pi)
            ctx.arc(-5, 4.5, 1.5, -0.5 * math.pi, 1.5 * math.pi)
        case "h":
            ctx.move_to(-7.8, 2.8)
            ctx.line_to(-5.2, 0.2)
            ctx.move_to(-6.5, 4.5)
            ctx.line_to(-3.5, 1.5)
            ctx.move_to(-4.8, 5.8)
            ctx.line_to(-2.2, 3.2)
            ctx.stroke()
        case "j":
            ctx.move_to(-5, 0.2)
            ctx.line_to(-5, 5.8)
            ctx.move_to(-3.5, 3)
            ctx.stroke()
            ctx.set_line_cap(cairo.LineCap.ROUND)
            ctx.arc(-5, 3, 1.5, 0, 2*math.pi)
            ctx.stroke()
            ctx.set_line_cap(cairo.LineCap.SQUARE)
        case "l":
            ctx.move_to(-5, 0)
            ctx.line_to(-5, 6)
            ctx.stroke()


def draw_vowel(vow: str, ctx: cairo.Context):
    match vow:
        case "i":
            pass
        case "a":
            ctx.move_to(-10, 0)
            ctx.line_to(-11, 3)
            ctx.line_to(-10, 6)
            ctx.stroke()
        case "ia":
            ctx.move_to(-11.5, 0)
            ctx.line_to(-10, 0)
            ctx.line_to(-11, 3)
            ctx.line_to(-10, 6)
            ctx.stroke()
        case "ai":
            ctx.move_to(-10, 0)
            ctx.line_to(-11, 3)
            ctx.line_to(-10, 6)
            ctx.line_to(-11.5, 6)
            ctx.stroke()
        case "e":
            ctx.move_to(-10, 0)
            ctx.line_to(-10, 6)
            ctx.stroke()
        case "ie":
            ctx.move_to(-11.5, 0)
            ctx.line_to(-10, 0)
            ctx.line_to(-10, 6)
            ctx.stroke()
        case "ei":
            ctx.move_to(-10, 0)
            ctx.line_to(-10, 6)
            ctx.line_to(-11.5, 6)
            ctx.stroke()
        case "y":
            ctx.move_to(-10, 0)
            ctx.line_to(-10, 1)
            ctx.move_to(-10, 5)
            ctx.line_to(-10, 6)
            ctx.stroke()
        case "yi":
            ctx.move_to(-10, 0)
            ctx.line_to(-10, 1.5)
            ctx.move_to(-10, 4.5)
            ctx.line_to(-10, 6)
            ctx.line_to(-11.5, 6)
            ctx.stroke()


def draw_cons(cons: str, ctx: cairo.Context, bottom: bool):
    ctx.translate(-5, 0)
    sign = (-1) if bottom else 1
    match cons:
        case "t":
            ctx.move_to(0, sign * -0.2)
            ctx.arc(0, 0, 3, -sign * 0.5 * math.pi, math.pi if bottom else 0)
            ctx.stroke()
        case "k":
            ctx.move_to(0.2, sign * -0.2)
            ctx.line_to(3, sign * -3)
            ctx.line_to(-3, sign * -3)
            ctx.stroke()
        case "n":
            ctx.move_to(0, 0)
            ctx.line_to(sign * -2, 3)
            ctx.line_to(sign * 2, 3)
            ctx.close_path()
            ctx.stroke()
        case "r":
            ctx.move_to(-1, 0)
            ctx.line_to(1, 0)
            ctx.move_to(-3, sign * -3)
            ctx.line_to(3, sign * -3)
            ctx.stroke()
        case "s":
            ctx.move_to(0, 0)
            angle = sign * 0.5 * math.pi
            ctx.arc(0, -1.5 * sign, 1.5, angle, angle + 2*math.pi)
            ctx.stroke()
        case "h":
            ctx.move_to(sign * -0.2, sign * -0.2)
            ctx.line_to(sign * -3, sign * -3)
            ctx.move_to(sign * 1, sign * -3)
            ctx.line_to(sign * 3, sign * -1)
            ctx.stroke()
        case "l":
            ctx.move_to(-3, 0)
            ctx.line_to(3, 0)
            ctx.stroke()
    ctx.translate(5, 0)


def parse_syl(in_str: str) -> (HiliSyl, str):
    if in_str == "":
        return (HiliSyl("", "", ""), "")
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


