import heapq
from collections import defaultdict

def build_a_star_graph():
    print("--- A* Search Algorithm Runner ---")
    is_directed = input("Is the graph directed? (y/n): ").strip().lower() == 'y'
    num_edges = int(input("Enter number of edges: "))
    
    graph = defaultdict(list)
    print("\nEnter edges as 'Node1 Node2 EdgeCost' (e.g., S A 1 or A B 3):")
    for i in range(num_edges):
        raw = input(f"Edge {i+1}: ").strip().split()
        if len(raw) != 3:
            print("  [!] Please enter 3 values: Node1 Node2 EdgeCost")
            continue
        
        u, v = raw[0].upper(), raw[1].upper()
        cost = float(raw[2])
        
        graph[u].append((v, cost))
        if not is_directed:
            graph[v].append((u, cost))
            
        if v not in graph:
            graph[v] = []

    # Get heuristic values h(n) for each node
    print("\nEnter heuristic values h(n) for each node:")
    heuristics = {}
    
    # Get all unique nodes in the graph
    all_nodes = set(graph.keys())
    for u in graph:
        for v, _ in graph[u]:
            all_nodes.add(v)
            
    for node in sorted(all_nodes):
        h_val = float(input(f"  h({node}): "))
        heuristics[node] = h_val

    return graph, heuristics

def a_star_search(graph, heuristics, start_node, goal_node):
    # Priority queue stores tuples of: (f_score, g_score, current_node, path)
    # Start node: g(start) = 0, f(start) = 0 + h(start)
    start_f = 0 + heuristics.get(start_node, 0)
    priority_queue = [(start_f, 0, start_node, [start_node])]
    
    # Keep track of the lowest g_score found for each node
    g_scores = {start_node: 0}
    visited = set()

    while priority_queue:
        # Pop the node with the lowest f(n) = g(n) + h(n)
        f, g, curr_node, path = heapq.heappop(priority_queue)

        if curr_node in visited:
            continue
            
        visited.add(curr_node)

        # Check if goal is reached
        if curr_node == goal_node:
            return path, g, f

        # Explore neighbors
        for neighbor, edge_cost in graph[curr_node]:
            tentative_g = g + edge_cost
            
            # If a shorter path to neighbor is found
            if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g
                h = heuristics.get(neighbor, 0)
                f_score = tentative_g + h
                
                heapq.heappush(priority_queue, (f_score, tentative_g, neighbor, path + [neighbor]))

    return None, float('inf'), float('inf')  # Goal unreachable

if __name__ == "__main__":
    user_graph, user_heuristics = build_a_star_graph()
    
    start = input("\nEnter starting node: ").strip().upper()
    goal = input("Enter goal node: ").strip().upper()

    path, path_cost_g, total_f = a_star_search(user_graph, user_heuristics, start, goal)

    print("\n--- A* Search Results ---")
    if path:
        print(f"Optimal Path :  {' -> '.join(path)}")
        print(f"Path Cost g(n) :  {path_cost_g}")
        print(f"Total f(n)    :  {total_f}")
    else:
        print(f"No path found from '{start}' to '{goal}'.")