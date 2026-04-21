# Optimisation Réseau et Performance

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
