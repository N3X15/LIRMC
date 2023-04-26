import argparse
import random
from typing import Dict, List, Tuple

from lirpy.mask import Mask
from lirpy.point import Point, dist_points
from lirpy.rect import Rect
from lirpy.rectangulator import Rectangulator

dirchoices = []
for axis in "XYZ":
    for plusmin in "+-":
        dirchoices.append(f"{plusmin}{axis}")


def main() -> None:
    argp = argparse.ArgumentParser()
    argp.add_argument("--x", type=int)
    argp.add_argument("--y", type=int)
    argp.add_argument("--z", type=int)
    argp.add_argument("--dump-steps", action="store_true", default=False)
    argp.add_argument("--axis", choices=dirchoices, default="-Y")
    argp.add_argument("--depth", "-d", type=int, default=1)
    argp.add_argument("--output-type", choices=["baritone", "pil"], default="pil")
    argp.add_argument("--output-file", metavar="out.png", default=None)

    subp = argp.add_subparsers()
    register_cmd_circle(subp)

    args = argp.parse_args()
    if not hasattr(args, "cmd"):
        argp.print_usage()
        return
    args.cmd(args)


def register_cmd_circle(subp: argparse._SubParsersAction) -> None:
    p = subp.add_parser("circle")
    p.add_argument("--outer-radius", "-r", type=int)
    p.add_argument("--inner-radius", "-i", type=int, default=0)
    p.set_defaults(cmd=cmd_circle)


def cmd_circle(args: argparse.Namespace) -> None:
    x: int = args.x
    y: int = args.y
    z: int = args.z
    o_r: int = args.outer_radius
    i_r: int = args.inner_radius
    d: int = args.depth - 1
    assert d >= 0
    c = Point(x=o_r, y=o_r)
    print(f"Center: {x} {y} {z}")
    print(f"Outer Radius: {o_r}")
    print(f"Inner Radius: {i_r}")
    print(f"Depth: {d}")
    print(f"Along axis: {args.axis}")
    m = Mask(height=o_r * 2 + 1, width=o_r * 2 + 1)

    def setmasktocircle(x: int, y: int, v: bool) -> bool:
        p = Point(x, y)
        _d = dist_points(p, c)
        return _d <= o_r and _d >= i_r

    m.setif(setmasktocircle)
    do_rectangulate(
        x,
        y,
        z,
        d,
        m,
        xo=-o_r,
        yo=-o_r,
        args=args,
    )


def register_cmd_ellipse(subp: argparse._SubParsersAction) -> None:
    p = subp.add_parser("ellipse")
    p.add_argument("-a", type=int, help="semi-axis a length")
    p.add_argument("-b", type=int, help="semi-axis b length")
    p.set_defaults(cmd=cmd_ellipse)


def cmd_ellipse(args: argparse.Namespace) -> None:
    x: int = args.x
    y: int = args.y
    z: int = args.z
    a: int = args.a
    b: int = args.b
    d: int = args.depth - 1
    assert d >= 0
    c = Point(x=a / 2, y=b / 2)
    print(f"Center: {x} {y} {z}")
    print(f"Semi-Axes:")
    print(f"  a: {a}")
    print(f"  b: {b}")
    print(f"Depth: {d}")
    print(f"Along axis: {args.axis}")
    m = Mask(height=b, width=a)

    def setmasktoellipse(x: int, y: int, v: bool) -> bool:
        return ((x - c.x) / a) ** 2 + ((y - c.y) / b) <= 1

    m.setif(setmasktoellipse)
    do_rectangulate(
        x,
        y,
        z,
        d,
        m,
        xo=-(a / 2),
        yo=-(b / 2),
        args=args,
    )


def do_rectangulate(
    x: int, y: int, z: int, d: int, m: Mask, xo: int, yo: int, args: argparse.Namespace
) -> None:
    dump_steps: bool = args.dump_steps
    rt = Rectangulator(m)
    rect: Rect
    written = set()
    cuboids: List[Tuple[Tuple[int, int, int], Tuple[int, int, int]]] = []
    allrects = []
    for rect in rt.findAll(verbose=dump_steps):
        allrects.append(rect)
        minx = rect.min.x
        miny = rect.min.y
        maxx = rect.max.x
        maxy = rect.max.y
        k = (minx, miny, maxx, maxy)
        if k in written:
            continue
        written.add(k)
        p1 = (0, 0, 0)
        p2 = (0, 0, 0)
        match args.axis:
            case "+X":
                p1 = (x, minx + xo + y, miny + yo + z)
                p2 = (x + d, maxx + xo + y, maxy + yo + z)
            case "-X":
                p1 = (x, minx + xo + y, miny + yo + z)
                p2 = (x - d, maxx + xo + y, maxy + yo + z)
            case "+Y":
                p1 = (minx + xo + x, y, miny + yo + z)
                p2 = (maxx + xo + x, y + d, maxy + yo + z)
            case "-Y":
                p1 = (minx + xo + x, y, miny + yo + z)
                p2 = (maxx + xo + x, y - d, maxy + yo + z)
            case "+Z":
                p1 = (minx + xo + x, miny + yo + y, z)
                p2 = (maxx + xo + x, maxy + yo + y, z + d)
            case "-Z":
                p1 = (minx + xo + x, miny + yo + y, z)
                p2 = (maxx + xo + x, maxy + yo + y, z - d)
        cuboids.append((p1, p2))
    match args.output_type:
        case "baritone":
            print("#sel clear")
            for p1, p2 in cuboids:
                p1 = " ".join(list(map(str, p1)))
                p2 = " ".join(list(map(str, p2)))
                print(f"#sel 1 {p1}")
                print(f"#sel 2 {p2}")
        case "pil":
            from PIL import Image

            img = Image.new(mode="HSV", size=(m.width, m.height))
            pixels = img.load()
            colors = [
                round((float(i) / float(len(allrects))) * 255.0)
                for i in range(len(allrects))
            ]
            random.shuffle(colors)
            rects: Dict[Rect, int] = {k: colors.pop(0) for k in allrects}
            for x in range(m.width):
                for y in range(m.height):
                    for r, h in rects.items():
                        if r.isPointIn(x, y):
                            pixels[x, y] = (h, 255, 255)

            img = img.convert("RGB")
            img.save(args.output_file, format="PNG", bitmap_format="PNG", optimize=True)


if __name__ == "__main__":
    main()
