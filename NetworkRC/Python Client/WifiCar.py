import requests
import win32api
import time

url = 'http://192.168.8.108/controls'

def keyState(keys):
    stack = []
    for key in keys:
        state = win32api.GetAsyncKeyState(ord(key))
        if(state < 0 or state == 1):
            stack.append(key)
    return stack

def main():
    pwmInc = 1023 # 1 - 1023
    steerInc = 20 #1 - 20
    speed = 0
    direction = 1
    steerAngle = 76
    payload = {}
    payload['aSpeed'] = str(speed)
    payload['aDir'] = str(direction)
    payload['steerAngle'] = str(steerAngle)
    on = False
    while True:
        keysOn = keyState('WASD')
        if(keysOn):
            if 'S' and 'D' not in keysOn:
                steerAngle = 76
            if 'W' or 'S' not in keysOn:
                speed = 0
            on = True
            for key in keysOn:
                if(key == 'W'):
                    if speed < 1023:
                        speed += pwmInc
                    if speed > 1023:
                        speed = 1023
                if(key == 'S'):
                    if speed > -1023:
                        speed -= pwmInc
                    if speed < -1023:
                        speed = -1023
                if(key == 'A'):
                    if steerAngle > 40:
                        steerAngle -= steerInc
                if(key == 'D'):
                    if steerAngle < 100:
                        steerAngle += steerInc
            if speed > 0:
                direction = 1
            else:
                direction = 0
        else:
            speed = 0
            direction = 1
            steerAngle = 76
        if speed < -1:
            payload['aSpeed'] = str(speed*-1)
        else:
            payload['aSpeed'] = str(speed)
        payload['aDir'] = str(direction)
        payload['steerAngle'] = str(steerAngle)
        if on:
            r = requests.get(url, params=payload)
            print(r.text, '\n')
            if speed == 0 and steerAngle == 76:
                on = False
                
main()
