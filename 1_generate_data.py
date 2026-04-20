"""
ÉTAPE 1: GÉNÉRATION DE DONNÉES SYNTHÉTIQUES
Script pour générer 50 tickets IT réalistes + 5 guides de documentation
"""

import csv
import random
from datetime import datetime, timedelta
import os

# ============================================================================
# CONFIGURATION DES DONNÉES
# ============================================================================

CATEGORIES = {
    "VPN": {
        "titres": [
            "Cisco AnyConnect se ferme brutalement",
            "Impossible de se connecter au VPN",
            "VPN déconnecte toutes les 5 minutes",
            "Error: 'Secure Gateway is unreachable'",
            "AnyConnect boucle infinie au démarrage",
        ],
        "descriptions": [
            "Quand je lance Cisco AnyConnect, l'application se ferme immédiatement sans message d'erreur. J'ai essayé de redémarrer l'ordinateur.",
            "Je suis en télétravail mais je ne peux plus accéder au VPN. Le mot de passe est correct. Avant cela ça marche. Il y a un message 'Connection refused'.",
            "Depuis ce matin, ma connexion VPN tombe toutes les 5 minutes. Je dois relancer AnyConnect manuellement chaque fois.",
            "Erreur: 'The Secure Gateway is unreachable'. J'ai essayé de vérifier la connectivité réseau mais je ne sais pas ce qui est cassé.",
            "AnyConnect se relance en boucle sans jamais établir une connexion. Je n'arrive pas à voir la fenêtre de connexion.",
        ],
        "resolutions": [
            "Réinstaller Cisco AnyConnect en version 4.10.07055 (version stable). Désinstaller complètement avant. Redémarrer après installation.",
            "Vérifier que le VPN gateway n'a pas changé d'IP. Réinitialiser les paramètres réseau via 'ipconfig /all'. Essayer une autre connexion réseau (mobile).",
            "Désactiver temporairement l'antivirus Windows Defender ou tout antivirus tiers. Vérifier les logs AnyConnect dans Program Files.",
            "Contacter l'équipe infrastructure pour vérifier le statut du serveur VPN. Pendant ce temps, utiliser le VPN web (WebVPN) sur portal.company.com",
            "Effacer le cache d'AnyConnect via %appdata%\\Cisco\\Cisco AnyConnect Secure Mobility Client. Redémarrer et relancer.",
        ]
    },
    "Active Directory": {
        "titres": [
            "Impossible de me connecter au domaine",
            "Mot de passe expiré - reset nécessaire",
            "Erreur 'Credentials are invalid'",
            "Compte utilisateur verrouillé après 5 tentatives",
            "Synchronisation Active Directory échouée",
        ],
        "descriptions": [
            "Je ne peux pas me connecter à mon ordinateur portable. L'écran me dit que mes identifiants sont invalides mais je suis sûr du mot de passe.",
            "Windows m'affiche 'Your password has expired'. Je dois le changer mais je ne sais pas comment dans le contexte d'un domaine Active Directory.",
            "Après plusieurs tentatives de connexion, j'ai un message d'erreur 'Your credentials are invalid'. Peut-être un bug système.",
            "Mon compte s'est verrouillé après 5 mauvaises tentatives de connexion. Comment déverrouiller?",
            "Je ne peux plus synchroniser mon profil utilisateur. Tous les services Microsoft 365 ne répondent plus.",
        ],
        "resolutions": [
            "Vérifier les majuscules/minuscules et la disposition clavier (AZERTY vs QWERTY). Redémarrer en Mode Sans Échec si nécessaire. Contacter IT si problème persiste.",
            "Utiliser Ctrl+Alt+Suppr sur l'écran de connexion, sélectionner 'Changer un mot de passe'. Entrer l'ancien mot de passe, puis le nouveau (minimum 12 caractères, 1 majuscule).",
            "Vérifier la connectivité réseau. Ping sur un contrôleur de domaine: ping dc1.company.local. Si timeout, réinitialiser la carte réseau.",
            "Attendre 15-30 minutes pour que le déverrouillage automatique se fasse, ou contacter IT pour un déblocage manuel immédiat.",
            "Redémarrer l'ordinateur avec une connexion réseau stable. Vérifier la synchronisation de l'horloge système (écart <5 minutes avec le DC).",
        ]
    },
    "Imprimantes": {
        "titres": [
            "Imprimante réseau introuvable",
            "Erreur 'Printer not responding'",
            "Qualité d'impression mauvaise - traits manquants",
            "Impossible d'imprimer depuis certaines applications",
            "Pilote d'imprimante incompatible",
        ],
        "descriptions": [
            "L'imprimante réseau n'apparaît plus dans la liste des imprimantes disponibles. Elle était disponible hier et rien n'a changé de mon côté.",
            "Quand j'essaie d'imprimer, Windows me dit 'The printer is not responding'. L'imprimante est allumée et connectée au réseau.",
            "Mes impressions sortent avec des zones blanches ou des traits manquants. Ça s'est aggravé progressivement.",
            "Je peux imprimer depuis Word mais pas depuis PDF Reader. C'est étrange.",
            "Après une mise à jour Windows 11, je ne peux plus imprimer. Le pilote n'est pas compatible.",
        ],
        "resolutions": [
            "Redémarrer l'imprimante (éteindre 30 secondes). Vérifier la connectivité: ping sur l'IP de l'imprimante (vérifier dans le menu réseau de l'imprimante). Ajouter manuellement via Paramètres > Imprimantes & Scanners.",
            "Effacer le file d'impression: net stop spooler / net start spooler dans Invite de Commande (Admin). Redémarrer l'imprimante.",
            "Nettoyer les têtes d'impression via le menu de l'imprimante. Sinon, remplacer les cartouches/toners même s'ils affichent du toner. Les capteurs peuvent être défaillants.",
            "Désinstaller et réinstaller le pilote. Vérifier que l'application autorise l'impression réseau (paramètres d'imprimante dans l'app).",
            "Télécharger le pilote Windows 11 depuis le site du fabricant (HP, Xerox, etc). Installer en tant qu'administrateur. Redémarrer.",
        ]
    },
    "Lenteur Réseau": {
        "titres": [
            "Internet très lent depuis ce matin",
            "Connexion réseau instable - packet loss",
            "Téléchargement très lent (< 1 Mbps)",
            "Latence élevée aux serveurs internes",
            "WiFi du bureau très faible",
        ],
        "descriptions": [
            "Depuis environ 9h du matin, mon Internet est extrêmement lent. Les pages web mettent 10 secondes à charger. Mon wifi affiche 3 barres.",
            "J'ai un problème de connexion intermittente. Parfois tout fonctionne, puis je perds la connexion pendant 2-3 secondes. Cela rend les appels Teams impossibles.",
            "Les téléchargements sont très lents, environ 500 kbps. Ma box affiche une bonne signal mais rien ne change.",
            "Je ne peux pas accéder à nos serveurs internes. Le ping à 'fileserver.local' prend 500ms au lieu de 20ms habituellement.",
            "Le WiFi dans mon bureau est très faible. Je reçois à peine 2-3 barres. Mon voisin en reçoit 5. Il y a peut-être un problème d'AP.",
        ],
        "resolutions": [
            "Redémarrer la box/routeur (30 secondes). Vérifier la qualité de la ligne (dégroupage) sur www.speedtest.net. Si < 5 Mbps, contacter FAI. Sinon, vérifier les processus réseau.",
            "Ouvrir Resource Monitor (resmon) et vérifier réseau TCP/UDP. Arrêter les applications qui uploadent/downloadent inutilement. Mettre en jour tous les antivirus/malwares.",
            "Redémarrer le PC. Vérifier que aucun torrent ou service cloud ne synchronise. Vérifier le débit réel: speedtest.net. Si stable, le problème est externe (FAI).",
            "Vérifier la latence au DC: ping dc1.company.local. Si > 100ms, il y a une congestion réseau. Contacter IT infrastructure. Essayer une connexion filaire (Ethernet) si possible.",
            "Vérifier le signal WiFi en se rapprochant du point d'accès. Si signal améliore, il y a une obstruction (murs épais, micro-ondes). Contacter IT pour repositionner l'AP. Alternativement, utiliser Ethernet.",
        ]
    },
    "Écran Bleu": {
        "titres": [
            "BSOD au démarrage de Windows",
            "Écran bleu aléatoire pendant le travail",
            "CRITICAL_PROCESS_DIED - PC qui redémarre",
            "DRIVER_IRQL_NOT_LESS_OR_EQUAL",
            "Écran bleu avec code SYSTEM_SERVICE_EXCEPTION",
        ],
        "descriptions": [
            "Au démarrage, Windows affiche un écran bleu avec un code d'erreur avant de redémarrer automatiquement. Je ne vois pas assez vite pour noter le code.",
            "Pendant que je travaille, l'écran devient bleu aléatoirement. C'est devenu plus fréquent cette semaine. Je dois redémarrer le PC.",
            "Mon PC redémarre constamment avec un écran bleu. Le message dit 'CRITICAL_PROCESS_DIED'. C'était stable hier.",
            "Écran bleu avec le message 'DRIVER_IRQL_NOT_LESS_OR_EQUAL'. Je crois que c'est un problème de driver.",
            "Écran bleu: SYSTEM_SERVICE_EXCEPTION. Pas d'erreur avant. C'est devenu impossible de travailler.",
        ],
        "resolutions": [
            "Redémarrer en Mode Sans Échec (F8 pendant démarrage). Désinstaller les mises à jour Windows récentes (Param > Historique des mises à jour). Relancer PC.",
            "Vérifier le disque dur avec chkdsk: chkdsk C: /F /R en Invite (Admin). Vérifier la RAM avec Windows Memory Diagnostic. Remplacer si erreurs détectées.",
            "Effectuer une restauration du système à une date antérieure (Param > Système > Protec. Système > Restauration système). Choisir un point de restaure d'il y a 3-5 jours.",
            "Mettre à jour les pilotes graphiques depuis le site du fabricant (NVIDIA/AMD). Désinstaller complètement l'ancien pilote avant installation.",
            "Utiliser l'outil BlueScreenView pour lire le fichier de dump. Contacter IT avec le code d'erreur exact. Cela aide à diagnostiquer rapidement.",
        ]
    }
}

DOCUMENTATION = {
    "VPN_Guide.md": """# Guide de Dépannage VPN Cisco AnyConnect

## Aperçu
Cisco AnyConnect est la solution VPN officielle de l'entreprise pour la connexion sécurisée en télétravail. Ce guide couvre les problèmes les plus courants.

## Installation Recommandée
- **Version stable:** 4.10.07055
- **Plateforme:** Windows 10/11, macOS 10.15+, Linux Ubuntu 20.04+
- **Prérequis:** .NET Framework 4.5+, droits administrateur

## Problèmes Courants et Solutions

### Problème 1: Application qui se ferme brutalement
**Symptôme:** AnyConnect se ferme sans message d'erreur au lancement.

**Solution:**
1. Désinstaller complètement AnyConnect (Panneau de Configuration > Programmes)
2. Télécharger la version 4.10.07055 depuis le portail IT
3. Installer avec droits administrateur
4. Redémarrer l'ordinateur
5. Relancer AnyConnect

### Problème 2: 'Secure Gateway is unreachable'
**Symptôme:** Message d'erreur lors de la connexion.

**Cause possible:** La passerelle VPN a changé d'adresse IP ou il y a une congestion réseau.

**Solution:**
1. Vérifier la connectivité: `ping 8.8.8.8`
2. Vérifier l'adresse du gateway dans l'interface AnyConnect
3. Contacter IT Infrastructure si le problème persiste
4. Utiliser le VPN Web comme alternative: https://portal.company.com

### Problème 3: Déconnexions fréquentes
**Symptôme:** Connexion VPN qui tombe toutes les 5-10 minutes.

**Solution:**
1. Désactiver temporairement l'antivirus
2. Vérifier les paramètres de proxy dans Windows
3. Effacer le cache AnyConnect: `%appdata%\\Cisco\\Cisco AnyConnect Secure Mobility Client`
4. Redémarrer le PC et relancer

## Informations de Contact
- **Support IT Level 1:** support@company.com
- **Support VPN spécialisé:** vpn-team@company.com
- **Portail de service:** https://support.company.local
""",

    "Active_Directory_Guide.md": """# Guide de Dépannage Active Directory

## Vue d'ensemble
Active Directory (AD) gère l'authentification et les autorisations pour tous les utilisateurs du domaine company.local.

## Connexion au Domaine

### Erreur: 'Credentials are invalid'
**Causes possibles:**
- Mot de passe incorrect (vérifier la disposition clavier AZERTY/QWERTY)
- Compte utilisateur désactivé
- Synchronisation AD échouée
- Horloge système désynchronisée (écart > 5 minutes avec le DC)

**Solutions rapides:**
1. Appuyer sur Maj+VerrumNum si le clavier semble inversé (AZERTY/QWERTY)
2. Vérifier que CapsLock n'est pas activé
3. Redémarrer l'ordinateur avec connexion réseau active
4. Tenter une connexion sur le VPN en priorité

### Réinitialisation de Mot de Passe
**Politique:** Les mots de passe expirent tous les 90 jours. Minimum 12 caractères avec 1 majuscule, 1 chiffre, 1 caractère spécial.

**Procédure:**
1. Écran de connexion Windows: Appuyer sur Ctrl + Alt + Suppr
2. Sélectionner "Changer un mot de passe"
3. Entrer l'ancien mot de passe
4. Entrer le nouveau mot de passe (2x pour confirmation)
5. Attendre 15 secondes pour la synchronisation AD
6. Se reconnecter

### Compte Verrouillé
**Symptôme:** "Your account has been locked. Please contact your administrator."

**Cause:** 5 tentatives de connexion échouées en 30 minutes

**Solution:**
- Attendre 30 minutes pour déblocage automatique
- OU contacter IT pour déblocage immédiat: `support@company.com`
- OU accéder via compte administrateur local (si disponible)

## Synchronisation avec Microsoft 365
Si le profil n'est pas synchronisé avec Microsoft 365 (Outlook, OneDrive, Teams):
1. Vérifier la connexion internet
2. Forcer une synchronisation: `gpupdate /force` en Invite (Admin)
3. Redémarrer l'ordinateur
4. Attendre 5-10 minutes pour que OneDrive se synchronise

## Contacter IT
- **Support AD:** ad-support@company.com
- **Password Reset Portal:** https://password.company.local
- **IT Helpdesk:** +33 1 XX XX XX XX
""",

    "Imprimantes_Guide.md": """# Guide Dépannage Imprimantes Réseau

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
del %systemroot%\\System32\\spool\\PRINTERS\\*
net start spooler
```

## Support Imprimantes
- **Maintenance:** maintenance@company.com
- **Problèmes techniques:** it-printers@company.com
- **Remplacement cartouches:** stock@company.com
""",

    "Reseau_Performance.md": """# Optimisation Réseau et Performance

## Diagnostic de la Connexion Réseau

### Vérifier votre débit
1. Visiter https://www.speedtest.net
2. Cliquer "Go" et attendre le résultat
3. **Attendu:** Minimum 10 Mbps download, 5 Mbps upload
4. Si inférieur: Problème FAI ou réseau local

### Tester la latence
**Ligne de commande:**
```
ping 8.8.8.8          (Test Internet)
ping dc1.company.local (Test domaine interne)
tracert company.com   (Tracer la route)
```

**Résultats normaux:**
- Internet externe: 20-50 ms
- Domaine interne: < 20 ms
- Si > 100 ms: Congestion réseau

## Problèmes Courants de Réseau

### Connexion Lente
**Causes possibles:**
1. **FAI:** Vitesse contractuelle non respectée
2. **WiFi faible:** Signal insuffisant ou interférences
3. **Processus actifs:** Synchronisation cloud, antivirus scanning
4. **Congestion réseau:** Trop d'utilisateurs simultanément

**Solutions:**
1. Redémarrer la box/routeur
2. Rapprocher-vous du point WiFi
3. Ouvrir Resource Monitor et vérifier les processus réseau
4. Utiliser Ethernet si possible (plus stable que WiFi)
5. Contacter IT Infrastructure si problème interne

### Déconnexions Fréquentes
1. Vérifier la stabilité WiFi (roaming, changement de canal)
2. Vérifier les logs d'événement Windows pour les erreurs réseau
3. Mettre à jour le pilote de la carte réseau
4. Désactiver la mise en veille réseau: Gestionnaire d'appareils > Propriétés carte réseau > Alimentation

### Problèmes avec Teams/Zoom
- Vérifier que votre connexion ne saturate pas (pas de téléchargement simultané)
- Réduire la qualité vidéo dans les paramètres (économise 1-2 Mbps)
- Utiliser un casque filaire plutôt que WiFi
- Fermer les navigateurs et applications inutiles

## Outils Recommandés
- **Speedtest.net:** Test de débit
- **Resource Monitor:** Analyse des processus réseau (resmon)
- **WiFi Analyzer:** Vérifier les interférences WiFi (app gratuite Windows Store)

## Support Réseau
- **Niveau 1:** support@company.com
- **Infrastructure:** network-team@company.com
- **ISP (FAI):** [Contacter directement votre FAI]
""",

    "Windows_Stability.md": """# Résolution des Problèmes Windows - Crash et Écran Bleu

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
- **Joindre les fichiers dump:** C:\\Windows\\minidump\\
- **Logs du problème:** Événements > Windows Logs > Erreur système
"""
}

# ============================================================================
# FUNCTIONS
# ============================================================================

def generate_tickets(num_tickets=50):
    """Génère une liste de tickets réalistes"""
    tickets = []
    ticket_id = 1000
    
    tickets_per_category = num_tickets // len(CATEGORIES)
    
    for category, content in CATEGORIES.items():
        for i in range(tickets_per_category):
            days_ago = random.randint(1, 90)
            resolved_date = datetime.now() - timedelta(days=days_ago)
            created_date = resolved_date - timedelta(days=random.randint(1, 7))
            
            ticket = {
                "Ticket_ID": f"TK{ticket_id:05d}",
                "Titre": random.choice(content["titres"]),
                "Description": random.choice(content["descriptions"]),
                "Catégorie": category,
                "Résolution_Apportée": random.choice(content["resolutions"]),
                "Date_Création": created_date.strftime("%Y-%m-%d"),
                "Date_Résolution": resolved_date.strftime("%Y-%m-%d"),
                "Sévérité": random.choice(["Basse", "Moyenne", "Haute"]),
            }
            tickets.append(ticket)
            ticket_id += 1
    
    return tickets

def export_tickets_to_csv(tickets, filename="tickets_historiques.csv"):
    """Exporte les tickets en fichier CSV"""
    fieldnames = ["Ticket_ID", "Titre", "Description", "Catégorie", "Résolution_Apportée", 
                  "Date_Création", "Date_Résolution", "Sévérité"]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tickets)
    
    print(f" {len(tickets)} tickets exportés dans: {filename}")

def create_documentation_files(docs=DOCUMENTATION, folder="./docs"):
    """Crée les fichiers de documentation Markdown"""
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    for filename, content in docs.items():
        filepath = os.path.join(folder, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f" Documentation: {filename}")

def main():
    print("\n" + "="*80)
    print(" ÉTAPE 1: GÉNÉRATION DE DONNÉES SYNTHÉTIQUES")
    print("="*80 + "\n")
    
    # Générer tickets
    print(" Génération de 50 tickets IT réalistes...")
    tickets = generate_tickets(50)
    
    # Exporter CSV
    print(" Export en CSV...")
    export_tickets_to_csv(tickets)
    
    # Créer documentation
    print(" Création de 5 guides Markdown...")
    create_documentation_files()
    
    print("\n" + "="*80)
    print(" ÉTAPE 1 TERMINÉE!")
    print("="*80)
    print(" Fichiers générés:")
    print("   • tickets_historiques.csv (50 tickets)")
    print("   • docs/ (5 guides Markdown)")
    print("\n Prochaine étape: 2_ingest_vectorize.py\n")

if __name__ == "__main__":
    main()
