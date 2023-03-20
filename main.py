import sys
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt
import copy

def is_acyclic(graph):
    """
    Checks whether a directed graph is acyclic or not. (acyclic if it can return to itself by any means along the path defined in the graph.)
    
    params:
        graph: A dictionary representing the directed graph.
    
    return: 
        True if the graph is acyclic,
        False otherwise.
    """
    visited = set() 
    path_to_focus_node = set()

    """
    Checks whether a node can return to itself by any means along the links defined in the graph.
    """
    def is_looped(node):
        visited.add(node)
        path_to_focus_node.add(node)
        
        # if len(graph[node]) == 0: # if this node is an endpoint
        #     path_to_focus_node.remove(node)
        #     return False
            
        for neighbor in graph[node]:
            if neighbor not in visited: # if neighbor has never been visited
                if is_looped(neighbor):
                    path_to_focus_node.remove(node)
                    return True
            else: # if neighbor has been visited ever
                if neighbor in path_to_focus_node: # if neighbor connected with any node in path
                    path_to_focus_node.remove(node)
                    return True
        
        # this means that all neighbors have no connection with the path
        path_to_focus_node.remove(node)
        return False

    for node in graph.keys():
        if node not in visited:
            if is_looped(node):
                return False

    return True

# Count the number of links at each node in the graph. (Consider both incoming and outgoing links.)
def get_node_links(graph: Dict[int, List[int]]) -> Dict[int, int]:
    node_links = dict()
    for node0 in graph.keys():
        node_links[node0] = len(graph[node0])
        for node in graph.keys():
            if node != node0:
                if node0 in graph[node]:
                    node_links[node0] = node_links[node0] + 1
        print(f'links of {node0} is {node_links[node0]}')
    return node_links

# Get nodes that are directly connected to nodes in a specific subgraph and are not part of a subgraph
def get_direct_links(graph: Dict[int, List[int]], sub_graph_nodes: List[int]) -> List[Tuple[int, int]]:
    direct_links = []
    for focus_node in sub_graph_nodes:
        for node in graph[focus_node]:
            if node in sub_graph_nodes:
                continue
            direct_links.append((focus_node, node))
    return direct_links    

# Take one node out of containing graph.
# 1) The node to be taken out must be linked with sub-graph
# 2) Select a node with minimum links among the nodes that satisfying above condition.
def get_node_subgraph_of_min_links(graph: Dict[int, List[int]], node_links: Dict[int, int], sub_graph_nodes:List[int], visited:List[int]) -> Tuple[int, int]:
    min_link_count = sys.maxsize
    min_node = (-1, -1)    
    direct_links = get_direct_links(graph, sub_graph_nodes)
    for link in direct_links:
        if link[1] in visited:
            continue
        
        if node_links[link[1]] < min_link_count:
            min_link_count = node_links[link[1]]
            min_node = link            
    return min_node

# Expand a sub-graph.
# Normally the sub-graph starts with one node and keeps expanding untill the cost sum is bigger than a threshold.
def expand_subgraph(graph: Dict[int, List[int]], node_costs: Dict[int, int], sub_graph: Dict[int, List[int]]):
    node_links = get_node_links(graph)
    visited = []
    while True:
        sub_graph_nodes = list(sub_graph.keys())
        node_2_add = get_node_subgraph_of_min_links(graph, node_links, sub_graph_nodes, visited)
        if node_2_add[0] < 0: # If there is no nodes to add
            return
        
        visited.append(node_2_add[1])
        
        sub_graph[node_2_add[0]].append(node_2_add[1])        
        sub_graph[node_2_add[1]] = []
        if cost_sum(node_costs, sub_graph) == subgraph_max_cost:
            return
        
        if cost_sum(node_costs, sub_graph) > subgraph_max_cost:            
            sub_graph.pop(node_2_add[1])
            sub_graph[node_2_add[0]].remove(node_2_add[1])

# Split the sub-graph from the parent graph.
# This time remove nodes from the parent graph that will be contained in sub-graph.
# And delete the links with these nodes to be removed.
def split_subgraph(parent_graph: Dict[int, List[int]], sub_graph:Dict[int, List[int]]) -> Dict[int, List[int]]: 
    new_graph = copy.deepcopy(parent_graph)
    for node in sub_graph.keys():
        new_graph.pop(node, None)
    for node0 in new_graph.keys():
        for node in sub_graph.keys():    
            if node in new_graph[node0]: new_graph[node0].remove(node)
    return new_graph

# Get sum of costs of each node in a graph
def cost_sum(node_costs: Dict[int, int], sub_graph:Dict[int, List[int]]) -> int:
    sum = 0
    for node in sub_graph.keys():
        sum = sum + node_costs[node]
    return sum
    
def partition_graph(
    graph: Dict[int, List[int]], 
    node_costs: Dict[int, int], 
    subgraph_max_cost: int) -> List[Dict[int, List[int]]]:
    """
    Partitions a directed acyclic graph
    into minimum number of contiguous sub-graphs
    such that each sub-graph has a total cost of
     no more than a given parameter
     subgraph_max_cost.

    :param graph: 
    A dictionary where the keys are the node ids and
     the values are lists of node ids
      that the key node has outgoing edges to.
    
    :param node_costs: 
    A dictionary where the keys are the node ids
     and the values are the positive cost of the node.
     
    :param subgraph_max_cost: 
    The maximum total cost allowed for each sub-graph.
    
    :return: 
    A list of Dictionaries
     where each inner dictionary is a contiguous sub-graph
      with total cost of no more than subgraph_max_cost.
    """
    sub_graph_list = []

    parent_graph = copy.deepcopy(graph)
    while(True):
        node_links = get_node_links(parent_graph)
        min_links_node = min(node_links.items(), key=lambda x: x[1]) # Select a node in graph with maximum links with othe nodes.
    
        sub_graph = dict()
        sub_graph[min_links_node[0]] = []
        expand_subgraph(parent_graph, node_costs, sub_graph)
        sub_graph_list.append(sub_graph)
        parent_graph = split_subgraph(parent_graph, sub_graph)
        if len(parent_graph.keys()) == 1:
            sub_graph_list.append(parent_graph)
            break
        if len(parent_graph.keys()) == 0:
            break
    
    return sub_graph_list

if __name__ == "__main__":
    # Sample graph
    """
    graph = {
        1: [2, 3],
        2: [4],
        3: [4],
        4: [5],
        5: []
    }

    # Sample node costs
    node_costs = {
        1: 2,
        2: 1,
        3: 1,
        4: 3,
        5: 2
    }
    
    graph = {
        1: [2],
        2: [3],
        3: [4],
        4: [5],
        5: [6],
        6: [7],
        7: [8],
        8: [9],
        9: [10],
        10: []
    }
    """
    graph = {
        1: [2, 3],
        2: [4, 5],
        3: [6, 7],
        4: [8],
        5: [8, 4],
        6: [9],
        7: [9, 4],
        8: [10],
        9: [10],
        10: []
    }
    
    node_costs = {
        1: 4,
        2: 1,
        3: 2,
        4: 3,
        5: 2,
        6: 3,
        7: 2,
        8: 4,
        9: 1,
        10: 5
    }

    # Maximum cost of each sub-graph
    subgraph_max_cost = 10
    
    # Plot the input graph
    plt.figure(figsize=(5, 5))
    for node in graph.keys():
        plt.scatter(node, node_costs[node], s=100)
        for neighbor in graph[node]:
            plt.arrow(node, node_costs[node], neighbor-node, node_costs[neighbor]-node_costs[node], head_width=0.1, head_length=0.2, length_includes_head=True, color='k')
    plt.title('Input Graph')
    plt.xlabel('Node ID')
    plt.ylabel('Node Cost')
    plt.ylim(0, max(node_costs.values())+1)
    plt.show()
    
    if not is_acyclic(graph):
        print("The main graph is not acyclic!")
        exit(-1)    
    
    # Partition the graph
    sub_graphs = partition_graph(graph, node_costs, subgraph_max_cost)

    # Print the resulting sub-graphs
    for sub_graph in sub_graphs:
        print(f'{sub_graph} -- sum_cost={cost_sum(node_costs, sub_graph)}')
        
    # Plot the resulting sub-graphs
    plt.figure(figsize=(5, 5))
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    for i, sub_graph in enumerate(sub_graphs):
        for node in sub_graph.keys():
            plt.scatter(node, node_costs[node], s=100, color=colors[i%len(colors)])
            for neighbor in sub_graph[node]:
                plt.arrow(node, node_costs[node], neighbor-node, node_costs[neighbor]-node_costs[node], head_width=0.1, head_length=0.2, length_includes_head=True, color=colors[i%len(colors)])
        plt.title('Resulting Sub-Graphs')
        plt.xlabel('Node ID')
        plt.ylabel('Node Cost')
        plt.ylim(0, max(node_costs.values())+1)
    plt.show()
    
    pass