#/usr/bin/python3

import re
import os

#temporary hardcoded image path
filepath = "PXL_TEST_IMAGE.jpg"
pictureFilepath = "IMG.jpg"
videoFilepath = "VID.mp4"

filesize = os.stat(filepath).st_size

# open the file found at the filepath in binary mode and read in the data 
file = open(filepath, "rb")
filedata = file.read()

# use the filedata library to find the start and end xmp tags and then extract everything in between
xmp_start=filedata.find(b'<x:xmpmeta')
xmp_end = filedata.find(b'</x:xmpmeta')
xmp_bytes = filedata[xmp_start:xmp_end+12]

# close up the file
file.close()

# convert the binary to a string
xmp_str = str(xmp_bytes)

# use a regular expression to get the strings that have "Length=*SOMENUMBER*" and then use a second regular expression to extract the numbers
lst = re.findall("Length=\"[^\"]*\"", xmp_str)
numstr =  re.findall(r'\d+', lst[0]+lst[1])

# find the maximum number out of the two numbers as the order could change or there could be multiple values
splitpoint = 0
for number in numstr:
    if int(number) > splitpoint and int(number) < filesize:
        splitpoint = int(number)


CHUNK_SIZE = 4096
# open all the files up
file = open(filepath, "rb")

try:
    picturefile = open(pictureFilepath, "wb")
    videofile = open(videoFilepath, "wb")
except:
    print("one of these files already exists")
    

curr_location = 0

chunk = file.read(CHUNK_SIZE)
curr_location += CHUNK_SIZE
flag = 0

# the splitpoint tells you how big the video is, not how big the photo is so we need to copy the photo until we make it to the video, so take the total size minus the size of the video and thats the photo size
splitpoint = filesize - splitpoint
while chunk:

    if curr_location <= splitpoint:
        picturefile.write(chunk)
        #print(splitpoint)
    else:
        videofile.write(chunk)
        #print(splitpoint)
    
    if curr_location + CHUNK_SIZE <= splitpoint:
        print("hi")
        chunk = file.read(CHUNK_SIZE)
        curr_location += CHUNK_SIZE
    elif not flag and (curr_location + CHUNK_SIZE > splitpoint ):
        
        chunk = file.read(splitpoint - curr_location )
        curr_location += (splitpoint - curr_location )
        flag = 1 # we need a flag because we get here once when the chunksize is bigger than the gap between the current location and then every time after because the current location is past the splitpoint
    else:
        chunk = file.read(CHUNK_SIZE)
        curr_location += CHUNK_SIZE
    
    


