import networkx as nx
from collections import defaultdict
import operator,sys,timeit
from find_connected_component_subgraphs import connected_subgraph_gml,connected_subgraph_pajek

def idfs_gml(g,start,k): 
    stack=[start] #initialize stack with the seed node
    time=defaultdict(float) #dictionary to keep account of the time spent in influencing upto that node starting from seed node
    influencedNodes=[] #list to contain the nodes influenced by seed node
    time.update({start:0}) #time needed to influence start node is 0
    
    while stack: #loop until stack is empty
        
        v=stack.pop()
        
        for i in g.neighbors(v):
            if time.has_key(i)!=True and time[v]+(1/g[v][i]['value'])<=k: #check if time spent in influencing upto this node is less than one timestamp
                stack.append(i)
                time.update({i:time[v]+1/g[v][i]['value']})
                if(influencedNodes.count(i)==0): #check duplicate
                    influencedNodes.append(i)
                    
    return len(influencedNodes),influencedNodes

def idfs_pajek(g,start,k): 
    stack=[start] #initialize stack with the seed node
    time=defaultdict(float) #dictionary to keep account of the time spent in influencing upto that node starting from seed node
    influencedNodes=[] #list to contain the nodes influenced by seed node
    time.update({start:0}) #time needed to influence start node is 0
    
    while stack: #loop until stack is empty
        
        v=stack.pop()
        
        for i in g.neighbors(v):
            if time.has_key(i)!=True and time[v]+(1/g[v][i][0]['weight'])<=k: #check if time spent in influencing upto this node is less than one timestamp
                stack.append(i)
                time.update({i:time[v]+1/g[v][i][0]['weight']})
                if(influencedNodes.count(i)==0): #check duplicate
                    influencedNodes.append(i)
                    
    return len(influencedNodes),influencedNodes


def phase2Influence(influenceCount,InfluencedNodes):
    
    newInfluenceCount=influenceCount
    newInfluencedNodes=InfluencedNodes
    grey=[];
    black=[];
    while(len(grey)!=g.order()):

        flag=0
        #find the node that has maximum influence
        #maximumInfluenceNode,maximumInfluence = [max(newInfluence.iteritems(), key=operator.itemgetter(1))
        maximumInfluence = 0
        for item in newInfluenceCount:
                if item not in black:
                    if maximumInfluence<newInfluenceCount[item]:
                        maximumInfluence=newInfluenceCount[item]
                        maximumInfluenceNode=item
                        flag = 1

        if flag==1:
            #mark the node with maximum influence as a black node
            #print("Black node entered "+str(maximumInfluenceNode))
            black.append(maximumInfluenceNode)
            
            #also include that node in the list of grey nodes
            if(grey.count(maximumInfluenceNode)==0):
                grey.append(maximumInfluenceNode)
                
            #mark all the nodes that this black node influences as grey nodes
            for a in newInfluencedNodes[maximumInfluenceNode]:
                if(grey.count(a)==0):
                    grey.append(a);
                   
            newInfluenceCount={}

            #check for white nodes among the rest
            for a in g.nodes():
                count=0
                temp=list()
                for b in newInfluencedNodes[a]:
                    if(grey.count(b)==0):
                        count=count+1
                        temp.append(b)
                newInfluencedNodes[a]=temp
                newInfluenceCount[a]=count
            #print "The nodes in black"+str(black)
            #print "The nodes in grey"+str(grey)
        else:
            break
    print 'number of black nodes '+str(len(black)),'number of grey nodes '+str(len(grey))
        



if __name__=="__main__":
    flag=False
    start=timeit.default_timer()
    #input graph
    inputGraphName=sys.argv[1]
    if inputGraphName[-4:]=='.gml':
        flag=True
    if flag==True:
        g=connected_subgraph_gml(inputGraphName)
    else:
        g=connected_subgraph_pajek(inputGraphName)

    k=int(sys.argv[2])
    print 'number of nodes '+str(len(g.nodes())),'number of edges '+str(len(g.edges()))
    #initialize
    influenceCount=defaultdict(int) #dictionary that contains the count of influenced nodes for each node in the graph
    InfluencedNodes=defaultdict(int) #dictionary that contains the list of influenced nodes for each node in the graph

    #calculating influence of every node in the graph by calling the idfs function in a loop
    for node in g.nodes():
        if flag==True:
            count,nodes=idfs_gml(g,node,k) #calling idfs function with parameters: the input graph and the node to be treated as seed node
        else:
            count,nodes=idfs_pajek(g,node,k)
        influenceCount[node]=count
        InfluencedNodes[node]=nodes
    
    #print influenceCount
    #print InfluencedNodes

    count=0
    for edge in g.edges():
        node1=edge[0]
        node2=edge[1]
        if g[node1][node2][0]['weight']<1:
            count+=1
    print 'number of edges having fractional weight '+str(count)

    #testing a bug
    count=0
    for i in influenceCount:
        if influenceCount[i]==0:
           count+=1
    print 'number of nodes having zero influence '+str(count)

    temp=set()
    for i in InfluencedNodes:
        temp=temp|set(InfluencedNodes[i])
    print 'total estimated coverage after building k power graph '+str(len(temp))

    #calling the function for phase 2
    phase2Influence(influenceCount,InfluencedNodes)
    
    stop=timeit.default_timer()
    print stop - start
    

