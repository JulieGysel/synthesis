import os
import pygraphviz as pgv

from .utils import *


class Graph:
    """A class for creating graphs from design space structures.
    """

    def __init__(self) -> None:
        """Initializes an instance of the Graph class.
        """
        self.graph = pgv.AGraph(strict=False, directed=True)

    def parse(self, design_space) -> None:
        """Parses the design space holes into the nodes dictionary:
                {start_node: {end_node1: [observation1],...}, end_node2: ...}

            design_space: list of holes
        """
        self.nodes = {}
        for hole in design_space:
            tmp = parse_hole(hole)

            for next in tmp["next"]:
                if tmp["type"] == "Assignment":
                    continue

                if tmp["memory"] in self.nodes.keys():
                    if next in self.nodes[tmp["memory"]].keys():
                        self.nodes[tmp["memory"]][next].append(
                            tmp["observation"])
                    else:
                        self.nodes[tmp["memory"]][next] = [tmp["observation"]]
                else:
                    self.nodes[tmp["memory"]] = {next: [tmp["observation"]]}

    def create_graph(self, show_labels=False) -> None:
        """Creates a graph from the parsed design space.
        """
        self.graph.clear()
        nodes = list(self.nodes.keys())
        self.graph.add_nodes_from(nodes, fontsize=12, width=0.5, height=0.5)

        for (start, ends) in self.nodes.items():
            for (end, labels) in ends.items():
                if show_labels:
                    self.graph.add_edge(start, end, label=",".join(
                        [str(l) for l in sorted(labels)]), fontsize=12)
                else:
                    self.graph.add_edge(start, end)
        self.graph.layout("circo")

    def print(self, design_space, file_name="out", show_labels=False, args="-Gsize=10! -Gratio=\"expand\" -Gnodesep=.5") -> None:
        """Prints a graph in .png format.

            design_space: list of Holes
            file_name: name of file where the graph will be saved without the extention (e.g. file_name=file => file.png)
            args: string with Graphvix arguments to specify the output format
        """

        if not design_space:
            return

        self.parse(design_space)
        self.create_graph(show_labels=show_labels)

        dir = "/".join(file_name.split("/")[:-1])
        if not os.path.exists(dir):
            os.mkdir(dir)

        try:
            self.graph.draw(file_name + ".png", format="png", args=args)
        except:
            pass

    def __str__(self) -> str:
        return self.graph.string()
