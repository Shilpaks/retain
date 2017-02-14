class user(object): 

	def __init__(self, name, email_address, concepts):
		self.name = name 
		self.email_address = email_address
		
		self.concept_next_time_dict = {} # map concept to a time (the next time user should be reminded of concept)
		self.initialize_concept_next_time_dict(concepts)

		self.concept_retention_rating_dict = {}
		self.initialize_concept_retention_rating_dict(concepts) # map concept to integer measure of user's retention of concept

	def initialize_concept_next_time_dict(self, concepts): 
		for concept in concepts:
			self.concept_next_time_dict[concept] = None

	def initialize_concept_retention_rating_dict(self, concepts):
		for concept in concepts: 
			self.concept_next_time_dict[concept] = 0


