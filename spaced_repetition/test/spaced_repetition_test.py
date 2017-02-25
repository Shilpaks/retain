import sys
sys.path.append('../')
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



