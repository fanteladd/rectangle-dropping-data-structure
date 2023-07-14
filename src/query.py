#!/usr/bin/env python3

from utils import *
from lemma16 import *
import rdds
from rdds import onClick
import matplotlib.pyplot as plt


if __name__ == "__main__":
    fig, ax = plt.subplots(1, 1, figsize=(20, 40))
    ax.set_aspect("equal", adjustable="box")
    fig.canvas.mpl_connect("button_press_event", lambda event: onClick(event, ax))
    plt.xticks(range(40))
    plt.yticks(range(20))
    rectangles = [
        rdds.Rectangle(0, 9, 5, 0),
        rdds.Rectangle(5, 7, 7, 5),
        rdds.Rectangle(2, 4, 3, 5),
        rdds.Rectangle(8, 13, 2, 5),
        rdds.Rectangle(19, 24, 10, 0),
        rdds.Rectangle(24, 27, 4, 0),
        rdds.Rectangle(13, 18, 4, 0),
        rdds.Rectangle(13, 16, 5, 4),
        rdds.Rectangle(17, 19, 5, 4),
        rdds.Rectangle(9, 13, 5, 0),
        rdds.Rectangle(0, 2, 2, 5),
        rdds.Rectangle(27, 28, 1, 0),
        rdds.Rectangle(28, 30, 4, 0),
        rdds.Rectangle(30, 34, 2, 0),
        rdds.Rectangle(33, 34, 3, 2),
        rdds.Rectangle(29, 30, 10, 4),
        rdds.Rectangle(9, 11, 3, 7),
        rdds.Rectangle(24, 26, 2, 4),
    ]
    rdds = rdds.RDDS(34, rectangles)
    ax.plot([0, 0], [0, 25], color="black")
    listrect = []
    for rect in rdds.rectangles:
        listrect.append(rect.draw(ax))
    ax.plot([rdds.width, rdds.width], [0, 25], color="black")
    plt.pause(6)
    # ax.cla()
    plt.xticks(range(40))
    plt.yticks(range(20))
    seg = displaySkyline(rdds.skyline, ax)
    plt.pause(3)
    sseg = rdds.displayChunks(ax)
    plt.pause(3)
    for r in listrect:
        r.remove()
    plt.pause(3)
    h = 11
    print(f"blocco di larghezza max ad altezza {h}: {rdds.query_height(h, ax,2)}")
    rdds.removeChunks(sseg)
    plt.show()
