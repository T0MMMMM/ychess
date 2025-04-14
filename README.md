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

## Instructions pour lancer le serveur et le client

### Prérequis
Si vous partez d'un PC sans Python ni dépendances installées, suivez ces étapes pour configurer votre environnement et exécuter le serveur et le client.

---

### Lancer le serveur

1. **Installer Python** :
   - Téléchargez et installez Python depuis [python.org](https://www.python.org/downloads/).
   - Assurez-vous de cocher l'option "Add Python to PATH" lors de l'installation.

2. **Cloner le projet** :
   ```bash
   git clone <URL_DU_REPO>
   cd ychess
   ```

3. **Créer un environnement virtuel** :
   - Sur **Windows** :
     ```bash
     python -m venv venv
     ```
   - Sur **Linux** :
     ```bash
     python3 -m venv venv
     ```

4. **Activer l'environnement virtuel** :
   - Sur **Windows** :
     ```bash
     .\venv\Scripts\activate
     ```
   - Sur **Linux** :
     ```bash
     source venv/bin/activate
     ```

5. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

6. **Lancer le serveur** :
   ```bash
   python -m chess_server.main
   ```

---

### Lancer le client

1. **Télécharger l'exécutable** :
   - Si vous êtes sur **Windows**, l'exécutable du client est déjà généré et se trouve dans le dossier `dist`.
   - Si vous êtes sur **Linux**, vous devez générer un exécutable spécifique (voir ci-dessous).

2. **Exécuter le client** :
   - Sur **Windows** :
     - Naviguez dans le dossier `dist`.
     - Double-cliquez sur `chess_client.exe` pour lancer l'application.
   - Sur **Linux** :
     - Générez un exécutable avec PyInstaller :
       ```bash
       pip install pyinstaller
       pyinstaller --onefile --noconsole -n chess_client chess_client/main.py
       ```
     - L'exécutable sera généré dans le dossier `dist`. Exécutez-le avec :
       ```bash
       ./dist/chess_client
       ```

3. **Assurez-vous que le serveur est en cours d'exécution avant de lancer le client.**
