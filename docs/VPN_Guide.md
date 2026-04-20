# Guide de Dépannage VPN Cisco AnyConnect

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
3. Effacer le cache AnyConnect: `%appdata%\Cisco\Cisco AnyConnect Secure Mobility Client`
4. Redémarrer le PC et relancer

## Informations de Contact
- **Support IT Level 1:** support@company.com
- **Support VPN spécialisé:** vpn-team@company.com
- **Portail de service:** https://support.company.local
