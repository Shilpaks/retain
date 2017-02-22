import networkx as nx
import matplotlib.pyplot as plt

class ConceptGraph(object): 
	def __init__(self, graph_csv): 
		self.graph = nx.DiGraph()
		self.graph_csv = graph_csv
		self.create_graph()

	def create_graph(self): 
		with open(self.graph_csv) as f: 
			lines = f.readlines()[0].split("\r")
		for line in lines:
			split_line = line.split(",")
			source = split_line[0]
			destination = split_line[1]
			self.graph.add_node(source) 
			self.graph.add_node(destination) 
			self.graph.add_edge(source, destination)

	def get_concept_list(self): 
		return self.graph.nodes()

	def print_out_degrees(self): 
		for node in self.graph.nodes(): 
			print self.graph.degree(node)

	def visualize_graph(self): 
		layout = nx.spring_layout(concept_graph.graph)
		nx.draw_networkx_labels(concept_graph.graph, pos=layout)
		nx.draw(concept_graph.graph, pos=layout)
		plt.show()

GRAPH_PATH = "data/concept_graph.csv"
concept_graph = ConceptGraph(GRAPH_PATH)
concept_graph.visualize_graph()

