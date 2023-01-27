# Documentation Technique

## Documentation

>[Github](https://github.com/Hugues862/1PROJ)

> Le but de cette documentation technique est de vous expliquer les différents choix techniques que nous avons mis en place durant ce projet. 
---
## Window :

Il faut au préalable installer les librairies nécessaires sur votre machine, sur Windows, exécutez le code suivant dans votre ligne de commande ou dans Powershell :

> `python -m pip install --upgrade pip`

> `pip install -r requirements.txt`
---
## Mac :

Ouvrez Terminal (Applications/Terminal) et exécutez :

> `-pip install -r requirements.txt`
---
## Présentation des différents modes de jeu :

Dans cette partie nous allons vous expliquer comment faire pour lancer les différents modes de jeu.

### Mode 1 contre 1

Version du jeu ou deux joueurs s’affrontent sur le même ordinateur
- Entrer préalablement les pseudos du joueur 1 et du joueur 2
- Lancer la partie avec bouton en bas de la fenêtre

### Mode en ligne

Une version du jeu ou deux joueurs s’affrontent en réseau sur deux machines différentes.
- Entrer soit l'IP de l'hôte qui a créé la partie
- Créer une partie en donnant l'IP au deuxième joueur
- Lancer la partie avec bouton en bas de la fenêtre

### Mode IA

Une version du jeu ou un joueur humain joue contre une intelligence artificielle, ce dernier choisissant ses coups de manière aléatoire
- Entrer préalablement les pseudos du joueur 1 et du joueur 2
- Lancer la partie avec bouton en bas de la fenêtre

---
## Justification du choix du langage et de la librairie graphique.

### Pourquoi avons-nous utilisés le langage Python ?

- Nous avons plus aisance sur le langage Python grâce aux différents modules qu’on a pu avoir au cours de l’année
- Nous avons plus de facilité à utiliser python car nous avons auparavant déjà réaliser des projets avec ce langage.
- Python dispose d’une Bibliothèques étendues qui permet d’utiliser le code à des fins diverses
- Python est un langage assez Facile à apprendre, comprendre, et coder.

### Pourquoi avons-nous utilisés la librairie graphique TKINTER ?

Nous avons utilisé la librairie TKINTER afin de pouvoir créer une interface graphique au jeu que nous avons voulu implémenter

- Auparavant nous avons eu l’occasion de réaliser des projet grâce à cette librairie, ce qui nous a donner un petit avantage.
- La librairie TKINTER est très simple d’utilisation, elle a de nombreuse fonctionnalité qui nous a permis d’améliorer le design et l’ergonomie afin que l’utilisateur puisse jouer dans de bonne condition.

---
## Description des structures de données.

Pour ce qui est de la structure on établit en premier lieu un dossier src pour contenir les fichier système de l’entièreté du jeu à l’intérieur de ce src on trouvera les dossiers assets et commun :

- Le dossier assets contiendras l’ensemble des supports visuels (images) afin de dynamiser son usage et de s’organiser selon nos différents supports

- Le dossier commun contiendra les différentes fonctions additionnels aidant à l’optimisation du jeu au niveau du gameplay ainsi qu’au niveau design.

- Le dossier src contiendra aussi les fichiers nécessaires au lancement et à la bonne mise en route du jeu.

Et tout ce qui se trouvera en dehors du src seront des fichiers globaux comme le .gitignore ou le .env qui nous permettront une gestion de fichiers et de variables plus efficace.

---
## Algorithmes & Grille Hexagonale

### Grille Hexagonale

À partir d’une étude visuelle du plateau de jeu, les hexagones sont placés d'une manière à première vue irrégulière avec des parties superposant d'autres "lignes" d'hexagones.

Afin de pouvoir reproduire un modèle du plateau de jeu sur une matrice, les hexagones ont été visuellement divisé en deux.

Pour une ligne de 7 hexagones, il faudra donc 14 valeurs dans la ligne en question avec un hexagone représenté par un couple de valeurs dont une est nulle.

Avec un ajout périodique d'hexagones vides (0), nous obtiendrons la base pour travailler sur le tableau d’hexagone ressemblant à :

    [[0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 0, 0, 0],
     [0, 0, 5, 0, 6, 0, 7, 0, 8, 0, 9, 0, 0, 0],
     [0, 10, 0, 11, 0, 12, 0, 13, 0, 14, 0, 15, 0, 0],
     [16, 0, 17, 0, 18, 0, 19, 0, 20, 0, 21, 0, 22, 0],
     ...]

Chaque valeur représente une cellule différente et -1 représente la cellule noire.

### Check Neighbors & Check Win Neighbors

Les deux fonctions sont similaires dans le fait qu'elles vont récursivement vérifier les voisins d'une cellule.

Cependant, elle ne partage pas les mêmes conditions afin de parcourir la matrice.

- Check Neighbors lui va simplement parcourir ses voisins hormis les cellules vides et ennemis
- Check Win Neighbors lui va vérifier les voisins d'une cellule adjacentes non alliée et ensuite continuer à vérifier toutes les cellules voisines hormis les cellules alliées.

Elles vont renvoyer la liste des voisins ainsi que la liste des côtés de ces mêmes voisins. Ces listes vont eux être utiliser afin de vérifier les conditions pour gagner le jeu.

### Mouse Click

Lors du click de la souris sur un hexagone quelconque, le joueur sélectionnera cet hexagone. Si le joueur clique à nouveau sur un hexagone sélectionné, alors s’il est possible de jouer sur cette hexagone, l'hexagone sera joué.

Cela fonctionne avec la modification des booléens 'selected' et 'last' propre à chaque hexagone lors du click de la souris.

En ligne, le clique ne sera pas possible si ce n'est pas le tour du joueur en question.

### Le fonctionnement de l'A.I.

L'AI qui va jouer avec le joueur procède avec une logique à trois étapes.
Afin de pouvoir jouer, L'AI va d'abord récupérer une liste des hexagones jouables et à partir de cette liste jouer en suivant cette logique:

* L'AI va premièrement essayer de jouer autour du dernier hexagone séléctionner par l'enemi.

* Sinon l'AI va essayer de sélectionner un hexagone qui serait proche d'un cluster d'au moins 3 hexagones alliés.

* Finalement, si les deux options précédentes ne sont pas possible alors l'AI jouera alétoirement parmi les hexagones jouables.

---
## Algorithmes implémentant les trois fins de partie possibles.

### Première implémentation de fin de partie

Au fur et à mesure de la partie, les cases se remplissent et dès qu’un des deux joueurs ne peut plus remplir une case la partie est fini

### Deuxième implémentation de fin de partie

Il s’agit-là de rejoindre les deux bords opposés de même couleur de la table de jeu afin de mettre fin à la partie, et donc si les deux bords de même couleur sont reliés de bout en bout par un joueur, on assistera à une fin de partie.

### Troisième implémentation de fin de partie

A chaque tour de jeu on va vérifier à partir de la dernière case posée si cette case possède des voisins non-alliés, de même nous allons vérifier les cases adjacentes allié ou non, de ces mêmes cases. De même nous listerons les côtés existants et SI un des groupes voisins ne possède pas de côté alors le joueur courant gagne. Il s’agit là d’entourer une case adverse afin de mettre fin à la partie

---
## Serveur

Pour la création du serveur, il suffit de lancer la fonction runServer() dans le fichier [src/server.py](src/server.py).

### Le Serveur fonctionne de la façon suivante :
* On crée une variable globale SRVDATA qui va contenir les données du jeux (plateau de jeu, tours, ...)
* On crée un serveur qui va attendre 2 connections
* Dès que le serveur reçois une connexion on crée un nouveau Thread, qui va gérer la connexion ou il va exécuter les fonctions suivantes :
    * Il va envoyer au client 
        * Un ID qui lui permet de s'identifier
        * La variable SRVDATA pour que le client puisse avoir accès à toutes les données du jeu
    * Une boucle est lancée pour exécuter les fonctions suivantes :
        * Le serveur va recevoir les données du client (les données après que le joueur a joué)
        * Assigne les données reçus à SRVDATA
        * Envoie à tous les clients la variable SRVDATA (actualise les données du jeu pour tous les clients)
    

### Au niveau du client, le client est lancé en mode online ou il va se connecter au serveur.
* Il se connecte au serveur avec une IP donné par l'utilisateur
* Le client reçois :
    * Un ID qui lui permet de s'identifier de la part du serveur
    * La variable SRVDATA pour que le client puisse avoir accès à toutes les données du jeu
* Le client vérifie ensuite si c'est son tour de jouer grâce à l'ID et les données dans la variable SRVDATA
* Si c'est son tour de jouer, et envoie les données SRVDATA au serveur



