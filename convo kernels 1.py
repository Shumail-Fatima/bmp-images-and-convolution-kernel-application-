#Syntax==>variable=open("filename","mode")
import struct
import shutil

fileNameAndPath = "image.bmp"
imageURL="image(bright3).bmp"


shutil.copyfile(fileNameAndPath,imageURL)
f2=open(imageURL,"r+b")
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
f2.seek(offset[0],0)

light=100

cv=100000
cv=(100+cv)/255

def color(value):
    if value<0:
        value=0
    elif value>255:
        value=255
    return value


def contrast(x):    
    nv=x
    nv=nv/255
    nv=nv-0.5
    nv=nv*cv
    nv=nv+0.5
    nv=nv*255
    nv=int(nv)
    return(nv)


for r in range(0,height[0]-1,1):
##
    for c in range(0,width[0],1):
##
        b = f.read(1)
        g = f.read(1)
        r = f.read(1)
        b = b[0]
        g = g[0]
        r = r[0]

#-------calculation for negative image--------------       
##        b=255-b
##        g=255-g
##        r=255-r

#-------calculation for grayscale image---------
        #print(b,g,r)
        #avg=(b+g+r)//3
        #gsc=int(avg).to_bytes(1,'little')

#--------calculation for brightness---------------------------
        #b=color(b-light)
        #g=color(g-light)
        #r=color(r-light)

        b = max(0, min(255, b + light))
        g = max(0, min(255, g + light))
        r = max(0, min(255, r + light))

#---------calculation for contrast---------------------------
#        bl=contrast(b)
#        gr=contrast(g)
#        re=contrast(r)
        
#        b=color(bl)
#        g=color(gr)
#        r=color(re)
#---------pixel for other calcs images------------------------
        b=int(b).to_bytes(1,'little')
        g=int(g).to_bytes(1,'little')
        r=int(r).to_bytes(1,'little')
##        print (gsc,gsc,gsc)
#------pixels for grey image--------------
#        b = gsc
#        g = gsc
#        r = gsc
#-------write new pixel value------------------        
        f2.write(b)
        f2.write(g)
        f2.write(r)
##        
f2.close()
f.close()

