#/usr/bin/python3

##############################
# 
# Written by Connor Corso
# 
# Game plan is to have one endpoint that will return the video portion of a file and one endpoint that will return only the picture
# 
# 
# 
##############################


import re #regex

from fastapi import FastAPI, UploadFile

import tempfile

# to handle sending a zip back down to the client
from fastapi.responses import FileResponse

# fast api stuff
app = FastAPI()
CHUNK_SIZE = 4096 # the size of chunks that we will use when moving parts of files around, I have no idea what a good value would be

async def get_file_data(inputfile):
    # read the inputfile
    await inputfile.seek(0)
    filedata = await inputfile.read()
    filesize = len(inputfile)

    # use the filedata library to find the start and end xmp tags and then extract everything in between
    xmp_start=filedata.find(b'<x:xmpmeta')
    xmp_end = filedata.find(b'</x:xmpmeta')
    xmp_bytes = filedata[xmp_start:xmp_end+12]

    # close up the file
    

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
    
    # the splitpoint tells you how big the video is, not how big the photo is so we need to copy the photo until we make it to the video, so take the total size minus the size of the video and thats the photo size
    splitpoint = filesize - splitpoint

    return splitpoint


# this endpoint will accept a file and will return the video portion of the file
@app.post("/splitfiles/video")
async def recover_video(file: UploadFile):
    ###################################
    # get the splitpoint
    splitpoint = await get_file_data(UploadFile)

    ###################################
    # get the video portion of the file

    try:
        # open up a temporary file to store the video in
        videofile = tempfile.NamedTemporaryFile(delete=True)
        
    
        # go to the seekpoint, because everything after that is the video
        UploadFile.seek(splitpoint)
        chunk = file.read(CHUNK_SIZE)

        while chunk:
            videofile.write(chunk)
            chunk = file.read(CHUNK_SIZE)

        ###################################
        # return the video portion of the file
        videofile.seek(0)
        return FileResponse(videofile.name, media_type='video/mp4')

    except Exception as e:
        print(f"failed somewhere: {str(e)}")
        return {"result": "failed"}




@app.post("/splitfiles/image")
async def recover_image(file: UploadFile):
    ###############################
    # get the splitpoint
    splitpoint = await get_file_data(UploadFile)
    
    ###############################
    # get the image portion of the file

    try:
        # open up a temporary file to store the video in
        imagefile = tempfile.NamedTemporaryFile(delete=True)
        

        # copy up until the seekpoint, because everything after that is the video
        position = 0
        await UploadFile.seek(splitpoint)
        chunk = await file.read(CHUNK_SIZE)
        position += CHUNK_SIZE

        while chunk:
            imagefile.write(chunk)
            # if the current position plus the chunk size goes past the splitpoint then only read up until the splitpoint
            if position + CHUNK_SIZE > splitpoint:
                chunk = await file.read(splitpoint - position)
                imagefile.write(chunk)
                break
            else: # otherwise just read a regular sized chunk
                chunk = await file.read(CHUNK_SIZE)


        ###################################
        # return the image portion of the file
        imagefile.seek(0)
        return FileResponse(imagefile.name, media_type='image/jpeg')

    except Exception as e:
        print(f"failed somewhere: {str(e)}")
        return {"result": "failed"}