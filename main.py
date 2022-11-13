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
window = {'top': 99, 'left': 93, 'width': 650, 'height': 130} # Area of Window To Be Captured
screen = mss()

while True:
    # Exit by pressing ~
    if cv.waitKey(1) & 0xFF == ord('`'):
        cv.destroyAllWindows()
        break
    
    begin_time = time()
    screen_img = screen.grab(window)
    img = Image.frombytes('RGB', (screen_img.size.width, screen_img.size.height), screen_img.rgb)
    img_bgr = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
    cv.imshow('Computer Vision', np.array(img_bgr))
    
    threshold = 0.7
    
    # Catch match
    catch_result = cv.matchTemplate(img_bgr, catch, cv.TM_CCOEFF_NORMED)
    catch_min_val, catch_max_val, catch_min_loc, catch_max_loc = cv.minMaxLoc(catch_result)
    
    # Fishbox match
    fishbox_result = cv.matchTemplate(img_bgr, fishbox, cv.TM_CCOEFF_NORMED)
    box_min_val, box_max_val, box_min_loc, box_max_loc = cv.minMaxLoc(fishbox_result)
    
    # Fish match
    fish_result = cv.matchTemplate(img_bgr, fish, cv.TM_CCOEFF_NORMED)
    fish_min_val, fish_max_val, fish_min_loc, fish_max_loc = cv.minMaxLoc(fish_result)
        
    # Take fish match
    takefish_result = cv.matchTemplate(img_bgr, takefish, cv.TM_CCOEFF_NORMED)
    takefish_min_val, takefish_max_val, takefish_min_loc, takefish_max_loc = cv.minMaxLoc(takefish_result)
    
    # Strike match
    strike_result = cv.matchTemplate(img_bgr, strike, cv.TM_CCOEFF_NORMED)
    strike_min_val, strike_max_val, strike_min_loc, strike_max_loc = cv.minMaxLoc(strike_result)
    
    if takefish_max_val >= threshold:
        autoit.mouse_click("left", 404, 512, 1)
        
    elif catch_max_val >= threshold:
        pyautogui.press('w')

    elif box_max_val >= threshold:
        if box_max_loc[0] > (fish_max_loc[0] - 5):
            pyautogui.keyUp('d')
            pyautogui.keyDown('a')
        elif box_max_loc[0] < (fish_max_loc[0] + 5):
            pyautogui.keyUp('a')
            pyautogui.keyDown('d')
            
    elif strike_max_val >= threshold:
        autoit.mouse_click("left", 404, 512, 1)
        pyautogui.press('w')
    
    else:
        pyautogui.moveTo(486, 430)
        autoit.mouse_click('left', 484, 424)
        sleep(1.5)
    
    # Print FPS
    print('FPS: {}'.format(1 / (time() - begin_time)))