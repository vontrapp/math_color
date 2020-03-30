import argparse
import os
import pprint
import random

def color_by_problem(note, problems, rows, histogram):
    if len(histogram) > len(problems):
        raise RuntimeError("Too many colors in image for chosen problem buckets")

    p2 = list(reversed(sorted([(len(v), [k]) for k,v in problems.items()])))

    while len(p2) > len(histogram):
        px, py = p2[-2:]
        p2 = p2[:-2] + [(px[0]+py[0],px[1]+py[1])]
        p2.sort()
        p2.reverse()

    h2 = list(reversed(sorted([(v,k) for k,v in histogram.items()])))

    pmap = {}
    noterows = []
    for ((pc,pk),(hc,hk)) in zip(p2, h2):
        pp = []
        map(pp.extend, map(problems.get, pk))
        pmap[hk] = pp
        noterows.append([hk] + pk)

    prows = []
    for r in rows:
        pr = []
        for c in r:
            pr.append(random.choice(pmap.get(c, [""])))
        prows.append(pr)

    prows.append([])
    prows.append([note])
    prows.extend(noterows)

    return prows

if "__main__" == __name__:
    argp = argparse.ArgumentParser()
    argp.add_argument("problemfile")
    argp.add_argument("ppmfile")

    args = argp.parse_args()

    # parse problems
    note = ""
    problems = {}
    with open(args.problemfile, "r") as f:
        while not note:
            line = f.readline().strip()
            if line.startswith("#"): continue
            note = line

        while True:
            line = f.readline()
            if not line: break
            line = line.strip()
            if not line: continue
            p = line.split(",")
            problems[p[0]] = p[1:]

    # parse image
    size = []
    rows = []
    histogram = {}
    with open(args.ppmfile, "r") as f:
        line = f.readline()
        if line.strip() != "P3":
            print "Error: must be in ppm 'plain' or 'ascii' format"
            exit(1)

        while not size:
            line = f.readline()
            if line.startswith("#"):
                print line
                continue
            size = map(int, line.split(" ", 1))

        if not size:
            print "Error: couldn't determine image size"
            exit(1)

        maxval = int(f.readline())
        if maxval != 255:
            print "Error: please use 8 bit color values"
            exit(1)

        for y in range(size[1]):
            row = []
            for x in range(size[0]):
                color = [f.readline() for i in range(3)]
                color = map(int, color)

                hexcolor = "#%0.2X%0.2X%0.2X" % tuple(color)

                row.append(hexcolor)
                histogram[hexcolor] = histogram.get(hexcolor, 0) + 1

            rows.append(row)

    prows = color_by_problem(note, problems, rows, histogram)
    print "\n".join(map(",".join, prows))
