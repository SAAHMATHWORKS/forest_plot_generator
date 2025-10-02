# 📊 Forest Plot Generator

Une application web interactive pour générer des Forest Plots professionnels à partir de vos données CSV ou Excel.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

## 🎯 Fonctionnalités

- ✅ **Import flexible** : Support des fichiers CSV et Excel (.xlsx, .xls)
- 🎨 **Personnalisation complète** : Thèmes de couleurs, dimensions, styles de marqueurs
- 🔍 **Filtres interactifs** : Sélection des catégories et groupes à afficher
- 📊 **Visualisation professionnelle** : Intervalles de confiance, zones colorées, ligne de référence
- 💾 **Export multiple** : HTML interactif, PNG, SVG
- 📈 **Statistiques descriptives** : Résumés statistiques par groupe
- 📱 **Interface responsive** : Design moderne et adaptatif

## 🚀 Démo en ligne

[Lien vers l'application Streamlit Cloud](https://forestplotgenerator.streamlit.app/)

## 📋 Prérequis

- Python 3.8 ou supérieur
- Fichier de données avec au minimum 5 colonnes :
  - Catégorie/Effet (ex: effets indésirables, biomarqueurs)
  - Groupe (ex: traitement A, traitement B)
  - Taux d'incidence (TI)
  - Intervalle de confiance inférieur (IC95_min)
  - Intervalle de confiance supérieur (IC95_max)

## 🛠️ Installation

### Installation locale

1. **Clonez le repository**
```bash
git clone https://github.com/SAAHMATHWORKS/forest_plot_generator.git
cd forest-plot-generator
```

2. **Créez un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installez les dépendances**
```bash
pip install -r requirements.txt
```

4. **Lancez l'application**
```bash
streamlit run forest_plot.py
```

5. **Ouvrez votre navigateur**
```
http://localhost:8501

```

## 📦 Dépendances

```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
numpy>=1.24.0
openpyxl>=3.1.0
kaleido==0.2.1  # Optionnel pour export PNG/SVG
```

## 📖 Guide d'utilisation

### 1️⃣ Importation des données

- Cliquez sur **"Choisissez un fichier CSV ou Excel"**
- Sélectionnez votre fichier
- Prévisualisez vos données

### 2️⃣ Configuration des colonnes

Associez chaque colonne de votre fichier aux variables requises :
- **Catégorie/Effet** : Variable principale (ex: type d'effet indésirable)
- **Groupe** : Variable de comparaison (ex: groupes de traitement)
- **TI** : Taux d'incidence ou mesure d'effet
- **IC95_min** : Borne inférieure de l'intervalle de confiance
- **IC95_max** : Borne supérieure de l'intervalle de confiance

### 3️⃣ Personnalisation

Dans la barre latérale, ajustez :
- **Filtres** : Sélectionnez les catégories et groupes à afficher
- **Dimensions** : Hauteur et largeur du graphique
- **Ligne de référence** : Valeur de comparaison (défaut: 1.0)
- **Thème de couleurs** : 5 palettes disponibles
- **Style des marqueurs** : Taille et forme

### 4️⃣ Export

Téléchargez votre graphique en :
- **HTML** : Format interactif (recommandé)
- **PNG** : Image haute résolution
- **SVG** : Format vectoriel éditable

## 📊 Format des données

### Exemple de structure CSV

```csv
Effet,Traitement,TI,IC95_min,IC95_max
Nausées,Placebo,0.15,0.12,0.18
Nausées,Médicament A,0.25,0.21,0.29
Nausées,Médicament B,0.20,0.16,0.24
Fatigue,Placebo,0.30,0.26,0.34
Fatigue,Médicament A,0.35,0.31,0.39
Fatigue,Médicament B,0.28,0.24,0.32
```

### Exemple Excel

| Effet    | Traitement   | TI   | IC95_min | IC95_max |
|----------|-------------|------|----------|----------|
| Nausées  | Placebo     | 0.15 | 0.12     | 0.18     |
| Nausées  | Médicament A| 0.25 | 0.21     | 0.29     |
| Fatigue  | Placebo     | 0.30 | 0.26     | 0.34     |

## 🎨 Thèmes de couleurs disponibles

- **Classique** : Palette standard pour publications scientifiques
- **Médical** : Couleurs professionnelles pour études cliniques
- **Moderne** : Design contemporain et vibrant
- **Pastel** : Tons doux et élégants
- **Vibrant** : Couleurs vives pour présentations

## 📈 Interprétation du Forest Plot

- **Points** : Représentent le taux d'incidence estimé
- **Barres horizontales** : Intervalles de confiance à 95%
- **Ligne verticale noire** : Valeur de référence (généralement 1.0)
- **Zone verte** : TI < référence (effet favorable/protecteur)
- **Zone rouge** : TI > référence (effet défavorable/risque accru)

### Signification statistique

Un intervalle de confiance qui **ne croise pas** la ligne de référence indique une différence statistiquement significative (p < 0.05).

## 🐛 Résolution des problèmes

### Erreur lors de l'import du fichier

**Problème** : "Erreur lors de la lecture du fichier"

**Solutions** :
- Vérifiez que votre fichier n'est pas corrompu
- Assurez-vous que l'encodage est UTF-8
- Pour Excel, vérifiez qu'aucune cellule fusionnée n'existe

### Erreur d'export PNG/SVG

**Problème** : "RuntimeError" lors du téléchargement PNG

**Solutions** :
- Utilisez l'export HTML (toujours fonctionnel)
- Utilisez le bouton 📷 en haut à droite du graphique
- Installez Kaleido : `pip install kaleido==0.2.1`

### Données manquantes

**Problème** : "X lignes supprimées en raison de valeurs manquantes"

**Solutions** :
- Vérifiez les cellules vides dans votre fichier
- Assurez-vous que les colonnes numériques contiennent des nombres
- Supprimez les lignes incomplètes avant l'import

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Committez vos changements (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Pushez vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👤 Auteur

**Thibaut SAAH**

- GitHub: [@votre-username](https://github.com/SAAHMATHWORKS)
- LinkedIn: [Votre profil](https://www.linkedin.com/in/thibaut-saah) 

## 🙏 Remerciements

- [Streamlit](https://streamlit.io/) - Framework d'application web
- [Plotly](https://plotly.com/) - Bibliothèque de visualisation
- [Pandas](https://pandas.pydata.org/) - Manipulation de données

## 📞 Support

Pour toute question ou problème :
- Ouvrez une [issue](https://github.com/SAAHMATHWORKS/forest_plot_generator/issues)
- Contactez-moi via [email](mailto:saahthibaut@gmail.com.com)

---

⭐ Si ce projet vous est utile, n'hésitez pas à lui donner une étoile !

**Développé avec ❤️ en Python**