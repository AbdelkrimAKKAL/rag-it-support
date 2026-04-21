# Guide Dépannage Imprimantes Réseau

## Configuration des Imprimantes Réseau

### Imprimantes Disponibles
- **Bureau principal (RDC):** HP OfficeJet Pro 8025 (192.168.1.100)
- **Étage 1:** Xerox VersaLink C405 (192.168.1.101)
- **Étage 2:** Ricoh MP C3003 (192.168.1.102)
- **Salle réunion:** Brother HL-L9310CDW (192.168.1.103)

### Ajouter une Imprimante Réseau

**Windows 10/11:**
1. Paramètres > Appareils > Imprimantes & Scanners
2. Cliquer sur "Ajouter une imprimante ou un scanner"
3. Si pas trouvée automatiquement: "L'imprimante souhaitée ne figure pas dans la liste"
4. Entrer l'adresse IP (ex: 192.168.1.100)
5. Windows trouvera le pilote automatiquement
6. Cliquer "Ajouter un périphérique"

### Problèmes d'Impression

**Problème: Imprimante introuvable sur le réseau**
1. Ping l'adresse IP de l'imprimante: `ping 192.168.1.100`
2. Si timeout: Vérifier la connexion réseau de l'imprimante via son menu
3. Redémarrer l'imprimante (éteindre 30 secondes)
4. Réessayer d'ajouter l'imprimante

**Problème: 'Printer Not Responding'**
1. Aller dans Imprimantes & Scanners
2. Sélectionner l'imprimante et cliquer "Ouvrir la file d'attente"
3. Menu: Imprimante > Annuler tous les documents
4. Redémarrer l'imprimante
5. Supprimer puis réajouter l'imprimante

**Problème: Qualité d'impression mauvaise (traits manquants)**
1. Ouvrir le menu de l'imprimante via son écran tactile
2. Sélectionner "Maintenance" > "Nettoyage des têtes"
3. Si problème persiste: Les cartouches peuvent être vides
4. Vérifier les niveaux de toner/encre dans le pilote Windows
5. Remplacer si nécessaire (références à disposition au bureau)

**Problème: Impossible d'imprimer depuis une application spécifique**
1. Vérifier les paramètres de l'application (imprimer en PDF d'abord pour tester)
2. Réinstaller le pilote de l'imprimante
3. Redémarrer l'application

## Gestion de la File d'Impression

Pour réinitialiser la file d'impression si elle est figée:

**Windows (Invite de Commande Admin):**
```
net stop spooler
del %systemroot%\System32\spool\PRINTERS\*
net start spooler
```

## Support Imprimantes
- **Maintenance:** maintenance@company.com
- **Problèmes techniques:** it-printers@company.com
- **Remplacement cartouches:** stock@company.com
