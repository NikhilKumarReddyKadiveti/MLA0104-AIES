import math

class Node:
    def __init__(self, name, is_max=True):
        self.name = name
        self.is_max = is_max  # True if MAX's turn, False if MIN's turn
        self.children = []
        self.value = None    # Utility value (set for leaf nodes)

def build_tree_interactive():
    print("--- Minimax & Alpha-Beta Tree Builder ---")
    depth = int(input("Enter tree depth (e.g., 2 or 3): "))
    branching_factor = int(input("Enter branching factor / children per node (e.g., 2 for binary tree): "))

    def build_node(current_depth, is_max, name_prefix):
        if current_depth == depth:
            # Reached leaf node level
            val = float(input(f"  Enter leaf utility value for node '{name_prefix}': "))
            node = Node(name_prefix, is_max)
            node.value = val
            return node

        node = Node(name_prefix, is_max)
        for i in range(branching_factor):
            child_name = f"{name_prefix}{i+1}"
            child_node = build_node(current_depth + 1, not is_max, child_name)
            node.children.append(child_node)
        return node

    root_is_max = input("Is the root node MAX turn? (y/n): ").strip().lower() == 'y'
    root = build_node(0, root_is_max, "Root")
    return root

# --- 1. Standard Minimax Algorithm ---
def minimax(node):
    # Base case: Leaf node
    if not node.children:
        return node.value

    if node.is_max:
        max_eval = -math.inf
        for child in node.children:
            eval_val = minimax(child)
            max_eval = max(max_eval, eval_val)
        return max_eval
    else:
        min_eval = math.inf
        for child in node.children:
            eval_val = minimax(child)
            min_eval = min(min_eval, eval_val)
        return min_eval

# --- 2. Alpha-Beta Pruning Algorithm ---
def alphabeta(node, alpha, beta, pruned_nodes):
    # Base case: Leaf node
    if not node.children:
        return node.value

    if node.is_max:
        max_eval = -math.inf
        for child in node.children:
            eval_val = alphabeta(child, alpha, beta, pruned_nodes)
            max_eval = max(max_eval, eval_val)
            alpha = max(alpha, max_eval)
            
            # Alpha-Beta Pruning Cutoff
            if beta <= alpha:
                # Mark remaining children as pruned
                idx = node.children.index(child)
                for skipped_child in node.children[idx+1:]:
                    pruned_nodes.append(skipped_child.name)
                break
        return max_eval
    else:
        min_eval = math.inf
        for child in node.children:
            eval_val = alphabeta(child, alpha, beta, pruned_nodes)
            min_eval = min(min_eval, eval_val)
            beta = min(beta, min_eval)
            
            # Alpha-Beta Pruning Cutoff
            if beta <= alpha:
                # Mark remaining children as pruned
                idx = node.children.index(child)
                for skipped_child in node.children[idx+1:]:
                    pruned_nodes.append(skipped_child.name)
                break
        return min_eval

if __name__ == "__main__":
    # 1. Interactively build tree
    root_node = build_tree_interactive()

    # 2. Run Standard Minimax
    minimax_result = minimax(root_node)

    # 3. Run Alpha-Beta Pruning
    pruned_list = []
    ab_result = alphabeta(root_node, -math.inf, math.inf, pruned_list)

    # 4. Results
    print("\n--- RESULTS ---")
    print(f"Minimax Optimal Value    : {minimax_result}")
    print(f"Alpha-Beta Optimal Value : {ab_result}")
    
    if pruned_list:
        print(f"Pruned Subtrees / Nodes  : {', '.join(pruned_list)}")
    else:
        print("Pruned Subtrees / Nodes  : None (Full tree explored)")