import cv2
import numpy as np

img = cv2.imread('cat.jpg')
img_dup = np.copy(img)
mouse_pressed = False
# defining starting and ending point of rectangle (crop image region)
starting_x = starting_y = ending_x = ending_y = -1

def mousebutton(event, x, y, flags, param):
    global img_dup, starting_x, starting_y, ending_x, ending_y, mouse_pressed
    # if left mouse button is pressed then takes the cursor position at starting_x and starting_y
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_pressed = True
        starting_x, starting_y = x, y
        img_dup = np.copy(img)

    elif event == cv2.EVENT_MOUSEMOVE:
        if mouse_pressed:
            img_dup = np.copy(img)
            radius = np.sqrt((x - starting_x)**2 + (y - starting_y)**2)
            cv2.circle(img_dup, (starting_x, starting_y), int(radius), (0, 255, 0), 1)
            # cv2.rectangle(img_dup,(starting_x,starting_y),(x,y),(0,255,0),1)
    # final position of rectange if left mouse button is up then takes the cursor position at ending_x and ending_y
    elif event == cv2.EVENT_LBUTTONUP:
        mouse_pressed = False
        ending_x, ending_y = x, y

cv2.namedWindow('image')
cv2.setMouseCallback('image', mousebutton)

while True:
    cv2.imshow('image', img_dup)
    k = cv2.waitKey(1)
    if k == ord('c'):
        # remove these condition and try to play weird output will give you idea why its done
        if starting_x > ending_x:
            starting_x, ending_x = ending_x, starting_x
        if ending_y - starting_y > 1 and ending_x - starting_x > 0:
            radius = np.sqrt((ending_x - starting_x)**2 + (ending_y - starting_y)**2)
            mask = np.zeros_like(img)  # create a mask with the same size as the image
            cv2.circle(mask, (starting_x, starting_y), int(radius), (255, 255, 255), -1)  # draw a white circle on the mask
            cropped_img = cv2.bitwise_and(img, mask)  # apply the mask to the image
            img_dup = np.copy(cropped_img)
    elif k == 27:
        break

cv2.destroyAllWindows()
