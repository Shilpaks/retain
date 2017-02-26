import time
import sys
sys.path.append('src/')

import spaced_repetition
import concept_graph

def test_bfs_with_layers():
	GRAPH_PATH = "TEST"
	cg = concept_graph.ConceptGraph(GRAPH_PATH, True)

	num_emails_limit_per_day = None
	user_info = None
	course_concept_graph = cg.graph
	reverse_course_concept_graph = None 

	sr = spaced_repetition.SpacedRepetition(num_emails_limit_per_day, user_info, course_concept_graph, reverse_course_concept_graph)
	distance_dict = sr.do_bfs_with_layers("G")
	assert distance_dict == {"A" : 2, "B" : 2, "C" : 1, "D" : 1, "G" : 0}

def test_populate_concept_ancestor_distance_dict(): 
	GRAPH_PATH = "TEST"
	cg = concept_graph.ConceptGraph(GRAPH_PATH, True)

	num_emails_limit_per_day = None
	user_info = None
	course_concept_graph = cg.graph
	reverse_course_concept_graph = None 

	sr = spaced_repetition.SpacedRepetition(num_emails_limit_per_day, user_info, course_concept_graph, reverse_course_concept_graph)
	concept_ancestor_distance_dict = sr.populate_concept_ancestor_distance_dict()
	assert concept_ancestor_distance_dict == {'A': {'A': 0}, 'C': {'A': 1, 'C': 0}, 'B': {'B': 0}, 'E': {'B': 1, 'E': 0}, 'D': {'A': 1, 'B': 1, 'D': 0}, 'G': {'A': 2, 'C': 1, 'B': 2, 'D': 1, 'G': 0}, 'F': {'A': 2, 'C': 1, 'F': 0}, 'H': {'H': 0, 'B': 2, 'E': 1}}

