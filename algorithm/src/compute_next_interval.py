import time

class ComputeNextInterval(object):

 	def __init__(self, concepts): 
 		self.concepts = concepts

	 	self.easiness_score_concept_dict = {}
		DEFAULT_EASINESS_SCORE = 2.5
		self.initialize_dict_with_concepts(self.easiness_score_concept_dict, DEFAULT_EASINESS_SCORE)
	
		self.consecutive_success_dict = {}
		DEFAULT_CONSECUTIVE_SUCCESS_NUM = 0
		self.initialize_dict_with_concepts(self.consecutive_success_dict, DEFAULT_CONSECUTIVE_SUCCESS_NUM)

		self.PERFORMACE_RATING_SUCCESS_THRESHOLD = 3 # if a performance rating is >= 3, we consider this a "success"
		
		self.ALMOST_ONE_DAY_IN_SECONDS = 60 * 60 * 23
		
 	def initialize_dict_with_concepts(self, dictionary, intial_value): 
		for concept in self.concepts:
			dictionary[concept] = intial_value

	# def generate_next_review_time(self, concept, retention_score):
	# 	easiness_score = -0.8 + (0.28 * retention_score) + (0.02 * pow(retention_score, 2))
	# 	concept_was_successfully_retained = retention_score >= self.PERFORMACE_RATING_SUCCESS_THRESHOLD
	# 	self.consecutive_success_dict[concept] = \
	# 		self.consecutive_success_dict[concept] + 1 if concept_was_successfully_retained else 0

	# 	now_in_seconds = time.time()

	# 	if concept_was_successfully_retained: 
	# 		next_review_time = now_in_seconds + (6 * pow(easiness_score, self.consecutive_success_dict[concept] - 1))
	# 		return next_review_time
	# 	else: 
	# 		next_review_time =  now_in_seconds + self.ONE_DAY_IN_SECONDS
	# 		return next_review_time

	def gen_next_interval_for_new_concept(self, concept):
		return time.time() + self.ALMOST_ONE_DAY_IN_SECONDS

	def generate_next_interval(self, concept, retention_score): 
		curr_time = time.time()
		return curr_time + self.ALMOST_ONE_DAY_IN_SECONDS