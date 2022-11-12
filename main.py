# PW Fishing Bot by Abyan Majid

from mss import mss
import cv2 as cv
from PIL import Image
import numpy as np
from time import time, sleep
import autoit
import pyautogui
import win32gui, win32ui, win32con

# Templates
lurebox = cv.imread('lurebox.png')
strike = cv.imread('strike.png')
fishbox = cv.imread('fishbox.png')

fish = cv.imread('fish.png')
green = cv.imread('greenfish.png')
red = cv.imread('redfish.png')

catch = cv.imread('catch.png')
takefish = cv.imread('takefish.png')

# Screen and Window
window = {'top': 99, 'left': 93, 'width': 650, 'height': 60} # Area of Window To Be Captured
screen = mss()

def fishing():
    # Match lurebox
    threshold = 0.8
    lurebox_result = cv.matchTemplate(img_bgr, lurebox, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(lurebox_result)
    if max_val >= threshold:
        print('Searching fish...')
        autoit.mouse_click("left", max_loc[0], max_loc[1], 20)
        
        searching_fish = True
        while searching_fish:
            # Match Strike
            threshold = 0.5
            strike_result = cv.matchTemplate(img_bgr, strike, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(strike_result)
            if max_val >= threshold:
                print('Fish found!')   
                sleep(1)
                pyautogui.press('space')
            

while True:
    # Exit by pressing ~
    if cv.waitKey(1) & 0xFF == ord('`'):
        cv.destroyAllWindows()
        break
    
    begin_time = time()
    screen_img = screen.grab(window)
    img = Image.frombytes('RGB', (screen_img.size.width, screen_img.size.height), screen_img.rgb)
    img_bgr = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
    cv.imshow('test', np.array(img_bgr))
    
    threshold = 0.8
    # Fish match
    fish_result = cv.matchTemplate(img_bgr, fish, cv.TM_CCOEFF_NORMED)
    fish_min_val, fish_max_val, fish_min_loc, fish_max_loc = cv.minMaxLoc(fish_result)
    
    # Green Fish match
    green_result = cv.matchTemplate(img_bgr, green, cv.TM_CCOEFF_NORMED)
    green_min_val, green_max_val, green_min_loc, green_max_loc = cv.minMaxLoc(green_result)
    
    # Red Fish match
    red_result = cv.matchTemplate(img_bgr, red, cv.TM_CCOEFF_NORMED)
    red_min_val, red_max_val, red_min_loc, red_max_loc = cv.minMaxLoc(red_result)
    
    # Fishbox match
    fishbox_result = cv.matchTemplate(img_bgr, fishbox, cv.TM_CCOEFF_NORMED)
    box_min_val, box_max_val, box_min_loc, box_max_loc = cv.minMaxLoc(fishbox_result)
    
    if box_max_val >= threshold:
        # print('Fish Correlation: %s' % fish_max_val) # correlation value between object and best match in img
        # print('Fishbox Correlation: %s' % box_max_val)
        autoit.mouse_click("left", 290, 432, 1)
        if box_max_loc[0] > fish_max_loc[0] or box_max_loc[0] > red_max_loc[0] or box_max_loc[0] > green_max_loc[0]:
            pyautogui.keyUp('d')
            pyautogui.keyDown('a')
        else:
            pyautogui.keyUp('a')
            pyautogui.keyDown('d')
    
    # min_val, max_val, min_loc, max_loc = cv.minMaxLoc(lurebox_result)
    # strike_result = cv.matchTemplate(img_bgr, lurebox, cv.TM_CCOEFF_NORMED)
    # fishbox_result = cv.matchTemplate(img_bgr, lurebox, cv.TM_CCOEFF_NORMED)
    # fish_result = cv.matchTemplate(img_bgr, lurebox, cv.TM_CCOEFF_NORMED)
    # catch_result = cv.matchTemplate(img_bgr, lurebox, cv.TM_CCOEFF_NORMED)
    # takefish_result = cv.matchTemplate(img_bgr, lurebox, cv.TM_CCOEFF_NORMED)
    
    # Print FPS
    print('FPS: {}'.format(1 / (time() - begin_time)))