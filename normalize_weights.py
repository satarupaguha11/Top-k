#for graphs which have edge weights less than 1, it is required to normalize them so that all of them are >1
#This program works for graphs in gml format only.
import networkx as nx
import sys

def normalize_weight(filename):
	g=nx.read_gml(filename)
	smallest_weight=999
	for edge in g.edges():
		#print g[edge[0]][edge[1]]['value']
		if smallest_weight>g[edge[0]][edge[1]]['value']:
			smallest_weight=g[edge[0]][edge[1]]['value']
	
	p=1/float(smallest_weight)
	for edge in g.edges():
		g[edge[0]][edge[1]]['value']=p*g[edge[0]][edge[1]]['value']
	
	
	#checking if weights are indeed all greater than 1 now
	for edge in g.edges():
		if g[edge[0]][edge[1]]['value']<1:
			print "failed"
	
	return g

if __name__=='__main__':
	filename=sys.argv[1]
	g=normalize_weight(filename)
	filename=filename[:-4]
	nx.write_gml(g,filename+'_normalized.gml')
