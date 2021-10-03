from math import sqrt
import load_maze

def find_moves(data, location):
    directions = [[-1,0], [1,0], [0, -1], [0, 1]]
    moves = []
    
    for direction in directions:
        move_location = [
            location[0] + direction[0],
            location[1] + direction[1]]
        if move_location[0] < 0 or move_location[1] < 0:
            continue
        elif move_location[0] == len(data) or move_location[1] == len(data[0]):
            continue
        elif data[move_location[0]][move_location[1]] == 1:
            moves.append(move_location)
    return moves

def taxicab_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def crowfly_distance(a, b):
    return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def find_que_position(que, move, end):
    i = 0
    for i, que_spot in enumerate(que):
        if move[1] < que_spot[1]:
            return i
        elif move[1] == que_spot[1]:
            move[2] = crowfly_distance(move[0], end)
            if que_spot[2] == None:
                que_spot[2] = crowfly_distance(que_spot[0], end)
            if move[2] <= que_spot[2]:
                return i
        continue
    return i + 1

def a_star_explore(start, end, data):
    que = [[start, None, None]]
    explored = []

    while len(que) > 0:
        moves = find_moves(data, que[0][0])
        explored.append(que.pop(0)[0])
        for move in moves:
            if move == end:
                return explored
            move = [move, taxicab_distance(move, end), None]
            if move in que or move[0] in explored:
                continue
            que.insert(find_que_position(que, move, end), move)
    return False

def depth_first_explore(start, end, data):
    que = [start]
    explored = []

    while len(que) > 0:
        moves = find_moves(data, que[0][0])
        explored.append(que.pop(0))
        for move in moves:
            if move == end:
                return explored
            if move in explored:
                continue
            if move in que:
                que.pop(que.index(move))
            que.insert(0, move)
    return False

def breadth_first_explore(start, end, data):
    que = [start]
    explored = []

    while len(que) > 0:
        moves = find_moves(data, que[0])
        explored.append(que.pop(0))
        for move in moves:
            if move == end:
                return explored
            if move in explored or move in que:
                continue
            else:
                que.append(move)
    return False

def find_path_from_explored(start, end, explored, data):
    move_list = [end]

    while True:
        moves = find_moves(data, move_list[-1])
        min_index = len(explored) + 1
        for move in moves:
            if move == start:
                move_list.append(start)
                break
            if move in explored:
                min_index = min(min_index, explored.index(move))
        if start in move_list:
            break
        move_list.append(explored[min_index])


    return move_list[::-1]

def a_star_main(maze_data, start, end):
    explored = a_star_explore(start, end, maze_data)
    if not explored:
        print("Failed to find solution")
        return False, False
    solution = find_path_from_explored(start, end, explored, maze_data)
    return explored, solution

def depth_first_main(maze_data, start, end):    
    explored = depth_first_explore(start, end, maze_data)
    if not explored:
        print("Failed to find solution")
        return False, False
    solution = find_path_from_explored(start, end, explored, maze_data)
    return explored, solution

def breadth_first_main(maze_data, start, end):    
    explored = breadth_first_explore(start, end, maze_data)
    if not explored:
        print("Failed to find solution")
        return False, False
    solution = find_path_from_explored(start, end, explored, maze_data)
    return explored, solution

if __name__ == '__main__':
    maze_data, start, end = load_maze.get_grid("Mazes/maze1.gif", True)
    explored, moves = breadth_first_main(maze_data, start, end)
    #explored, moves = depth_first_main(maze_data, start, end)
    data = load_maze.draw_explored(explored, maze_data)
    load_maze.draw_path("BFS_complete_path.png", moves, data)