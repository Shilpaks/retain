import time 

class SpacedRepetition(object): 

	def __init__(self, num_emails_limit_per_day, course_concept_graph, user_info):
		self.num_emails_limit_per_day = num_emails_limit_per_day # upper bound on the number of emails we can send a given user each day 
		self.course_concept_graph = course_concept_graph
		self.user_info = user_info

		concepts = self.course_concept_graph.nodes()

		self.concept_next_time_dict = {} # map concept to a time (the next time user should be reminded of concept)
		self.initialize_dict_with_concepts(concepts, self.concept_next_time_dict, None)

		self.concept_retention_rating_dict = {}
		self.initialize_dict_with_concepts(concepts, self.concept_retention_rating_dict, 0) # map concept to integer measure of user's retention of concept

		self.concept_comprehension_rating_dict = {}
		self.initialize_dict_with_concepts(concepts, self.concept_comprehension_rating_dict, 0)

	def initialize_dict_with_concepts(self, concepts, dictionary, intial_value): 
		for concept in concepts:
			dictionary[concept] = intial_value

	def determine_concepts_for_the_day(self):
		todays_concepts_candidates = []
		for concept, time in self.concept_next_time_dict.iteritems():
			if has_time_passed(time): 
				todays_concepts_candidates.append(time)

	def has_time_passed(self, time):
		""" Determine whether @param time has passed (is smaller than the cur time)"""
		
		curr_time = time.time() # current time in seconds
		return time < curr_time

	def assign_next_revisit_time(self, concept): 
		""" change this later with spaced repetition equations """ 

		curr_time = time.time()
		one_day_in_seconds = 60*60*24
		self.concept_next_time_dict[concept] = curr_time + one_day_in_seconds

	def register_student_feedback(self, concept, comprehension_score, retention_score):
	""" concept: the name of the concept that the student is providing feedback on 
		comprehension_score: integer score that represents the student's comprehension of the concept
		retention_score: integer score that represents the student's retention of the concept """

		self.concept_comprehension_rating_dict[concept] = comprehension_score # in the future, keep track of all scores for analytics 
		self.concept_retention_rating_dict[concept] = retention_score # in the future, keep track of all scores for analytics 

	def update_student_information(self, concept, comprehension_score, retention_score):
		""" Upon recieving feedback from a student about a concept we recently reminded them of, update the respective information about the student """
		
		self.assign_next_revisit_time()
		self.register_student_feedback(concept, comprehension_score, retention_score)

	def find_ancesteral_path(concept): 
		# parent_dict = {}
		pass 

"""
1) iterate through all of the concepts to figure out which concepts we should remind the student of today
2) a given concept is ready to be sent to a student if all of its dependencies have been understood (or attempted 3 times)
3) if a concept's dependency hasn't been understood and it's time for it to be sent to the user, find the "oldest/most ancesteral" dependency and send that 
concept instead. 
4) constantly update the retention of concepts. we never throw away concepts because we assume the student has understood/retained them 
5) more "fundamental" concepts have priority
"""