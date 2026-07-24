from pathlib import Path
import json, networkx as nx

def main():
    G=nx.Graph();G.add_weighted_edges_from([('A','B',2),('B','C',1),('A','C',5),('C','D',2),('B','D',6)])
    save({'path':nx.shortest_path(G,'A','D',weight='weight'),'distance':nx.shortest_path_length(G,'A','D',weight='weight')})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
