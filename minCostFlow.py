"""
Originally written by Anthony Gitter
Edited by Chris Magnano for batch use

This script attempts to connect sources to targets in a graph
using a minimum-cost flow algorithm. Minimum cost flow is solved using
Google's OR-Tools library: https://developers.google.com/optimization/flow/mincostflow

updated to use python 3
"""
import argparse
from ortools.graph.python.min_cost_flow import SimpleMinCostFlow

# (node1, node2) : weight
directed_dict = dict()
undirected_dict = dict()

def parse_nodes(node_file):
    ''' Parse a list of sources or targets and return a set '''
    with open(node_file) as node_f:
        lines = node_f.readlines()
        nodes = set(map(str.strip, lines))
    return nodes


def construct_digraph(edges_file, cap):
    ''' Parse a list of weighted undirected edges.  Construct a weighted
    directed graph in which an undirected edge is represented with a pair of
    directed edges.  Use the specified weight as the edge weight and a default
    capacity of 1.
    '''
    G = SimpleMinCostFlow()
    idDict = dict() # Hold names to number ids
    curID = 0
    default_capacity = int(cap)

    with open(edges_file) as edges_f:
        for line in edges_f:
            tokens = line.strip().split()
            node1 = tokens[0]
            if not node1 in idDict:
                idDict[node1] = curID
                curID += 1
            node2 = tokens[1]
            if not node2 in idDict:
                idDict[node2] = curID
                curID += 1
            # Google's solver can only handle int weights, so round to the 100th 
            w = int((1-(float(tokens[2])))*100) # lower the weight from token[2], higher the cost
            d = tokens[3]
            edge = (node1, node2)
            sorted_edge = tuple(sorted(edge))
            
            if d == "D":
                if edge in directed_dict:
                    if w < directed_dict[edge]:
                        directed_dict[edge] = w
                elif sorted_edge in undirected_dict:
                    del undirected_dict[sorted_edge]
                    directed_dict[edge] = w
                else: # edge not in directed_dict 
                    directed_dict[edge] = w

            elif d == "U":
                if edge not in directed_dict and sorted_edge not in directed_dict and sorted_edge not in undirected_dict:
                    undirected_dict[sorted_edge] = w
                elif sorted_edge in undirected_dict:
                    if w < undirected_dict[sorted_edge]:
                        undirected_dict[sorted_edge] = w
            else:
                raise ValueError (f"Cannot add edge: d = {d}")

    # print("undirected_dict: ", undirected_dict)
    # print("directed_dict: ", directed_dict)
    # go through and add the edges from directed_dict and undirected_dict to G
    for key, value in directed_dict.items():
        G.add_arc_with_capacity_and_unit_cost(idDict[key[0]],idDict[key[1]], default_capacity, int(value))
    for key, value in undirected_dict.items():
        G.add_arc_with_capacity_and_unit_cost(idDict[key[0]],idDict[key[1]], default_capacity, int(value))
        G.add_arc_with_capacity_and_unit_cost(idDict[key[1]],idDict[key[0]], default_capacity, int(value))
    
    idDict["maxID"] = curID
    return G,idDict


def print_graph(graph):
    ''' Print the edges in a graph '''
    print('\n'.join(sorted(map(str, graph.edges(data=True)))))


def add_sources_targets(G, sources, targets, idDict, flow):
    ''' Similar to ResponseNet, add an artificial source node that is connected
    to the real source nodes with directed edges.  Unlike ResponseNet, these
    directed edges should have weight of 0 and Infinite capacity.  Also add an
    artificial target node that has directed edges from the real target nodes
    with the same weights and capacities as the source node edges.  The new
    nodes must be named "source" and "target".
    '''
    default_weight = 0
    default_capacity = flow*10
    curID = idDict["maxID"]
    idDict["source"] = curID
    curID += 1
    idDict["target"] = curID

    for source in sources:
        if source in idDict:
            G.add_arc_with_capacity_and_unit_cost(idDict["source"],idDict[source], default_capacity, default_weight)

    for target in targets:
        if target in idDict:
            G.add_arc_with_capacity_and_unit_cost(idDict[target],idDict["target"], default_capacity, default_weight)


def write_output_to_sif(G,out_file_name,idDict):
    ''' Convert a flow dictionary from networkx.min_cost_flow into a list
    of directed edges with the flow.  Edges are represented as tuples.
    '''

    out_file = open(out_file_name,"w")
    names = {v: k for k, v in idDict.items()}
    numE = 0
    for i in range(G.num_arcs()):
        node1 = names[G.tail(i)]
        node2 = names[G.head(i)]
        
        flow = G.flow(i)
        if flow <= 0:
            continue
        if node1 in ["source","target"]:
            continue
        if node2 in ["source","target"]:
            continue
        numE+=1

        edge = (node1, node2)
        sorted_edge = tuple(sorted(edge))

        if edge in directed_dict:
            out_file.write(node1+"\t"+node2+"\t"+"D"+"\n")
        elif sorted_edge in undirected_dict:
            out_file.write(node1+"\t"+node2+"\t"+"U"+"\n")
        else: 
            raise KeyError(f"edge {edge} is not in the dicts")
        
    print("Final network had %d edges" % numE)
    out_file.close()

    return

def min_cost_flow(G, flow, output, idDict):
    ''' Use the min cost flow algorithm to distribute the specified amount
    of flow from sources to targets.  The artificial source should have
    demand = -flow and the traget should have demand = flow.  output is the
    filename of the output file.  The graph should have artificial nodes
    named "source" and "target".
    '''
    G.set_node_supply(idDict['source'],int(flow))
    G.set_node_supply(idDict['target'],int(-1*flow))

    print("Computing min cost flow")
    if G.solve() == G.OPTIMAL:
        print("Solved!")
    else:
        print("There was an issue with the solver")
        return

    write_output_to_sif(G,output,idDict)

def main(args):
    ''' Parse a weighted edge list, source list, and target list.  Run
    min cost flow or k-shortest paths on the graph to find source-target
    paths.  Write the solutions to a file.
    '''
    flow = int(args.flow)

    sources = parse_nodes(args.sources_file)

    targets = parse_nodes(args.targets_file)

    G,idDict = construct_digraph(args.edges_file, args.capacity)

    add_sources_targets(G, sources, targets, idDict, flow)

    out_file = args.output+"_flow"+str(flow)+"_c"+str(args.capacity)+".sif"
    min_cost_flow(G, flow, out_file, idDict)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--edges_file',
                        help='Network file. File should be in SIF file format.',
                        type=str,
                        required=True)
    parser.add_argument('--sources_file',
                        help='File which denotes source nodes, with one node per line.',
                        type=str,
                        required=True)
    parser.add_argument('--targets_file',
                        help='File which denotes source nodes, with one node per line.',
                        type=str,
                        required=True)
    parser.add_argument('--flow',
                        help='The amount of flow pushed through the network.',
                        type=int,
                        required=False,
                        default=1)
    parser.add_argument('--output',
                        help='Prefix for all output files.',
                        type=str,
                        required=True)
    parser.add_argument('--capacity',
                        help='The amount of flow which can pass through a single edge.',
                        type=float,
                        required=False,
                        default=1.0)

    args = parser.parse_args()
main(args)
