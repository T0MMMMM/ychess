# ✅ Serveur de Matchmaking – Suivi du projet

Ce projet consiste à développer un **serveur de matchmaking** pour des jeux de plateau au tour par tour. Il est composé de trois éléments :  
- Un **serveur**  
- Un **logiciel client**  
- Une **base de données**

---

## 📦 Modèle de données

- [x] File d’attente
  - [x] Moyen de communication (IP, port)
  - [x] Pseudo
  - [x] Date d’entrée
- [x] Matchs
  - [x] Moyen de communication joueur 1
  - [x] Moyen de communication joueur 2
  - [x] Plateau de jeu
  - [x] Statut de fin du match
  - [x] Résultat (victoire joueur 1 / joueur 2 / égalité)
- [x] Tours
  - [x] Liaison avec le match
  - [x] Joueur ayant joué
  - [x] Information du coup joué

---

## 🧠 Serveur de Matchmaking

- [x] Lien avec la base de données
- [x] Système de socket :
  - [x] Réception : client entre dans la file d’attente
  - [x] Envoi : début d’un match
  - [x] Réception + Envoi : un tour est joué
  - [x] Envoi : fin d’un match
- [x] Vérification constante de la file d’attente
- [x] Création automatique des matchs
- [x] Implémentation de la logique du jeu (choix libre : morpion, puissance 4, etc.)

---

## 🧑‍💻 Logiciel client

- [x] Système de socket :
  - [x] Envoi : entrée en file d’attente
  - [x] Réception : début d’un match
  - [x] Envoi : jouer un coup
  - [x] Réception : coup adverse
  - [x] Réception : fin du match
- [x] Partie de la logique du jeu choisie
- [x] Interface utilisateur :
  - [x] IHM (interface graphique)  
    **ou**
  - [ ] CLI avec IA

---

## Comment lancer le serveur

1. **Créer un environnement virtuel** :
   - Sur **Windows** :
     ```bash
     python -m venv venv
     ```
   - Sur **Linux** :
     ```bash
     python3 -m venv venv
     ```

2. **Activer l'environnement virtuel** :
   - Sur **Windows** :
     ```bash
     .\venv\Scripts\activate
     ```
   - Sur **Linux** :
     ```bash
     source venv/bin/activate
     ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer le serveur** :
   ```bash
   python -m chess_server.main
   ```

## Comment lancer le client

1. Naviguez dans le dossier `dist` où se trouve l'exécutable du client.
2. Double-cliquez sur le fichier `chess_client.exe` pour lancer l'application client.

Assurez-vous que le serveur est en cours d'exécution avant de lancer le client.
