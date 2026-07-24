from pathlib import Path
import json, networkx as nx

def main():
    G=nx.Graph();G.add_weighted_edges_from([('A','B',2),('B','C',1),('A','C',5),('C','D',2),('B','D',6)])
    T=nx.minimum_spanning_tree(G);save({'edges':[(a,b,d['weight']) for a,b,d in T.edges(data=True)],'total':T.size(weight='weight')})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
