import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Forest Plot Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2C3E50;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #3498DB;
        margin-bottom: 2rem;
    }
    
    .upload-section {
        background-color: #E8F4F8;
        padding: 2rem;
        border-radius: 10px;
        border: 2px dashed #3498DB;
        margin-bottom: 2rem;
    }
    
    .config-section {
        background-color: #FFF9E6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #F39C12;
        margin-bottom: 2rem;
    }
    
    .metric-container {
        background-color: #F8F9FA;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #3498DB;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">📊 Générateur de Forest Plot</h1>', unsafe_allow_html=True)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'column_mapping' not in st.session_state:
    st.session_state.column_mapping = {}

# Section 1: File Upload
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown("## 📂 Étape 1 : Importation des données")

col1, col2 = st.columns([3, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Choisissez un fichier CSV ou Excel",
        type=['csv', 'xlsx', 'xls'],
        help="Format requis : colonnes pour les groupes, taux d'incidence (TI), IC95_min, IC95_max, et une colonne pour les catégories/effets"
    )

with col2:
    st.markdown("**📋 Colonnes requises :**")
    st.markdown("""
    - Catégorie/Effet
    - Groupe
    - TI
    - IC95_min
    - IC95_max
    """)

if uploaded_file is not None:
    try:
        # Read file
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'csv':
            df_raw = pd.read_csv(uploaded_file)
        elif file_extension in ['xlsx', 'xls']:
            df_raw = pd.read_excel(uploaded_file)
        
        st.success(f"✅ Fichier chargé : **{uploaded_file.name}** ({len(df_raw)} lignes, {len(df_raw.columns)} colonnes)")
        
        # Display preview
        with st.expander("👀 Aperçu des données (10 premières lignes)"):
            st.dataframe(df_raw.head(10), use_container_width=True)
        
        st.session_state.df = df_raw
        
    except Exception as e:
        st.error(f"❌ Erreur lors de la lecture du fichier : {str(e)}")
        st.stop()

st.markdown('</div>', unsafe_allow_html=True)

# Stop if no data
if st.session_state.df is None:
    st.info("👆 Veuillez uploader un fichier pour commencer")
    st.stop()

df_raw = st.session_state.df

# Section 2: Column Mapping
st.markdown('<div class="config-section">', unsafe_allow_html=True)
st.markdown("## 🔧 Étape 2 : Configuration des colonnes")

st.markdown("**Associez les colonnes de votre fichier aux variables du Forest Plot :**")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    category_col = st.selectbox(
        "📌 Colonne Catégorie/Effet",
        options=df_raw.columns.tolist(),
        help="Colonne contenant les catégories ou effets indésirables",
        key="category_col"
    )

with col2:
    group_col = st.selectbox(
        "👥 Colonne Groupe",
        options=df_raw.columns.tolist(),
        index=min(1, len(df_raw.columns)-1),
        help="Colonne contenant les groupes de traitement",
        key="group_col"
    )

with col3:
    ti_col = st.selectbox(
        "📈 Colonne TI",
        options=df_raw.columns.tolist(),
        index=min(2, len(df_raw.columns)-1),
        help="Taux d'incidence",
        key="ti_col"
    )

with col4:
    ic_min_col = st.selectbox(
        "📉 Colonne IC95_min",
        options=df_raw.columns.tolist(),
        index=min(3, len(df_raw.columns)-1),
        help="Borne inférieure de l'intervalle de confiance à 95%",
        key="ic_min_col"
    )

with col5:
    ic_max_col = st.selectbox(
        "📊 Colonne IC95_max",
        options=df_raw.columns.tolist(),
        index=min(4, len(df_raw.columns)-1),
        help="Borne supérieure de l'intervalle de confiance à 95%",
        key="ic_max_col"
    )

# Validate mapping
if len(set([category_col, group_col, ti_col, ic_min_col, ic_max_col])) != 5:
    st.error("❌ Erreur : Vous devez sélectionner des colonnes différentes pour chaque variable")
    st.stop()

# Create standardized dataframe
try:
    df = pd.DataFrame({
        'Category': df_raw[category_col].astype(str),
        'Group': df_raw[group_col].astype(str),
        'TI': pd.to_numeric(df_raw[ti_col], errors='coerce'),
        'IC95_min': pd.to_numeric(df_raw[ic_min_col], errors='coerce'),
        'IC95_max': pd.to_numeric(df_raw[ic_max_col], errors='coerce')
    })
    
    # Remove rows with NaN values
    df_clean = df.dropna()
    
    if len(df_clean) < len(df):
        st.warning(f"⚠️ {len(df) - len(df_clean)} ligne(s) supprimée(s) en raison de valeurs manquantes ou invalides")
    
    df = df_clean
    
    # Calculate errors
    df['Error_Low'] = df['TI'] - df['IC95_min']
    df['Error_High'] = df['IC95_max'] - df['TI']
    
    st.success(f"✅ Configuration validée ! {len(df)} points de données prêts à être visualisés")
    
except Exception as e:
    st.error(f"❌ Erreur lors de la conversion des données : {str(e)}")
    st.stop()

st.markdown('</div>', unsafe_allow_html=True)

# Section 3: Filters and Configuration
st.markdown("## 🎛️ Étape 3 : Personnalisation du graphique")

# Sidebar for controls
st.sidebar.title("⚙️ Paramètres du graphique")
st.sidebar.markdown("---")

# Filters
st.sidebar.subheader("📊 Filtres de données")

categories_available = sorted(df['Category'].unique())
selected_categories = st.sidebar.multiselect(
    f"Sélectionner les {category_col} :",
    options=categories_available,
    default=categories_available,
    help=f"Choisissez les {category_col} à afficher"
)

groups_available = sorted(df['Group'].unique())
selected_groups = st.sidebar.multiselect(
    f"Sélectionner les {group_col} :",
    options=groups_available,
    default=groups_available,
    help=f"Choisissez les {group_col} à afficher"
)

# Plot dimensions
st.sidebar.markdown("---")
st.sidebar.subheader("📐 Dimensions")
plot_height = st.sidebar.slider("Hauteur (px)", 400, 1500, 900, 50)
plot_width = st.sidebar.slider("Largeur (px)", 800, 2000, 1300, 50)

# Reference line
st.sidebar.markdown("---")
st.sidebar.subheader("📍 Ligne de référence")
reference_line = st.sidebar.number_input("Valeur de référence", value=1.0, step=0.1)
show_zones = st.sidebar.checkbox("Afficher les zones colorées", value=True)

# Color theme
st.sidebar.markdown("---")
st.sidebar.subheader("🎨 Thème de couleurs")
color_theme = st.sidebar.selectbox(
    "Palette de couleurs :",
    options=["Classique", "Médical", "Moderne", "Pastel", "Vibrant"],
    index=0
)

color_palettes = {
    "Classique": ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'],
    "Médical": ['#2E86C1', '#E74C3C', '#27AE60', '#F39C12', '#8E44AD', '#16A085', '#E67E22', '#95A5A6'],
    "Moderne": ['#6C5CE7', '#FD79A8', '#00CEC9', '#FDCB6E', '#E17055', '#74B9FF', '#A29BFE', '#55EFC4'],
    "Pastel": ['#A8DADC', '#F1FAEE', '#E63946', '#457B9D', '#F4A261', '#2A9D8F', '#E9C46A', '#264653'],
    "Vibrant": ['#FF006E', '#FB5607', '#FFBE0B', '#8338EC', '#3A86FF', '#06FFA5', '#FF1654', '#FFB400']
}

selected_colors = color_palettes[color_theme]
group_colors = {group: selected_colors[i % len(selected_colors)] 
                for i, group in enumerate(groups_available)}

# Marker style
st.sidebar.markdown("---")
st.sidebar.subheader("🔷 Style des marqueurs")
marker_size = st.sidebar.slider("Taille des marqueurs", 4, 16, 10, 1)
marker_symbol = st.sidebar.selectbox(
    "Forme des marqueurs :",
    options=["circle", "diamond", "square", "cross"],
    index=0
)

# Filter data
filtered_df = df[
    (df['Group'].isin(selected_groups)) & 
    (df['Category'].isin(selected_categories))
].copy()

# Data summary
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric(f"{category_col} sélectionnées", len(selected_categories))
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric(f"{group_col} sélectionnés", len(selected_groups))
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Points de données", len(filtered_df))
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    if len(filtered_df) > 0:
        st.metric("TI Max", f"{filtered_df['TI'].max():.3f}")
    else:
        st.metric("TI Max", "N/A")
    st.markdown('</div>', unsafe_allow_html=True)

# Create Forest Plot
def create_forest_plot(data, height, width, colors, ref_line, show_bg_zones):
    if data.empty:
        return None
    
    unique_categories = data['Category'].unique()
    n_categories = len(unique_categories)
    unique_groups = data['Group'].unique()
    n_groups = len(unique_groups)
    
    # Calculate y positions
    y_positions = []
    y_labels = []
    
    for idx, row in data.iterrows():
        category = row['Category']
        group = row['Group']
        
        category_idx = list(unique_categories).index(category)
        group_idx = list(unique_groups).index(group)
        
        spacing = n_groups + 1
        base_pos = (n_categories - category_idx - 1) * spacing
        y_pos = base_pos - group_idx * 0.8
        y_positions.append(y_pos)
        
        if group_idx == 0:
            y_labels.append(category)
        else:
            y_labels.append('')
    
    data = data.copy()
    data['y_pos'] = y_positions[:len(data)]
    
    # X-axis range
    x_min = data['IC95_min'].min()
    x_max = data['IC95_max'].max()
    x_buffer = (x_max - x_min) * 0.1
    x_range_min = max(0, x_min - x_buffer)
    x_range_max = x_max + x_buffer
    
    # Create figure
    fig = go.Figure()
    
    # Background zones
    if show_bg_zones:
        fig.add_vrect(
            x0=x_range_min, x1=ref_line,
            fillcolor="lightgreen", opacity=0.15,
            layer="below", line_width=0,
        )
        fig.add_vrect(
            x0=ref_line, x1=x_range_max,
            fillcolor="lightcoral", opacity=0.15,
            layer="below", line_width=0,
        )
    
    # Add traces for each group
    for group in unique_groups:
        if group not in selected_groups:
            continue
            
        group_data = data[data['Group'] == group]
        if group_data.empty:
            continue
        
        error_low = np.maximum(group_data['Error_Low'], 0)
        error_high = np.maximum(group_data['Error_High'], 0)
        
        fig.add_trace(go.Scatter(
            x=group_data['TI'],
            y=group_data['y_pos'],
            mode='markers',
            marker=dict(
                color=colors.get(group, '#1f77b4'),
                size=marker_size,
                symbol=marker_symbol,
                line=dict(width=1.5, color='black')
            ),
            error_x=dict(
                type='data',
                symmetric=False,
                array=error_high,
                arrayminus=error_low,
                color=colors.get(group, '#1f77b4'),
                thickness=2.5,
                width=4
            ),
            name=group,
            hovertemplate=f'<b>{group}</b><br>' +
                         f'{category_col}: ' + '%{customdata[0]}<br>' +
                         'TI: %{x:.3f}<br>' +
                         'IC 95%: [%{customdata[1]:.3f}, %{customdata[2]:.3f}]<extra></extra>',
            customdata=np.column_stack((group_data['Category'],
                                       group_data['IC95_min'],
                                       group_data['IC95_max']))
        ))
    
    # Reference line
    fig.add_vline(x=ref_line, line_dash="dash", line_color="black", line_width=2.5,
                  annotation_text=f"Référence = {ref_line}", annotation_position="top", annotation_font=dict(color='black', size=13))
    
    # Layout
    fig.update_layout(
        title=dict(
            text=f'Forest Plot - {category_col} par {group_col}',
            x=0.5,
            xanchor='center',
            font=dict(size=20, color="#080D13", family="Arial Black")
        ),
        xaxis=dict(
            title=dict(text='Taux d\'incidence (IC 95%)', font=dict(size=15, color='black')),
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            range=[x_range_min, x_range_max],
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='black',
            tickfont=dict(color='black') 
        ),
        yaxis=dict(
            title=dict(text=category_col, font=dict(size=15, color='black')),
            tickmode='array',
            tickvals=[pos for i, pos in enumerate(y_positions[:len(data)]) if i < len(y_labels) and y_labels[i] != ''],
            ticktext=[label for label in y_labels if label != ''],
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            range=[-1.5, max(y_positions[:len(data)]) + 1.5] if y_positions else [0, 1],
            tickfont=dict(color='black') 
        ),
        height=height,
        width=width,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="right",
            x=1.15,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="black",
            borderwidth=1,
            font=dict(color='black') 
        ),
        margin=dict(l=250, r=200, t=120, b=80),
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='closest'
    )
    
    return fig

# Generate plot
st.markdown("---")
st.markdown("## 📊 Forest Plot")

if len(selected_groups) > 0 and len(selected_categories) > 0:
    fig = create_forest_plot(filtered_df, plot_height, plot_width, group_colors, reference_line, show_zones)
    
    if fig:
        st.plotly_chart(fig, use_container_width=True)
        
        # Download options
        st.markdown("### 💾 Téléchargement")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Télécharger HTML", type="primary", use_container_width=True):
                fig.write_html("forest_plot.html")
                st.success("✅ Sauvegardé : forest_plot.html")
        
        with col2:
            if st.button("📥 Télécharger PNG", use_container_width=True):
                fig.write_image("forest_plot.png", width=plot_width, height=plot_height, scale=2)
                st.success("✅ Sauvegardé : forest_plot.png")
        
        with col3:
            if st.button("📥 Télécharger SVG", use_container_width=True):
                fig.write_image("forest_plot.svg", width=plot_width, height=plot_height)
                st.success("✅ Sauvegardé : forest_plot.svg")
    else:
        st.warning("⚠️ Impossible de générer le graphique")
else:
    st.warning("⚠️ Veuillez sélectionner au moins une catégorie et un groupe")

# Data table
st.markdown("---")
st.markdown("### 📋 Tableau des données filtrées")

if st.checkbox("Afficher le tableau détaillé"):
    display_df = filtered_df[['Category', 'Group', 'TI', 'IC95_min', 'IC95_max']].copy()
    display_df.columns = [category_col, group_col, 'TI', 'IC95_min', 'IC95_max']
    st.dataframe(display_df.round(3), use_container_width=True, height=400)
    
    # Export filtered data
    if st.button("📥 Télécharger les données filtrées (CSV)"):
        display_df.to_csv("donnees_filtrees.csv", index=False)
        st.success("✅ Données sauvegardées : donnees_filtrees.csv")

# Statistics summary
if st.checkbox("Afficher les statistiques"):
    st.markdown("### 📈 Statistiques descriptives")
    
    stats_df = filtered_df.groupby('Group').agg({
        'TI': ['count', 'mean', 'median', 'min', 'max', 'std'],
        'IC95_min': 'mean',
        'IC95_max': 'mean'
    }).round(3)
    
    st.dataframe(stats_df, use_container_width=True)

# Help section
st.markdown("---")
with st.expander("ℹ️ Guide d'utilisation et interprétation"):
    st.markdown("""
    ### 📖 Comment utiliser cet outil ?
    
    1. **Importez vos données** : Fichier CSV ou Excel avec au minimum 5 colonnes
    2. **Configurez les colonnes** : Associez chaque colonne à sa variable (catégorie, groupe, TI, IC95_min, IC95_max)
    3. **Personnalisez** : Utilisez les filtres et options dans la barre latérale
    4. **Exportez** : Téléchargez votre graphique en HTML, PNG ou SVG
    
    ### 📊 Interprétation du Forest Plot
    
    - **Points** : Représentent le taux d'incidence (TI)
    - **Barres horizontales** : Intervalles de confiance à 95%
    - **Ligne verticale** : Valeur de référence (généralement 1.0)
    - **Zone verte** : TI < référence (effet favorable)
    - **Zone rouge** : TI > référence (effet défavorable)
    
    ### 💡 Conseils
    
    - Plus l'intervalle de confiance est étroit, plus l'estimation est précise
    - Un IC95 qui ne croise pas la ligne de référence indique une différence statistiquement significative
    - Comparez les groupes pour identifier les tendances et différences
    """)

st.markdown("---")
st.markdown("*Développé par Jasmine Kadji avec Streamlit et Plotly* 🚀")