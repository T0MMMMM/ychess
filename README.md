# Projet Jeu d'Échecs avec Matchmaking

## Architecture du Projet
- Module `chess-common` : Modèles et DTOs partagés
- Module `chess-server` : Serveur de matchmaking Spring Boot
- Module `chess-client` : Application bureau JavaFX

## Fonctionnalités à Implémenter

### 1. Système de Matchmaking
- [ ] File d'attente des joueurs
- [ ] Appariement automatique des joueurs
- [ ] Gestion des déconnexions
- [ ] Système de classement ELO

### 2. Jeu d'Échecs
- [ ] Implémentation des règles complètes
  - [ ] Mouvements des pièces
  - [ ] Échec et mat
  - [ ] Pat
  - [ ] Roque
  - [ ] Prise en passant
  - [ ] Promotion des pions
- [ ] Validation des coups
- [ ] Historique des coups
- [ ] Timer de jeu

### 3. Interface Client
- [ ] Écran de connexion/inscription
- [ ] Lobby avec file d'attente
- [ ] Échiquier interactif
- [ ] Chat in-game
- [ ] Historique des parties
- [ ] Profil joueur

### 4. Base de Données
- [ ] Gestion des utilisateurs
- [ ] Historique des parties
- [ ] Statistiques des joueurs
- [ ] Classement ELO

### 5. Communication Client/Serveur
- [ ] Protocol WebSocket
- [ ] Gestion des événements en temps réel
- [ ] Sécurisation des échanges

## Technologies Utilisées
- Java 17
- Spring Boot 3.1.5
- JavaFX
- WebSocket
- JPA/Hibernate
- Base de données H2

## Planning de Développement
1. Phase 1 : Architecture de base
2. Phase 2 : Implémentation du jeu d'échecs
3. Phase 3 : Système de matchmaking
4. Phase 4 : Interface utilisateur
5. Phase 5 : Tests et optimisation
