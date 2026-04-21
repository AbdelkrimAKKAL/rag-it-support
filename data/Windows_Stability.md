# Résolution des Problèmes Windows - Crash et Écran Bleu

## Comprendre les Écrans Bleus (BSOD)

Un écran bleu (Blue Screen of Death - BSOD) indique une erreur système critique. Windows affiche un code d'erreur et redémarre automatiquement.

### Codes d'Erreur Courants

**DRIVER_IRQL_NOT_LESS_OR_EQUAL**
- Problème: Conflit de pilote ou corruption de pilote
- Solution: Mettre à jour les pilotes graphiques/réseau

**CRITICAL_PROCESS_DIED**
- Problème: Un processus système critique s'est arrêté
- Solution: Restauration système ou réparation Windows

**SYSTEM_SERVICE_EXCEPTION**
- Problème: Service système défaillant
- Solution: Désactiver les logiciels antivirus/tiers et relancer

## Diagnostic et Dépannage

### Étape 1: Noter le Code d'Erreur
Si l'écran bleu reste visible quelques secondes, noter:
- Le code d'erreur (ex: 0x0000007E)
- Le message textuel
- Chercher en ligne: "[Code d'erreur] Windows 11" + votre version

### Étape 2: Vérifier l'Intégrité du Disque
1. Ouvrir Invite de Commande (Admin)
2. Taper: `chkdsk C: /F /R`
3. Redémarrer et attendre la vérification (peut prendre 1-2 heures)
4. Noter si des erreurs sont détectées

### Étape 3: Vérifier la RAM
1. Windows Search: "Memory Diagnostic"
2. Cliquer "Restart now and check for problems"
3. L'outil redémarre et teste la mémoire
4. Si erreurs détectées: RAM défaillante à remplacer

### Étape 4: Restauration Système
Si les BSOD sont récents:
1. Paramètres > Système > Protection du système
2. Cliquer "Restauration système"
3. Choisir un point de restauration antérieur (avant les BSOD)
4. Cliquer "Suivant" et confirmer
5. Laisser s'exécuter (15-30 minutes)

## Prévention des Crashes

### Mises à Jour
- Garder Windows à jour (mises à jour mensuelles)
- Mettre à jour les pilotes (surtout graphiques, réseau)
- Installer les patches de sécurité

### Antivirus
- Utiliser Windows Defender (inclus gratuitement)
- Ou un antivirus professionnel approuvé
- Éviter plusieurs antivirus simultanément (conflits)

### Nettoyage
- Supprimer les fichiers temporaires chaque mois
- Maintenir au minimum 20% d'espace libre sur C:
- Utiliser "Nettoyage de disque" régulièrement

## Outils Utiles

**BlueScreenView:** 
- Télécharger sur https://www.nirsoft.net/utils/blue_screen_view.html
- Affiche les fichiers dump des BSOD passés
- Aide à identifier le driver/service en cause

## Support Avancé
- **IT Helpdesk:** support@company.com
- **Joindre les fichiers dump:** C:\Windows\minidump\
- **Logs du problème:** Événements > Windows Logs > Erreur système
