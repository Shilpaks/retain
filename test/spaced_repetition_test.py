import time
import sys
sys.path.append('src/')

import spaced_repetition
import concept_graph

""" Set up methods """ 
""""""""""""""""""""""""

def set_up_for_concept_ancestor_tests():
	GRAPH_PATH = "TEST"
	cg = concept_graph.ConceptGraph(GRAPH_PATH, True)

	num_emails_limit_per_day = 3
	user_info = None
	course_concept_graph = cg.graph
	reverse_course_concept_graph = None 

	sr = spaced_repetition.SpacedRepetition(num_emails_limit_per_day, user_info, course_concept_graph, reverse_course_concept_graph)
	sr.populate_concept_ancestor_distance_dict()
	return sr 

""" Testing methods """ 
""""""""""""""""""""""""

def test_bfs_with_layers():
	sr = set_up_for_concept_ancestor_tests()
	distance_dict = sr.do_bfs_with_layers("G")
	assert distance_dict == {"A" : 2, "B" : 2, "C" : 1, "D" : 1, "G" : 0}

def test_populate_concept_ancestor_distance_dict():
	sr = set_up_for_concept_ancestor_tests()
	concept_ancestor_distance_dict = sr.populate_concept_ancestor_distance_dict()
	assert concept_ancestor_distance_dict == {'A': {'A': 0}, 'C': {'A': 1, 'C': 0}, 'B': {'B': 0}, 'E': {'B': 1, 'E': 0}, 'D': {'A': 1, 'B': 1, 'D': 0}, 'G': {'A': 2, 'C': 1, 'B': 2, 'D': 1, 'G': 0}, 'F': {'A': 2, 'C': 1, 'F': 0}, 'H': {'H': 0, 'B': 2, 'E': 1}}

def test_compute_aggregate_concept_ancestor_distance_dict():
	sr = set_up_for_concept_ancestor_tests()

	lowC = set(["A", "B", "C"])
	T = set(["F", "H"])
	T_union_lowC = lowC.union(T)

	aggregate_concept_ancestor_distance_dict = sr.compute_aggregate_concept_ancestor_distance_dict(T_union_lowC)
	assert aggregate_concept_ancestor_distance_dict == {'A': 2, 'C': 1, 'B': 0, 'E': 1, 'F': 0, 'H': 0}

def test_compute_lowC_set(): 
	sr = set_up_for_concept_ancestor_tests()

	timely_concept_set = ["F"]
	sr.concept_comprehension_rating_dict_simulation = {"A": 2, "B": 1, "C": 5, "D": 2, "E" : 2, "F": 1, "G": 2, "H": 1}
	lowC_set = sr.compute_lowC_set(set(timely_concept_set))
	assert lowC_set == set(["A", "F"])

def test_determine_next_concept_for_the_day(): 
	sr = set_up_for_concept_ancestor_tests()
	LARGE_NUMBER = sys.maxint 
	SMALLER_NUMBER = 1
	SMALLEST_NUMBER = 0
	sr.concept_comprehension_rating_dict_simulation = {"A": 2, "B": 1, "C": 5, "D": 2, "E" : 2, "F": 1, "G": 2, "H": 1}
	sr.concept_next_time_dict = {"A" : LARGE_NUMBER, "B": LARGE_NUMBER, "C" : LARGE_NUMBER, "D": LARGE_NUMBER, "E" : LARGE_NUMBER, "F": LARGE_NUMBER, "G": SMALLER_NUMBER, "H":  SMALLEST_NUMBER}
	assert sr.determine_next_concept_for_the_day(set()) == "A"

def test_determine_concepts_for_the_day_1(): 
	sr = set_up_for_concept_ancestor_tests()
	LARGE_NUMBER = sys.maxint 
	SMALLER_NUMBER = 1
	SMALLEST_NUMBER = 0
	sr.concept_comprehension_rating_dict = {"A": 2, "B": 1, "C": 5, "D": 2, "E" : 2, "F": 1, "G": 2, "H": 1}
	sr.concept_next_time_dict = {"A" : LARGE_NUMBER, "B": LARGE_NUMBER, "C" : LARGE_NUMBER, "D": LARGE_NUMBER, "E" : LARGE_NUMBER, "F": LARGE_NUMBER, "G": SMALLER_NUMBER, "H":  SMALLEST_NUMBER}
	assert sr.determine_concepts_for_the_day() == ["A", "B", "D"]
	sr.num_emails_limit_per_day = 5
	assert sr.determine_concepts_for_the_day() == ['A', 'B', 'D', 'H', 'E']
	
def test_determine_concepts_for_the_day_2(): 
	sr = set_up_for_concept_ancestor_tests()
	LARGE_NUMBER = sys.maxint 
	SMALLER_NUMBER = 1
	SMALLEST_NUMBER = 0
	sr.concept_comprehension_rating_dict = {"A": 2, "B": 1, "C": 5, "D": 2, "E" : 2, "F": 1, "G": 2, "H": 1}
	sr.concept_next_time_dict = {"A" : LARGE_NUMBER, "B": LARGE_NUMBER, "C" : LARGE_NUMBER, "D": LARGE_NUMBER, "E" : LARGE_NUMBER, "F": LARGE_NUMBER, "G": SMALLER_NUMBER, "H":  SMALLEST_NUMBER}
	sr.num_emails_limit_per_day = 5
	assert sr.determine_concepts_for_the_day() == ['A', 'B', 'D', 'H', 'E']
