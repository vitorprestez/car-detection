# OpenCV Python program to detect cars in video frame
# import libraries of python OpenCV
import cv2

# capture frames from a video
cap = cv2.VideoCapture('tesstando.mp4')

# Trained XML classifiers describes some features of some object we want to detect
car_cascade = cv2.CascadeClassifier('cars.xml')

# loop runs if capturing has been initialized.
while True:
    # reads frames from a video
    ret, frames = cap.read()

    # convert to gray scale of each frames
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

    # Detects cars of different sizes in the input image
    cars, rejectLevels, levelWeigths = car_cascade.detectMultiScale3(
        gray, 1.1, 1, outputRejectLevels=True)
    print(levelWeigths)

    i = 0
    # To draw a rectangle in each cars
    for (x, y, w, h) in cars:
        if levelWeigths[i] > 1:
            cv2.rectangle(frames, (x, y), (x+w, y+h), (0, 0, 255), 2)
        if levelWeigths[i]:
            print(levelWeigths[i])
        i += 1
   # Display frames in a window
    cv2.imshow('video2', frames)

    # Wait for Esc key to stop
    if cv2.waitKey(1) & 0XFF == 27:
        break

# De-allocate any associated memory usage
cv2.destroyAllWindows()
