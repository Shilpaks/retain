import time 
import copy
import compute_next_interval

class SpacedRepetition(object): 

	def __init__(self, num_emails_limit_per_day, user_name, email_addr, course_concept_graph):

		# upper bound on the number of emails we can send a given user each day 
		self.num_emails_limit_per_day = num_emails_limit_per_day 

		self.course_concept_graph = course_concept_graph
		self.user_name = user_name
		self.email_addr = email_addr

		self.concepts = self.course_concept_graph.nodes()

		# map concept to a time (the next time user should be reminded of concept)
		self.concept_next_time_dict = {} 
		
		self.initialize_dict_with_concepts(self.concept_next_time_dict, None)

		self.concept_retention_rating_dict = {}

		# map concept to integer measure of user's retention of concept
		self.initialize_dict_with_concepts(self.concept_retention_rating_dict, 0) 

		self.concept_comprehension_rating_dict = {}
		self.initialize_dict_with_concepts(self.concept_comprehension_rating_dict, 0)

		self.COMPREHENSION_SCORE_THRESHOLD = 3 # based on a 1 to 5 Likert scale

		self.MAX_COMPREHENSION_SCORE = 5

		self.compute_next_interval = compute_next_interval.ComputeNextInterval(self.concepts)

		self.populate_concept_ancestor_distance_dict()

	""" INITIALIZATON """ 

	def initialize_dict_with_concepts(self, dictionary, intial_value): 
		for concept in self.concepts:
			dictionary[concept] = intial_value

	def populate_concept_ancestor_distance_dict(self):
		self.concept_ancestor_distance_dict = {}
		for concept in self.concepts:
			distance_dict = self.do_bfs_with_layers(concept)
			self.concept_ancestor_distance_dict[concept] = distance_dict
		return self.concept_ancestor_distance_dict

	def do_bfs_with_layers(self, concept):
		""" do a bfs through the concept graph starting at @param concept. 
		return a dict that gives distances from concept to each ancestor """ 

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

	""" UTILITY METHODS FOR RANKING ALGORITHM """ 

	def has_time_passed(self, concept_time):
		""" Determine whether @param time has passed (is smaller than the cur time)"""
		
		curr_time = time.time() # current time in seconds
		return concept_time < curr_time

	def is_timely_concept(self, concept):
		return self.has_time_passed(self.concept_next_time_dict[concept])

	def has_low_comprehension_score(self, concept): 
		""" checks if simulated concept_comprehension_rating_dict has a low comprehension score for @param concept """
		return self.concept_comprehension_rating_dict_simulation[concept] < self.COMPREHENSION_SCORE_THRESHOLD

	def get_all_timely_concepts(self):
		""" return a list of all timely concepts sorted by next_time values -- ordered earliest to latest """ 

		all_timely_concepts = []
		for concept in self.concepts: 
			if self.is_timely_concept(concept):
				all_timely_concepts.append(concept)
		all_timely_concepts.sort(key=lambda x : self.concept_next_time_dict[x])
		return all_timely_concepts

	def assign_next_revisit_time(self, concept, retention_score): 
		""" assign a new revisit time for a @param concept. change this later with spaced repetition equations """ 

		self.concept_next_time_dict[concept] = self.compute_next_interval.generate_next_interval(concept, retention_score)

	def return_ancestors_with_low_comprehension_scores(self, concept): 
		""" for a given concept, @param concept, return all of the ancestors that have comprehension scores below
		 COMPREHENSION_SCORE_THRESHOLD in the simulated concept_comprehension_rating_dict """
		all_ancestors = self.concept_ancestor_distance_dict[concept].keys()
		return set([ancestor for ancestor in all_ancestors \
			if self.has_low_comprehension_score(ancestor)])
	
	def compute_aggregate_concept_ancestor_distance_dict(self, T_union_lowC):
		aggregate_concept_ancestor_distance_dict = {}
		for concept in T_union_lowC:
			aggregate_concept_ancestor_distance_dict.update(self.concept_ancestor_distance_dict[concept])
		return aggregate_concept_ancestor_distance_dict

	def compute_lowC_set(self, timely_concept_set):
		""" LowC is the set of concepts that depend on C that have low C-scores. 
		Additionally, each concept in LowC has at least one concept in T 
		(the set of timely concepts) that depends on it. """

		low_c_set = set()
		for concept in timely_concept_set:
			low_comprehension_score_ancestors = self.return_ancestors_with_low_comprehension_scores(concept)
			low_c_set.update(low_comprehension_score_ancestors)
		return low_c_set

	def satisfies_recommendation_membership_requirements(self, concept, chosen_concepts): 
		""" @return true if is timely concept or has a low comprehension score and has not yet been chosen """ 
		is_timely = self.is_timely_concept(concept)
		has_low_comprehension_score = self.has_low_comprehension_score(concept)
		has_been_chosen = True if concept in chosen_concepts else False
		return (is_timely or has_low_comprehension_score) and not has_been_chosen

	def determine_next_concept_for_the_day(self, chosen_concepts):
		""" determine the next best concept to send today. 
		@param chosen_concepts is a list of concepts that have already been chosen """ 

		todays_concepts = []
		T = set(self.get_all_timely_concepts()) # timely concepts 
		lowC = self.compute_lowC_set(T)
		T_union_lowC = T.union(lowC) - chosen_concepts
		aggregate_concept_ancestor_distance_dict = self.compute_aggregate_concept_ancestor_distance_dict(T_union_lowC)

		# remove exculuded concpets from dictionary
		# we do this because we need to make sure that we don't choose a concept that has already been chosen
		aggregate_concept_ancestor_distance_dict = \
			{key: aggregate_concept_ancestor_distance_dict[key] \
				for key in aggregate_concept_ancestor_distance_dict \
					if self.satisfies_recommendation_membership_requirements(key, chosen_concepts)} 
					  
		sorted_ancestral_concept_dist_pairs = \
			sorted(aggregate_concept_ancestor_distance_dict.items(), key=lambda x : x[1], reverse=True)
		chosen_ancestral_concept_dist_pairs = sorted_ancestral_concept_dist_pairs[:self.num_emails_limit_per_day]
		
		# list of only the first value (the concept) in each tuple
		ranked_concepts =  \
			[concept_distance_pair[0] for concept_distance_pair in chosen_ancestral_concept_dist_pairs] 

		if len(ranked_concepts) > 0: 
			chosen_concept = ranked_concepts.pop(0)
			self.artificially_set_comprehension_score_for_chosen_concept(chosen_concept)
			return chosen_concept
		else: 
			return None

	def determine_concepts_for_the_day(self): 
		todays_concepts_ordered_list = []
		self.concept_comprehension_rating_dict_simulation = copy.deepcopy(self.concept_comprehension_rating_dict)
		while len(todays_concepts_ordered_list) < self.num_emails_limit_per_day:
			next_concept = self.determine_next_concept_for_the_day(set(todays_concepts_ordered_list))
			if next_concept is not None: 
				todays_concepts_ordered_list.append(next_concept)
			else: 
				return todays_concepts_ordered_list

		return todays_concepts_ordered_list

	def artificially_set_comprehension_score_for_chosen_concept(self, concept):
		""" Once we choose a concept, the algorithm dictates that we choose the 
		rest of the concepts for today under the assumption 
		that this @param concept was perfectly comprehended (has a perfect comprehension score). 
		In this method, we set artificially set the comprehension of 
		a chosen concept to a high value (perfect score - 5) """

		self.concept_comprehension_rating_dict_simulation[concept] = self.MAX_COMPREHENSION_SCORE

	""" REGISTER STUDENT FEEDBACK """ 

	def add_concept(self, concept, comprehension_score):
		if concept not in self.concept_next_time_dict: 
			return "Invalid Concept"
		elif self.concept_next_time_dict[concept] is None:
			self.concept_next_time_dict[concept] = self.compute_next_interval.gen_next_interval_for_new_concept(concept)
			self.concept_comprehension_rating_dict[concept] = comprehension_score
			return "Concept was successfully added."
		else: 
			return "Error: concept has already been added."

	def revisit_concept(self, concept, comprehension_score, retention_score):
		if concept not in self.concept_next_time_dict: 
			return "Invalid Concept"
		elif self.concept_next_time_dict[concept] is None: 
			return "Error: concept has not yet been added"
		else: 
			self.assign_next_revisit_time(concept, retention_score)
			self.concept_comprehension_rating_dict[concept] = comprehension_score
			self.concept_retention_rating_dict[concept] = retention_score
			return "Concept successfully revisited."
