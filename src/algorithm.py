import time
import heapq
import multiprocessing

def flatten_matrix(matrix): 
    return [item for sublist in matrix for item in sublist]

def Kurang(i, matrix):
    flat_matrix = flatten_matrix(matrix)
    pos_i = flat_matrix.index(i)
    count = 0
    for j in flat_matrix[pos_i+1:]:
        if j != 0 and j < i:
            count += 1
    return count

def sum_kurang_X(matrix):
    flat_matrix = flatten_matrix(matrix)
    count = 0
    for i in flat_matrix:
        if i != 0:
            count += Kurang(i, matrix)
    X = flat_matrix.index(0)
    X = (X // len(matrix)) + 1
    return count + X

def is_solvable(matrix):
    return sum_kurang_X(matrix) % 2 == 0

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(['_' if x == 0 else str(x) for x in row]))

def manhattan_distance(matrix):
    """Calculate the Manhattan distance of a given matrix."""
    distance = 0
    size = len(matrix)
    for i in range(size):
        for j in range(size):
            if matrix[i][j] != 0:
                target_x = (matrix[i][j] - 1) // size
                target_y = (matrix[i][j] - 1) % size
                distance += abs(i - target_x) + abs(j - target_y)
    return distance

def possible_moves(matrix):
    """Generate all possible moves from the current empty space."""
    size = len(matrix)
    x, y = [(i, j) for i in range(size) for j in range(size) if matrix[i][j] == 0][0]
    moves = []
    
    # Up
    if x > 0:
        new_matrix = [row[:] for row in matrix]  # Shallow copy of the matrix
        new_matrix[x][y], new_matrix[x-1][y] = new_matrix[x-1][y], new_matrix[x][y]
        moves.append(new_matrix)
    
    # Down
    if x < size - 1:
        new_matrix = [row[:] for row in matrix]
        new_matrix[x][y], new_matrix[x+1][y] = new_matrix[x+1][y], new_matrix[x][y]
        moves.append(new_matrix)
    
    # Left
    if y > 0:
        new_matrix = [row[:] for row in matrix]
        new_matrix[x][y], new_matrix[x][y-1] = new_matrix[x][y-1], new_matrix[x][y]
        moves.append(new_matrix)
    
    # Right
    if y < size - 1:
        new_matrix = [row[:] for row in matrix]
        new_matrix[x][y], new_matrix[x][y+1] = new_matrix[x][y+1], new_matrix[x][y]
        moves.append(new_matrix)
    
    return moves

def branch_and_bound_worker(heap, visited, goal, pattern_database, best_cost, best_solution, result_queue):
    while heap:
        priority, cost, current_matrix, path = heapq.heappop(heap)
        
        if cost > best_cost.value:
            continue
        
        if current_matrix == goal:
            best_cost.value = cost
            best_solution.value = path
            result_queue.put(best_solution.value)
            return
        
        for move in possible_moves(current_matrix):
            move_tuple = tuple(tuple(row) for row in move)
            if move_tuple not in visited or visited[move_tuple] > priority:
                new_cost = cost + 1
                pattern_key = tuple(flatten_matrix(move))
                heuristic_estimate = pattern_database.get(pattern_key, float('inf'))
                new_priority = new_cost + heuristic_estimate
                new_path = path + [move]
                visited[move_tuple] = new_priority
                heapq.heappush(heap, (new_priority, new_cost, move, new_path))

def parse_txt_to_matrix(file_path): 
    matrix = [] 
    with open(file_path, 'r') as file: 
        for line in file: 
            row = line.strip().split()
            row = [int(x) if x != '_' else None for x in row] 
            matrix.append(row)
    return matrix 

def main():
    while True:
        file_path = input("Enter the path to the matrix file (or 'exit' to quit): ")
        
        if file_path.lower() == 'exit':
            print("Exiting the program.")
            break
        
        try:
            initial_matrix = parse_txt_to_matrix(file_path)
            
            if is_solvable(initial_matrix):
                print("Solvable")
                print("Generating solution...")
                
                start_time = time.time()
                
                size = len(initial_matrix)
                goal = [[size * i + j + 1 for j in range(size)] for i in range(size)]
                goal[-1][-1] = 0
                
                pattern_database = {
                    (0, 0, 0, 0): 0,  
                }
                
                heap = []
                initial_state = (manhattan_distance(initial_matrix), 0, initial_matrix, [])
                heapq.heappush(heap, initial_state)
                
                # Shared variables
                manager = multiprocessing.Manager()
                visited = manager.dict()
                visited[tuple(tuple(row) for row in initial_matrix)] = initial_state[0]
                
                best_cost = manager.Value('i', float('inf'))
                best_solution = manager.Value('i', None)
                result_queue = manager.Queue()
                
                num_processes = multiprocessing.cpu_count()
                processes = []
            
                for _ in range(num_processes):
                    p = multiprocessing.Process(target=branch_and_bound_worker,
                                                args=(heap, visited, goal, pattern_database, best_cost, best_solution, result_queue))
                    processes.append(p)
                    p.start()
                
                for p in processes:
                    p.join()
                
                solution = result_queue.get()
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                if solution:
                    for step in solution:
                        print_matrix(step)
                        print()
                    print(f"Execution time: {execution_time:.4f} seconds")
                else:
                    print("No solution found.")
            else:
                print("The puzzle is not solvable.")
        
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
