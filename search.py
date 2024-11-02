import heapq
import math

# Goal State to reach
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

class Problem:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def get_neighbors(self, state):
        neighbors = []
        # Find the blank position
        index = state.index(0)
        # Get the row and column of the blank position
        row, col = divmod(index, 3)

        # Move up, left, right, down
        possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in possible_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 3 and 0 <= c < 3:
                new_index = r * 3 + c
                new_state = list(state)
                # Swap the blank with the adjacent tile
                new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
                neighbors.append(tuple(new_state))

        return neighbors

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        # Cost to reach from initial to this node
        self.g = 0 
        # Cost of the heuristic h(n) value
        self.h_value = 0
        # Initialize depth
        self.depth = 0

    def h(self):
        # Heuristic: Euclidean distance
        distance = 0
        for i in range(9):
            # Do not consider a blank tile
            if self.state[i] != 0:
                # Goal position
                goal_x, goal_y = divmod(self.state[i] - 1, 3)
                # Current player position
                current_x, current_y = divmod(i, 3)
                # Distance from current player position to the goal.
                distance += math.sqrt((goal_x - current_x) ** 2 + (goal_y - current_y) ** 2)
        return distance

    def h_misplaced(self):
        # Heuristic: Number of misplaced tiles
        return sum(1 for i in range(9) if self.state[i] != 0 and self.state[i] != GOAL_STATE[i])

    def f(self):
        # Cost for heuristic f(n)
        return self.g + self.h_value

    def __lt__(self, other):
        return self.f() < other.f()

    def get_solution_path(self):
        path = []
        node = self
        while node:
            # Append the Node object
            path.append(node)
            node = node.parent
        # Reverse the path to get from the root to the goal
        return path[::-1]

class Tree:
    def __init__(self, root_state):
        self.root = Node(root_state)
        self.root.g = 0
        self.root.depth = 0

    def GRAPH_SEARCH(self, problem, heuristic=None):
        # Use a priority queue for A* or a regular queue for UCS
        frontier = []
        heapq.heappush(frontier, (0, self.root))

        # Use a set for a quick lookup
        explored = set()

        # How many nodes expanded and the max queue size
        nodes_expanded = 0
        max_queue_size = len(frontier)

        while frontier:
            # If not frontier, return None
            if not frontier: 
                return None
            
            # Choose a leaf node and remove it from the frontier
            total_cost, current_node = heapq.heappop(frontier)

            # Check for the goal state
            if current_node.state == problem.goal_state:
                return current_node.get_solution_path(), nodes_expanded, max_queue_size, current_node.depth
            
            # Add the node to the explored set
            explored.add(current_node.state)

            # Expand the chosen node
            for neighbor_state in problem.get_neighbors(current_node.state):
                neighbor_node = Node(neighbor_state, parent=current_node)
                neighbor_node.g = current_node.g + 1
                neighbor_node.depth = current_node.depth + 1

                # Calculate heuristic value if provided, UCS is 0
                if heuristic:
                    neighbor_node.h_value = heuristic(neighbor_node)
                else:
                    neighbor_node.h_value = 0 

                # Calculate total cost of g and n
                total_cost = neighbor_node.g + neighbor_node.h_value
                
                # Only add to frontier if not in frontier or explored set
                if neighbor_state not in explored and not any(n.state == neighbor_state and n.g <= neighbor_node.g for _, n in frontier):
                    heapq.heappush(frontier, (total_cost, neighbor_node))

            # Add to the nodes expanded
            nodes_expanded += 1
            # Add to the max queue size based on the length of the frontier
            max_queue_size = max(max_queue_size, len(frontier))

        return None, nodes_expanded, max_queue_size, None

    # Function for A Star With Euclidean heuristic
    def AStarWithEuclidean(self, problem):
        return self.GRAPH_SEARCH(problem, heuristic=lambda node: node.h())

    # Function for A Start with Misplaced Tile heuristic
    def AStarWithMisplacedTile(self, problem):
        return self.GRAPH_SEARCH(problem, heuristic=lambda node: node.h_misplaced())

    # Function for the Uniform Cost Search algorithm
    def UCS(self, problem):
        return self.GRAPH_SEARCH(problem, heuristic=None)  # No heuristic for UCS

# Function for the game interface
def gameInterface():
    print("Welcome to tcai019's 8 puzzle solver")
    user_input = input("Type 1 to use a default puzzle, or 2 to enter your own puzzle.\n")
    
    # Give a default puzzle or have a user input a puzzle themselves
    if user_input == '1':
        puzzle = (1, 2, 3, 4, 8, 0, 7, 6, 5)
        print("Using default puzzle:")
    elif user_input == '2':
        print("Enter your puzzle, use a zero to represent the blank.")
        puzzle = []
        for i in range(3):
            row = input(f"Enter row {i + 1} (space or tab between numbers): ")
            puzzle.extend(list(map(int, row.split())))
        puzzle = tuple(puzzle)  # Convert to tuple for immutability
    else:
        print("Invalid input. Please enter 1 or 2.")
        return

    # Print the puzzle for confirmation
    for i in range(0, 9, 3):
        print(puzzle[i:i + 3])

    # Create a Problem instance
    problem = Problem(puzzle, GOAL_STATE)
    user_input = input("1 for UCS, 2 for A* with Misplaced Tile, 3 for A* with Euclidean distance.\n")
    
    # Create a Tree
    puzzle_tree = Tree(problem.initial_state)
    
    if user_input == '1':
        solution_path, nodes_expanded, max_queue_size, goal_depth = puzzle_tree.UCS(problem)
    elif user_input == '2':
        solution_path, nodes_expanded, max_queue_size, goal_depth = puzzle_tree.AStarWithMisplacedTile(problem)
    elif user_input == '3':
        solution_path, nodes_expanded, max_queue_size, goal_depth = puzzle_tree.AStarWithEuclidean(problem)
    else:
        return

    # Print out the solution path and the g(n) and h(n) values. Also output nodes expanded, max queue, and the solution depth.
    if solution_path:
        print("Solution found:")
        for node in solution_path:
            for i in range(0, 9, 3):
                print(node.state[i:i + 3])
            print(f"g(n): {node.g}, h(n): {node.h_value}\n")
        print(f"To solve this problem, the search algorithm expanded a total of {nodes_expanded} nodes.")
        print(f"The maximum number of nodes in the queue at any one time: {max_queue_size}.")
        print(f"The depth of the goal node was: {goal_depth}.")
    else:
        print("No solution found.")

# Run the game interface
gameInterface()