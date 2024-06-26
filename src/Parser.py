
def parse_txt_to_matrix(file_path): 
    matrix = [] 
    with open(file_path, 'r') as file: 
        for line in file: 
            row = line.strip().split()
            row = [int(x) if x != '_' else None for x in row] 
            matrix.append(row)
    return matrix 