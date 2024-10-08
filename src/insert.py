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
        rdds.Rectangle(5, 7, 4, 5),
        rdds.Rectangle(2, 4, 3, 5),
        rdds.Rectangle(8, 13, 2, 5),
        rdds.Rectangle(19, 24, 10, 0),
        rdds.Rectangle(24, 27, 4, 0),
        rdds.Rectangle(13, 19, 4, 0),
        rdds.Rectangle(13, 17, 5, 4),
        rdds.Rectangle(17, 19, 5, 4),
        rdds.Rectangle(9, 13, 5, 0),
        rdds.Rectangle(0, 2, 2, 5),
        rdds.Rectangle(27, 28, 1, 0),
        rdds.Rectangle(28, 30, 4, 0),
        rdds.Rectangle(30, 34, 2, 0),
        rdds.Rectangle(33, 34, 3, 2),
        rdds.Rectangle(29, 30, 5, 4),
        rdds.Rectangle(9, 11, 3, 7),
        rdds.Rectangle(24, 26, 2, 4),
    ]
    rdds1 = rdds.RDDS(34, rectangles)
    ax.plot([0, 0], [0, 25], color="lightgrey")
    listrect = []
    # rec = rdds.Rectangle(6, 19, 3, 20, "blue").draw(ax)
    ax.get_xticklabels()[6].set_color("red")
    for rect in rdds1.rectangles:
        listrect.append(rect.draw(ax))
    ax.plot([rdds1.width, rdds1.width], [0, 25], color="lightgrey")
    ax.plot([0, rdds1.width], [0, 0], color="lightgrey")
    plt.pause(3)
    # ax.cla()
    for r in listrect:
        r.remove()
    rdds1.insert(13,3,6,ax,2,"blue")
    # plt.pause(2)
    # eraseSkyline(seg,ax)
    # seg = displaySkyline(rdds.skyline, ax)
    # plt.pause(4)

    # rec.remove()
    # listrect = []
    # for rect in rdds1.rectangles:
    #     listrect.append(rect.draw(ax))
    # # eraseSkyline(seg,ax)
    # plt.pause(2)
    # for r in listrect:
    #     r.remove()
    # rdds1.insert(3,2,3,ax,1,"red")
    # # plt.pause(2)
    # # eraseSkyline(seg,ax)
    # # seg = displaySkyline(rdds.skyline, ax)
    # # plt.pause(4)

    # listrect = []
    # for rect in rdds1.rectangles:
    #     rect.draw(ax)
    # # eraseSkyline(seg,ax)
    # plt.pause(2)
    plt.show()
