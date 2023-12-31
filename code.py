from time import sleep
import board
import digitalio
import usb_hid
import pwmio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

kbd = Keyboard(usb_hid.devices)

remotePushSequence = [Keycode.A, Keycode.B, Keycode.C, Keycode.D, Keycode.E, Keycode.F, Keycode.G, Keycode.H, Keycode.I, Keycode.J, Keycode.K, Keycode.L, Keycode.M]
remotePushSequencePosition = 0

ledDim = 5000   
ledBright = 30000 

remote1Btn = digitalio.DigitalInOut(board.GP0)
remote1Btn.direction = digitalio.Direction.INPUT 
remote1Btn.pull = digitalio.Pull.DOWN
remote1BtnIsDown = False

remote2Btn = digitalio.DigitalInOut(board.GP1)
remote2Btn.direction = digitalio.Direction.INPUT
remote2Btn.pull = digitalio.Pull.DOWN
remote2BtnIsDown = False

goBtn = digitalio.DigitalInOut(board.GP2)
goBtn.direction = digitalio.Direction.INPUT
goBtn.pull = digitalio.Pull.DOWN
goBtnIsDown = False

stopBtn = digitalio.DigitalInOut(board.GP3)
stopBtn.direction = digitalio.Direction.INPUT
stopBtn.pull = digitalio.Pull.DOWN
stopBtnIsDown = False

goLed = pwmio.PWMOut(board.GP4, frequency=ledBright)
goLed.duty_cycle = ledDim

stopLed = pwmio.PWMOut(board.GP5, frequency=ledBright)
stopLed.duty_cycle = ledDim

remoteLed = pwmio.PWMOut(board.GP6, frequency=ledBright)
remoteLed.duty_cycle = 0

showIsRunning = False
flashStatus = False

while True:
    if showIsRunning == False:
        #This is the show start safety
        #The black box will not respond to any remote commands unless the flashing green go button is pressed
        if flashStatus == False:
            flashStatus = True
            goLed.duty_cycle = ledBright
        else:
            flashStatus = False
            goLed.duty_cycle = 0
        
        if goBtn.value == 1:
            print("Start the Show")
            showIsRunning = True
            for duty in range(ledBright, ledDim, -1):
                goLed.duty_cycle = duty
                stopLed.duty_cycle = duty                
            goLed.duty_cycle = ledBright
            stopLed.duty_cycle = ledBright  
            sleep(0.25)
            goLed.duty_cycle = ledDim
            stopLed.duty_cycle = ledDim
        #flash delay
        sleep(0.1)
            
    else:
      
        if goBtn.value == 1 and not goBtnIsDown:
            print("Go Button Push - SPACE")      
            goBtnIsDown = True          
            kbd.send(Keycode.SPACE,)
            goLed.duty_cycle = ledBright
            #button bounce delay
            sleep(0.25)
            for duty in range(ledBright, ledDim, -2):
                goLed.duty_cycle = duty
        if goBtn.value == 0 and goBtnIsDown:
            print("Go Button Is Up")          
            goBtnIsDown = False
            #button bounce delay
            sleep(0.25)
            
        if stopBtn.value == 1 and not stopBtnIsDown:
            print("Stop Button Push - ESC")
            stopBtnIsDown = True
            kbd.send(Keycode.ESCAPE,)             
            stopLed.duty_cycle = ledBright
            #button delay
            sleep(0.25)
            for duty in range(ledBright, ledDim, -2):
                stopLed.duty_cycle = duty
        if stopBtn.value == 0 and stopBtnIsDown:
            print("Stop Button Is Up")
            stopBtnIsDown = False
            #button bounce delay
            sleep(0.25)
              
        if remote1Btn.value == 1 and not remote1BtnIsDown:
            print("Remote Button 1 Is Down")            
            print(remotePushSequence[remotePushSequencePosition])
            remote1BtnIsDown = True
            kbd.send(remotePushSequence[remotePushSequencePosition],)
            remotePushSequencePosition += 1
            if (remotePushSequencePosition + 1) > len(remotePushSequence):
                remotePushSequencePosition = 0
                showIsRunning = False
            remoteLed.duty_cycle = ledBright
            #button bounce delay
            sleep(0.25)
            for duty in range(ledBright, 0, -2):
                remoteLed.duty_cycle = duty
        if remote1Btn.value == 0 and remote1BtnIsDown:
            print("Remote Button 1 Is Up")
            remote1BtnIsDown = False
            #button bounce delay
            sleep(0.25)
       
        if remote2Btn.value == 1 and not remote2BtnIsDown:
            print("Remote Button 2 Is Down")  
            remote2BtnIsDown = True
            remotePushSequencePosition += 1
            #button bounce delay
            sleep(0.25)
        if remote2Btn.value == 0 and remote2BtnIsDown:
            print("Remote Button 2 Is Up")
            remote2BtnIsDown = False
            #button bounce delay
            sleep(0.25)
             
            
            
            
                
                
                        
                        
                    
       
            
                     
            
            
            

    

