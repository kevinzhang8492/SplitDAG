# SplitDAG

This project was started to solve the following problem.

Given a (directed acyclic) graph with __N__ nodes and each node having a known positive __"cost"__, suggest one algorithm that partition the graph into __minimum number__ of __contiguous__ sub-graphs, such that each sub-graph has a total cost of no more than a given parameter **subgraph_max_cost**.

The basic method is how to split a subgraph such that the number of subgraphs produced by the split is minimal.
I think that the number of subgraphs produced by the split will be minimal if I select a node with minimal links in graph.
The solution works well with my test cases.

__Note:__
This solution use the matplotlib library for illustration purposes. So you must first run the following command in terminal.

pip install matplotlib


