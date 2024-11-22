import requests
from fonctions import *
import time
from bs4 import BeautifulSoup
from multiprocessing import Process

"""
def pingplease(ip):
    try: requests.post("http://"+ip+"/com?nature=ping&id=VOTRE_LETTRE_DE_VOITURE_ICI_EN_MINUSCULE",data={})
    except:
        return(False)
    return(True)   

L=["137.194.173.38:8000","137.194.173.40:8000","137.194.173.37:8000","137.194.173.36:8000","137.194.173.39:8000"]
for i in L:
    p = Process(target=pingplease, args=(i))
    p.start()
"""
#Code pour ping tous les serveurs, dont le chef du coup qui enregistre

def partage(a,s,k): #Gère le partage de dictionnaires avec les serveurs redondants
    L=["137.194.173.38:8000","137.194.173.40:8000","137.194.173.37:8000","137.194.173.36:8000","137.194.173.39:8000"]
    
    while True:
        for K in range(2):
            if K==0:
                Dico=a
                nature="alive"
            else: 
                Dico=s
                nature="status"
            j=0
            while j<len(L):
                if j!=k:
                    donnee=str(Dico["a"])+"k"+str(Dico["b"])+"k"+str(Dico["c"])+"k"+str(Dico["d"])+"k"+str(Dico["e"]) #On envoie tout le dico d'un coup, plus opti
                    url="http://"+L[j]+"/updatedicts?nature="+nature+"&donnee="+donnee
                    try: requests.post(url, data={})
                    except Exception as error:
                        #print("An error occurred:", error) # An error occurred: name 'x' is not defined
                        #print("Erreur d'envoi à"+L[j])
                        pass
                j=j+1
        time.sleep(1)


def ping(a,s,k): #Système de vérification des pings des voitures
    c=0
    
    while c==0:
        t=None
        for key in a.keys():
            if a[key]>=0: a[key] -= 1
            if a[key]==-1: 
                #dead(key,a,s)
                t=Process(target=dead,args=(key,a,s)) #Tue une voiture si son "Alive" devient négatif
                t.start()
        if t!=None: t.join() #On attend que le dernier join
        time.sleep(1) #On attend une seconde avant de reboucler si tout le monde n'est pas mort
        if all([a[j]==-2 for j in a.keys()]): #Si tout le monde est mort on print pour debug
            c=1
            for key in a.keys():
                print("\t-",key,":", a[key], s[key])

def alive(k,Chef,a,s): #Permet d'attribuer le chef
    L=["137.194.173.38:8000","137.194.173.40:8000","137.194.173.37:8000","137.194.173.36:8000","137.194.173.39:8000"]

    def Check(i): #Fait la vérfication savoir si son "N+1" est encore en vie, sinon le N+2, etc jusqu'à boucler sur un serveur moins prioritaire, sur quoi il reprend la tête
        x=None
        print(i,k)
        if i==k or i==0:
            print("On a fait la boucle et il reste que lui, il devient chef",i,k)
            return True
        else: 
            x=None
            try:
                x=requests.get(L[i]+"/chef")
            except:
                print("Serveur", i, "mort")
                time.sleep(0.5)
                return(Check((i-1)%len(L)))
            print("On reçoit bien des infos de" ,i)
            return False  
    
    if k!=0: time.sleep(5) #permet de lancer le serveur 0 avant les autres pour de la marge
    else:
        for j in range(1,len(L)): #Le serveur 0 prend la tête par défaut mais en cas de redémarrage vérifie qu'il n'y a pas déjà un autre chef
            x=None
            soup=False
            try: 
                x=requests.get(L[j]+"/chef")
                soup = bool(BeautifulSoup(x.content, "html.parser")) #On extrait le "True" OU "False" de l'HTML pour savoir quoi faire
                print(soup)
            except:
                if j!=len(L)-1: continue #Si on connecte pas, un passe au suivant
            if soup==True:
                print("Quelqu'un d'autre est chef, on devient subordonné")
                break
            if j==len(L)-1: 
                Chef[0]=True
                print("Devient chef par défaut")

    while True:
        if Chef[0]==False:
            Chef[0]=Check((k-1)%len(L))
            if Chef[0]:
                print("On reprend la tête")
                continue
            time.sleep(5)
        else: 
            print("On est le chef donc on lance la logique")
            p = Process(target=ping, args=(a,s,k)) #On lance les process de ping et de partage si on est chef
            sha = Process(target=partage, args=(a,s,k))
            sha.start()
            p.start()
            p.join()
            sha.join()
            break
    print("Travail fini")
