"""
SmartPath+ - Sistema de Optimización de Rutas Ferroviarias del Reino Unido
Universidad Peruana de Ciencias Aplicadas
Curso: Complejidad Algorítmica

Aplicación Streamlit para planificación de viajes en tren
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from graph_algorithms import RailwayGraph
import time



# Configuración de la página
st.set_page_config(
    page_title="SmartPath+ | Optimización de Rutas Ferroviarias",
    page_icon="🚂",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .route-step {
        background-color: #e8f4f8;
        padding: 0.8rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
        border-radius: 0.3rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Carga los datos y construye el grafo"""
    # Cargar estaciones
    stations_df = pd.read_csv('data/stations_with_city.csv')
    
    # Limpiar valores NaN en la columna city
    stations_df['city'] = stations_df['city'].fillna('Unknown')
    
    # Cargar conexiones
    edges_df = pd.read_csv('data/edges.csv')
    
    # Construir grafo
    graph = RailwayGraph()
    
    # Añadir estaciones al grafo
    for _, row in stations_df.iterrows():
        graph.add_station(
            code=row['code'],
            name=row['name'],
            city=row['city'],
            lat=row['lat'],
            lon=row['long']
        )
    
    # Añadir aristas
    for _, row in edges_df.iterrows():
        graph.add_edge(
            source=row['source'],
            target=row['target'],
            distance=row['distance']
        )
    
    return graph, stations_df, edges_df


def create_map(stations_df, route_details=None):
    """Crea un mapa interactivo con las estaciones usando OpenStreetMap"""
    fig = go.Figure()
    
    fig.add_trace(go.Scattermapbox(
        lon=stations_df['long'],
        lat=stations_df['lat'],
        mode='markers',
        marker=dict(
            size=6,
            color='rgba(100, 100, 100, 0.7)',
            allowoverlap=True
        ),
        text=stations_df['name'],
        hovertemplate='<b>%{text}</b><extra></extra>',
        name='Estaciones',
        showlegend=True
    ))
    
    if route_details:
        route_lats = [detail['lat'] for detail in route_details]
        route_lons = [detail['lon'] for detail in route_details]
        route_names = [detail['name'] for detail in route_details]
        
        fig.add_trace(go.Scattermapbox(
            lon=route_lons,
            lat=route_lats,
            mode='lines+markers',
            line=dict(width=4, color='#1f77b4'),
            marker=dict(size=10, color='#1f77b4'),
            text=route_names,
            hovertemplate='<b>%{text}</b><extra></extra>',
            name='Ruta',
            showlegend=True
        ))
        
        fig.add_trace(go.Scattermapbox(
            lon=[route_lons[0]],
            lat=[route_lats[0]],
            mode='markers',
            marker=dict(size=20, color='#28a745'),
            text=[f"🏁 ORIGEN: {route_names[0]}"],
            hovertemplate='<b>%{text}</b><extra></extra>',
            name='🏁 Origen',
            showlegend=True
        ))
        
        fig.add_trace(go.Scattermapbox(
            lon=[route_lons[-1]],
            lat=[route_lats[-1]],
            mode='markers+text',
            marker=dict(size=20, color='#dc3545'),
            text=[f"🎯 DESTINO: {route_names[-1]}"],
            hovertemplate='<b>%{text}</b><extra></extra>',
            name='🎯 Destino',
            showlegend=True
        ))
    
    fig.update_layout(
        height=600,
        margin={"r":0,"t":5,"l":0,"b":60},
        showlegend=True,
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=54.5, lon=-3),
            zoom=5
        ),
        hovermode='closest',
        dragmode='pan'
    )
    
    return fig


def display_route_details(graph, route_info):
    """Muestra los detalles de la ruta encontrada"""
    if not route_info['found']:
        st.error(route_info['message'])
        return
    
    st.success("✅ ¡Ruta encontrada con éxito!")

    num_stops = len(route_info['path'])
    
    # Para Dijkstra y A*, la métrica es directamente la distancia
    if route_info['algorithm'] in ['dijkstra', 'a_star']:
        total_distance = float(route_info['metric'])
    # Para BFS, calculamos la distancia sumando todas las aristas
    elif route_info['algorithm'] == 'bfs':
        route_details_temp = graph.get_route_details(route_info['path'])
        total_distance = sum(detail.get('distance_to_next', 0) for detail in route_details_temp)    
    else:
        total_distance = 0
    
    estimated_price = graph.calculate_price(total_distance)
    estimated_time = graph.calculate_time(total_distance, num_stops)
    
    hours = int(estimated_time)
    minutes = int((estimated_time - hours) * 60)
    time_str = f"{hours}h {minutes}min" if hours > 0 else f"{minutes}min"
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Determinar el nombre del algoritmo
    algorithm_names = {
        'dijkstra': 'Dijkstra (menor distancia)',
        'bfs': 'BFS (menos paradas)',
        'a_star': 'A* (menor distancia + heurística)'
    }
    algorithm_display = algorithm_names.get(route_info['algorithm'], route_info['algorithm'])
    

    with col1:
        st.markdown("#### 🚉 Origen")
        st.markdown(f"""
        <div style="background-color: #d4edda; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #28a745;">
            <p style="margin: 0; color: #155724; font-weight: bold; font-size: 0.95rem;">{route_info['origin_station']['name']}</p>
            <p style="color: #666; margin-top: 0.3rem; font-size: 0.8rem;">Código: {route_info['origin_station']['code']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🎯 Destino")
        st.markdown(f"""
        <div style="background-color: #f8d7da; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #dc3545;">
            <p style="margin: 0; color: #721c24; font-weight: bold; font-size: 0.95rem;">{route_info['destination_station']['name']}</p>
            <p style="color: #666; margin-top: 0.3rem; font-size: 0.8rem;">Código: {route_info['destination_station']['code']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("#### 📏 Distancia")
        st.markdown(f"""
        <div style="background-color: #e8f4f8; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #1f77b4;">
            <h2 style="margin: 0; color: #1f77b4; text-align: center; font-size: 1.5rem;">{total_distance:.1f} km</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("#### ⏱️ Tiempo")
        st.markdown(f"""
        <div style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #ffc107;">
            <h2 style="margin: 0; color: #856404; text-align: center; font-size: 1.5rem;">{time_str}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("#### 💷 Precio")
        st.markdown(f"""
        <div style="background-color: #d1ecf1; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #17a2b8;">
            <h2 style="margin: 0; color: #0c5460; text-align: center; font-size: 1.5rem;">£{estimated_price}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 0.8rem; border-radius: 0.3rem; margin-top: 1rem;">
        <p style="margin: 0; font-size: 0.9rem; color: #666;">
            🔢 <strong>{num_stops}</strong> paradas • 
            🚄 Velocidad promedio: <strong>80 km/h</strong> • 
            💡 Algoritmo usado: <strong>{algorithm_display}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.subheader("📍 Itinerario Detallado")
    
    route_details = graph.get_route_details(route_info['path'])
    
    itinerary_data = []
    for detail in route_details:
        row = {
            'Paso': detail['step'],
            'Código': detail['code'],
            'Estación': detail['name'],
            'Ciudad': detail['city']
        }
        
        if 'distance_to_next' in detail:
            row['Distancia al siguiente'] = f"{detail['distance_to_next']:.2f} km"
        else:
            row['Distancia al siguiente'] = '-'
        
        itinerary_data.append(row)
    
    itinerary_df = pd.DataFrame(itinerary_data)
    st.dataframe(itinerary_df, width='stretch', hide_index=True)
    
    route_details_with_coords = []
    for detail in route_details:
        station_info = graph.get_station_info(detail['code'])
        route_details_with_coords.append({
            'name': detail['name'],
            'lat': station_info['lat'],
            'lon': station_info['lon']
        })
    
    return route_details_with_coords



def main():
    """Función principal de la aplicación"""
    
    st.markdown('<h1 class="main-header">🚂 SmartPath+</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Sistema Inteligente de Optimización de Rutas Ferroviarias del Reino Unido</p>', unsafe_allow_html=True)
    
    with st.spinner('Cargando red ferroviaria...'):
        graph, stations_df, edges_df = load_data()
    
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/train.png", width=80)
        st.title("ℹ️ Información")
        st.markdown(""" 
        ### Acerca del Proyecto
        
        **SmartPath+** es un sistema de planificación de viajes en tren que utiliza 
        algoritmos de grafos para optimizar rutas entre ciudades del Reino Unido.
        
        ### 🎓 Equipo
        - Sulca Silva, Melisa
        - Sánchez Martínez, Nicole
        - Roque Tello, Jack Eddie
        
        ### 🏛️ Institución
        Universidad Peruana de Ciencias Aplicadas
        
        **Curso:** Complejidad Algorítmica  
        **NRC:** 1398  
        **Profesor:** Abraham Sopla Maslucán
        """)
        
        st.markdown("---")
        
        stats = graph.get_statistics()
        st.markdown("### 📊 Estadísticas de la Red")
        st.metric("Estaciones Totales", f"{stats['total_stations']:,}")
        st.metric("Conexiones", f"{stats['total_connections']:,}")
        st.metric("Ciudades", f"{stats['total_cities']:,}")
        st.metric("Conexiones promedio", stats['avg_connections_per_station'])
    
    tab1, tab2, tab3 = st.tabs(["🔍 Búsqueda de Rutas", "📊 Visualización", "📖 Documentación"])

    with tab1:
        st.header("Planifica tu Viaje")
        
        mode = st.radio("¿Buscar ruta entre ciudades o entre estaciones?", options=["Ciudad a Ciudad", "Estación a Estación"])
        
        if mode == "Ciudad a Ciudad":
            col1, col2 = st.columns(2)
            
            cities = graph.get_cities()
            with col1:
                origin_city = st.selectbox("🏁 Ciudad de Origen", cities)
            with col2:
                destination_city = st.selectbox("🎯 Ciudad de Destino", cities)
            
            st.markdown("---")
            st.subheader("⚙️ Opciones de Optimización")
            
            algorithm = st.radio(
                "Selecciona el criterio de optimización:",
                options=['dijkstra', 'bfs'],
                format_func=lambda x: '📏 Menor Distancia (Dijkstra)' if x == 'dijkstra' else '🔢 Menor Número de Paradas (BFS)',
                horizontal=True,
                help=""" 
                - **Dijkstra**: Encuentra la ruta con menor distancia en kilómetros
                - **BFS**: Encuentra la ruta con menor número de estaciones intermedias
                """
            )
            
            if st.button("🔎 Buscar Mejor Ruta", type="primary"):
                if origin_city == destination_city:
                    st.warning("⚠️ Por favor selecciona ciudades diferentes de origen y destino")
                else:
                    with st.spinner('Calculando la mejor ruta...'):
                        route_info = graph.find_best_route_between_cities(origin_city, destination_city, algorithm)
                        st.markdown("---")
                        route_coords = display_route_details(graph, route_info)
                        if route_info['found']:
                            st.subheader("🗺️ Visualización de la Ruta")
                            map_fig = create_map(stations_df, route_coords)
                            st.plotly_chart(map_fig, use_container_width=True)

        elif mode == "Estación a Estación":
            # Convertir los códigos de estaciones a nombres
            stations = list(graph.stations.keys())
            stations_names = [graph.stations[station]['name'] for station in stations]
            
            col1, col2 = st.columns(2)
            with col1:
                origin_station_name = st.selectbox("🏁 Estación de Origen", stations_names)
            with col2:
                destination_station_name = st.selectbox("🎯 Estación de Destino", stations_names)
            
            # CORRECTO
            origin_station_code = [station for station, info in graph.stations.items() if info['name'] == origin_station_name][0]
            destination_station_code = [station for station, info in graph.stations.items() if info['name'] == destination_station_name][0] 
            st.markdown("---")
            st.subheader("⚙️ Opciones de Optimización")
            
            # Solo A* se muestra en Estación a Estación
            algorithm = st.radio(
                "Selecciona el criterio de optimización:",
                options=['a_star'],
                format_func=lambda x: '✨ A* (Menor Distancia)',
                horizontal=True
            )
            
            if st.button("🔎 Buscar Mejor Ruta", type="primary"):
                if origin_station_name == destination_station_name:
                    st.warning("⚠️ Por favor selecciona estaciones diferentes de origen y destino")
                else:
                    with st.spinner('Calculando la mejor ruta...'):
                        route_info = graph.find_best_route_between_stations(origin_station_code, destination_station_code, algorithm)
                        st.markdown("---")
                        route_coords = display_route_details(graph, route_info)
                        if route_info['found']:
                            st.subheader("🗺️ Visualización de la Ruta")
                            map_fig = create_map(stations_df, route_coords)
                            st.plotly_chart(map_fig, use_container_width=True)


    with tab2:
        st.header("📊 Visualización de la Red Ferroviaria")
        
        st.markdown("""
        Esta sección muestra la distribución geográfica de todas las estaciones 
        de tren en el Reino Unido.
        """)
        
        # Mapa general
        map_fig = create_map(stations_df)
        st.plotly_chart(map_fig, use_container_width=True)
        
        st.markdown("---")
        
        # Gráficos adicionales
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Top 10 Ciudades con Más Estaciones")
            city_counts = stations_df['city'].value_counts().head(10)
            fig_cities = px.bar(
                x=city_counts.values,
                y=city_counts.index,
                orientation='h',
                labels={'x': 'Número de Estaciones', 'y': 'Ciudad'},
                color=city_counts.values,
                color_continuous_scale='Blues'
            )
            fig_cities.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_cities, use_container_width=True)
        
        with col2:
            st.subheader("📊 Estaciones Más Conectadas")
            # Top 10 estaciones con más conexiones
            connections_per_station = edges_df['source'].value_counts().head(10)
            
            # Obtener nombres de las estaciones
            station_names = []
            for code in connections_per_station.index:
                station_info = graph.get_station_info(code)
                if station_info:
                    station_names.append(f"{station_info['name']} ({code})")
                else:
                    station_names.append(code)
            
            fig_connections = px.bar(
                x=connections_per_station.values,
                y=station_names,
                orientation='h',
                labels={'x': 'Número de Conexiones', 'y': 'Estación'},
                color=connections_per_station.values,
                color_continuous_scale='Reds'
            )
            fig_connections.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_connections, use_container_width=True)
    
    with tab3:
        st.header("📖 Documentación del Proyecto")
        
        st.markdown("""
        ## Descripción del Problema
        
        El transporte ferroviario en el Reino Unido presenta un desafío significativo para 
        los viajeros: la existencia de múltiples estaciones en una misma ciudad. Londres, 
        por ejemplo, cuenta con 14 estaciones terminales principales, cada una conectada 
        a diferentes regiones del país.
        
        ### 🎯 Objetivo
        
        Desarrollar un sistema computacional basado en grafos que optimice la selección 
        de estaciones para viajes interurbanos, considerando:
        - Menor distancia física entre estaciones
        - Menor número de transbordos/paradas
        
        ## 🧮 Algoritmos Implementados
        
        ### 1. Algoritmo de Dijkstra
        
        **Propósito:** Encontrar la ruta más corta en términos de distancia (km).
        
        **Características:**
        - Complejidad temporal: O((V + E) log V) con heap de prioridad
        - Garantiza encontrar el camino óptimo en grafos con pesos no negativos
        - Ideal para minimizar la distancia física del viaje
        
        **Aplicación:** Útil para viajeros que priorizan minimizar la distancia total 
        del trayecto, lo que generalmente se traduce en menor tiempo de viaje y menor costo.
        
        ### 2. Algoritmo BFS (Breadth-First Search)
        
        **Propósito:** Encontrar la ruta con menor número de paradas.
        
        **Características:**
        - Complejidad temporal: O(V + E)
        - Explora el grafo nivel por nivel
        - Encuentra el camino con menor número de aristas
        
        **Aplicación:** Ideal para turistas o viajeros ocasionales que prefieren 
        trayectos directos con menos transbordos, independientemente de la distancia.
        
        ## 💰 Fórmulas de Cálculo
        
        ### Cálculo de Precio Estimado
        
        El precio del viaje se calcula utilizando una tarifa base más un costo por kilómetro:
        
        **Fórmula:**
        
        ```
        Precio = Tarifa Base + (Distancia × Tarifa por km)
        ```
        
        **Valores utilizados:**
        - Tarifa Base: **£5.00** (costo fijo de entrada al sistema)
        - Tarifa por kilómetro: **£0.15/km** (basado en tarifas promedio de UK Rail)
        
        **Ejemplo:** Para un viaje de 200 km:
        - Precio = £5.00 + (200 × £0.15) = £5.00 + £30.00 = **£35.00**
        
        ### Cálculo de Tiempo Estimado
        
        El tiempo de viaje considera tanto el tiempo de desplazamiento como las paradas:
        
        **Fórmula:**
        
        ```
        Tiempo = (Distancia / Velocidad Promedio) + ((Número de Paradas - 1) × Tiempo por Parada)
        ```
        
        **Valores utilizados:**
        - Velocidad Promedio: **80 km/h** (velocidad típica de trenes interurbanos UK)
        - Tiempo por Parada: **3 minutos** (0.05 horas - tiempo promedio de detención)
        
        **Ejemplo:** Para un viaje de 200 km con 5 paradas:
        - Tiempo de viaje = 200/80 = 2.5 horas
        - Tiempo de paradas = (5-1) × 0.05 = 0.2 horas (12 minutos)
        - Tiempo total = 2.5 + 0.2 = **2.7 horas** (2h 42min)
        
        **Nota:** Estos valores son estimaciones basadas en promedios del sistema ferroviario 
        británico y pueden variar según el tipo de servicio (express, regional, etc.).
        
        ## 📊 Dataset
        
        El proyecto utiliza datos reales de la red ferroviaria del Reino Unido:
        
        - **Estaciones:** 2,580 nodos con información geográfica (latitud, longitud)
        - **Conexiones:** 7,637 aristas con distancias en kilómetros
        - **Ciudades:** Más de 1,000 ciudades conectadas
        
        **Fuente:** UK Train Stations dataset (Kaggle)
        
        ## 🎓 Equipo de Desarrollo
        
        - **Sulca Silva, Melisa Geraldine** - U20222460
        - **Sánchez Martínez, Nicole Abigail** - U202419766
        - **Roque Tello, Jack Eddie** - U20221C448
        
        ### Institución
        Universidad Peruana de Ciencias Aplicadas  
        Curso: Complejidad Algorítmica - NRC 1398  
        Profesor: Sopla Maslucán Abraham  
        Ciclo: 2025-2
        
        ## 📚 Referencias
        
        - Department for Transport. (2025). Rail factsheet: 2024
        - Wagner, D., & Willhalm, T. (2007). Speed-Up Techniques for Shortest-Path Computations
        - Suprihatin et al. (2023). Improved Breadth First Search for Public Transit Line Search Optimization
        - Transport Focus. (2023). Motivations and barriers to train usage
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #666;">© 2025 SmartPath+ | UPC - Complejidad Algorítmica</p>',
        unsafe_allow_html=True
    )                        

if __name__ == "__main__":
    main()
