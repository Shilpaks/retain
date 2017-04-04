import algorithm.src.spaced_repetition as spaced_repetition
import algorithm.src.concept_graph as concept_graph

class User(object): 

	def __init__(self, name, email): 
		self.create_spaced_repetition_instance(name, email)

	def create_spaced_repetition_instance(self, name, email):
		num_emails_limit_per_day = 3
		

		GRAPH_PATH = "TEST"
		cg = concept_graph.ConceptGraph(GRAPH_PATH, True)
		course_concept_graph = cg.graph

		self.sr_instance = spaced_repetition.SpacedRepetition(num_emails_limit_per_day, name, email, course_concept_graph)





