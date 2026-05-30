"""
Graph Memory Engine - Atoms को आपस में जोड़ने वाला नेटवर्क
"""
import networkx as nx
from typing import List, Dict

class GraphMemory:
    def __init__(self):
        # MultiDiGraph का उपयोग ताकि दो Atoms के बीच कई तरह के रिश्ते हो सकें
        self.graph = nx.MultiDiGraph()
        
    def add_atom(self, atom) -> bool:
        """ग्राफ में एक नया Knowledge Atom जोड़ें। डुप्लीकेट होने पर इग्नोर करें।"""
        if atom.atom_id not in self.graph:
            self.graph.add_node(atom.atom_id, **atom.to_dict())
            return True
        return False

    def add_relation(self, source_id: str, target_id: str, relation_type: str, weight: float = 1.0):
        """दो Atoms के बीच कारण (Cause/Effect) या लॉजिक का रिश्ता बनाएं।"""
        if source_id in self.graph and target_id in self.graph:
            self.graph.add_edge(source_id, target_id, relation=relation_type, weight=weight)

    def retrieve_context(self, start_atom_id: str, depth: int = 2) -> List[Dict]:
        """Multi-hop Reasoning: एक एटम से जुड़े आस-पास के सभी एटम्स ढूँढें (Depth-limit के साथ)"""
        if start_atom_id not in self.graph:
            return []
        
        # ego_graph उस नोड के आस-पास का पूरा 'मोहल्ला' निकाल लेता है
        subgraph = nx.ego_graph(self.graph, start_atom_id, radius=depth)
        return list(subgraph.nodes(data=True))

    def memory_stats(self) -> dict:
        return {
            "total_atoms": self.graph.number_of_nodes(),
            "total_relations": self.graph.number_of_edges()
        }
