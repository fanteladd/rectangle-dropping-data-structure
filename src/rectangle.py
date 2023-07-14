#!/usr/bin/env python3

from uuid import uuid4
import random
import matplotlib.patches as ptc

class Rectangle:
    def __init__(self, x_i, x_f, height, offset=0, color=None, id=None) -> None:
        if not id:
            self.id = uuid4()
        else:
            self.id = id
        self.x_i = x_i
        self.x_f = x_f
        self.height = height
        self.offset = offset
        if not color:
            self.color = "#" + "".join(
                [random.choice("0123456789ABCDEF") for _ in range(6)]
            )
        else:
            self.color = color

    def draw(self, ax):
        (x, y) = self.x_i, self.offset
        width = self.x_f - self.x_i
        height = self.height
        return ax.add_patch(ptc.Rectangle((x, y), width, height, facecolor=self.color))

    def extend_bottom(self):
        """
        create a copy of Rectangle object with height = height + offset and offset = 0
        """
        return Rectangle(
            self.x_i, self.x_f, self.height + self.offset, 0, self.color, self.id
        )
