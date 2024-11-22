import requests

L=["a","b","c","d","e"]
Timeout=60 #Donne le temps de vie des voitures avant de se faire kill sans ping
BaseIp="137.194.173."
Ips=["38","40","37","36","39"]

def idtoint(id, spec=0): #permet d'utiliser les lettres pour requesting
    if spec==0: return(int(id,16)-10)
    return L[id]

def requesting(id,port,suburl): #Envoie une requête post à l'adresse précisée d'une des voitures
    try: requests.post("http://"+BaseIp+Ips[idtoint(id)]+":"+str(port)+"/"+suburl,data={})
    except Exception as error:
        print(error)
        print("Requête ",id," ",suburl," échouée")
        return(False)
    return(True)   

def dead(id,a,s): #Sert à tuer proprement une voiture dans le programme et en dehors

    print("On tue ", id," à cause d'un timeout/une erreur")
    requesting(id,5000,"kill")#Envoie la requête de kill à une voiture hors-jeu
    a[id]=-2
    s[id]=-2

def startnext(id,a,s): #Regarde quelle voiture lancer et la lance ensuite
    k=1
    ID=(idtoint(id)+1)%5
    while k<5: #Cherche parmis les voitures suivant celle arrivée la première pouvant partir
        k+=1
        ID=(ID+1)%5
        print(s[L[ID]])
        if s[L[ID]]!=-1:
            if requesting(L[ID],5000,"start"):
                s[L[ID]]=1
                print("On lance ensuite", L[ID])
                return True
            else: 
                Relive(id,a,s)
                print("On arrive pas à contacter", L[ID], "on lui laisse 60 secondes pour se reconnecter")
    if k>=5: 
        print("Aucune voiture trouvée pour partir") #Si on est à vide, on stop
        return False

def Relive(id,a,s): #Pour remettre le Alive à Timeout
    print(a)
    if a[id]>0: 
        a[id]=Timeout
    print("Ping reçu de la part de ", id)

