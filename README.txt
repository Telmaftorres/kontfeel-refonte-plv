Espace de présentation des maquettes de refonte Kontfeel
https://kontfeel-refonte-plv.vercel.app/

Déploiement : automatique par Vercel à chaque push sur la branche main du dépôt GitHub (projet statique, aucun build). outils/ est exclu du déploiement (.vercelignore).

Structure :
- index.html : page d'accueil listant les familles et les maquettes.
- voir.html?m=<id> : consultation d'une maquette avec une barre de retour, la maquette étant chargée telle quelle dans un cadre.
- maquettes.js : registre des familles et maquettes, à compléter pour en ajouter.
- p2.html, p3.html, p4.html : présentoir de comptoir. seeding-box.html : seeding box (P5), avec ses images dans assets/seeding-box/.
- assets/apercus/ : captures du haut de chaque maquette (Chrome sans interface, 1440 × 900, réduites à 960 px).

Ajouter une maquette : déposer le HTML (et ses images) à la racine, faire sa capture dans assets/apercus/, puis ajouter une entrée dans maquettes.js.

Indexation : en-tête X-Robots-Tag noindex, nofollow (vercel.json) et balise meta robots. Noindex ne protège pas la confidentialité : toute personne ayant le lien peut consulter le site.
