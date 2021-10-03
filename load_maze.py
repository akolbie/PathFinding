from PIL import Image
from time import sleep
import numpy as np
import csv
from numpy.core.numeric import outer
from numpy.lib.function_base import average

def load_image(location):
    image = Image.open(location)
    image_data = np.asarray(image)

    return image_data

def write_image(location, data):
    with open(location, 'w+') as f:
        csv_writer = csv.writer(f)
        for row in data:
            csv_writer.writerow(row)

def remove_white_border(image_data):
    i, j, k, z = 0, 0, 0, 0
    rev_data = image_data[::-1]
    output_data = []
    for index, row in enumerate(image_data): #finds start of black border @ top
        if 0 in row:
            i = index
            break
    for index, row in enumerate(rev_data): #find end of black border @ bottom
        if 0 in row:
            j = index
            break
    for ii in range(len(image_data[0])): # find start of black border @ left
        if 0 in image_data[:,ii]:
            k = ii
            break
    for ii in range(1, len(image_data[0])): # find end of black border @ right
        if 0 in image_data[:, len(image_data[0]) - ii]:
            z = ii
            break
    
    output_data = []
    for index, row in enumerate(image_data[i:-j]):
        output_data.append(row[k:-z+1]) # removes left and right white border

    return output_data


def find_smallest(colour, data):
    smallest = 1000
    current = 0
    for row in data:
        for i in row:
            if i != colour:
                if current < smallest and current != 0:
                    smallest = current
                current = 0
                continue
            else:
                current += 1
        if current < smallest and current != 0:
            smallest = current
        current = 0
    return smallest

def num_sections(data_length, yes, no):
    sections = (data_length - no) // (no + yes) #finds how many sections there are of no and yes
    sections *= 2 # multiplies by 2 to account for both yes and no
    sections += 1 # adds 1 for iniital no
    return int(sections)

def create_grid(data, yes_row, yes_col, no_row, no_col):
    test1 = len(data) - no_col
    test1 = test1 % (yes_col + no_col)
    test2 = len(data[0]) - no_row
    test2 = test2 % (yes_row + no_row)

    if test1 + test2 != 0:
        print(f"Error, data length {len(data)} or {len(data[0])} not divisable")
        return 0
    sections_col = num_sections(len(data), yes_col, no_col)
    sections_row = num_sections(len(data[0]), yes_row, no_row)

    output_grid = []


    for i in range(sections_row):
        no_row_multipler = i // 2 + i % 2
        yes_row_multipler = i // 2
        ii = no_row_multipler * no_row + yes_row_multipler * yes_row
        
        output_grid.append([])
        
        for j in range(sections_col):
            no_col_multipler = j // 2 + j % 2
            yes_col_multipler = j // 2
            jj = no_col_multipler * no_col + yes_col_multipler * yes_col

            output_grid[-1].append(data[ii][jj])

    return output_grid

def find_start_end(data):
    output = []
    for index, i in enumerate(data[0]):
        if i == 1:
            output.append([0, index])
            if len(output) == 2:
                return output[0], output[1]
    for index, i in enumerate(data[-1]):
        if i == 1:
            output.append(len(data) - 1, index)
            if len(output) == 2:
                return output[0], output[1]

    for i in range(len(data)):
        if data[i][0] == 1:
            output.append([i, 0])
        if data[i][-1] == 1:
            output.append([i, len(data[0]) - 1])
        if len(output) == 2:
            return output[0], output[1]
    print(f'Error, only found entrance {output}')
    return 0

def change_shape(data):
    output = []
    for row in data:
        output.append([])
        for column in row:
            if average(column) <= 127:
                output[-1].append(0)
            else:
                output[-1].append(1)
    return output

def normalize(data):
    output = []
    for i in range(len(data)):
        output.append([])
        for j in range(len(data[0])):
            if data[i][j] == 0:
                output[-1].append(0)
            else:
                output[-1].append(1)
    return output

def get_grid(input_location, white_border = False):
    data = load_image(input_location)
    print(data.shape)
    if len(data.shape) > 2:
        data = change_shape(data)
        data = np.array(data)
        print(data.shape)
    data = normalize(data)

    if white_border:
        data = remove_white_border(np.array(data))
        image = Image.fromarray(np.uint8(data * 255), "L")
        image.save("testing1.png")
    white_row_smallest = find_smallest(1, data)
    white_col_smallest = find_smallest(1, np.transpose(data))
    black_row_smallest = find_smallest(0, data)
    black_col_smallest = find_smallest(0, np.transpose(data))
    maze_grid = create_grid(
        data,
        white_row_smallest,
        white_col_smallest,
        black_row_smallest,
        black_col_smallest
    )
    start, end = find_start_end(maze_grid)

    return maze_grid, start, end

def draw_explored(points, data):
    for point in points:
        data[point[0]][point[1]] = .3
    return data

def draw_path(output_location, points, data):
    for point in points:
        data[point[0]][point[1]] = 0.6
    data_array = np.array(data)
    image = Image.fromarray(np.uint8(data_array * 255), "L")
    image.save(output_location)

if __name__ == "__main__":
    # data = load_image("Mazes/maze1.gif")
    # data_no_border = remove_white_border(data)
    # data_no_border_array = np.array(data_no_border)
    # white_row_smallest = find_smallest(1, data_no_border)
    # white_col_smallest = find_smallest(1, np.transpose(data_no_border))
    # black_row_smallest = find_smallest(0, data_no_border)
    # black_col_smallest = find_smallest(0, np.transpose(data_no_border))
    # maze_grid = create_grid(
    #     data_no_border_array,
    #     white_row_smallest,
    #     white_col_smallest,
    #     black_row_smallest,
    #     black_col_smallest
    # )
    # start, end = find_start_end(maze_grid)
    # maze_grid_array = np.array(maze_grid)
    # image = Image.fromarray(np.uint8(maze_grid_array * 255), "L")
    # image.save('test.png')
    #grid, start, end = get_grid("Mazes/maze1.gif",True)
    #grid, start, end = get_grid("Mazes/maze2.jpg", True)
    grid, start, end = get_grid("Mazes/maze3.png")
    print(f"{start} {end}")
    
