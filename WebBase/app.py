from flask import Flask, request, render_template
from multiprocessing import Process, Value, Manager
from fonctions import * #Importe les fonctions utiles
from child_fonctions import * #Importe les "enfants" qui seront créés par le serveur


#137.194.13.137

Timeout #Temps en secondes avant de tuer les voitures sans ping
k=0  #Le numéro du serveur (à modifier pour chaque)

if __name__ == "__main__":
    manager=Manager() #On va créer les dictionnaires synchronisés avec les enfants 
    Alive = manager.dict() #alive est construit avec les timeout, il garde en tête leur temps
    Status = manager.dict() #Status donne l'état de chaque voiture, -1 en standby, 1 si partit, 2 si arrivé, -2 si tué
    Chef=manager.list() #Sous forme de liste pour pouvoir le passer dans les child
    Chef.append(False)
    for l in L:
        Status[l]=-1
        Alive[l]=Timeout

app = Flask(__name__)

"""
@app.route('/') #Purement utilisé en debug
def index():
    global Alive
    global Status
    print("keys :")
    for key in Alive.keys():
        print("\t-",key,":", Alive[key])
    print("\n")
    for key in Status.keys():
        print("\t-",key,":", Status[key])
    return "<div style='text-align: center'><h1>Serveur</h1></div>"
"""

@app.route('/com', methods = ['POST']) #Pour la communcation reçue de part les voitures
def com():
    global Alive
    global Status
    id= request.args.get('id')
    nature= request.args.get('nature')
    print(id,nature)

    if nature=="ping" and Chef[0]==True:
        Relive(id,Alive,Status)
        return("Ping reçu de la part de ", id)
    
    if nature=="depart" and Chef[0]==True:
        if Status[id]!=-1: #Ici du debug/indication d'erreur
            dead(id,Alive,Status)
            print("Erreur, envoi de départ alors que la voiture est déjà partie, killed.")
            return("Commande de départ reçue pour ", id , " mais erreur sur l'état sur la voiture, killed.")
        else: #On met a jour le status et 
            Status[id]=1
            print("Commande de départ de ", id, " bien reçue")
            return("Commande de départ de ", id, " bien reçue")
        
    if nature=="arrive" and Chef[0]==True:
        if Status[id]==2: #Plein de cas de debug/signalisation
            print("Problème, voiture",id,"déjà arrivée")
            return("Problème, voiture",id,"déjà arrivée")
        elif Status[id]==-2:
            print("Voiture",id, "déjà morte")
            return(print("Problème, voiture ", id, " déjà morte"))
        elif Status[id]!=1:
            print("Problème, voiture ", id, " pas partie")
            dead(id,Alive,Status)
            return(print("Problème, voiture ", id, " pas partie"))
        else:
            Status[id]=2
            if not startnext(id,Alive,Status): print("PLUS AUCUNE VOITURE DISPONIBLE") #On envoie la prochaine voiture une fois la précédente arrivée
        
        Alive[id]=0
        print("Voiture ", id, " arrivée à bon port")
        print(Status)
        return("Voiture ", id, " arrivée à bon port")
    
    return("N'a rien fait")

@app.route("/sendrequest",methods=["GET"]) #Pour l'envoi manuel
def sendrequest():
    return render_template('request.html') 

@app.route("/forceinrequest",methods=["POST"]) #Pour simuler l'envoi en interne
def forceinrequest():
        nature=request.args.get("nature")
        id=request.args.get("id")
        print("Requête"+nature+"lancée à"+id)
        return(str(requesting(str(id),"5000",str(nature))))


@app.route("/chef",methods=["GET"]) #Renvoie si le serveur est chef ou pas, utile pour checker
def chefing():
    global Chef
    return str(Chef[0])

"""
@app.route("/chefchange",methods=["POST"]) #Force le changement du chef, uniquement en debug
def chefchange():
    global Chef
    Chef=False
    return "Chef changé"
"""

@app.route("/updatedicts",methods=["POST"]) #Permet le partage d'information entre les serveurs
def updatedict():
    nature=request.args.get("nature")
    donnee=request.args.get("donnee")
    A=donnee.split("k")
    if nature=="alive":
        for i in range(len(L)):
            Alive[L[i]]=int(A[i])
        print("Dictionnaire mis à jour:")
        print(Alive)
        return("On a update Alive")
    if nature=="status":
        for i in range(len(L)):
            Status[L[i]]=int(A[i])
        print("Dictionnaire mis à jour:")
        print(Status)
        return("On a update Status")
    return("On a pas compris")

if __name__ == "__main__": #Lance toute la logique...
    with Manager() as manager:
        t=Process(target=alive,args=(k,Chef,Alive,Status)) #... le premier enfant...
        t.start()
        app.run(host='0.0.0.0', port=8000, debug=False) #... et le site web