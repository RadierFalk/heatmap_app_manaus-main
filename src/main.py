import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__))) 

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import folium
from folium.plugins import HeatMap
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from meteostat import Point, Hourly, Daily
import geopandas as gpd

app = Flask(__name__)
Bootstrap(app)

# Coordenadas centrais de Manaus
MANAUS_LAT = -3.1190
MANAUS_LON = -60.0217

def get_weather_data(start_date, end_date, factor='temp'):
    manaus = Point(MANAUS_LAT, MANAUS_LON)
    
    if factor == 'humidity':
        data = Hourly(manaus, start_date, end_date)
        data = data.fetch()
        data = data.resample('D').mean()
        selected_factor = 'rhum'
    elif factor == 'temp':
        data = Daily(manaus, start_date, end_date)
        data = data.fetch()
        selected_factor = 'tavg'
    elif factor == 'precipitation':
        data = Daily(manaus, start_date, end_date)
        data = data.fetch()
        selected_factor = 'prcp'
    else:
        # fallback se o fator for inválido
        data = Daily(manaus, start_date, end_date)
        data = data.fetch()
        selected_factor = 'tavg'

    # Remover nulos
    data = data.dropna(subset=[selected_factor])

    return data, selected_factor

def generate_heatmap_data(weather_data, selected_factor, num_points=500):
    if weather_data.empty:
        avg_value = 25
    else:
        avg_value = weather_data[selected_factor].mean()
    
    np.random.seed(42)
    
    # Definir limites usando as coordenadas fornecidas
    # Assumindo que o primeiro valor em cada par é a coordenada relevante
    lat_min = -3.157431
    lat_max = -2.950733
    lon_min = -60.110890
    lon_max = -59.877197
    
    # Coordenada de base fornecida
    BASE_LAT = -3.1190
    BASE_LON = -60.0217
    
    # Gerar coordenadas aleatórias dentro dos novos limites
    lats = np.random.uniform(lat_min, lat_max, num_points)
    lons = np.random.uniform(lon_min, lon_max, num_points)
    
    values = []
    
    for lat, lon in zip(lats, lons):
        # Calcular distância da coordenada de base
        dist = ((lat - BASE_LAT) ** 2 + (lon - BASE_LON) ** 2) ** 0.5
        
        # Áreas mais próximas do centro são mais quentes (ilha de calor)
        # Quanto menor a distância, maior o valor (para temperatura)
        if selected_factor == 'tavg':
            # Para temperatura: centro mais quente
            value = avg_value * (1 + (0.2 * (1 - min(dist * 20, 1))))
        elif selected_factor == 'rhum':
            # Para umidade: centro menos úmido
            value = avg_value * (1 - (0.2 * (1 - min(dist * 20, 1))))
        else:
            # Para outros fatores
            value = avg_value * (1 + 0.2 * np.random.randn())
        
        values.append(value)
    
    # Criar DataFrame com os pontos e valores
    heatmap_data = pd.DataFrame({
        'lat': lats,
        'lon': lons,
        'value': values
    })
    
    return heatmap_data
# Função para identificar locais potenciais para intervenções sustentáveis
def identify_intervention_locations(heatmap_data, factor='temp', threshold_percentile=90):
    # Para temperatura, queremos os locais mais quentes
    # Para umidade, queremos os locais menos úmidos
    
    if factor == 'temp':
        # Locais mais quentes (acima do percentil definido)
        threshold = np.percentile(heatmap_data['value'], threshold_percentile)
        potential_locations = heatmap_data[heatmap_data['value'] >= threshold]
    elif factor == 'humidity':
        # Locais menos úmidos (abaixo do percentil inverso)
        threshold = np.percentile(heatmap_data['value'], 100 - threshold_percentile)
        potential_locations = heatmap_data[heatmap_data['value'] <= threshold]
    else:
        # Para outros fatores, usamos o mesmo critério da temperatura
        threshold = np.percentile(heatmap_data['value'], threshold_percentile)
        potential_locations = heatmap_data[heatmap_data['value'] >= threshold]
    
    # Selecionar até 10 locais para intervenção
    if len(potential_locations) > 10:
        potential_locations = potential_locations.sample(10)
    
    return potential_locations

@app.route('/')
def index():
    # Criar mapa base centrado em Manaus
    m = folium.Map(location=[MANAUS_LAT, MANAUS_LON], zoom_start=12,
                  tiles='CartoDB positron')
    
    # Adicionar marcador para o centro de Manaus
    folium.Marker(
        [MANAUS_LAT, MANAUS_LON],
        popup='Manaus, AM',
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)
    
    # Converter para HTML
    map_html = m._repr_html_()
    
    # Obter data atual e data de um mês atrás para valores padrão
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    return render_template('index.html', 
                          map_html=map_html,
                          start_date=start_date.strftime('%Y-%m-%d'),
                          end_date=end_date.strftime('%Y-%m-%d'))

@app.route('/generate_heatmap', methods=['POST'])
def generate_heatmap():
    # Obter parâmetros do formulário
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    factor = request.form.get('factor', 'temp')
    
    # Converter strings para objetos datetime
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Obter dados meteorológicos
    weather_data, selected_factor = get_weather_data(start_date, end_date, factor)
    
    # Gerar dados para o mapa de calor
    heatmap_data = generate_heatmap_data(weather_data, selected_factor)
    
    # Identificar locais potenciais para intervenção
    intervention_locations = identify_intervention_locations(heatmap_data, factor)
    
    # Criar mapa base
    m = folium.Map(location=[MANAUS_LAT, MANAUS_LON], zoom_start=12,
                  tiles='CartoDB positron')
    
    # Adicionar camada de mapa de calor
    HeatMap(
        data=heatmap_data[['lat', 'lon', 'value']].values.tolist(),
        radius=15,
        max_zoom=13,
        gradient={0.4: 'blue', 0.65: 'lime', 0.8: 'yellow', 1: 'red'}
    ).add_to(m)
    
    # Adicionar marcadores para locais de intervenção potenciais
    for idx, row in intervention_locations.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f'Local potencial para intervenção<br>Valor: {row["value"]:.2f}',
            icon=folium.Icon(color='green', icon='leaf')
        ).add_to(m)
    
    # Adicionar legenda
    title_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 250px; height: 120px; 
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color: white; padding: 10px;
                border-radius: 5px;">
        <b>Legenda:</b><br>
        <i class="fa fa-map-marker fa-2x" style="color:red"></i> Áreas críticas (mais quentes)<br>
        <i class="fa fa-leaf fa-2x" style="color:green"></i> Locais sugeridos para intervenção<br>
        <div style="background: linear-gradient(to right, blue, lime, yellow, red); 
                    height: 10px; margin-top: 5px;"></div>
        <span style="float: left;">Menor</span>
        <span style="float: right;">Maior</span>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Converter para HTML
    map_html = m._repr_html_()
    
    # Calcular estatísticas para exibição
    stats = {
        'periodo': f"{start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}",
        'fator': {
            'temp': 'Temperatura',
            'humidity': 'Umidade',
            'precipitation': 'Precipitação'
        }.get(factor, 'Temperatura'),
        'num_locais': len(intervention_locations),
        'valor_medio': weather_data[selected_factor].mean() if not weather_data.empty else 'N/A',
        'valor_max': weather_data[selected_factor].max() if not weather_data.empty else 'N/A',
        'valor_min': weather_data[selected_factor].min() if not weather_data.empty else 'N/A'
    }
    
    return render_template('heatmap_result.html', 
                          map_html=map_html,
                          stats=stats,
                          start_date=start_date.strftime('%Y-%m-%d'),
                          end_date=end_date.strftime('%Y-%m-%d'),
                          factor=factor)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
