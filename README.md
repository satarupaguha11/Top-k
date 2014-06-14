Top-k
=====
Implementation of algorithm to find the top k influentials for weighted graphs, incorporating the concept of time stamps: In this algorithm , we have considered edges with weights, where weight is the frequency of communication between the two nodes. For each node we find the number of nodes it can influence in one time stamp. For example if A and B have an edge weighted x, the time needed by A to influence B is 1/x.

Requirements:
------------
Python has to be installed in the system along with Python library networkx.

Input:
------
This program takes as input a weighted social network graph where the weights on the edges denote the frequency of communication between two nodes. Graph that has to be given as input must be in GML or Pajek file format.

How to run:
------------
python weightedInfluence_largeGraph.py /path/to/dataset number/of/hops
