from pathlib import Path
import json, networkx as nx

def main():
    G=nx.DiGraph();G.add_edge('s','a',capacity=5);G.add_edge('s','b',capacity=4);G.add_edge('a','t',capacity=3);G.add_edge('a','b',capacity=2);G.add_edge('b','t',capacity=5)
    value,flow=nx.maximum_flow(G,'s','t');save({'max_flow':value,'flow':flow})
def save(o):
    p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
if __name__=='__main__':main()
