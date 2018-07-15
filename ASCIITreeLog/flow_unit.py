# -*- coding: utf-8 -*-

class PlotBit(object):
    def __init__(self):
        self._up = False
        self._right = False
        self._down = False
        self._left = False

        self.plotitem = {(True, False, True, False):self.vert(),
                         (True, True, True, False):self.vert_right(),
                         (True, False, True, True):self.vert_left(),
                         (False, True, False, True):self.hori(),
                         (True, True, False, True):self.hori_up(),
                         (False, True, True, True):self.hori_down(),
                         (False, False, True, True):self.corner_ur(),
                         (False, True, True, False):self.corner_ul(),
                         (True, False, False, True):self.corner_lr(),
                         (True, True, False, False):self.corner_ll(),
                         (True, True, True, True):self.cross(),
                         (False, False, False, False):" "}
    @classmethod
    def vert(self):
        return "|"
    @classmethod
    def vert_right(self):
        return "├"
    @classmethod
    def vert_left(self):
        return "┤"
    @classmethod
    def hori(self):
        return "─"
    @classmethod
    def hori_up(self):
        return "┴"
    @classmethod
    def hori_down(self):
        return "┬"
    @classmethod
    def corner_ur(self):
        return "┐"
    @classmethod
    def corner_ul(self):
        return "┌"
    @classmethod
    def corner_lr(self):
        return "┘"
    @classmethod
    def corner_ll(self):
        return "└"
    @classmethod
    def cross(self):
        return "┼"

    @property
    def up(self):
        return self._up
    @up.setter
    def up(self, value):
        self._up = value

    @property
    def right(self):
        return self._right
    @right.setter
    def right(self, value):
        self._right = value

    @property
    def down(self):
        return self._down
    @down.setter
    def down(self, value):
        self._down = value

    @property
    def left(self):
        return self._left
    @left.setter
    def left(self, value):
        self._left = value

    def get_plot_item(self):
        return self.plotitem.get((self._up, self._right, self._down, self._left), "?")

class RoundBit(PlotBit):
    def corner_ur(self):
        return "╮"
    def corner_ul(self):
        return "╭"
    def corner_lr(self):
        return "╯"
    def corner_ll(self):
        return "╰"