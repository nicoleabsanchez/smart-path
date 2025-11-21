# 🚂 SmartPath+

**Sistema Inteligente de Optimización de Rutas Ferroviarias del Reino Unido**

## 📋 Descripción del Proyecto

SmartPath+ es una aplicación web desarrollada con Streamlit que permite planificar viajes en tren por el Reino Unido de manera óptima. El sistema utiliza algoritmos de grafos avanzados para encontrar las mejores rutas entre ciudades, considerando múltiples estaciones por ciudad.

### 🎯 Objetivo

Resolver el problema de selección óptima de estaciones en ciudades con múltiples terminales ferroviarias, ayudando a viajeros a identificar la mejor combinación de estación origen-destino según criterios objetivos:

- **Menor distancia física** (Algoritmo de Dijkstra)
- **Menor número de paradas** (Algoritmo BFS)

## 🎓 Equipo de Desarrollo

**Universidad Peruana de Ciencias Aplicadas**  
Curso: Complejidad Algorítmica - NRC 1398  
Profesor: Sopla Maslucán Abraham  
Ciclo: 2025-2

### Integrantes:

- Sulca Silva, Melisa Geraldine - U20222460
- Sánchez Martínez, Nicole Abigail - U202419766
- Roque Tello, Jack Eddie - U20221C448

## 🚀 Características

✨ **Búsqueda Inteligente de Rutas**

- Encuentra automáticamente la mejor combinación de estaciones entre ciudades
- Considera todas las estaciones disponibles en cada ciudad
- Optimización basada en distancia o número de paradas

📊 **Visualización Interactiva**

- Mapa interactivo de todas las estaciones del Reino Unido
- Visualización de rutas calculadas
- Gráficos estadísticos de la red ferroviaria

🧮 **Algoritmos Implementados**

- **Dijkstra**: Ruta más corta por distancia (km)
- **BFS (Breadth-First Search)**: Ruta con menos paradas

## 📊 Dataset

El proyecto utiliza datos reales de la red ferroviaria del Reino Unido:

- **Estaciones**: 2,580 nodos con información geográfica
- **Conexiones**: 7,637 aristas con distancias calculadas
- **Ciudades**: Más de 1,000 ciudades conectadas

**Fuente**: UK Train Stations dataset (Kaggle)

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**
- **Streamlit**: Framework para la aplicación web
- **Pandas**: Procesamiento de datos
- **Plotly**: Visualizaciones interactivas
- **Estructuras de Datos**: Grafos, Heap de prioridad, Cola (Queue)

## 📦 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/nicoleabsanchez/smart-path.git
cd smart-path
```

2. **Crear entorno virtual (recomendado)**

```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Mac/Linux
source venv/bin/activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

## 🎮 Uso

### Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### Cómo usar SmartPath+

1. **Seleccionar ciudades**: Elige tu ciudad de origen y destino en los menús desplegables
2. **Elegir criterio**: Selecciona si deseas optimizar por distancia o por número de paradas
3. **Buscar ruta**: Haz clic en "Buscar Mejor Ruta"
4. **Ver resultados**: La aplicación mostrará:
   - Estaciones óptimas de origen y destino
   - Itinerario completo paso a paso
   - Visualización de la ruta en el mapa
   - Métricas de distancia/paradas

## 📁 Estructura del Proyecto

```
smart-path/
│
├── data/
│   ├── edges.csv                    # Conexiones entre estaciones
│   └── stations_with_city.csv       # Información de estaciones
│
├── app.py                           # Aplicación principal Streamlit
├── graph_algorithms.py              # Implementación de algoritmos
├── requirements.txt                 # Dependencias del proyecto
└── README.md                        # Documentación
```

## 🧮 Algoritmos

### Algoritmo de Dijkstra

**Complejidad**: O((V + E) log V) con heap de prioridad

**Uso**: Encuentra la ruta con menor distancia en kilómetros entre dos estaciones.

**Ventajas**:

- Garantiza encontrar el camino óptimo
- Eficiente para grafos con pesos no negativos
- Ideal para minimizar distancia/costo

### Algoritmo BFS (Breadth-First Search)

**Complejidad**: O(V + E)

**Uso**: Encuentra la ruta con menor número de paradas (estaciones intermedias).

**Ventajas**:

- Explora el grafo nivel por nivel
- Encuentra el camino con menos aristas
- Ideal para trayectos directos

## 📈 Funcionalidades Principales

### 1. Búsqueda de Rutas

- Selección de ciudad origen y destino
- Optimización por distancia o paradas
- Resultados instantáneos

### 2. Visualización

- Mapa interactivo de la red completa
- Visualización de rutas calculadas
- Gráficos estadísticos

### 3. Itinerario Detallado

- Lista completa de estaciones
- Distancias entre paradas
- Códigos y nombres de estaciones

## 🎯 Casos de Uso

### Turistas Internacionales

Visitantes que desconocen la estructura del sistema ferroviario británico.

### Viajeros Ocasionales

Residentes locales con viajes interurbanos esporádicos.

### Nuevos Residentes

Personas recién llegadas al Reino Unido.

## 📊 Estadísticas del Sistema

- **2,580** estaciones únicas
- **7,637** conexiones ferroviarias
- **1,000+** ciudades conectadas
- **15,800** km de vías activas

## 🔬 Metodología

El proyecto modela la red ferroviaria como un **grafo dirigido ponderado**:

- **Nodos**: Estaciones de tren
- **Aristas**: Conexiones entre estaciones
- **Pesos**: Distancia en kilómetros (calculada con fórmula de Haversine)

## 📚 Referencias

- Department for Transport. (2025). Rail factsheet: 2024
- Wagner, D., & Willhalm, T. (2007). Speed-Up Techniques for Shortest-Path Computations
- Suprihatin et al. (2023). Improved Breadth First Search for Public Transit Line Search Optimization
- Transport Focus. (2023). Motivations and barriers to train usage
- Kaggle. (2023). UK Train Stations Dataset

## 🤝 Contribuciones

Este proyecto es parte del trabajo parcial del curso de Complejidad Algorítmica y tiene fines educativos.

## 📄 Licencia

Este proyecto es desarrollado con fines académicos para la Universidad Peruana de Ciencias Aplicadas.

## 📧 Contacto

Para consultas sobre el proyecto:

- Nicole Sánchez - u202419766@upc.edu.pe
- Melisa Sulca - u202224602@upc.edu.pe
- Jack Roque - u20221C448@upc.edu.pe

---

**© 2025 SmartPath+ | UPC - Complejidad Algorítmica**
