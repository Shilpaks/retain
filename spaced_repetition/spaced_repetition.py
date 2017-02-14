import time 

class SpacedRepetition(object): 

	def __init__(self, num_emails_limit_per_day, course_concept_graph, user_info):
		self.num_emails_limit_per_day = num_emails_limit_per_day # upper bound on the number of emails we can send a given user each day 
		self.course_concept_graph = course_concept_graph
		self.user_info = user_info

		concepts = self.course_concept_graph.nodes()

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

	def determine_concepts_for_the_day(self):
		todays_concepts_candidates = []
		for concept, time in self.concept_next_time_dict.iteritems():
			if has_time_passed(time): 
				todays_concepts_candidates.append(time)

	""" Determine whether @param time has passed (is smaller than the cur time)"""
	def has_time_passed(time): 
		curr_time = time.time() # current time in seconds
		return time < curr_time

	def determine_next_revisit_time(concept): 
		pass

"""
1) iterate through all of the concepts to figure out which concepts we should remind the student of today
2) a given concept is ready to be sent to a student if all of its dependencies have been understood (or attempted 3 times)
3) if a concept's dependency hasn't been understood and it's time for it to be sent to the user, find the "oldest/most ancesteral" dependency and send that 
concept instead. 
4) constantly update the retention of concepts. we never throw away concepts because we assume the student has understood/retained them 
5) more "fundamental" concepts have priority
"""