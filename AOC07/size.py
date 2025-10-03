import os
# ls gives directories

# I can make a "file" class with: 
# type - folder/file 
# children - [list]
# size 



class File: 
    def __init__(self, name, type, parent, size):
        name = name 
        type = type
        #children = children 
        parent = parent
        size = size

# parse input into a list? 
files = {}

file_path = 'AOC07/input.txt'

with open(file_path, 'r') as file:
    input = file.read()

lines = input.split("\n")

list_2d = [line.split() for line in lines]
print("list: ", list_2d[:10])

# $ cd name 
# $ ls 
# $ cd ".." (going up a level?)
# single dot exists - a file name -> size exists 

# loop needs to record file names and sizes

current_path = "/"
filesystem = {} 
# 
for line in list_2d:
    if line[0] == "$":
        if line[1] == "cd":
            if line[2] == "..":
                # Go up: remove last part of current path
                current_path = "/".join(current_path.rstrip("/").split("/")[:-1]) or "/" 
            elif line[2] == "/":
                current_path = "/" 
            else:    
                # go down: add to path
                current_path = current_path.rstrip("/") + "/" + line[2]
        
    elif line[0] == "dir":
        # add subdirectory to current path
        dir_name = line[1]
        if current_path not in filesystem:
            filesystem[current_path] = {"files": [], "subdirs": []}
        filesystem[current_path]["subdirs"].append(dir_name)

    else:
        # add files to current path
        file_size = int(line[0])
        file_name = line[1]
        if current_path not in filesystem:
            filesystem[current_path] = {"files": [], "subdirs": []}
        filesystem[current_path]["files"].append((file_name, file_size))

# Function to calculate directory size recursively
def calculate_dir_size(dir_path):
    if dir_path not in filesystem:
        return 0
    
    total_size = 0
    
    # Add size of files in this directory
    for file_name, file_size in filesystem[dir_path]["files"]:
        total_size += file_size
    
    # Add size of subdirectories recursively
    for subdir in filesystem[dir_path]["subdirs"]:
        subdir_path = dir_path.rstrip("/") + "/" + subdir
        total_size += calculate_dir_size(subdir_path)
    
    return total_size

# Calculate sizes for all directories
dir_sizes = {}
for dir_path in filesystem:
    dir_sizes[dir_path] = calculate_dir_size(dir_path)

# Find directories with size <= 100000
small_dirs = {path: size for path, size in dir_sizes.items() if size <= 100000}

print("Small directories (<= 100000):")
for path, size in small_dirs.items():
    print(f"{path}: {size}")

print(f"\nSum of small directories: {sum(small_dirs.values())}")
