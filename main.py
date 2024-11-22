# https://www.digitalocean.com/community/tutorials/how-to-use-templates-in-a-flask-application
# Youtube : MakerSnack Installing and Testing the Waveshare Motor dRIVER HAT for Rasberry PI
from flask import *
import requests
from PCA9685 import PCA9685
import time
import requests
import math
from multiprocessing import Process

import cv2
import numpy as np

# ------------------------------------ PARTIE MOTEUR ----------------------------------------------------- #

continuer = True

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
        if (motor == 0):
            pwm.setDutycycle(self.PWMA, speed)
            if (index == Dir[0]):
                # print ("1")
                pwm.setLevel(self.AIN1, 0)
                pwm.setLevel(self.AIN2, 1)
            else:
                # print ("2")
                pwm.setLevel(self.AIN1, 1)
                pwm.setLevel(self.AIN2, 0)
        else:
            pwm.setDutycycle(self.PWMB, speed)
            if (index == Dir[0]):
                # print ("3")
                pwm.setLevel(self.BIN1, 0)
                pwm.setLevel(self.BIN2, 1)
            else:
                # print ("4")
                pwm.setLevel(self.BIN1, 1)
                pwm.setLevel(self.BIN2, 0)

    def MotorStop(self, motor):
        if (motor == 0):
            pwm.setDutycycle(self.PWMA, 0)
        else:
            pwm.setDutycycle(self.PWMB, 0)


# print("this is a motor driver test code")
Motor = MotorDriver()

# -----------------------------------PARTIE ARUCO--------------------------------------------------- #
aruco_dict = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_6X6_50)  # Definir le dictionnaire ArUco (peut egalement utiliser d'autres dictionnaires)
parameters = cv2.aruco.DetectorParameters()
aruco_detecteur = cv2.aruco.ArucoDetector(aruco_dict,
                                          parameters)  # Initialiser le détecteur d'ArucoCode avec un dictionnaire et les paramètres de détection
def ping_serveur():
    def pingplease(ip):
        try: requests.post("http://" +ip+ "/com?nature=ping&id=e",data={},timeout=1)
        except:
            print("Je Ping Nicolas Besson")
            return(False)
        return(True)
    L=["137.194.173.38:8000","137.194.173.40:8000","137.194.173.37:8000","137.194.173.36:8000","137.194.173.39:8000"]
    for i in L:
        p = Process(target=pingplease, args=(i,))
        p.start()

def ping_depart():
    def pingplease(ip):
        try: requests.post("http://" +ip+ "/com?nature=depart&id=e",data={},timeout=1)
        except:
            print("Je Ping Nicolas Besson")
            return(False)
        return(True)
    L=["137.194.173.38:8000","137.194.173.40:8000","137.194.173.37:8000","137.194.173.36:8000","137.194.173.39:8000"]
    for i in L:
        p = Process(target=pingplease, args=(i,))
        p.start()


def attendre():
    pass
def ping_arrivee():
    def pingplease(ip):
        try: requests.post("http://" +ip+ "/com?nature=arrive&id=e"
                                          "",data={},timeout=1)
        except:
            print("ljvhegfkdyvfkdyg")
            return(False)
        return(True)
    L=["137.194.173.38:8000","137.194.173.40:8000","137.194.173.37:8000","137.194.173.36:8000","137.194.173.39:8000"]
    for i in L:
        p = Process(target=pingplease, args=(i,))
        p.start()

def detecter_aruco():
    #cap = cv2.VideoCapture(0)
    if cap.get(cv2.CAP_PROP_FRAME_COUNT) == 0:
        print("Buffer vide de sens")
        stop()
        return None
    ret, frame = cap.read()  # Lire un cadre video depuis la camera
    # print(ret)
    if not ret:  # Dans le cas
        print("Erreur de lecture camera")
        #cap.release()
        return None

    gray = cv2.cvtColor(frame,
                        cv2.COLOR_BGR2GRAY)  # Convertir le cadre en echelle de gris (ArUco fonctionne mieux avec des images en niveaux de gris)
    corners, ids, rejectedImgPoints = aruco_detecteur.detectMarkers(gray)  # Detecter les marqueurs ArUco
    a,b = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #print("Voici cela ",rejectedImgPoints)
    try:
        if ids != (None) and (len(ids)) > 0:
            ping_serveur()


            print("Je vois")
            largest_marker_index = np.argmax(
                np.array([cv2.contourArea(corner) for corner in corners]))  # Trouver l'indice du marqueur le plus grand
            largest_marker_id = ids[largest_marker_index][0]  # Recuperer l'ID du plus grand marqueur
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)  # Dessiner le plus grand marqueur detecte
            hauteur_en_pixel = ((corners[largest_marker_index][0][0][0] - corners[largest_marker_index][0][3][0]) ** 2 + (
                        corners[largest_marker_index][0][0][1] - corners[largest_marker_index][0][3][1]) ** 2) ** 0.5
            distance = 5374.1 * (hauteur_en_pixel ** (-0.964))
            #cap.release()
            return (largest_marker_id, distance, corners[largest_marker_index][0])

        else:
            print("Je vois pas")
            #pass
            #cap.release()
            #print("Pas de QRcode")
            return None
    except:
        pass


# ----------------------------------- PARTIE SERVEUR WEB   -------------------------------------------- #
app = Flask(__name__)  # Création d'une application app


@app.route('/')  # Permet d'éxecuter le def hello
def hello():
    return render_template('site_web.html')  # render_template est un module de Flask, cherche le dossier template


def avancer():
    Motor.MotorRun(0, 'forward', 60)
    Motor.MotorRun(1, 'forward', 60)
    print("Avancer")
    #requests.post('http://137.194.13.82:5000/com?id=e&nature=ping')




def reculer():
    Motor.MotorRun(0, 'backward', 75)
    Motor.MotorRun(1, 'backward', 75)
    print("Reculer")
    return ''


def gauche():
    Motor.MotorRun(0, 'forward', 75)
    Motor.MotorRun(1, 'forward', 0)
    print("Gauche")
    return ''


def droite():
    Motor.MotorRun(0, 'backward', 75)
    Motor.MotorRun(1, 'forward', 75)
    print("Droite")
    return ''


def stop():
    Motor.MotorStop(0)
    Motor.MotorStop(1)
    # print("Stop")
    return ''


def recherche_methodique(n):

    for i in range(n):
        resultat = detecter_aruco()
        if (resultat != None):
            break
    if resultat != None :
        pass
    else:
        print("Pas de QRcode")

    return resultat


def chercher_aruco(i,d):
    if d == "gauche":
        m = 1
    else:
        m = 0
    while True:
        Motor.MotorRun(m, 'forward', 50)
        Motor.MotorRun(not m, 'backward', 50)
        time.sleep(0.08)
        stop()
        time.sleep(0.5)
        resultat = detecter_aruco()
        if resultat != None:
            n,_,_ = resultat
            print(n)
            if n == i:
                print("j'ai trouvé")
                break






def avancer_aruco():
    speed = 25
    speed_max = speed + 10
    distance = 1000

    while distance > 48 :

        resultat = detecter_aruco()
        flag = 1
        speed_reel = speed
        if resultat != None:

            id, distance, corners = resultat
            k = position_relative_aruco(corners)
            if k>0: #Image à Gauche
                flag = 0
            if abs(k) > 50:
                speed_reel = speed_max

        Motor.MotorRun(not flag, 'forward', speed_reel)
        Motor.MotorRun(flag, 'forward', speed)  # Tourne à Gauche
    stop()
    #time.sleep(0.001)
    print(distance)



def centrer_aruco():
    id, distance, corners = recherche_methodique(1000)
    distance_relative = position_relative_aruco(corners)
    while abs(distance_relative) > 20 :
        if distance_relative > 0:
            Motor.MotorRun(1, 'forward', 20)
            Motor.MotorRun(0, 'backward', 20)

        else :
            Motor.MotorRun(0, 'forward', 20)
            Motor.MotorRun(1, 'backward', 20)
        id, distance, corners = recherche_methodique(1000)
        distance_relative = position_relative_aruco(corners)
    stop()


def position_relative_aruco(corners):
    position_horizontale = (corners[0][0] + corners[1][0]) / 2
    centre_image = 320
    distance_relatif = centre_image - position_horizontale
    return distance_relatif





# ----------------Algo du parcours------------- #
def fct_aruco():
    global cap

    ping_depart()

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    Motor.MotorRun(0, 'forward', 18)
    Motor.MotorRun(1, 'backward', 0)
    cap.set(cv2.CAP_PROP_FPS, 30)
    exposure = cap.get(cv2.CAP_PROP_EXPOSURE)
    new_exposure = 0.05
    cap.set(cv2.CAP_PROP_EXPOSURE, new_exposure)

    avancer()
    time.sleep(5)
    stop()

    chercher_aruco(1, "gauche")
    avancer_aruco()

    reculer()
    time.sleep(1)
    stop()
    gauche()
    time.sleep(1.1)
    stop()
    time.sleep(0.1)
    avancer()
    time.sleep(3.5)
    stop()
    cap.release()

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    Motor.MotorRun(0, 'forward', 18)
    Motor.MotorRun(1, 'backward', 0)
    cap.set(cv2.CAP_PROP_FPS, 30)
    exposure = cap.get(cv2.CAP_PROP_EXPOSURE)
    new_exposure = 0.05
    cap.set(cv2.CAP_PROP_EXPOSURE, new_exposure)

    chercher_aruco(6, "gauche")
    avancer_aruco()

    reculer()
    time.sleep(1)
    stop()
    gauche()
    time.sleep(1.1)
    stop()
    time.sleep(0.1)
    avancer()
    time.sleep(3.5)
    stop()
    cap.release()

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    Motor.MotorRun(0, 'forward', 18)
    Motor.MotorRun(1, 'backward', 0)
    cap.set(cv2.CAP_PROP_FPS, 30)
    exposure = cap.get(cv2.CAP_PROP_EXPOSURE)
    new_exposure = 0.05
    cap.set(cv2.CAP_PROP_EXPOSURE, new_exposure)

    chercher_aruco(3, "gauche")
    avancer_aruco()

    reculer()
    time.sleep(1)
    stop()
    gauche()
    time.sleep(1.1)
    stop()
    time.sleep(0.1)
    avancer()
    time.sleep(3.5)
    stop()
    cap.release()

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    Motor.MotorRun(0, 'forward', 18)
    Motor.MotorRun(1, 'backward', 0)
    cap.set(cv2.CAP_PROP_FPS, 30)
    exposure = cap.get(cv2.CAP_PROP_EXPOSURE)
    new_exposure = 0.05
    cap.set(cv2.CAP_PROP_EXPOSURE, new_exposure)

    chercher_aruco(9, "gauche")
    avancer_aruco()
    cap.release()
    ping_arrivee()

# https://stackoverflow.com/questions/25034123/flask-value-error-view-function-did-not-return-a-response
# Comment j'ai fixé le 'OK'
@app.route('/action', methods=['POST'])
def direction():
    global continuer
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

    if (direction == "stop"):
        stop()
        return 'OK'
    if (direction == "passage_auto"):
        fct_aruco()
        return 'OK'

process1 = 0
@app.route('/depart', methods=['POST'])
def start():
     global process1
     global continuer
     continuer = False
     print("Start")
     #list_ping[0]=False
     p = Process(target =  fct_aruco, args = ())
     process1 = p
     p.start()

     return 'dfvf'


@app.route('/kill', methods=['POST'])
def kill():
    global process1
    print("Kill")
    process1.terminate()
    stop()
    return 'rvr'




if __name__ == '__main__':
    # cap.set(cv2.CAP_PROP_FPS,60)
    app.run(debug=False, port=5000, host='0.0.0.0')  # Démarage de l'application

# ---------------------------------------------------------------------------------------- #












