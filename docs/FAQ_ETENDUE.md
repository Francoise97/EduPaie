# FAQ etendue - EduPaie

## Installation

### Sur quel systeme fonctionne EduPaie ?

Windows 10 et 11 (64 bits). Une version Linux/Mac est possible.

### Faut-il Python installe ?

Non. La version executable est autonome.

### Combien d'espace disque ?

Environ 100 Mo pour l'application + quelques Mo pour les donnees.

## Utilisation

### Combien d'eleves puis-je gerer ?

Plusieurs milliers sans probleme.

### Puis-je imprimer plusieurs recus a la fois ?

Oui, en les selectionnant un par un.

### Que se passe-t-il si j'annule un paiement ?

Le paiement est marque "Annule" (visible dans l'historique).
Le solde est recalcule. Rien n'est supprime.

### Puis-je restaurer un paiement annule ?

Non directement. Il faut creer un nouveau paiement.

### Comment sauvegarder mes donnees ?

Copier data/edupaie.db sur une cle USB.

## Donnees

### Ou sont stockees les donnees ?

Dans data/edupaie.db (fichier SQLite).

### Puis-je exporter les donnees vers Excel ?

Pas encore. Prevu dans la roadmap v1.1.

### Les donnees sont-elles securisees ?

La base n'est pas chiffree. Sauvegardez regulierement.

## Technique

### Quel langage utilise ?

Python 3.10+ avec PySide6.

### Quelle base de donnees ?

SQLite 3.

### Comment contribuer ?

Voir CONTRIBUTING.md sur GitHub.
