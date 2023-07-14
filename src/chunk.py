#!/usr/bin/env python3

from bintrees import FastAVLTree
from utils import *
from vertex import Vertex

class Chunk:
    def __init__(self, skyline: list[Vertex]):
        self.skyline = skyline
        self.left_staircase, self.right_staircase = self.staircases()
        self.query_height = self.query_height_ds()
        self.max_height = self.query_height.max_key()

    def query_height_ds(self):
        width_left = dict()
        width_right = dict()
        width_vertices = dict()
        width_heights = FastAVLTree()

        w = self.skyline[-1].x
        x_start = self.skyline[0].x

        # left to right
        visited = []
        for v in self.skyline:
            u = findNearest(v, visited)
            if u == None:
                x_i = x_start
                x_f = v.x
                width = x_f - x_i
            else:
                x_i = u.x
                x_f = v.x
                width = v.x - u.x

            width_left[v] = (x_i, x_f, width)

            visited.append(v)

        # right to left
        visited = []
        for v in reversed(self.skyline):
            u = findNearest(v, visited)
            if u == None:
                x_i = v.x
                x_f = w
                width = x_f - x_i
            else:
                x_i = v.x
                x_f = u.x
                width = x_f - x_i

            width_right[v] = (x_i, x_f, width)
            visited.append(v)

        for vertex in width_right:
            x_i = width_left[vertex][0]
            x_f = width_right[vertex][1]
            width = x_f - x_i
            width_vertices[vertex] = (x_i, x_f, width)

        for vertex in width_vertices:
            h = vertex.y
            if h not in width_heights:
                width_heights[h] = width_vertices[vertex]
            if width_vertices[vertex][2] > width_heights[h][2]:
                width_heights[h] = width_vertices[vertex]

        heights = list(width_heights.keys())
        prec_h = heights[0]
        for h in heights[1:]:
            if width_heights[prec_h][2] > width_heights[h][2]:
                width_heights[h] = width_heights[prec_h]
            prec_h = h

        return width_heights

    def staircases(self):
        h = 0
        w = self.skyline[-1].x
        s = self.skyline[0].x
        left_staircase = []
        right_staircase = []
        for v in self.skyline:
            if h < v.y:
                left_staircase.append((v.x, h, v.y))
                h = v.y
        left_staircase.append((w, h, 20))
        h = 0
        for v in reversed(self.skyline):
            if h < v.y:
                right_staircase.append((v.x, h, v.y))
                h = v.y
        right_staircase.append((s, h, 20))
        return left_staircase, right_staircase

def findNearest(v, vertices):
    for u in vertices[::-1]:
        if u.y > v.y:
            return u
    return None
