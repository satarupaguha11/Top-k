import networkx as nx
import sys

def connected_subgraph_gml(input_graph_name):

	graph=nx.read_gml(input_graph_name)
	connected_graph=nx.connected_component_subgraphs(graph)[0]
	return connected_graph

def connected_subgraph_pajek(input_graph_name):

	graph=nx.read_pajek(input_graph_name)
	graph=graph.to_undirected()
	connected_graph=nx.connected_component_subgraphs(graph)[0]
	return connected_graph

def connected_subgraph_gexf(input_graph_name):

	graph=nx.read_gexf(input_graph_name)
	connected_graph=nx.connected_component_subgraphs(graph)[0]
	return connected_graph


