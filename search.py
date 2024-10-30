def AStarWithEuclideanDistance():
    return

def AStarWithMisplacedTile():
    return

def uniformCostSearch():
    return

def gameInterface():
    print("Welcome to tcai019's 8 puzzle solver")
    user_input = input("Type 1 to use a default puzzle, or 2 to enter your own puzzle.\n")
    
    if user_input == '1':
        # Default puzzle
        puzzle = [
            [1, 0, 3], # 0 represents a blank space
            [4, 2, 6],
            [7, 5, 8]
        ]
        print("Using default puzzle:")
    elif user_input == '2':
        print("Enter your puzzle, use a zero to represent the blank.")
        puzzle = []
        for i in range(3):
            row = input(f"Enter row {i + 1} (space or tab between numbers): ")
            # Split input into a list of integers
            puzzle.append(list(map(int, row.split())))
        print("Your puzzle:")
    else:
        print("Invalid input. Please enter 1 or 2.")
        return

    # Print the puzzle for confirmation
    for row in puzzle:
        print(row)

    user_input = input("Enter your choice of algorithm from 1 to 3\n")
    
    if user_input == '1':
        uniformCostSearch()
    elif user_input == '2':
        AStarWithMisplacedTile()
    elif user_input == '3':
        AStarWithEuclideanDistance()
    else:
        print("Invalid choice. Pick 1, 2, or 3")


def main():
    gameInterface()

if __name__ == "__main__":
    main()