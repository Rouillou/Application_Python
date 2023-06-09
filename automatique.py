import j2l.pytactx.agent as pytactx
agent = None

def setAgent(nouvelAgent):
  """
   
  """
  global agent
  agent = nouvelAgent


def rechercheMin(dictionnaire):
  """
  Renvoie la valeur min et sa clé associée dans le dictionnaire spécifié en paramètre
  :param dictionnaire: dictionnaire de clé et valeurs entieres
  :type dictionnaire: dict de key Any, value int or float
  :return: tuple comprenant la clé, la valeur minimale
  """
  minValue = None
  minKey = None
  for key, value in dictionnaire.items():
    if (minValue == None or value < minValue):
      minValue = value
      minKey = key
  return (minKey, minValue)
  

def testRechercheMin():
  print("debut test rechercheMin")
  dictATester = {"agent1":2, "agent2": 4}
  resultat = rechercheMin(dictATester)
  resultatAttendu = ("agent1",2)
  assert resultat==resultatAttendu, "Erreur rechercheMin renvoie "+str(resultat)+" pour un dictionnaire à tester: "+str(dictATester)+". Or attend :"+str(resultatAttendu)
  print("fin test rechercheMin")
testRechercheMin()


def eval(agentRef, voisin):
  """
  Renvoie un nombre representaant le cout pour notre agent de referent pour aller abattre le voisin spécifié. Cout faible pour voisin interressant à aller abattre.
    type agentRef: dict avec clé str comme attributs d'agent "x", "y" ... 
    type voisin: dict avec clé str comme attributs d'agent "x", "y" ... 
  """
  dx = (agentRef["x"]-voisin["x"])**2
  dy = (agentRef["y"]-voisin["y"])**2
  #rajouter ce que vous voulez pour prendre en compte d'autre critères que la distance comme heuristique
  return dx+dy
  

def testEval():
  print("debut test eval")
  agentRefATester = {"x":0, "y": 0, "life":100}
  voisinInterressant = {"x":2, "y": 0, "life":10}
  voisinPasInterressant = {"x":20, "y": 10, "life":1000}
  resultatInterressant = eval(agentRefATester, voisinInterressant)
  resultatPasInterressant = eval(agentRefATester, voisinPasInterressant)
  assert resultatInterressant < resultatPasInterressant, "Erreur cout interressant est supérieur au coût pas interressant. eval interressant renvoie "+str(resultatInterressant)+ " eval pas interressant renvoie "+str(resultatPasInterressant)
  print("fin test eval")
testEval()


def evaluationPossibilite():
  """ 
  Evalue toutes les possibilités : pour chaque agent ennemi dont l'id est mis en clé, on associe en valeur son coût calculé par l'heuristique eval
  """
  possibilites = {}
  global voisinCibleInfos
  for voisinId, voisinInfos in agent.voisins.items():
    agentInfo = {"x":agent.x, "y":agent.y}
    possibilites[voisinId] = eval(agentInfo, voisinInfos)
  # Si des ennemis sont dans le dico possibilités ...
  if (len(possibilites) > 0):
    # Trouver celui qui à le score minimum
    voisinCibleId, voisinCibleCout = rechercheMin(possibilites)
    # Puis se déplacer à sa position en la récupérant dans le dico agent voisin
    voisinCibleInfos = agent.voisins[voisinCibleId]


xEnnemi = 0
yEnnemi = 0
etat = "recherche"
etatDeGarde = "gardeHautGauche"
orientation = 0
veilleTimer = 0
veilleDuration = 20

def gardeBasGauche():
  global etatDeGarde
  etatDeGarde = "gardeBasGauche"
  if agent.x == 3 and agent.y == 26:
    etatDeGarde = "gardeHautGauche"
    print(etatDeGarde)
  else:
    agent.deplacerVers(3,26)

def gardeHautGauche():
  global etatDeGarde
  etatDeGarde = "gardeHautGauche"
  if agent.x == 3 and agent.y == 3:
    etatDeGarde = "gardeHautDroite"
    print(etatDeGarde)
  else:
    agent.deplacerVers(3,3)
  

def gardeBasDroite():
  global etatDeGarde
  etatDeGarde = "gardeBasDroite"
  if agent.x == 36 and agent.y == 26:
    etatDeGarde = "gardeBasGauche"
    print(etatDeGarde)
  else:
    agent.deplacerVers(36,26)

def gardeHautDroite():
  global etatDeGarde
  etatDeGarde = "gardeHautDroite"
  if agent.x == 36 and agent.y == 3:
    etatDeGarde = "gardeBasDroite"
    print(etatDeGarde)
  else:
    agent.deplacerVers(36,3)


def rechercher():
  """
  l'agent recherche l'ennemi
  """
  agent.orienter((agent.orientation+1)%4)
  agent.changerCouleur(0,255,0)
  evaluationPossibilite()
  
  #detection d'un agent ennemi  A CHANGER
  if len(agent.voisins) != 0 :
    agent.changerCouleur(255,0,0)
    global etat
    etat = "poursuite"
  elif len(agent.voisins) != 0 and voisinCibleInfos["life"] > agent.vie and agent.vie <= 25 :
    etat = "fuite"
  

  #garde
  elif etatDeGarde == "gardeHautGauche":
    gardeHautGauche()
  elif etatDeGarde == "gardeHautDroite":
    gardeHautDroite()
  elif etatDeGarde == "gardeBasGauche":
    gardeBasGauche()
  elif etatDeGarde == "gardeBasDroite":
    gardeBasDroite()
    

def poursuivre():
  """
  mode poursuite l'agent va a la position de l'agent en tirant ou pas
  """ 
  global etat

  #un agent est detecter donc je tire 
  if agent.distance != 0:
    evaluationPossibilite()
    agent.tirer(True)
    agent.changerCouleur(255,0,0)

  #si dès que l'agent est arriver a la position il n'y a personne passer en veille
  elif agent.x == voisinCibleInfos["x"] and agent.y == voisinCibleInfos["y"] and agent.distance == 0:
    agent.tirer(False)
    agent.changerCouleur(255,255,0)
    etat= "veille"
   

  #si l'ennemi tire je fais une esquive de sa balle (MATRIX)
  elif voisinCibleInfos["fire"] == True :
    if agent.x == voisinCibleInfos["x"] :
      agent.deplacer(1 or -1,0)
    if agent.y == voisinCibleInfos["y"] :
      agent.deplacer(0,1 or -1)

  
  if agent.x == voisinCibleInfos["x"] :
    agent.tirer(True)
    agent.deplacer(1 or -1,0)
  if agent.y == voisinCibleInfos["y"] :
    agent.tirer(True)
    agent.deplacer(0,1 or -1)

  #sinon allez a la position de l'ennemi sans tirer
  else:
    evaluationPossibilite()
    agent.deplacerVers(voisinCibleInfos["x"], voisinCibleInfos["y"]) 
    agent.tirer(False)
    agent.changerCouleur(255,0,0)
    agent.orienter((agent.orientation+1)%4)


def veille():
  """
  mode veille l'agent cherche l'ennemi a sa position
  """
  global etat
  global veilleTimer

  #si agent detecter remettre le timer a zero et declencher poursuite
  if len(agent.voisins) != 0 and voisinCibleInfos["life"] <= agent.vie :
      evaluationPossibilite()
      etat = "poursuite"
      veilleTimer = 0
      agent.changerCouleur(255,0,0)
  elif len(agent.voisins) != 0 and voisinCibleInfos["life"] > agent.vie and agent.vie <= 25 :
    etat = "fuite"

  #si fin du timer atteint retourner en recherche 
  if veilleTimer >= veilleDuration:
    veilleTimer = 0
    etat = "recherche"
    agent.changerCouleur(0,255,0)

  #sinon tourner en rond en rajoutant 1 au timer 
  else:
    agent.orienter((agent.orientation+1)%4)
    veilleTimer += 1

def Fuite():
  """
  mode fuite l'agent fuit l'ennemi car il est trop fort
  """
  global etat
  if voisinCibleInfos["life"] > agent.vie and agent.vie <= 25 and (agent.deplacerVers != (40,agent.y) or agent.deplacerVers != (-1,agent.y) or agent.deplacerVers != (agent.x,-1) or agent.deplacerVers != (agent.x, 30)) :
    evaluationPossibilite()
    agent.deplacerVers(voisinCibleInfos["x"] + 1 or -1, voisinCibleInfos["y"] + 1 or -1)
  else :
    etat = "recherche"


def actualiserAgent():
  print(etat)
  if etat == "recherche":
    rechercher()
    
  elif etat == "poursuite":
    poursuivre()
    
  elif etat == "veille":
    veille()

  elif etat == "fuite":
    Fuite()
