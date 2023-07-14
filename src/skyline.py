#!/usr/bin/env python3

from utils import *
from lemma16 import *
import rdds
import matplotlib.pyplot as plt


if __name__ == "__main__":
    fig, ax = plt.subplots(1, 1,figsize=(20, 40))
    fig.canvas.mpl_connect('button_press_event', rdds.onClick)
    plt.xticks(range(40))
    plt.yticks(range(20))
    rectangles = [
        rdds.Rectangle(0, 9, 5, 0),
        rdds.Rectangle(5, 7, 7, 5),
        rdds.Rectangle( 2, 4, 3, 5),
        rdds.Rectangle( 8, 13, 2, 5),
        rdds.Rectangle( 19, 24, 10, 0),
        rdds.Rectangle( 24, 27, 4, 0),
        rdds.Rectangle( 13, 18, 4, 0),
        rdds.Rectangle( 13, 16, 5, 4),
        rdds.Rectangle( 17, 19, 5, 4),
        rdds.Rectangle( 9, 13, 5, 0),
        rdds.Rectangle( 0, 2, 2, 5),
        rdds.Rectangle( 27, 28, 1, 0),
        rdds.Rectangle( 28, 30, 4, 0),
        rdds.Rectangle( 30, 34, 2, 0),
        rdds.Rectangle( 33, 34, 3, 2),
        rdds.Rectangle( 29, 30, 10, 4),
        rdds.Rectangle( 9, 11, 3, 7),
        rdds.Rectangle( 24, 26, 2, 4),
    ]
    rdds = rdds.RDDS(34,rectangles)
    # data = lemma16(skyline.skyline,lcase,rcase,34)
    # print("data", data)
    for rect in rdds.rectangles:
        rect.draw(ax)
    plt.pause(3)
    # ax.cla()
    plt.xticks(range(40))
    plt.yticks(range(20))
    seg = displaySkyline(rdds.skyline, ax)
    sseg = rdds.displayChunks(ax)
    h = 10
    print(f"blocco di larghezza max ad altezza {h}: {rdds.query_height(h, ax,2)}")
    rdds.removeChunks(sseg)
    w = 7
    # print(f"altezza minima: {rdds.query(w,ax)}")

    rdds.insert(25,3,8,ax)
    plt.pause(3)
    eraseSkyline(seg,ax)
    for rect in rdds.rectangles:
        rect.draw(ax)
    seg = displaySkyline(rdds.skyline, ax)
    plt.pause(3)
    plt.cla()
    plt.xticks(range(40))
    plt.yticks(range(20))
    seg = displaySkyline(rdds.skyline, ax)
    # rdds.displayChunks(ax)
    h = 5
    # width = rdds.query_height(h, ax)
    plt.pause(5)
    rdds.insert(13,2,13,ax)
    plt.pause(3)
    plt.cla()
    plt.xticks(range(40))
    plt.yticks(range(20))
    displaySkyline(rdds.skyline, ax)
    # rdds.displayChunks(ax)
    plt.pause(5)
    plt.show()
