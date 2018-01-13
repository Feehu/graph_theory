import xml.etree.ElementTree as ET
import networkx as nx
import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GXL parser')
    parser.add_argument('graph_file', help='GXL file')
    args = parser.parse_args()
    tree = ET.parse(args.graph_file)

    graph = nx.Graph()
    
    for edge in tree.findall(".//edge"):
        try:
            graph.add_edge(edge.get("from"), edge.get("to"), weight=float(edge.find("attr").find("int").text))
        except:
            graph.add_edge(edge.get("from"), edge.get("to"))
    
    if not nx.is_connected(graph) or not nx.is_bipartite(graph):
        print "Graph is not connected/bipartite, algorithm won't work."
        exit(0)
        
    matching = nx.max_weight_matching(graph)
    
    print "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
    print "<!DOCTYPE gxl SYSTEM \"http://www.gupro.de/GXL/gxl-1.0.dtd\">"
    print "<!-- simple example 05.02.2002 -->"
    print "<gxl xmlns:xlink=\" http://www.w3.org/1999/xlink\">"
    print "  <graph id=\"BM\" edgeids=\"true\" edgemode=\"undirected\" hypergraph=\"false\">"

    nodes = [node.get("id") for node in tree.findall(".//node")]

    for node in nodes:
        print "    <node id=\"" + node + "\">"
        print "    </node>"

    for i, start in enumerate(matching):
        print "    <edge id=\"e" + str(i) + "\" to=\"" + str(start) + "\" from=\"" + str(matching[start]) + "\">"
        print "      <attr name=\"weight\">"
        print "        <float>" + str(graph[start][matching[start]]['weight']) + "</float>"
        print "      </attr>"
        print "    </edge>"
    print "  </graph>"
    print "</gxl>"

