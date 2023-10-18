import cairo
import re
import argh
import os
import typing

import uruu
import hili


unitsize_default = 10


class UruuHiliWord:
    def __init__(self, in_str: str):
        self.empty = len(in_str) == 0
        if self.empty:
            return
        self.syllables = []
        self.punctuation = None
        if in_str[0] in ".,>!":
            self.punctuation = in_str[0]
            in_str = in_str[1:]
        if "-" in in_str:
            (uruu_str, hili_str) = in_str.split("-")
            while (len(uruu_str) > 0 or len(hili_str) > 0):
                (usyl, uruu_str) = uruu.parse_syl(uruu_str)
                (hsyl, hili_str) = hili.parse_syl(hili_str)
                self.syllables.append((usyl, hsyl))
        else:
            work_str = in_str
            while len(work_str) > 0:
                mode = work_str[0]
                work_str = work_str[1:]
                temp_str = ""
                while len(work_str) > 0 and work_str[0] not in "¹²":
                    temp_str += work_str[0]
                    work_str = work_str[1:]
                while len(temp_str) > 0:
                    if mode == "¹":
                        (usyl, temp_str) = uruu.parse_syl(temp_str)
                        self.syllables.append((usyl, hili.HiliSyl("", "", "")))
                    if mode == "²":
                        (hsyl, temp_str) = hili.parse_syl(temp_str)
                        self.syllables.append((uruu.UruuSyl("", "", ""), hsyl))

    def __repr__(self):
        if self.empty:
            return ""
        return " ".join([f"[{syl[0]}-{syl[1]}]" for syl in self.syllables])

    def length(self) -> int:
        if self.empty:
            return 0
        syl_lengths = [max(syl[0].length(), syl[1].length())
                       for syl in self.syllables]
        return sum(syl_lengths) + punctuation_len(self.punctuation) + 2

    def draw(self, ctx: cairo.Context):
        if self.empty:
            return
        match self.punctuation:
            case ".":
                ctx.move_to(-8, 0)
                ctx.line_to(8, 0)
                ctx.move_to(-8, 2)
                ctx.line_to(8, 2)
            case ",":
                ctx.move_to(-8, 0)
                ctx.line_to(8, 0)
            case ">":
                ctx.move_to(-2, 0)
                ctx.line_to(-2.5, 0)
                ctx.move_to(2, 0)
                ctx.line_to(2.5, 0)
            case "!":
                ctx.move_to(-8, 0)
                ctx.line_to(8, 0)
                ctx.line_to(8, 4)
                ctx.line_to(-8, 4)
                ctx.close_path()
                ctx.move_to(-5, 0.2)
                ctx.line_to(-3, 3.8)
                ctx.move_to(5, 0.2)
                ctx.line_to(3, 3.8)
            case None:
                ctx.move_to(-2.5, 0)
                ctx.line_to(2.5, 0)
        ctx.move_to(0, 0)
        ctx.line_to(0, self.length())
        ctx.stroke()
        ctx.translate(0, punctuation_len(self.punctuation))
        for syl in self.syllables:
            syl[0].draw(ctx)
            syl[1].draw(ctx)
            ctx.translate(0, max(syl[0].length(), syl[1].length()))
        ctx.translate(0, 2)


def punctuation_len(ch: str | None) -> int:
    match ch:
        case ".": return 4
        case "!": return 6
        case _: return 2


def parse_line(in_str: str) -> list[UruuHiliWord]:
    words = in_str.split(" ")
    return list(map(lambda s: UruuHiliWord(s), words))


def parse_str(in_str: str) -> list[list[UruuHiliWord]]:
    lines = in_str.split("\n")
    return list(map(parse_line, lines))


def get_line_len(line: list[UruuHiliWord]) -> int:
    return sum(map(lambda w: w.length(), line))


def get_size(text: list[list[UruuHiliWord]]) -> (int, int):
    return (len(text) * 25, max(map(get_line_len, text)))


def draw_line(ctx: cairo.Context, line: list[UruuHiliWord]):
    for word in line:
        word.draw(ctx)
    ctx.translate(0, -get_line_len(line))


def draw_str(
        string: str | None = None,
        infile: str | None = None,
        name: str | None = None,
        mode: str = "png",
        maxsize: int = 2000,
        colors: str = "w"):

    if name is None:
        if infile is None:
            name = "out"
        else:
            name = os.path.splitext(os.path.basename(infile))[0]

    if string is None and infile is None:
        print("either string or infile must be specified")
        exit(1)
    if string is None:
        with open(infile) as f:
            string = f.read()

    lines = parse_str(string)

    (size_x, size_y) = get_size(lines)

    print(f"computed size: {size_x}, {size_y}")

    unitsize = int(min(maxsize/size_x, maxsize/size_y, unitsize_default))

    match mode:
        case "png":
            surface: cairo.Surface = cairo.ImageSurface(
                cairo.FORMAT_ARGB32,
                int((size_x + 4) * unitsize),
                int((size_y + 4) * unitsize)
            )
        case "svg":
            surface: cairo.Surface = cairo.SVGSurface(
                f"{name}.svg",
                int((size_x + 4) * unitsize),
                int((size_y + 4) * unitsize)
            )
        case _:
            print("unsupported format")

    ctx = cairo.Context(surface)

    ctx.set_line_width(1)
    ctx.set_line_cap(cairo.LineCap.SQUARE)
    ctx.set_line_join(cairo.LineJoin.BEVEL)
    ctx.set_source_rgb(1.0, 1.0, 1.0)
    ctx.scale(unitsize, unitsize)
    ctx.translate(size_x - 8.5, 2)

    for line in lines:
        draw_line(ctx, line)
        ctx.translate(-25, 0)

    match mode:
        case "png":
            surface.write_to_png(f"{name}.png")


if __name__ == "__main__":
    argh.dispatch_command(draw_str)
