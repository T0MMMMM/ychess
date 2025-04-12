# ✅ Serveur de Matchmaking – Suivi du projet

Ce projet consiste à développer un **serveur de matchmaking** pour des jeux de plateau au tour par tour. Il est composé de trois éléments :  
- Un **serveur**  
- Un **logiciel client**  
- Une **base de données**

---

## 📦 Modèle de données

- [ ] File d’attente
  - [ ] Moyen de communication (IP, port)
  - [ ] Pseudo
  - [ ] Date d’entrée
- [ ] Matchs
  - [ ] Moyen de communication joueur 1
  - [ ] Moyen de communication joueur 2
  - [ ] Plateau de jeu
  - [ ] Statut de fin du match
  - [ ] Résultat (victoire joueur 1 / joueur 2 / égalité)
- [ ] Tours
  - [ ] Liaison avec le match
  - [ ] Joueur ayant joué
  - [ ] Information du coup joué

---

## 🧠 Serveur de Matchmaking

- [ ] Lien avec la base de données
- [ ] Système de socket :
  - [ ] Réception : client entre dans la file d’attente
  - [ ] Envoi : début d’un match
  - [ ] Réception + Envoi : un tour est joué
  - [ ] Envoi : fin d’un match
- [ ] Vérification constante de la file d’attente
- [ ] Création automatique des matchs
- [ ] Implémentation de la logique du jeu (choix libre : morpion, puissance 4, etc.)

---

## 🧑‍💻 Logiciel client

- [ ] Système de socket :
  - [ ] Envoi : entrée en file d’attente
  - [ ] Réception : début d’un match
  - [ ] Envoi : jouer un coup
  - [ ] Réception : coup adverse
  - [ ] Réception : fin du match
- [ ] Partie de la logique du jeu choisie
- [ ] Interface utilisateur :
  - [ ] IHM (interface graphique)  
    **ou**
  - [ ] CLI avec IA

---

## 🗂️ TODO GÉNÉRAL

- [ ] Choix du jeu de plateau (ex : Morpion, Puissance 4, Dames...)
- [ ] Architecture technique (schémas, choix techno)
- [ ] Définition des protocoles socket
- [ ] Création de la base de données
- [ ] Développement serveur
- [ ] Développement client
- [ ] Tests unitaires / fonctionnels
- [ ] Documentation technique

---

> 🔄 N'oublie pas de cocher les cases au fur et à mesure !