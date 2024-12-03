#matrix=[[0,0,0,0,0],[1,1,1,1,1],[0,0,0,0,0],[1,1,1,1,1]]
##matrix=[[0,0,0,0],
##        [1,0,0,0],
##        [0,1,0,0],
##        [0,0,1,0],
##        [0,0,0,1]]

import struct

fileNameAndPath = "lines.bmp"

f = open (fileNameAndPath,"rb")

fs=f.read(4)
print(fs)

fsize=struct.unpack("i",fs)
print ("File size in bytes = ", fsize)#

f.seek(18,0)
w = f.read(4)
width=struct.unpack("i",w)
print ("Image width = ", width[0])# 348

h = f.read(4)
height=struct.unpack("i",h)
print ("Image height = ", height[0]) # 328

f.seek(10,0)
o = f.read(4)
offset = struct.unpack("i",o)
f.seek(offset[0],0)


rows=[]
for y in range(height[0]):
    cols=[]
    for x in range(width[0]):
        bl = f.read(1)
        gr = f.read(1)
        re = f.read(1)
        blue = bl[0]
        green = gr[0]
        red = re[0]        
        if (blue==255 and green==255 and red==255):  #when pixels (r,g,b) equal to white
            cols.append(0)
        else:
            cols.append(1)
    rows.append(cols)
print(len(cols))
matrix=rows
print(len(matrix))
#print ("matrix=",matrix)

# Iterative blob counting function
def blobCountIterative(img, r, c):
    if img[r][c] == 0:  # If the starting cell is not part of a blob
        return 0

    stack = [(r, c)]  # Stack to track cells to visit
    count = 0

    while stack:
        x, y = stack.pop()
        if x < 0 or y < 0 or x >= len(img) or y >= len(img[0]):  # Boundary check
            continue
        if img[x][y] == 0:  # Skip already visited or zero-value cells
            continue

        # Mark cell as visited
        img[x][y] = 0
        count += 1

        # Push all 4-connected neighbors onto the stack
        stack.append((x-1, y))  # Up
        stack.append((x+1, y))  # Down
        stack.append((x, y-1))  # Left
        stack.append((x, y+1))  # Right

    return count


road=1    
for row in range(len(matrix)):
    for col in range(len(matrix[0])):
        if matrix[row][col]==1:
            num=blobCountIterative(matrix,row,col)
        else:
            continue
        print("length of road ",road," is ",num," pixels")
        road+=1
