import cv2

# This function extracts a frame from the given video in between the given
# start and end data points.
def extractFrame(video_filename, start, end, filename):

    # Every 500 rows = 1 second
    # Calculates the frame that is to be extracted
    seconds_elapsed_start = start / 500
    seconds_elapsed_end = end / 500
    seconds_elapsed_mid = ((seconds_elapsed_end - seconds_elapsed_start) / 2) + seconds_elapsed_start
    frameNum = round(seconds_elapsed_mid * 25)

    # Iterates until the desired frame is selected, saves the frame under the given filename
    vidcap = cv2.VideoCapture(video_filename)
    readSuccess, image = vidcap.read()
    counter = 0
    while (counter <= frameNum):
        if(counter == frameNum):
            cv2.imwrite(filename, image)
        readSuccess, image = vidcap.read()
        counter += 1

    return