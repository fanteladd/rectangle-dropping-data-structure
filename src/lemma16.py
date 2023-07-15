#!/usr/bin/env python3

from bintrees import FastAVLTree
import matplotlib.pyplot as plt
from utils import displaySkyline
import rdds

pause = False


def onClick(event):
    global pause
    pause ^= True


def lemma16(skyline, w, s, ax):
    width_left = FastAVLTree()
    width_right = FastAVLTree()
    width_vertices = FastAVLTree()
    width_heights = FastAVLTree()

    x_start = skyline[0].x

    visited = []
    for v in skyline:
        h = v.y
        p1 = ax.scatter(v.x, v.y, s=100, marker="o", color="green")
        u = findNearest(v, visited)
        plt.pause(s)
        while pause:
            plt.pause(0.1)
        plt.pause(s)
        if u == None:
            x_i = x_start
            x_f = v.x
            width = x_f - x_i
            p2 = ax.scatter(0, h, s=100, marker="^", color="red")
        else:
            x_i = u.x
            x_f = v.x
            width = v.x - u.x
            p2 = ax.scatter(u.x, u.y, s=100, marker="^", color="red")
            plt.pause(s)
            while pause:
                plt.pause(0.1)
            plt.pause(s)

        ar = ax.annotate(
            text="",
            xy=(x_i, h + 0.3),
            xytext=(x_f, h + 0.3),
            arrowprops=dict(arrowstyle="<->", color="blue"),
        )
        text = ax.annotate(text=str(width), xy=((width / 2) + x_i, h + 0.4))
        width_left[(v.x, h)] = (x_i, x_f, width, ar, text)
        plt.pause(s)
        while pause:
            plt.pause(0.1)
        plt.pause(s)
        ar.remove()
        text.remove()
        p2.remove()
        p1.remove()

        visited.append(v)

    todraw_left = dict()
    todraw_right = dict()
    h_drawed = []
    for key in width_left:
        if key[1] not in h_drawed and width_left[key][2] > 0:
            todraw_left[key] = width_left[key]
            h_drawed.append(key[1])

    for r in todraw_left:
        ax.add_artist(todraw_left[r][3])
        ax.add_artist(todraw_left[r][4])

    visited = []
    for v in reversed(skyline):
        h = v.y
        u = findNearest(v, visited)
        if u == None:
            x_i = v.x
            x_f = w
            width = x_f - x_i
        else:
            x_i = v.x
            x_f = u.x
            width = x_f - x_i

        width_right[(v.x, h)] = (x_i, x_f, width)
        visited.append(v)

    for key in width_right:
        if key in todraw_left:
            t = width_right[key]
            h = key[1]
            x_i = t[0]
            x_f = t[1]
            width = t[2]
            ar = ax.annotate(
                text="",
                xy=(x_i, h + 0.2),
                xytext=(x_f, h + 0.2),
                arrowprops=dict(arrowstyle="<->", color="orange"),
            )
            text = ax.annotate(text=str(width), xy=((width / 2) + x_i, h + 0.5))
            todraw_right[key] = (x_i, x_f, width, ar, text)

    plt.pause(2)
    plt.pause(s)
    while pause:
        plt.pause(0.1)
    plt.pause(s)

    for key in width_left:
        if key in todraw_left:
            todraw_left[key][3].remove()
            todraw_right[key][3].remove()
            todraw_left[key][4].remove()
            todraw_right[key][4].remove()
            h = key[1]
            x_i = width_left[key][0]
            x_f = width_right[key][1]
            width = x_f - x_i
            ar = ax.annotate(
                text="",
                xy=(x_i, h + 0.2),
                xytext=(x_f, h + 0.2),
                arrowprops=dict(arrowstyle="<->", color="red"),
            )
            text = ax.annotate(text=str(width), xy=((width / 2) + x_i, h + 0.3))
            width_vertices[key] = (x_i, x_f, width, ar, text)
        else:
            x_i = width_left[key][0]
            x_f = width_right[key][1]
            width = x_f - x_i
            width_vertices[key] = (x_i, x_f, width)

    plt.pause(2)
    plt.pause(s)
    while pause:
        plt.pause(0.1)
    plt.pause(s)

    for key in todraw_left:
        t = width_vertices[key]
        t[3].remove()
        t[4].remove()
        x_i = t[0]
        x_f = t[1]
        width = t[2]
        width_vertices[key] = (x_i, x_f, width)

    plt.pause(1)
    for key in width_vertices:
        h = key[1]
        if h not in width_heights:
            x_i = width_vertices[key][0]
            x_f = width_vertices[key][1]
            width = x_f - x_i
            ar = ax.annotate(
                text="",
                xy=(x_i, h + 0.2),
                xytext=(x_f, h + 0.2),
                arrowprops=dict(arrowstyle="<->", color="red"),
            )
            text = ax.annotate(text=str(width), xy=((width / 2) + x_i, h + 0.3))
            width_heights[h] = (x_i, x_f, width, ar, text)
        if width_vertices[key][2] > width_heights[h][2]:
            width_heights[h][3].remove()
            width_heights[h][4].remove()
            x_i = width_vertices[key][0]
            x_f = width_vertices[key][1]
            width = x_f - x_i
            ar = ax.annotate(
                text="",
                xy=(x_i, h + 0.2),
                xytext=(x_f, h + 0.2),
                arrowprops=dict(arrowstyle="<->", color="red"),
            )
            text = ax.annotate(text=str(width), xy=((width / 2) + x_i, h + 0.3))
            width_heights[h] = (x_i, x_f, width, ar, text)

    plt.pause(2)
    plt.pause(s)
    while pause:
        plt.pause(0.1)
    plt.pause(s)

    heights = list(width_heights.keys())
    print(heights)
    prec_h = heights[0]

    for h in heights[1:]:
        if width_heights[prec_h][2] > width_heights[h][2]:
            width_heights[h][3].remove()
            width_heights[h][4].remove()
            width_heights[h] = width_heights[prec_h]
            x_i = width_heights[h][0]
            x_f = width_heights[h][1]
            width = x_f - x_i
        prec_h = h

    plt.pause(10)
    plt.pause(s)
    while pause:
        plt.pause(0.1)
    plt.pause(s)
    return width_vertices


def findNearest(v, vertices):
    for u in vertices[::-1]:
        if u.y > v.y:
            return u
    return None


def bsearchinterval(x, intervals):
    l = 0
    r = len(intervals) - 1

    while l <= r:
        mid = l + (r - l) // 2
        # Check if x is present at mid
        if x >= intervals[mid][1] and x < intervals[mid][2]:
            return intervals[mid][0]

        # If x is greater, ignore left half
        elif x >= intervals[mid][2]:
            l = mid + 1

        # If x is smaller, ignore right half
        else:
            r = mid - 1

    # If we reach here, then the element
    # was not present
    return 0


if __name__ == "__main__":
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))
    fig.canvas.mpl_connect("button_press_event", onClick)
    ax.set_aspect("equal", adjustable="box")
    rectangles = [
        rdds.Rectangle(1, 3, 1, 0),
        rdds.Rectangle(1, 2, 2, 1),
        rdds.Rectangle(3, 6, 3, 0),
        rdds.Rectangle(4, 6, 3, 3),
        rdds.Rectangle(5, 6, 1, 6),
        rdds.Rectangle(6, 9, 4, 0),
        rdds.Rectangle(7, 8, 2, 4),
        rdds.Rectangle(8, 9, 1, 4),
    ]
    rdds = rdds.RDDS(10, rectangles)
    ax.plot([0, 0], [0, 15], color="black")
    listrect = []
    for rect in rdds.rectangles:
        listrect.append(rect.draw(ax))
    ax.plot([rdds.width, rdds.width], [0, 15], color="black")
    plt.pause(3)
    displaySkyline(rdds.skyline, ax)
    for r in listrect:
        r.remove()
    plt.pause(3)
    data = lemma16(rdds.skyline, rdds.width, 0.7, ax)
    print("data", data)
