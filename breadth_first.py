from numpy.lib.function_base import trapz
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
        elif data[move_location[0]][move_location[1]] == 1:
            moves.append(move_location)
    return moves

def main(location, bordered = False):
    maze_data, end, start = load_maze.get_grid(location, True)
    que = [start]
    explored = []
    solution_found = False
    while True:
        moves = find_moves(maze_data, que[0])
        explored.append(que.pop(0))
        for move in moves:
            if move == end:
                solution_found = True
                break
            if move in explored or move in que:
                continue
            else:
                que.append(move)
        if solution_found:
            break

    move_list = [end]
    while True:
        moves = find_moves(maze_data, move_list[-1])
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


    return move_list[::-1], maze_data


if __name__ == '__main__':
   moves, data = main("Mazes/maze2.jpg", True )
   load_maze.draw_path("BFS_complete_path.png", moves, data)
   print(moves)