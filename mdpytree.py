# -*- coding: utf-8 -*-

from markdown import markdown
from bs4 import BeautifulSoup


class Node:
    def __init__(self, mother, level=0, el=""):
        self.mother = mother
        self.el = el
        self.level = level
        self.children = []
        self.content = []

    def add_child(self, child):
        self.children.append(child)

    def add_content(self, content):
        self.content.append(Node(self.mother, self.level, content))

    def get_children(self):
        return self.children

    def get_mother(self):
        return self.mother

    def tell_mother(self):
        self.mother.add_child(self)

    @staticmethod
    def fromMarkdown(md, *args, **kwargs):
        """
        Creates abstraction using path to file

        :param str path: path to markdown file
        :return: Node object
        """
        return Node.fromHTML(markdown(md, *args, **kwargs))

    @staticmethod
    def fromHTML(html, *args, **kwargs):
        """
        Creates abstraction using HTML

        :param str html: HTML
        :return: Node object
        """
        source = BeautifulSoup(html, "html.parser", *args, **kwargs)

        tree = Node(mother=None, level=0)
        for el in source:
            if el.name is None:
                continue
            level = get_heading_level(el.name)
            if level:
                if level <= tree.level:
                    moved_tree = tree
                    for i in range(1 + tree.level - level):
                        moved_tree = moved_tree.get_mother()
                    tree = moved_tree

                new_tree = Node(mother=tree, level=level, el=el)
                new_tree.tell_mother()
                tree = new_tree
            else:
                tree.add_content(el)

        for i in range(tree.level):
            tree = tree.get_mother()

        return tree


def get_heading_level(s):
    for i in range(10):
        if s == "h" + str(i):
            return i
