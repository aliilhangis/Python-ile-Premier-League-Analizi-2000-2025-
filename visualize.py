import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import numpy as np
from matplotlib import patheffects as pe
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import mplcursors

# Stil ayarları
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Veritabanı bağlantısı
conn = sqlite3.connect('epl.db')

# Sezonlara göre gol istatistikleri
goals_query = """
SELECT 
    Season as season,
    AVG(FullTimeHomeGoals + FullTimeAwayGoals) as avg_goals_per_match,
    AVG(FullTimeHomeGoals) as avg_home_goals,
    AVG(FullTimeAwayGoals) as avg_away_goals,
    AVG(HalfTimeHomeGoals + HalfTimeAwayGoals) as avg_first_half_goals,
    AVG((FullTimeHomeGoals + FullTimeAwayGoals) - (HalfTimeHomeGoals + HalfTimeAwayGoals)) as avg_second_half_goals
FROM matches
GROUP BY Season
ORDER BY Season
"""

goals_df = pd.read_sql_query(goals_query, conn)

# Görselleştirme ayarları
plt.rcParams['figure.figsize'] = (15, 8)
plt.rcParams['font.size'] = 12
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.facecolor'] = '#f0f0f0'
plt.rcParams['figure.facecolor'] = 'white'

# 1. Maç başına ortalama goller - Gradient arka plan ve gölgeli çizgi
plt.figure()
ax = plt.gca()
ax.set_facecolor('#f8f9fa')
plt.plot(goals_df['season'], goals_df['avg_goals_per_match'], 
         marker='o', linewidth=3, markersize=8, color='#2ecc71',
         path_effects=[pe.Stroke(linewidth=5, foreground='#27ae60'), pe.Normal()])
plt.fill_between(goals_df['season'], goals_df['avg_goals_per_match'], 
                 alpha=0.2, color='#2ecc71')
plt.title('Sezonlara Göre Maç Başına Ortalama Gol Sayısı', 
          pad=20, fontsize=14, fontweight='bold')
plt.xlabel('Sezon', fontsize=12)
plt.ylabel('Ortalama Gol Sayısı', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('goals_per_season.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Ev sahibi ve deplasman golleri - Gradient renkli çizgiler
plt.figure()
ax = plt.gca()
ax.set_facecolor('#f8f9fa')
colors = ['#e74c3c', '#3498db']
for i, (col, label) in enumerate(zip(['avg_home_goals', 'avg_away_goals'], 
                                   ['Ev Sahibi', 'Deplasman'])):
    plt.plot(goals_df['season'], goals_df[col], marker='o', linewidth=3, 
             markersize=8, label=label, color=colors[i],
             path_effects=[pe.Stroke(linewidth=5, foreground='#c0392b' if i==0 else '#2980b9'), 
                         pe.Normal()])
    plt.fill_between(goals_df['season'], goals_df[col], alpha=0.2, color=colors[i])
plt.title('Sezonlara Göre Ev Sahibi ve Deplasman Golleri', 
          pad=20, fontsize=14, fontweight='bold')
plt.xlabel('Sezon', fontsize=12)
plt.ylabel('Ortalama Gol Sayısı', fontsize=12)
plt.xticks(rotation=45)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('home_away_goals.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. İlk yarı ve ikinci yarı golleri - Gradient renkli çizgiler
plt.figure()
ax = plt.gca()
ax.set_facecolor('#f8f9fa')
colors = ['#f1c40f', '#9b59b6']
for i, (col, label) in enumerate(zip(['avg_first_half_goals', 'avg_second_half_goals'], 
                                   ['İlk Yarı', 'İkinci Yarı'])):
    plt.plot(goals_df['season'], goals_df[col], marker='o', linewidth=3, 
             markersize=8, label=label, color=colors[i],
             path_effects=[pe.Stroke(linewidth=5, foreground='#f39c12' if i==0 else '#8e44ad'), 
                         pe.Normal()])
    plt.fill_between(goals_df['season'], goals_df[col], alpha=0.2, color=colors[i])
plt.title('Sezonlara Göre İlk Yarı ve İkinci Yarı Golleri', 
          pad=20, fontsize=14, fontweight='bold')
plt.xlabel('Sezon', fontsize=12)
plt.ylabel('Ortalama Gol Sayısı', fontsize=12)
plt.xticks(rotation=45)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('half_time_goals.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Gol dağılımı analizi - Gradient renkli yığın grafik
goals_dist_query = """
SELECT 
    Season as season,
    SUM(CASE WHEN (FullTimeHomeGoals + FullTimeAwayGoals) = 0 THEN 1 ELSE 0 END) as zero_goals,
    SUM(CASE WHEN (FullTimeHomeGoals + FullTimeAwayGoals) = 1 THEN 1 ELSE 0 END) as one_goal,
    SUM(CASE WHEN (FullTimeHomeGoals + FullTimeAwayGoals) = 2 THEN 1 ELSE 0 END) as two_goals,
    SUM(CASE WHEN (FullTimeHomeGoals + FullTimeAwayGoals) = 3 THEN 1 ELSE 0 END) as three_goals,
    SUM(CASE WHEN (FullTimeHomeGoals + FullTimeAwayGoals) >= 4 THEN 1 ELSE 0 END) as four_plus_goals,
    COUNT(*) as total_matches
FROM matches
GROUP BY Season
ORDER BY Season
"""

goals_dist_df = pd.read_sql_query(goals_dist_query, conn)

# Yüzdeleri hesapla
for col in ['zero_goals', 'one_goal', 'two_goals', 'three_goals', 'four_plus_goals']:
    goals_dist_df[col] = (goals_dist_df[col] / goals_dist_df['total_matches']) * 100

# Gol dağılımı grafiği
plt.figure(figsize=(15, 8))
ax = plt.gca()
ax.set_facecolor('#f8f9fa')
colors = ['#e74c3c', '#e67e22', '#f1c40f', '#2ecc71', '#3498db']
goals_dist_df.plot(x='season', 
                  y=['zero_goals', 'one_goal', 'two_goals', 'three_goals', 'four_plus_goals'],
                  kind='bar', stacked=True, color=colors, ax=ax)
plt.title('Sezonlara Göre Gol Dağılımı (%)', pad=20, fontsize=14, fontweight='bold')
plt.xlabel('Sezon', fontsize=12)
plt.ylabel('Maç Yüzdesi', fontsize=12)
plt.xticks(rotation=45)
plt.legend(['0 Gol', '1 Gol', '2 Gol', '3 Gol', '4+ Gol'], fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('goals_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Yüksek skorlu maçlar analizi - Gradient arka plan ve gölgeli çizgi
high_scoring_query = """
SELECT 
    Season as season,
    SUM(CASE WHEN (FullTimeHomeGoals + FullTimeAwayGoals) >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as high_scoring_percentage
FROM matches
GROUP BY Season
ORDER BY Season
"""

high_scoring_df = pd.read_sql_query(high_scoring_query, conn)

plt.figure()
ax = plt.gca()
ax.set_facecolor('#f8f9fa')
plt.plot(high_scoring_df['season'], high_scoring_df['high_scoring_percentage'], 
         marker='o', linewidth=3, markersize=8, color='#e74c3c',
         path_effects=[pe.Stroke(linewidth=5, foreground='#c0392b'), pe.Normal()])
plt.fill_between(high_scoring_df['season'], high_scoring_df['high_scoring_percentage'], 
                 alpha=0.2, color='#e74c3c')
plt.title('Sezonlara Göre Yüksek Skorlu Maç Oranı (4+ Gol)', 
          pad=20, fontsize=14, fontweight='bold')
plt.xlabel('Sezon', fontsize=12)
plt.ylabel('Maç Yüzdesi (%)', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('high_scoring_matches.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. Isı Haritası - Gol Dağılımı
heatmap_query = """
SELECT 
    Season,
    SUM(CASE WHEN FullTimeHomeGoals + FullTimeAwayGoals = 0 THEN 1 ELSE 0 END) as zero_goals,
    SUM(CASE WHEN FullTimeHomeGoals + FullTimeAwayGoals = 1 THEN 1 ELSE 0 END) as one_goal,
    SUM(CASE WHEN FullTimeHomeGoals + FullTimeAwayGoals = 2 THEN 1 ELSE 0 END) as two_goals,
    SUM(CASE WHEN FullTimeHomeGoals + FullTimeAwayGoals = 3 THEN 1 ELSE 0 END) as three_goals,
    SUM(CASE WHEN FullTimeHomeGoals + FullTimeAwayGoals = 4 THEN 1 ELSE 0 END) as four_goals,
    SUM(CASE WHEN FullTimeHomeGoals + FullTimeAwayGoals >= 5 THEN 1 ELSE 0 END) as five_plus_goals
FROM matches
GROUP BY Season
ORDER BY Season
"""

heatmap_df = pd.read_sql_query(heatmap_query, conn)
heatmap_df.set_index('Season', inplace=True)

# Yüzdeleri hesapla
total_matches = heatmap_df.sum(axis=1)
for col in heatmap_df.columns:
    heatmap_df[col] = (heatmap_df[col] / total_matches) * 100

plt.figure(figsize=(15, 8))
sns.heatmap(heatmap_df, annot=True, fmt='.1f', cmap='YlOrRd', 
            cbar_kws={'label': 'Maç Yüzdesi (%)'})
plt.title('Sezonlara Göre Gol Dağılımı Isı Haritası', pad=20, fontsize=14, fontweight='bold')
plt.xlabel('Gol Sayısı', fontsize=12)
plt.ylabel('Sezon', fontsize=12)
plt.tight_layout()
plt.savefig('goals_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# 7. Radar Grafikleri - Takım Performansları
radar_query = """
SELECT 
    HomeTeam as Team,
    AVG(FullTimeHomeGoals) as avg_goals_scored,
    AVG(FullTimeAwayGoals) as avg_goals_conceded,
    AVG(HomeShots) as avg_shots,
    AVG(HomeShotsOnTarget) as avg_shots_on_target,
    AVG(HomeFouls) as avg_fouls,
    AVG(HomeYellowCards + HomeRedCards) as avg_cards
FROM matches
GROUP BY HomeTeam
ORDER BY avg_goals_scored DESC
LIMIT 5
"""

radar_df = pd.read_sql_query(radar_query, conn)

# Verileri normalize et
for col in radar_df.columns[1:]:
    radar_df[col] = (radar_df[col] - radar_df[col].min()) / (radar_df[col].max() - radar_df[col].min())

# Radar grafiği
categories = ['Gol Atma', 'Gol Yeme', 'Şut', 'İsabetli Şut', 'Faul', 'Kart']
fig = go.Figure()

for i, team in enumerate(radar_df['Team']):
    values = radar_df.iloc[i, 1:].values
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=team
    ))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1]
        )),
    showlegend=True,
    title='En İyi 5 Takımın Performans Karşılaştırması',
    font=dict(size=12)
)

fig.write_html('team_radar.html')

# 8. Animasyonlu Grafik - Sezonlara Göre Gol Trendi
animation_query = """
SELECT 
    Season,
    AVG(FullTimeHomeGoals + FullTimeAwayGoals) as avg_goals,
    AVG(FullTimeHomeGoals) as avg_home_goals,
    AVG(FullTimeAwayGoals) as avg_away_goals
FROM matches
GROUP BY Season
ORDER BY Season
"""

animation_df = pd.read_sql_query(animation_query, conn)

fig = px.line(animation_df, x='Season', y=['avg_goals', 'avg_home_goals', 'avg_away_goals'],
              title='Sezonlara Göre Gol Trendi',
              labels={'value': 'Ortalama Gol', 'variable': 'Gol Türü'},
              animation_frame='Season',
              range_y=[0, 4])

fig.update_layout(
    xaxis_title='Sezon',
    yaxis_title='Ortalama Gol',
    legend_title='Gol Türü'
)

fig.write_html('goals_animation.html')

# 9. 3D Görselleştirme - Gol ve Şut İlişkisi
d3_query = """
SELECT 
    Season,
    AVG(FullTimeHomeGoals + FullTimeAwayGoals) as avg_goals,
    AVG(HomeShots + AwayShots) as avg_shots
FROM matches
GROUP BY Season
ORDER BY Season
"""

d3_df = pd.read_sql_query(d3_query, conn)

# Sezonları sayısal değerlere dönüştür
d3_df['Season_Num'] = range(len(d3_df))

# 3D çizgi grafiği oluştur
fig = go.Figure()

# Ana çizgi
fig.add_trace(go.Scatter3d(
    x=d3_df['avg_goals'],
    y=d3_df['avg_shots'],
    z=d3_df['Season_Num'],
    mode='lines',
    line=dict(
        color='#2ecc71',
        width=4
    ),
    name='Trend'
))

# Noktalar
fig.add_trace(go.Scatter3d(
    x=d3_df['avg_goals'],
    y=d3_df['avg_shots'],
    z=d3_df['Season_Num'],
    mode='markers',
    marker=dict(
        size=8,
        color=d3_df['Season_Num'],
        colorscale='Viridis',
        opacity=0.8
    ),
    text=d3_df['Season'],
    name='Sezonlar'
))

# Grafik düzenini güncelle
fig.update_layout(
    title=dict(
        text='Sezonlara Göre Gol ve Şut Trendi',
        font=dict(size=20),
        y=0.95
    ),
    scene=dict(
        xaxis_title='Ortalama Gol',
        yaxis_title='Ortalama Şut',
        zaxis_title='Sezon',
        camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.5)
        )
    ),
    showlegend=True,
    width=1000,
    height=800
)

fig.write_html('goals_shots_3d.html')

print("Tüm grafikler başarıyla oluşturuldu!") 