ABOUT_TEXT = """Ce logiciel est le projet no 1 du cours C52.
Il a été réalisé par :
Fatou Ly Basse
Eloi Vertefeuille 
Emille Larouche
Félix Larose

** mot de passe hardcoder (AAAaaa123) dans db_dao **

Il consiste à faire la classification automatique d'images 2D à partir de descripteurs de forme avec les concepts suivants :
- Algorithme des K plus proches voisins (KNN) avec filtrage par distance maximale
- Réduction de complexité par extraction de caractéristiques 3D
- Visualisation interactive de l'espace de solution en 3D
- Accès et requêtage de données relationnelles PostgreSQL via DAO
Nos 3 descripteurs de forme sont :
- Indice de compacité (circularité)
  - en ratio adimensionnel pour le domaine [0, 1]
  - correspondant à la mesure de circularité normalisée basée sur le rapport (4 * π * Aire) / Périmètre²
- Taux de remplissage du cercle englobant
  - en ratio adimensionnel pour le domaine [0, 1]
  - correspondant à la proportion de pixels occupés par la forme dans son cercle circumscrit minimal
- Ratio de la distance moyenne sur la distance maximale au centroïde
  - en ratio adimensionnel pour le domaine [0, 1]
  - correspondant au rapport entre la distance moyenne des pixels au centroïde et la distance maximale au centroïde
Plus précisément, ce laboratoire permet de mettre en pratique les notions de :
- Traitement d'images numériques et calculs matriciels vectorisés avec NumPy (aires, périmètres, centroïdes)
- Implémentation générique de l'algorithme de classification KNN et résolution des cas d'égalité/distances limites
- Développement d'interfaces graphiques interactives et visualisations 3D avec PySide6 (Qt)
- Persistance, extraction et décodage de données binaires PNG depuis PostgreSQL avec un pattern DAO
Un effort d'abstraction a été fait pour ces points :
- Découpage strict de l'architecture logicielle (Accès BDD / Analyse d'image / KNN / Interface graphique)
- Généricité de la classe KNN (indépendante de la nature des métriques et adaptable aux dimensions choisies)
- Normalisation et conditionnement uniforme de l'espace de solution dans la plage [0, 1]³
Finalement, l’ensemble de données le plus complexe que nous avons été capable de résoudre est Zoo Large (peut prendre du temps sur une mauvaise machine)
- 
"""