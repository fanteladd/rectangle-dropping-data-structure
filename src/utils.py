#!/usr/bin/env python3


def displaySkyline(skyline, ax):
    n = len(skyline)
    y_max = 0
    segments = []
    for i in range(0, n - 1):
        x_0 = skyline[i].x
        y_0 = skyline[i].y
        x_1 = skyline[i + 1].x
        y_1 = skyline[i + 1].y
        x, y = [x_0, x_1], [y_0, y_1]
        if y_0 > y_max:
            y_max = y_0
        if y_1 > y_max:
            y_max = y_1
        seg = ax.plot(x, y, color="black")
        segments.append(seg[0])
    return segments


def eraseSkyline(segments, ax):
    for seg in segments:
        seg.remove()


def displayStaircases(lcase, rcase, ax):
    for t in lcase:
        x, y = [t[0], t[0]], [t[1], t[2]]
        ax.plot(x, y, color="cyan", linestyle="dashed")
    for t in rcase:
        x, y = [t[0], t[0]], [t[1], t[2]]
        ax.plot(x, y, color="red", linestyle="dashed")
