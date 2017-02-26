import time 
from collections import Counter

class SpacedRepetition(object): 

	def __init__(self, num_emails_limit_per_day, user_info, course_concept_graph, reverse_course_concept_graph):
		self.num_emails_limit_per_day = num_emails_limit_per_day # upper bound on the number of emails we can send a given user each day 
		self.course_concept_graph = course_concept_graph
		self.reverse_course_concept_graph = reverse_course_concept_graph
		self.user_info = user_info

		self.concepts = self.course_concept_graph.nodes()

		self.concept_next_time_dict = {} # map concept to a time (the next time user should be reminded of concept)
		self.initialize_dict_with_concepts(self.concept_next_time_dict, None)

		self.concept_retention_rating_dict = {}
		self.initialize_dict_with_concepts(self.concept_retention_rating_dict, 0) # map concept to integer measure of user's retention of concept

		self.concept_comprehension_rating_dict = {}
		self.initialize_dict_with_concepts(self.concept_comprehension_rating_dict, 0)

		self.COMPREHENSION_SCORE_THRESHOLD = 3 # based on a 1 to 5 scale

	def initialize_dict_with_concepts(self,dictionary, intial_value): 
		for concept in self.concepts:
			dictionary[concept] = intial_value

	def determine_concepts_for_the_day(self):
		todays_concepts_candidates = []
		for concept, time in self.concept_next_time_dict.iteritems():
			if has_time_passed(time): 
				todays_concepts_candidates.append(time)

	def populate_concept_ancestor_distance_dict(self):
		self.concept_ancestor_distance_dict = {}
		for concept in self.concepts:
			distance_dict = self.do_bfs_with_layers(concept)
			self.concept_ancestor_distance_dict[concept] = distance_dict
		print self.concept_ancestor_distance_dict


	def do_bfs_with_layers(self, concept):
		""" do a bfs through the concept graph starting at @param concept. populate num_dependent_timely_concept_dict. 
		@return num_dependent_timely_concept_dict i """ 

		visited = set()
		distance_dict = {concept : 0}
		queue = [concept]
		while len(queue) > 0: 
			cur_node = queue.pop(0)
			for neighbor in self.course_concept_graph.neighbors(cur_node): 
				if neighbor not in visited:
					distance_dict[neighbor] = distance_dict[cur_node] + 1
					queue.append(neighbor)
					visited.add(neighbor)
		return distance_dict

	def has_time_passed(self, time):
		""" Determine whether @param time has passed (is smaller than the cur time)"""
		
		curr_time = time.time() # current time in seconds
		return time < curr_time

	def is_timely_concept(self, concept):
		return self.has_time_passed(self.concept_next_time_dict[concept])

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

	def return_concept_from_list_with_lowest_ret_comp_score(concept_candidates): 
		""" Iterate through all of the concepts in concept_candidates. Return the concept with the lowest ret-comp score. 
		    ret-comp score = retention_score + comprehension_score  """ 

		if len(concept_candidates) == 0: 
			return None
		elif len(concept_candidates) == 0: 
			return concept_candidates.pop()
		else: 
			ret_comp_score_dict = dict(Counter(self.concept_retention_rating_dict) + Counter(self.concept_comprehension_rating_dict))
			return min(ret_comp_score_dict, key=ret_comp_score_dict.get) #return concept with lowest ret-comp score

	def determine_rank_for_concept(self, ancestor_distance_aggregate):
		return dist_aggregate + (1.0 / (1.0 + self.concept_comprehension_rating_dict[k]))
	
	# def determine_todays_concepts(timely_concepts):
	# 	todays_concepts = []
	# 	aggregate_concept_ancestor_distance_dict = Counter()
	# 	for concept in timely_concepts:
	# 		aggregate_concept_ancestor_distance_dict += Counter(self.concept_ancestor_distance_dict[concept])

	# 	aggregate_concept_ancestor_distance_dict = {ancestor : self.determine_rank_for_concept(dist_aggregate) for (ancestor, dist_aggregate) in aggregate_concept_ancestor_distance_dict}

	# 	for concept in timely_concepts:
	# 		ancestors = self.concept_ancestor_distance_dict.keys()
	# 		for ancestor in ancestors: 




"""
1) iterate through all of the concepts to figure out which concepts we should remind the student of today
2) a given concept is ready to be sent to a student if all of its dependencies have been understood (or attempted 3 times)
3) if a concept's dependency hasn't been understood and it's time for it to be sent to the user, find the "oldest/most ancesteral" dependency and send that 
concept instead. 
4) constantly update the retention of concepts. we never throw away concepts because we assume the student has understood/retained them 
5) more "fundamental" concepts have priority
"""



