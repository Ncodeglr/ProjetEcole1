import cv2
import numpy as np


aruco_dict = cv2.aruco.getPredefinedDictionary( cv2.aruco.DICT_6X6_50)  # Definir le dictionnaire ArUco (peut egalement utiliser d'autres dictionnaires)
parameters = cv2.aruco.DetectorParameters()
aruco_detecteur = cv2.aruco.ArucoDetector(aruco_dict, parameters)  # Initialiser le détecteur d'ArucoCode avec un dictionnaire et les paramètres de détection
cap = cv2.VideoCapture(0)  # Initialisation de la camera (0 pour la camera par defaut, ou specifiez l'index de la camera)
ret, frame = cap.read()


def detecter_aruco():

    ret, frame = cap.read()  # Lire un cadre video depuis la camera
    print(ret)
    if not ret:  # Dans le cas
        print("Erreur de lecture camera")
        return None

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertir le cadre en echelle de gris (ArUco fonctionne mieux avec des images en niveaux de gris)
    corners, ids, rejectedImgPoints = aruco_detecteur.detectMarkers(gray)  # Detecter les marqueurs ArUco

    if ids != (None) and (len(ids)) > 0:
        largest_marker_index = np.argmax( np.array([cv2.contourArea(corner) for corner in corners]))  # Trouver l'indice du marqueur le plus grand
        largest_marker_id = ids[largest_marker_index][0]  # Recuperer l'ID du plus grand marqueur
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)  # Dessiner le plus grand marqueur detecte
        hauteur_en_pixel = ((corners[largest_marker_index][0][0][0] - corners[largest_marker_index][0][3][0]) ** 2 + (corners[largest_marker_index][0][0][1] - corners[largest_marker_index][0][3][1]) ** 2) ** 0.5
        distance = 5374.1 * (hauteur_en_pixel ** (-0.964))
        return (largest_marker_id, distance)
    else :
        return None



