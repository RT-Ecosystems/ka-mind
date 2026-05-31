"""
Vector Graph - भाषा के बजाय 'अर्थ' (Meaning) से डेटा खोजना।
"""
from sentence_transformers import util
from ka_mind.core.vector_atom import VectorAtom

class VectorGraph:
    def __init__(self):
        self.graph = {}

    def add_atom(self, atom: VectorAtom):
        self.graph[atom.atom_id] = atom

    def search_by_meaning(self, query: str):
        """
        यूजर किसी भी भाषा में सवाल पूछे, यह नंबरों (Vectors) को मैच करके सही जवाब ढूंढेगा!
        """
        query_vector = VectorAtom.encoder.encode(query)
        
        best_match = None
        highest_score = 0.0
        
        for atom in self.graph.values():
            # गणित के ज़रिए अर्थ मैच करना (Cosine Similarity)
            score = util.cos_sim(query_vector, atom.vector).item()
            if score > highest_score:
                highest_score = score
                best_match = atom
                
        return best_match, highest_score
