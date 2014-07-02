#How to run: python optimization.py /path/to/dataset number_of_hops
import networkx as nx
from collections import defaultdict
import operator,sys,timeit
from find_connected_component_subgraphs import connected_subgraph_gml,connected_subgraph_pajek,connected_subgraph_gexf
from copy import deepcopy

def idfs_gml(g,start,k): 
    
    stack=[start] #initialize stack with the seed node
    time=defaultdict(float) #dictionary to keep account of the time spent in influencing upto that node starting from seed node
    kHopNeighbors=set() #set to contain the nodes influenced by seed node
    time.update({start:0}) #time needed to influence start node is 0
    
    while stack: #loop until stack is empty
        
        v=stack.pop()
        
        for i in g.neighbors(v):
            if time.has_key(i)!=True and time[v]+(1/g[v][i]['value'])<=k: #check if time spent in influencing upto this node is less than one timestamp
                stack.append(i)
                time.update({i:time[v]+1/g[v][i]['value']})
                kHopNeighbors.add(i)
                    
    return len(kHopNeighbors),kHopNeighbors

def idfs_pajek(g,start,k): 
    stack=[start] #initialize stack with the seed node
    time=defaultdict(float) #dictionary to keep account of the time spent in influencing upto that node starting from seed node
    kHopNeighbors=set() #list to contain the nodes influenced by seed node
    time.update({start:0}) #time needed to influence start node is 0
    
    while stack: #loop until stack is empty
        
        v=stack.pop()
        
        for i in g.neighbors(v):
            if time.has_key(i)!=True and time[v]+(1/g[v][i][0]['weight'])<=k: #check if time spent in influencing upto this node is less than one timestamp
                stack.append(i)
                time.update({i:time[v]+1/g[v][i][0]['weight']})
                kHopNeighbors.add(i)
                    
    return len(kHopNeighbors),kHopNeighbors

def idfs_gexf(g,start,k): 
    stack=[start] #initialize stack with the seed node
    time=defaultdict(float) #dictionary to keep account of the time spent in influencing upto that node starting from seed node
    kHopNeighbors=set() #list to contain the nodes influenced by seed node
    time.update({start:0}) #time needed to influence start node is 0
    
    while stack: #loop until stack is empty
        
        v=stack.pop()
        
        for i in g.neighbors(v):
            if time.has_key(i)!=True and time[v]+(1/g[v][i]['count'])<=k: #check if time spent in influencing upto this node is less than one timestamp
                stack.append(i)
                time.update({i:time[v]+1/g[v][i]['count']})
                kHopNeighbors.add(i)
                    
    return len(kHopNeighbors),kHopNeighbors


def phase2Influence(kHopDegree,kHopNeighbors):
    
    grey=set();
    black=set();
    previous_node=999
    while len(grey)+len(black)<=g.order():    
        #find the node that has maximum influence    
        #maximumInfluenceNode = max(kHopDegree.iteritems(), key=operator.itemgetter(1))[0]
        #print len(black)+len(grey)
        flag=0
        maximumInfluence = -1
        maximumInfluenceNode = -1
        for item in kHopDegree:
                if maximumInfluence<kHopDegree[item]:
                    maximumInfluence=kHopDegree[item]
                    maximumInfluenceNode=item
                    
        if maximumInfluenceNode!=previous_node:           
                          
            #mark the node with maximum influence as a black node
            black.add(maximumInfluenceNode)
            
            
            #delete this node from neighbors list of all other nodes which contains this node
            for neigh in neighbors_of[maximumInfluenceNode]: 
                kHopNeighbors[neigh].discard(maximumInfluenceNode)
                kHopDegree[neigh]-=1

            #list of neighbors of this node. To be made grey
            removed=kHopNeighbors[maximumInfluenceNode]
            #print removed

            #delete entry of this node from neighbors and degree datastructures
            

            del kHopNeighbors[maximumInfluenceNode]
            del kHopDegree[maximumInfluenceNode] 

            

            #mark all the nodes that this black node influences as grey nodes      
            grey.update(removed)

            for a in removed:
                #remove these grey nodes from the neighbor lists of all nodes that contain them
                for n in neighbors_of[a]:
                    #print kHopNeighbors[n]
                    kHopNeighbors[n].discard(a)
                    kHopDegree[n]-=1
            previous_node=maximumInfluenceNode    

    return black,grey
    
 
if __name__=="__main__":
    flag=0
    start=timeit.default_timer()
    #input graph
    inputGraphName=sys.argv[1]

    #extract largest connected componet subgraph from graph
    if inputGraphName[-4:]=='.gml':
        flag=1
    elif inputGraphName[-4:]=='.net':
        flag=2

    if flag==1:
        g=connected_subgraph_gml(inputGraphName)
    elif flag==2:
        g=connected_subgraph_pajek(inputGraphName)
    elif flag==0:
        g=connected_subgraph_gexf(inputGraphName)
    else:
        print "INVALID FILE FORMAT"

    
    k=int(sys.argv[2])
    print 'number of nodes '+str(len(g.nodes())),'number of edges '+str(len(g.edges()))
    #initialize
    kHopDegree=defaultdict(int) #dictionary that contains the count of influenced nodes for each node in the graph
    kHopNeighbors=defaultdict(set) #dictionary that contains the set of influenced nodes for each node in the graph

    
    #calculating influence of every node in the graph by calling the idfs function in a loop
    for node in g.nodes():
        if flag==1:
            count,nodes=idfs_gml(g,node,k) #calling idfs function with parameters: the input graph and the node to be treated as seed node
        elif flag==2:
            count,nodes=idfs_pajek(g,node,k)
        else:
            count,nodes=idfs_gexf(g,node,k)
        kHopDegree[node]=count
        kHopNeighbors[node]=nodes
   

    #construct neighbors_of data structure, to store node i is neighbor of which all nodes
    neighbors_of=defaultdict(set)
    for node_a in kHopNeighbors:
        for node_b in kHopNeighbors[node_a]:
            neighbors_of[node_b].add(node_a)

    print "neighbors of created"
    
    if flag==0:

        count=0
        for edge in g.edges():
            node1=edge[0]
            node2=edge[1]
            if g[node1][node2]['count']<1:
                count+=1
    elif flag==1:
        count=0
        for edge in g.edges():
            node1=edge[0]
            node2=edge[1]
            if g[node1][node2]['value']<1:
                count+=1
    else:
        count=0
        for edge in g.edges():
            node1=edge[0]
            node2=edge[1]
            if g[node1][node2][0]['weight']<1:
                count+=1
    print 'number of edges having fractional weight '+str(count)


    #testing a bug
    count=0
    for i in kHopDegree:
        if kHopDegree[i]==0:
           count+=1
    print 'number of nodes having zero influence '+str(count)

    temp=set()
    for i in kHopNeighbors:
        temp=temp|set(kHopNeighbors[i])
    print 'total estimated coverage after building k power graph '+str(len(temp))
    
   
    #calling the function for phase 2
    black,grey=phase2Influence(kHopDegree,kHopNeighbors)
    print 'number of black nodes '+str(len(black)),'number of grey nodes '+str(len(grey))

    

    stop=timeit.default_timer()
    print stop - start
    
