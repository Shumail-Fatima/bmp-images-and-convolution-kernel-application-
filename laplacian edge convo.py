import struct
import shutil

fileNameAndPath = "image.bmp"
imageURL = "image_processed2.bmp"

# Copy the original file to create a writable duplicate
shutil.copyfile(fileNameAndPath, imageURL)
f2 = open(imageURL, "r+b")
f = open(fileNameAndPath, "rb")

# Read file size
f.seek(2)
fs = f.read(4)
fsize = struct.unpack("<I", fs)[0]
print("File size in bytes =", fsize)

# Read image width and height
f.seek(18)
width = struct.unpack("<I", f.read(4))[0]
height = struct.unpack("<I", f.read(4))[0]
print("Image width =", width)
print("Image height =", height)

# Read pixel array offset
f.seek(10)
offset = struct.unpack("<I", f.read(4))[0]
print("Pixel data starts at byte =", offset)

f.seek(offset)
f2.seek(offset)

# Read the pixel data into a 3D array (height x width x 3)
pixels = []
for h in range(height):
    row = []
    for w in range(width):
        b, g, r = f.read(1), f.read(1), f.read(1)
        row.append([b[0], g[0], r[0]])
    pixels.append(row)

# Sharpening convolution mask
mask = [[-1,-1,-1],
                  [-1,8,-1],
                  [-1,-1,-1]]

# Helper function to clamp values to [0, 255]
def clamp(value):
    return max(0, min(255, value))

# Apply convolution
def apply_convolution(pixels, height, width):
    output = [[[0, 0, 0] for _ in range(width)] for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            for color in range(3):  # Process each color channel separately
                new_value = 0
                for ky in range(-1, 2):
                    for kx in range(-1, 2):
                        new_value += pixels[y + ky][x + kx][color] * mask[ky + 1][kx + 1]
                output[y][x][color] = clamp(new_value)
    
    return output

processed_pixels = apply_convolution(pixels, height, width)

# Write the processed pixels back to the output file
for h in range(height):
    for w in range(width):
        b, g, r = processed_pixels[h][w]
        f2.write(bytes([b, g, r]))

print("Processing complete")
f2.close()
f.close()
