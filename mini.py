import argparse
import networkx as nx
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script which shows minimum flow in given graph")
    parser.add_argument("nodes_file", help="File which contain nodes and their demands")
    parser.add_argument("edges_file", help="File which contain edges with their weights and capacities")
    args = parser.parse_args()
    #we need directed graph
    G = nx.DiGraph()
    #load nodes[0] and their demands[1]
    with open(args.nodes_file) as nodes:
        for data in nodes:
            node_demand = data.split(" ")
            G.add_node(node_demand[0], demand=int(node_demand[1]))
    #load edges with their data
    with open(args.edges_file) as edges:
        for data in edges:
            edge_data = data.split(" ")
            G.add_edge(edge_data[0], edge_data[1], capacity=int(edge_data[2]), weight=int(edge_data[3]))

    flow_cost, flow_dict = nx.network_simplex(G)
    print "Flow cost : " + str(flow_cost)

    for verticle, neighbours in flow_dict.iteritems():
        for neighbour, weight in neighbours.iteritems():
            print "From: %s to: %s weight: %s" %(verticle, neighbour, weight)
