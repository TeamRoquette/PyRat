mySuperFastAndCleverBot - A PyRat I.A. from Team Roquette
=========================================================

Description
-----------

PyRat est un jeu proposé par [Télécom Bretagne](http://formations.telecom-bretagne.eu/pyrat/)
dont le but est de programmer une intelligence artificielle. Il s'agit de récupérer des pièces
dans un labyrinthe et ce plus rapidement que notre adversaire.

Vous trouverez ici nos I.A.s pour ce jeu.


Structure
---------

Le code est modulaire, dans lib plusieurs modules:

* PyratApi.py          : Communication avec le jeu PyRat.
* connard.py           : Mise en évidence et exploitation de failles du jeu.
* shortestPaths.py     : Algorithme de calcul de plus court chemin.
* travelHeuristics.py  : Plusieurs heuristiques de résolution du problème de voyageur de commerce.
* utils.py             : Divers petites fonctions. 


Bots
----

Plusieurs bots sont dispos :

* enculay.py      : Met en oeuvre la lib connard pour tricher.
* fourmis.py      : Implémente une heuristique d'optimisation par colonie de fourmis.
* greedy.py       : Algorithme glouton avec annulation si l'adversaire a pris notre objectif.
* parralelTry.py  : Tentative de parralélisation du calcul du méta-graphe (mono-coeur sur python, abandon).
* template.py     : template d'I.A.s, va en haut à chaque tour.


Auteur/Contact
--------------

Théo JACQUIN et Quentin JODELET, élève 1A FIG à Télécom Bretagne (et fiers de l'etre).
