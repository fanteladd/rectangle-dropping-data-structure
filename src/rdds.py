#!/usr/bin/env python3

from bintrees import FastAVLTree
from utils import *
import math
from bisect import bisect_left, bisect_right
import matplotlib.pyplot as plt
import matplotlib.text as txt
from sortedcontainers import SortedSet
from operator import attrgetter
from chunk import Chunk
from vertex import Vertex
from rectangle import Rectangle
from collections import namedtuple


pause = False


def onClick(event, ax):
    global pause
    pause ^= True
    if pause == True:
        ax.scatter(0, 0, s=20, marker="o", color="red")
    else:
        ax.scatter(0, 0, s=25, marker="o", color="white")


def ppause(s):
    if s != 0:
        plt.pause(s)


class RDDS:
    def __init__(self, width, rectangles=[]):
        self.rectangles = rectangles
        self.width = width
        self.skyline = []
        self.createSkyline()
        self.chunks = []
        self.heights = SortedSet()
        self.createchunks()

    def createSkyline(self):
        if not self.rectangles:
            self.skyline = [Vertex(0, 0), Vertex(self.width, 0)]
            return 0
        rectangles = [rectangle.extend_bottom() for rectangle in self.rectangles]
        Point = namedtuple("Point", "id x h start")
        S = FastAVLTree()
        T = []
        R = []

        for r in rectangles:
            T.append(Point(r.id, r.x_i, r.height, True))
            T.append(Point(r.id, r.x_f, r.height, False))

        T.sort(key=lambda x: x.x)

        h_max = 0
        id_max = 0
        x_max = 0

        for tup in T:
            if tup.start:
                S[tup.h] = tup.id
                if tup.h > h_max:
                    id_max = tup.id
                    if h_max == 0 and x_max == 0:
                        R.append((tup.x, id_max, 0))
                    elif x_max == tup.x and x_max != 0:
                        R.pop()
                        if R[-1][0] == tup.x and R[-1][2] == tup.h:
                            R.pop()
                    else:
                        R.append((tup.x, id_max, h_max))
                    x_max = tup.x
                    h_max = tup.h
                    R.append((x_max, id_max, h_max))
            else:
                S.pop(tup.h)
                if tup.id == id_max:
                    R.append((tup.x, id_max, h_max))
                    if not S:
                        h_max = 0
                        id_max = None
                    else:
                        h_max = max(list(S.keys()))
                        id_max = S.get(h_max)
                    R.append((tup.x, id_max, h_max))
                    x_max = tup.x

        self.skyline = [Vertex(r[0], r[2]) for r in R]
        return 0

    def createchunks(self):
        skyline = self.skyline[:]
        n = len(skyline)
        size = int(math.sqrt(n * math.log(n)))

        while skyline:
            if len(skyline) - 1 < size:
                chunk = Chunk(skyline)
                for height in chunk.query_height:
                    self.heights.add(height)
                self.chunks.append(chunk)
                skyline = []
            else:
                if skyline[size].x == skyline[size - 1].x:
                    size -= 1
                skyline_chunk = skyline[: size + 1]
                chunk = Chunk(skyline_chunk)
                for height in chunk.query_height:
                    self.heights.add(height)
                self.chunks.append(chunk)
                skyline = skyline[size:]

    def query_height(self, h, ax, s):
        if s != 0:
            ax.get_yticklabels()[h].set_color("red")
        width = (0, 0, 0)
        ar = None
        text = None
        ar_prec = None
        text_prec = None
        L = self.chunks
        global pause
        ppause(s)
        while pause:
            plt.pause(0.1)
        ppause(s)

        for chunk in L:
            if h < min(chunk.query_height):
                (x_i, x_f, w) = (0, 0, 0)
            else:
                (_, (x_i, x_f, w)) = chunk.query_height.floor_item(h)

            if s != 0:
                ar, text = drawLine(x_i, x_f, h + 0.2, ax, "blue")

            ppause(s)
            while pause:
                plt.pause(0.1)
            ppause(s)

            if w >= width[0]:
                width = (w, x_i, x_f)
                if s != 0:
                    eraseLine(ar, text)
                    ar, text = drawLine(x_i, x_f, h + 0.2, ax, "blue")
                    if ar_prec != None and text_prec != None:
                        eraseLine(ar_prec, text_prec)
                    ar_prec = ar
                    text_prec = text
            else:
                if s != 0:
                    eraseLine(ar, text)

        n = len(L)
        p1 = 0
        p2 = 1
        pointer1 = ax.annotate(
            text="p1",
            xy=(L[p1].skyline[0].x + 0.5, 15),
            xytext=(L[p1].skyline[0].x + 1, 14),
            arrowprops=dict(arrowstyle="<-", color="green"),
        )
        pointer2 = ax.annotate(
            text="p2",
            xy=(L[p2].skyline[0].x + 0.5, 15),
            xytext=(L[p2].skyline[0].x + 1, 14),
            arrowprops=dict(arrowstyle="<-", color="green"),
        )

        ppause(s)
        while pause:
            plt.pause(0.1)
        ppause(s)

        while p1 < n - 1:
            while pause:
                plt.pause(0.1)

            ppause(s)

            if L[p2].max_height <= h and p2 < n - 1:
                p2 += 1

                pointer2.xy = (L[p2].skyline[0].x + 0.5, 15)
                pointer2.set_x(L[p2].skyline[0].x + 1)
                pointer2.set_y(14)
            else:
                ppause(s)
                while pause:
                    plt.pause(0.1)
                ppause(s)
                (x_i, y_1i, y_1f) = bsearch_staircase(h, L[p1].right_staircase)
                (x_f, y_2i, y_2f) = bsearch_staircase(h, L[p2].left_staircase)
                w = x_f - x_i
                ppause(s)
                while pause:
                    plt.pause(0.1)
                ppause(s)
                stair1 = ax.plot(
                    [x_i, x_i], [y_1i, y_1f], color="red", linestyle="dashed"
                )
                ppause(s)
                while pause:
                    plt.pause(0.1)
                ppause(s)
                stair2 = ax.plot(
                    [x_f, x_f], [y_2i, y_2f], color="cyan", linestyle="dashed"
                )
                ppause(s)

                ppause(s)
                while pause:
                    plt.pause(0.1)
                ppause(s)
                if s != 0:
                    ar, text = drawLine(x_i, x_f, h + 0.4, ax, "yellow")

                ppause(s)
                while pause:
                    plt.pause(0.1)
                ppause(s)

                stair1[0].remove()
                stair2[0].remove()

                ppause(s)

                if w > width[0]:
                    width = (w, x_i, x_f)
                    if s != 0:
                        eraseLine(ar, text)
                        ar, text = drawLine(x_i, x_f, h + 0.2, ax, "blue")
                        if ar_prec != None and text_prec != None:
                            eraseLine(ar_prec, text_prec)
                            ar_prec = ar
                            text_prec = text
                else:
                    if s != 0:
                        eraseLine(ar, text)

                p1 = p2
                if p2 < n - 1:
                    p2 += 1

                ppause(s)
                while pause:
                    plt.pause(0.1)
                ppause(s)

                pointer1.xy = (L[p1].skyline[0].x + 0.5, 15)
                pointer1.set_x(L[p1].skyline[0].x + 1)
                pointer1.set_y(14)
                pointer2.xy = (L[p2].skyline[0].x + 0.5, 15)
                pointer2.set_x(L[p2].skyline[0].x + 1)
                pointer2.set_y(14)

        pointer1.remove()
        pointer2.remove()
        # ax.get_yticklabels()[h].set_color("black")

        return width

    def query(self, width, ax):
        i = 0
        j = len(self.heights) - 1

        while i <= j:
            mid = int((i + j) / 2)
            w, _, _ = self.query_height(self.heights[mid], ax, 0)
            if width > w:
                i = mid + 1

            if width <= w:
                j = mid - 1

        _, x_d, _ = self.query_height(self.heights[i], ax, 0)
        return self.heights[i], x_d

    def insert(self, width: int, height: int, x_d: int, ax, s, color):
        sg = displaySkyline(self.skyline, ax)
        seg = []
        r1, r2, r3, r4 = [], [], [], []
        stair1, stair2 = [], []

        stair1 = []
        if s != 0:
            ax.get_xticklabels()[x_d].set_color("red")

        x_i = x_d
        x_f = x_i + width

        ppause(s)

        if s != 0:
            r1 = ax.plot([x_i, x_f], [20 + height, 20 + height], color="orange")
            r2 = ax.plot([x_i, x_f], [20, 20], color="orange")
            r3 = ax.plot([x_i, x_i], [20, 20 + height], color="orange")
            r4 = ax.plot([x_f, x_f], [20, 20 + height], color="orange")

        ppause(s)

        while pause:
            plt.pause(0.1)

        ppause(s)

        if s != 0:
            seg = self.displayChunks(ax)

        height_pos = 0
        covered = []
        p1 = 0
        n = len(self.chunks)

        # cerca chunks coinvolti
        for i in range(n):
            if i == 0 and x_i < self.chunks[i].skyline[-1].x:
                p1 = i
                break
            if (
                x_i >= self.chunks[i].skyline[0].x
                and x_i < self.chunks[i].skyline[-1].x
            ):
                p1 = i
                break

        pointer1 = ax.annotate(
            text="p1",
            xy=(self.chunks[p1].skyline[0].x + 0.5, 15),
            xytext=(self.chunks[p1].skyline[0].x + 1, 14),
            arrowprops=dict(arrowstyle="<-", color="green"),
        )

        ppause(s)

        while pause:
            plt.pause(0.1)

        ppause(s)

        p2 = p1
        for i in range(p2, n):
            if (
                x_f < self.chunks[i].skyline[-1].x
                and x_f >= self.chunks[i].skyline[0].x
            ):
                p2 = i
                break
            else:
                if p1 != i:
                    covered.append(self.chunks[i])

        pointer2 = ax.annotate(
            text="p2",
            xy=(self.chunks[p2].skyline[0].x + 0.5, 15),
            xytext=(self.chunks[p2].skyline[0].x + 1, 14),
            arrowprops=dict(arrowstyle="<-", color="green"),
        )

        ppause(s)

        while pause:
            plt.pause(0.1)

        ppause(s)

        if p1 == p2:
            # troviamo altezza
            p = p1
            vertices = self.chunks[p].skyline
            del_sin = bisect_right(vertices, x_i, key=lambda v: v.x)
            del_des = bisect_left(vertices, x_f, key=lambda v: v.x)
            height_pos = max(vertices[del_sin : del_des + 1], key=attrgetter("y")).y
            self.heights.add(height_pos + height)

            if s != 0:
                ax.get_yticklabels()[height_pos].set_color("red")

            ppause(s)

            while pause:
                plt.pause(0.1)

            ppause(s)

            # inseriamo blocco
            del_sin = bisect_right(vertices, x_i, key=lambda v: v.x)
            if del_sin > 1 and vertices[del_sin - 1].x == x_i:
                del_sin -= 1

            vertices.insert(del_sin, Vertex(x_i, height_pos + height))
            vertices.insert(del_sin, Vertex(x_i, vertices[del_sin - 1].y))

            if p > 0:
                self.chunks[p - 1].skyline[-1] = vertices[0]

            del_des = bisect_left(vertices, x_f, key=lambda v: v.x)
            if del_des < len(vertices) - 1 and vertices[del_des].x == x_f:
                del_des += 1
            else:
                del_des -= 1

            if del_des == len(vertices) - 1:
                vertices.insert(del_des + 1, Vertex(x_f, vertices[del_des].y))
                vertices.insert(del_des + 1, Vertex(x_f, height_pos + height))
            else:
                vertices.insert(del_des + 1, Vertex(x_f, vertices[del_des + 1].y))
                vertices.insert(del_des + 1, Vertex(x_f, height_pos + height))

            if p < len(self.chunks) - 1:
                self.chunks[p + 1].skyline[0] = vertices[-1]

            vertices[del_sin + 2 : del_des + 1] = []

            # now rebuild chunk p
            self.chunks[p] = Chunk(vertices)

        else:
            # troviamo altezza
            if covered:
                height_pos = max(covered, key=attrgetter("max_height")).max_height

            if s != 0:
                ax.get_yticklabels()[height_pos].set_color("red")

            ppause(s)

            while pause:
                plt.pause(0.1)

            ppause(s)

            staircase = list(reversed(self.chunks[p1].right_staircase))
            i = bisect_right(staircase, x_d, key=lambda x: x[0]) - 1

            h = staircase[i][1]
            x = staircase[i][0]
            y_1i = staircase[i][1]
            y_1f = staircase[i][2]
            stair1 = ax.plot([x, x], [y_1i, y_1f], color="red", linestyle="dashed")

            if h > height_pos:
                ax.get_yticklabels()[height_pos].set_color("black")
                ax.get_yticklabels()[h].set_color("red")
                height_pos = h

            ppause(s)
            while pause:
                plt.pause(0.1)
            ppause(s)

            staircase = self.chunks[p2].left_staircase
            j = bisect_left(staircase, x_f, key=lambda x: x[0])

            h = staircase[j][1]
            x = staircase[j][0]
            y_2i = staircase[j][1]
            y_2f = staircase[j][2]
            stair2 = ax.plot([x, x], [y_2i, y_2f], color="cyan", linestyle="dashed")

            if h > height_pos:
                ax.get_yticklabels()[height_pos].set_color("black")
                ax.get_yticklabels()[h].set_color("red")
                height_pos = h

            ppause(s)
            while pause:
                plt.pause(0.1)
            ppause(s)

            self.heights.add(height_pos + height)

            # inseriamo blocco
            left_chunk_skyline = self.chunks[p1].skyline
            del_sin = bisect_right(left_chunk_skyline, x_i, key=lambda v: v.x)
            if del_sin > 0 and left_chunk_skyline[del_sin - 1].x == x_i:
                del_sin = del_sin - 2
            self.chunks[p1].skyline = left_chunk_skyline[:del_sin]

            right_chunk_skyline = self.chunks[p2].skyline
            del_des = bisect_left(right_chunk_skyline, x_f, key=lambda v: v.x)
            if (
                del_des < len(right_chunk_skyline) - 2
                and right_chunk_skyline[del_des].x == x_f
            ):
                del_des = del_des + 2
            self.chunks[p2].skyline = right_chunk_skyline[del_des:]

            left_chunk_skyline = self.chunks[p1].skyline
            if not left_chunk_skyline:
                left_chunk_skyline.append(
                    Vertex(x_i, self.chunks[p1 - 1].skyline[-2].y)
                )
            else:
                left_chunk_skyline.append(Vertex(x_i, self.chunks[p1].skyline[-1].y))
            left_chunk_skyline.append(Vertex(x_i, height_pos + height))
            left_chunk_skyline.append(Vertex(x_f, height_pos + height))

            right_chunk_skyline = self.chunks[p2].skyline
            right_chunk_skyline.insert(0, Vertex(x_f, self.chunks[p2].skyline[0].y))
            right_chunk_skyline.insert(0, Vertex(x_f, height_pos + height))

            self.chunks = self.chunks[: p1 + 1] + self.chunks[p2:]

            p2 = p1 + 1

            if p1 > 0:
                self.chunks[p1 - 1].skyline[-1] = self.chunks[p1].skyline[0]

            if p2 < len(self.chunks) - 1:
                self.chunks[p2 + 1].skyline[0] = self.chunks[p2].skyline[-1]

            # now rebuild chunk p1 and p2
            self.chunks[p1] = Chunk(self.chunks[p1].skyline)
            self.chunks[p2] = Chunk(self.chunks[p2].skyline)

        if s != 0:
            r1[0].remove()
            r2[0].remove()
            r3[0].remove()
            r4[0].remove()
            ax.plot(
                [x_i, x_f], [height_pos + height, height_pos + height], color="orange"
            )
            ax.plot([x_i, x_f], [height_pos, height_pos], color="orange")
            ax.plot([x_i, x_i], [height_pos, height_pos + height], color="orange")
            ax.plot([x_f, x_f], [height_pos, height_pos + height], color="orange")

        ppause(s)

        while pause:
            plt.pause(0.1)

        ppause(s)

        self.rectangles.append(Rectangle(x_i, x_f, height, height_pos, color))

        pointer1.remove()
        pointer2.remove()
        if stair1:
            stair1[0].remove()
            stair2[0].remove()

        ppause(s)

        # ricostruzione struttura dati

        n = len(self.skyline)
        size = int(math.sqrt(n * math.log(n)))
        minsize = int(math.sqrt(n * math.log(n)) / 2)
        print(f"size: {size}")
        print(f"minsize: {minsize}")

        if s != 0:
            self.removeChunks(seg)
            seg = self.displayChunks(ax)

        end = p2 + 2
        if p1 != 0:
            p2 = p1
            p1 = p1 - 1

        self.skyline = []
        for chunk in self.chunks:
            self.skyline += chunk.skyline
        ppause(s)
        eraseSkyline(sg, ax)
        sg = displaySkyline(self.skyline, ax)

        while p2 < end:
            if s != 0:
                pointer1 = ax.annotate(
                    text="p1",
                    xy=(self.chunks[p1].skyline[0].x + 0.5, 15),
                    xytext=(self.chunks[p1].skyline[0].x + 1, 14),
                    arrowprops=dict(arrowstyle="<-", color="green"),
                )
                pointer2 = ax.annotate(
                    text="p2",
                    xy=(self.chunks[p2].skyline[0].x + 0.5, 15),
                    xytext=(self.chunks[p2].skyline[0].x + 1, 14),
                    arrowprops=dict(arrowstyle="<-", color="green"),
                )
            ppause(s)
            while pause:
                plt.pause(0.1)
            ppause(s)
            if len(self.chunks[p1].skyline) > size:
                if s != 0:
                    l = ax.annotate(
                        text="split", xy=(self.chunks[p1].skyline[0].x + 5, 18)
                    )
                    ppause(s)
                    self.removeChunks(seg)

                half = int(len(self.chunks[p1].skyline) / 2)
                skyline1 = self.chunks[p1].skyline[: half + 1]
                skyline2 = self.chunks[p1].skyline[half:]
                del self.chunks[p1]
                chunk = Chunk(skyline2)
                self.chunks.insert(p1, chunk)
                chunk = Chunk(skyline1)
                self.chunks.insert(p1, chunk)
                if s != 0:
                    seg = self.displayChunks(ax)
                    l.remove()
            if len(self.chunks[p1].skyline) + len(self.chunks[p2].skyline) < minsize:
                if s != 0:
                    self.removeChunks(seg)
                    l = ax.annotate(
                        text="merge p1 and p2",
                        xy=(self.chunks[p1].skyline[0].x + 5, 18),
                    )
                    ppause(s)
                skyline = self.chunks[p1].skyline + self.chunks[p1].skyline[1:]
                del self.chunks[p1]
                del self.chunks[p2]
                chunk = Chunk(skyline)
                self.chunks.insert(p2, chunk)
                if s != 0:
                    seg = self.displayChunks(ax)
                    l.remove()
            if p2 == len(self.chunks) - 1:
                break
            p1 = p2
            p2 += 1
            if s != 0:
                pointer1.remove()
                pointer2.remove()

        self.skyline = []
        for chunk in self.chunks:
            self.skyline += chunk.skyline
        ppause(s)
        eraseSkyline(sg, ax)
        if s != 0:
            self.removeChunks(seg)

    def displayChunks(self, ax):
        seg = []
        for i in self.chunks:
            seg.append(
                ax.plot([i.skyline[0].x, i.skyline[0].x], [0, 25], color="green")
            )
        # displayStaircases(i[2], i[3], ax)
        return seg

    def removeChunks(self, seg):
        for i in seg:
            i[0].remove()


def drawLine(x_i, x_f, h, ax, color="blue"):
    if x_i > x_f:
        return -1, -1
    width = x_f - x_i
    ar = txt.Annotation(
        text="",
        xy=(x_i, h),
        xytext=(x_f, h),
        arrowprops=dict(arrowstyle="<->", color=color),
    )
    text = txt.Annotation(text=str(width), xy=((width / 2) + x_i, h + 0.1))
    ax.add_artist(ar)
    ax.add_artist(text)
    return ar, text


def eraseLine(ar, text):
    ar.remove()
    text.remove()


def bsearch_staircase(h, staircase):
    l = 0
    r = len(staircase) - 1

    while l <= r:
        mid = l + (r - l) // 2

        if h >= staircase[mid][1] and h < staircase[mid][2]:
            return staircase[mid]

        elif h >= staircase[mid][2]:
            l = mid + 1

        else:
            r = mid - 1

    return 0
