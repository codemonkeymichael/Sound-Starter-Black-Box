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

#not wired
#remote2Btn = digitalio.DigitalInOut(board.GP1)
#remote2Btn.direction = digitalio.Direction.INPUT
#remote2Btn.pull = digitalio.Pull.DOWN

goBtn = digitalio.DigitalInOut(board.GP2)
goBtn.direction = digitalio.Direction.INPUT
goBtn.pull = digitalio.Pull.DOWN

stopBtn = digitalio.DigitalInOut(board.GP3)
stopBtn.direction = digitalio.Direction.INPUT
stopBtn.pull = digitalio.Pull.DOWN

goLed = pwmio.PWMOut(board.GP4, frequency=ledBright)
goLed.duty_cycle = ledDim

stopLed = pwmio.PWMOut(board.GP5, frequency=ledBright)
stopLed.duty_cycle = ledDim

remoteLed = pwmio.PWMOut(board.GP6, frequency=ledBright)
remoteLed.duty_cycle = 0

gunIsCocked = False
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
            for duty in range(ledBright, ledDim, -10):
                goLed.duty_cycle = duty
                stopLed.duty_cycle = duty
                sleep(0.001)
            goLed.duty_cycle = ledBright
            stopLed.duty_cycle = ledBright  
            sleep(2.5)
            goLed.duty_cycle = ledDim
            stopLed.duty_cycle = ledDim
        #flash delay
        sleep(0.1)
            
    else:
              
        if goBtn.value == 1:
            kbd.send(Keycode.SPACE,)
            print("Go Button Push - SPACE")
            goLed.duty_cycle = ledBright
            #button delay
            sleep(1.0)
            for duty in range(ledBright, ledDim, -3):
                goLed.duty_cycle = duty                
        if stopBtn.value == 1:
            kbd.send(Keycode.ESCAPE,) 
            print("Stop Button Push - ESC")
            stopLed.duty_cycle = ledBright
            #button delay
            sleep(1.0)
            for duty in range(ledBright, ledDim, -3):
                stopLed.duty_cycle = duty
                   
              
        if remote1Btn.value == 1 and gunIsCocked == False:        
            gunIsCocked = True
            kbd.send(remotePushSequence[remotePushSequencePosition],)
            remotePushSequencePosition += 1
            if (remotePushSequencePosition + 1) > len(remotePushSequence):
                remotePushSequencePosition = 0
                showIsRunning = False
            remoteLed.duty_cycle = ledBright
            for duty in range(ledBright, 0, -20):
                remoteLed.duty_cycle = duty
                sleep(0.001)
                           
        if remote1Btn.value == 0 and gunIsCocked == True:
                gunIsCocked = False
                kbd.send(remotePushSequence[remotePushSequencePosition],)        
                print("Remote Button D Push " + str(remotePushSequence[remotePushSequencePosition]))
                remotePushSequencePosition += 1
                if (remotePushSequencePosition + 1) > len(remotePushSequence):
                    remotePushSequencePosition = 0
                    showIsRunning = False
                remoteLed.duty_cycle = ledBright       
                for duty in range(ledBright, 0, -20):
                    remoteLed.duty_cycle = duty
                    sleep(0.001)
                sleep(2.0)
        #if remote2Btn.value:
            #print("Skip a cue")
           
                
                
                        
                        
                    
       
            
                     
            
            
            

    


