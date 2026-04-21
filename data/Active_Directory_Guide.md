# Guide de Dépannage Active Directory

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
