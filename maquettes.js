/*
  Registre des maquettes présentées sur l'espace de présentation (index.html)
  et dans la page de consultation (voir.html).

  Pour ajouter une maquette : ajouter un objet dans « maquettes » de la famille concernée.
  Pour ajouter une famille : ajouter un objet dans KONTFEEL_FAMILLES.
  - id       : identifiant utilisé dans l'adresse voir.html?m=<id> (unique)
  - fichier  : page HTML de la maquette, à la racine du dépôt
  - apercu   : capture du haut de la page (1440 × 900 réduite à 960 px de large)
  - maj      : date de dernière modification, au format AAAA-MM-JJ
  - statut   : statut affiché sur la carte (ex. « En attente de validation »)
*/
window.KONTFEEL_FAMILLES = [
  {
    id: 'presentoir-comptoir',
    titre: 'Présentoir de comptoir',
    intro: 'Propositions de refonte de la page catégorie « Présentoir comptoir ».',
    maquettes: [
      {
        id: 'p2',
        titre: 'P2 — Filtres visibles à gauche',
        description: 'Filtres visibles à gauche et catégories en vignettes.',
        fichier: 'p2.html',
        apercu: 'assets/apercus/p2.jpg',
        maj: '2026-11-26',
        statut: 'En attente de validation'
      },
      {
        id: 'p3',
        titre: 'P3 — Version commerciale simplifiée',
        description: 'Une version plus courte, centrée sur les produits, les réalisations, les matériaux et la prise de contact.',
        fichier: 'p3.html',
        apercu: 'assets/apercus/p3.jpg',
        maj: '2026-11-26',
        statut: 'En attente de validation'
      },
      {
        id: 'p4',
        titre: 'P4 — Découverte interactive',
        description: 'Une page très courte au départ : on déplie les familles, les matériaux ou les secteurs, et la galerie se filtre selon la sélection.',
        fichier: 'p4.html',
        apercu: 'assets/apercus/p4.jpg',
        maj: '2026-11-26',
        statut: 'En attente de validation'
      }
    ]
  },
  {
    id: 'seeding-box',
    titre: 'Seeding box & coffrets influenceurs',
    intro: 'Proposition de page pour les seeding boxes, box influenceurs et coffrets presse.',
    maquettes: [
      {
        id: 'seeding-box',
        titre: 'P5 — Seeding box et coffrets influenceurs',
        description: 'Page de présentation avec la réalisation Céréal Bio — Love Tofu, des concepts par univers et une FAQ.',
        fichier: 'seeding-box.html',
        apercu: 'assets/apercus/seeding-box.jpg',
        maj: '2026-11-27',
        statut: 'En attente de validation'
      }
    ]
  }
];
