# import statements
import cv2
import numpy as np
import pyautogui
import keyboard

# start video capture
cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)


    # defining the region of interest for efficiency - loop play
    roi = frame[75:200, 75:200]

    # defining the region of interest for recording
    # note for self: the range for y comes first apparently
    roi_2 = frame[75:200, 250:375]


    # drawing a rectangle around the first region of interest
    cv2.putText(frame, "Loop", (75, 63), cv2.FONT_HERSHEY_SIMPLEX, 1, (203, 192, 255), 2, cv2.LINE_AA)
    cv2.rectangle(frame, (75, 75), (200, 200), (0, 0, 0), 2)

    # drawing a rectangle around the second region of interest
    cv2.putText(frame, "Record", (250, 63), cv2.FONT_HERSHEY_SIMPLEX, 1, (203, 192, 255), 2, cv2.LINE_AA)
    cv2.rectangle(frame, (250, 75), (375, 200), (0, 0, 0), 2)

    # creating a gaussian blurred frame
    blurred_frame = cv2.GaussianBlur(roi, (5, 5), 0)

    # creating a gaussian blurred frame for the second  roi
    blurred_frame_2 = cv2.GaussianBlur(roi_2, (5, 5), 0)

    # converting BGR to HSV for the first roi
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    # converting BGR to HSV for the second roi
    hsv_2 = cv2.cvtColor(blurred_frame_2, cv2.COLOR_BGR2HSV)


    # mask creation for brown-ish objects since the headstock of my guitar is brown
    # This code isn't really the best way to go about it, so I used the colour of my tuner instead
    #lower_brown = np.array([10, 100, 50], dtype=np.uint8)
    #upper_brown = np.array([20, 255, 200], dtype=np.uint8)

    # color of guitar tuner
    lower_blue = np.array([100, 150, 0], dtype=np.uint8)
    upper_blue = np.array([255, 255, 255], dtype=np.uint8)


    # mask for the first roi
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # mask for the second roi
    mask_2 = cv2.inRange(hsv_2, lower_blue, upper_blue)

    # filtering kernel
    kernel = np.ones((3, 3), np.uint8)

    # filtering for blue mask
    mask = cv2.dilate(mask, kernel, iterations=4) # dilation
    mask = cv2.GaussianBlur(mask, (5, 5), 100) # gaussian blur filtering

    # filtering for blue mask in the second roi
    mask_2 = cv2.dilate(mask_2, kernel, iterations=4) # dilation
    mask_2 = cv2.GaussianBlur(mask_2, (5, 5), 100) # gaussian blur filtering

    # finding contours for the masked objects/blue objects
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # finding contours for the blue objects in the second roi
    contours_2, _ = cv2.findContours(mask_2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


    # sorting the contours in ascending order
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    contours_2 = sorted(contours_2, key=lambda x: cv2.contourArea(x), reverse=True)

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 300:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.circle(roi, (x, y), 20, (0, 255, 0), 2)
            cv2.drawContours(roi, contour, -1, (255, 0, 0), 1)

            # He's a little confused, but he's got the spirit
            if x > 75 and y > 75 and x < 200 and y < 200:
                cv2.putText(frame, "No Action", (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame, "Action", (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                keyboard.press_and_release('shift + space')


    for contour_2 in contours_2:
        area = cv2.contourArea(contour_2)

        if area > 300:
            (x, y, w, h) = cv2.boundingRect(contour_2)
            cv2.circle(roi_2, (x, y), 20, (0, 255, 0), 2)
            cv2.drawContours(roi_2, contour_2, -1, (255, 0, 0), 1)


            if x > 250 and y > 75 and x < 375 and y < 200:
                cv2.putText(frame, "No Action", (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame, "Record", (500, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                keyboard.press_and_release('r')
                keyboard.press_and_release('enter')







    # opening the mask window for reference
    cv2.imshow("Mask", mask)

    # resizing and showing the main window
    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Frame", 1400, 1000)
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
