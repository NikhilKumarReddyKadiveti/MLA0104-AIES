from collections import deque, defaultdict

def build_graph():
    print("--- AI Course Search Strategy Runner ---")
    is_directed = input("Is the graph directed? (y/n): ").strip().lower() == 'y'
    num_edges = int(input("Enter number of edges: "))
    
    graph = defaultdict(list)
    print("\nEnter edges (Node1 Node2):")
    for i in range(num_edges):
        raw = input(f"Edge {i+1}: ").strip().split()
        if len(raw) != 2:
            print("  [!] Invalid edge format. Skipping...")
            continue
        # Standardize uppercase to prevent casing mismatches (e.g., 'c' vs 'C')
        u, v = raw[0].upper(), raw[1].upper()
        graph[u].append(v)
        if not is_directed:
            graph[v].append(u)
        if v not in graph:
            graph[v] = []

    return graph

def bfs(graph, start_node, priority_order):
    visited = set([start_node])
    queue = deque([start_node])
    order = []

    while queue:
        curr = queue.popleft()
        order.append(curr)
        
        # Sort neighbors according to priority before adding to queue
        neighbors = list(graph[curr])
        if priority_order == '2':
            neighbors.sort()                  # Ascending order
        elif priority_order == '3':
            neighbors.sort(reverse=True)      # Descending order

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order

def dfs(graph, start_node, priority_order):
    visited = set()
    order = []

    def _dfs_recursive(node):
        visited.add(node)
        order.append(node)
        
        # Sort neighbors according to priority before exploring
        neighbors = list(graph[node])
        if priority_order == '2':
            neighbors.sort()                  # Ascending order
        elif priority_order == '3':
            neighbors.sort(reverse=True)      # Descending order

        for neighbor in neighbors:
            if neighbor not in visited:
                _dfs_recursive(neighbor)

    _dfs_recursive(start_node)
    return order

if __name__ == "__main__":
    user_graph = build_graph()
    start = input("\nEnter starting node: ").strip().upper()
    
    print("\nSelect Neighbor Expansion Priority:")
    print("1. As Entered (Order typed in input)")
    print("2. Ascending  (e.g., 2 before 4, or A before B)")
    print("3. Descending (e.g., 4 before 2, or B before A)")
    priority = input("Choice (1/2/3): ").strip()

    print("\n--- Search Strategy Results ---")
    print("BFS Order : ", " -> ".join(bfs(user_graph, start, priority)))
    print("DFS Order : ", " -> ".join(dfs(user_graph, start, priority)))