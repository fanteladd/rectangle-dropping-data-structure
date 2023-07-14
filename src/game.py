#!/usr/bin/env python3

from utils import *
import rdds
from rectangle import Rectangle
import matplotlib.pyplot as plt


if __name__ == "__main__":
    fig, ax = plt.subplots(1, 1, figsize=(40, 40))
    # fig.canvas.mpl_connect('button_press_event', rdds.onClick)
    ax.set_aspect("equal", adjustable="box")
    plt.xticks(range(40))
    plt.yticks(range(40))
    rectangles = [
        Rectangle(0, 9, 5, 0),
        Rectangle(4, 7, 7, 5),
        Rectangle(2, 4, 3, 5),
        Rectangle(8, 13, 2, 5),
        Rectangle(19, 24, 10, 0),
        Rectangle(24, 27, 4, 0),
        Rectangle(13, 19, 4, 0),
        Rectangle(13, 16, 5, 4),
        Rectangle(17, 19, 5, 4),
        Rectangle(9, 13, 5, 0),
        Rectangle(0, 2, 2, 5),
        Rectangle(27, 28, 4, 0),
        Rectangle(28, 30, 4, 0),
        Rectangle(30, 34, 2, 0),
        Rectangle(33, 34, 3, 2),
        Rectangle(29, 30, 10, 4),
        Rectangle(24, 26, 2, 4),
    ]
    rdds1 = rdds.RDDS(34, rectangles)
    ax.plot([0, 0], [0, 25], color="black")
    ax.plot([rdds1.width, rdds1.width], [0, 25], color="black")
    for rect in rdds1.rectangles:
        rect.draw(ax)
    seg = displaySkyline(rdds1.skyline, ax)

    insert = [
        Rectangle(10, 20, 2, 31, "purple"),
        Rectangle(10, 13, 3, 30, "blue"),
        Rectangle(10, 13, 7, 26, "green"),
        Rectangle(10, 15, 3, 30, "red"),
        Rectangle(10, 12, 3, 30, "orange"),
        Rectangle(10, 14, 1, 32, "cyan"),
    ]

    plt.pause(10)

    i = 0 
    for c in rdds1.chunks:
        print(f"chunk {i}")
        for v in c.skyline:
            print(f"x: {v.x}, y: {v.y}")
        i+=1

    for rect in insert:
        r = rect.draw(ax)
        plt.pause(3)

        width = rect.x_f - rect.x_i
        height = rect.height
        h, x_d = rdds1.query(width, ax)
        print(h, x_d)
        rdds1.insert(width, height, x_d, ax, 0, rect.color)
        for rect in rdds1.rectangles:
            rect.draw(ax)
        eraseSkyline(seg, ax)
        seg = displaySkyline(rdds1.skyline, ax)
        r.remove()
        i = 1
        for c in rdds1.chunks:
            print(f"chunk {i}")
            for v in c.skyline:
                print(f"x: {v.x}, y: {v.y}")
            i+=1
        plt.pause(2)

    # rect = Rectangle(10,13,2,30,"green")
    # r = rect.draw(ax)
    # plt.pause(5)
    # width = rect.x_f - rect.x_i
    # height = rect.height
    # h,x_d = rdds1.query(width,ax)
    # print(h,x_d)
    # rdds1.insert(width,height,x_d,ax,0,rect.color)
    # for rect in rdds1.rectangles:
    #     rect.draw(ax)
    # eraseSkyline(seg,ax)
    # seg = displaySkyline(rdds1.skyline, ax)
    # r.remove()
    # plt.pause(5)

    # rect = Rectangle(10,15,3,30,"red")
    # r = rect.draw(ax)
    # plt.pause(5)
    # width = rect.x_f - rect.x_i
    # height = rect.height
    # h,x_d = rdds1.query(width,ax)
    # print(h,x_d)
    # rdds1.insert(width,height,x_d,ax,0,rect.color)
    # for rect in rdds1.rectangles:
    #     rect.draw(ax)
    # eraseSkyline(seg,ax)
    # seg = displaySkyline(rdds1.skyline, ax)
    # r.remove()
    # plt.pause(5)
    plt.show()
