#https://www.digitalocean.com/community/tutorials/how-to-use-templates-in-a-flask-application
#Youtube : MakerSnack Installing and Testing the Waveshare Motor dRIVER HAT for Rasberry PI

from flask import*
from PCA9685 import PCA9685
import time
import requests


Dir = [
    'forward',
    'backward',
]
pwm = PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)

class MotorDriver():
    def __init__(self):
        self.PWMA = 0
        self.AIN1 = 1
        self.AIN2 = 2
        self.PWMB = 5
        self.BIN1 = 3
        self.BIN2 = 4


    def MotorRun(self, motor, index, speed):
        if speed > 100:
            return
        if(motor == 0):
            pwm.setDutycycle(self.PWMA, speed)
            if(index == Dir[0]):
                #print ("1")
                pwm.setLevel(self.AIN1, 0)
                pwm.setLevel(self.AIN2, 1)
            else:
                #print ("2")
                pwm.setLevel(self.AIN1, 1)
                pwm.setLevel(self.AIN2, 0)
        else:
            pwm.setDutycycle(self.PWMB, speed)
            if(index == Dir[0]):
                #print ("3")
                pwm.setLevel(self.BIN1, 0)
                pwm.setLevel(self.BIN2, 1)
            else:
                #print ("4")
                pwm.setLevel(self.BIN1, 1)
                pwm.setLevel(self.BIN2, 0)

    def MotorStop(self, motor):
        if (motor == 0):
            pwm.setDutycycle(self.PWMA, 0)
        else:
            pwm.setDutycycle(self.PWMB, 0)

#print("this is a motor driver test code")
Motor = MotorDriver()
"""
#print("forward 2 s")
Motor.MotorRun(0, 'forward', 100)
Motor.MotorRun(1, 'forward', 100)
time.sleep(2)

#print("backward 2 s")
Motor.MotorRun(0, 'backward', 100)
Motor.MotorRun(1, 'backward', 100)
time.sleep(2)

#print("stop")
Motor.MotorStop(0)
Motor.MotorStop(1)

"""





###########################  PARTIE SERVEUR WEB   ########################################
app = Flask(__name__) #Création d'une application app
@app.route('/') #Permet d'éxecuter le def hello
def hello():
    return render_template('site_web.html')#render_template est un module de Flask, cherche le dossier template




def avancer():
    Motor.MotorRun(0, 'forward', 100)
    Motor.MotorRun(1, 'forward', 100)
    print("Avancer")
    return ''


def reculer():
    Motor.MotorRun(0, 'backward', 100)
    Motor.MotorRun(1, 'backward', 100)
    print("Reculer")
    return ''

def gauche():
    Motor.MotorRun(0, 'forward', 100)
    Motor.MotorRun(1, 'forward', 0)
    print("Gauche")
    return ''

def droite():
    Motor.MotorRun(0, 'forward', 0)
    Motor.MotorRun(1, 'forward', 100)
    print("Droite")
    return ''

def stop():
    Motor.MotorStop(0)
    Motor.MotorStop(1)
    print("Stop")
    return ''


#https://stackoverflow.com/questions/25034123/flask-value-error-view-function-did-not-return-a-response
#Comment j'ai fixé le 'OK'
@app.route('/action', methods=['POST'])
def direction():
    direction = request.form['direction']
    if (direction == "avancer"):
        avancer()
        return 'OK'
    if (direction == "reculer"):
        reculer()
        return 'OK'
    if (direction == "gauche"):
        gauche()
        return 'OK'
    if (direction == "droite"):
        droite()
        return 'OK'
    """"
    if (direction == "stop"):
        stop()
        return 'OK'
"""




if __name__=='__main__':
    app.run(debug=True, port=5000, host='0.0.0.0') # Démarage de l'application








