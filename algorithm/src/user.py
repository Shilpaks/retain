import spaced_repetition
import compute_next_interval

class User(object): 
	def __init__(self, user_name, email_addr, concept_graph):
		self.name = name 
		self.email_address = email_address
		self.spaced_repetition = SpacedRepetition(num_emails_limit_per_day, user_name, email_addr, course_concept_graph, reverse_course_concept_graph)
		self.compute_next_interval = ComputeNextInterval()
		
