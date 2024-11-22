import cv2
import numpy as np
import pickle

with open("calibration.pkl", "rb") as f:

    cameraMatrix, dist = pickle.load(f)


aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50) # Definir le dictionnaire ArUco (peut egalement utiliser d'autres dictionnaires)

parameters = cv2.aruco.DetectorParameters()

#Initialiser le détecteur d'ArucoCode avec un dictionnaire et les paramètres de détection
aruco_detecteur = cv2.aruco.ArucoDetector(aruco_dict,parameters)

cap = cv2.VideoCapture(0) # Initialisation de la camera (0 pour la camera par defaut, ou specifiez l'index de la camera)
marker_size=3.8 # Taille reel de l'aruco

while True:


    ret, frame = cap.read() # Lire un cadre video depuis la camera


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convertir le cadre en echelle de gris (ArUco fonctionne mieux avec des images en niveaux de gris)


    corners, ids, rejectedImgPoints = aruco_detecteur.detectMarkers(gray) # Detecter les marqueurs ArUco


    if corners:

        rvec,tvec,_= cv2.aruco.estimatePoseSingleMarkers(corners,marker_size,cameraMatrix, dist) # defini la liste des positions des arucos code leur rotation puis leur translation


    if ids is not None and len(ids) > 0:


        largest_marker_index = np.argmax(np.array([cv2.contourArea(corner) for corner in corners])) # Trouver l'indice du marqueur le plus grand


        largest_marker_id = ids[largest_marker_index][0] # Recuperer l'ID du plus grand marqueur

        #print(largest_marker_id)



        distance=np.sqrt(tvec[largest_marker_index][0][0]**2+tvec[largest_marker_index][0][1]**2+tvec[largest_marker_index][0][2]**2) #calculer distance
        print(distance)

        cv2.aruco.drawDetectedMarkers(frame, corners, ids) # Dessiner le plus grand marqueur detecte


    ###cv2.imshow('ArUco Detection', frame) # Afficher le cadre video avec les marqueurs detectes


    # Sortir de la boucle lorsque la touche 'q' est enfoncee
    if cv2.waitKey(1) & 0xFF == ord('q'):

        break



# Liberer la camera et detruire toutes les fenetres OpenCV
cap.release()
cv2.destroyAllWindows()







