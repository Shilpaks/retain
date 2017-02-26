import networkx as nx
import matplotlib.pyplot as plt

class ConceptGraph(object): 
	def __init__(self, graph_csv, is_test): 
		self.graph_csv = graph_csv
		if is_test:
			self.create_test_graph()
		else: 
			self.create_graph()
			self.create_reversed_graph()

	def create_graph(self):
		""" Edges go from children to parents """

		self.graph = nx.DiGraph()
		with open(self.graph_csv) as f: 
			lines = f.readlines()[0].split("\r")
		for line in lines:
			split_line = line.split(",")
			source = split_line[0]
			destination = split_line[1]
			self.graph.add_node(source) 
			self.graph.add_node(destination) 
			self.graph.add_edge(source, destination)
		print self.graph.edges()

	def create_reversed_graph(self):
		""" Edges go from parents to children """ 

		self.reversed_graph = nx.DiGraph()
		with open(self.graph_csv) as f: 
			lines = f.readlines()[0].split("\r")
		for line in lines:
			split_line = line.split(",")
			source = split_line[1]
			destination = split_line[0]
			self.reversed_graph.add_node(source) 
			self.reversed_graph.add_node(destination) 
			self.reversed_graph.add_edge(source, destination)

	def create_test_graph(self): 
		self.graph = nx.DiGraph()
		self.graph.add_nodes_from(["A", "B", "C", "D", "E", "F", "G", "H"])
		self.graph.add_edges_from([("C", "A"), ("D", "A"), ("D", "B"), ("E", "B"), ("F", "C"), ("G", "C"), ("G", "D"), ("H", "E")])

	def get_concept_list(self): 
		return self.graph.nodes()

	def visualize_graph(self): 
		layout = nx.spring_layout(concept_graph.graph)
		nx.draw_networkx_labels(concept_graph.graph, pos=layout)
		nx.draw(concept_graph.graph, pos=layout)
		plt.show()

# GRAPH_PATH = "data/concept_graph.csv"
# concept_graph = ConceptGraph(GRAPH_PATH, True)
# concept_graph.visualize_graph()


