# Dashboard de Analítica de Fútbol
Aplicación interactiva desarrollada en **Python** con **Dash y Plotly** para visualizar y analizar datos de jugadores de fútbol.

El dashboard permite explorar:
* 📊 **Rendimiento de jugadores** (Goals vs xG y radar ofensivo)
* 💰 **Valor de mercado** en función de edad, liga y posición
* 🔎 Filtros dinámicos de jugadores y posiciones
* 📋 Tabla interactiva con datos de jugadores
* 📄 Exportación de informes en **PDF**

# Requisitos
* Python **3.10 o superior**
* pip instalado

# Instalación
1. Descargar y descomprimir el archivo **.zip** del proyecto.
2. Abrir una terminal dentro de la carpeta del proyecto.
3. (Opcional pero recomendado) Crear un entorno virtual:

```bash
python -m venv venv
```


4. Activar el entorno virtual:
**Windows**
```bash
venv\Scripts\activate
```

**Mac / Linux**
```bash
source venv/bin/activate
```


5. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

# Ejecutar la aplicación
Desde la carpeta del proyecto ejecutar:

```bash
python app.py
```

Una vez iniciada la aplicación, abrir el navegador y acceder con el usuario y contraseña 'admin' a:

```
http://127.0.0.1:8080/
```

# Estructura básica del proyecto
```
project/
│
├── app.py
├── config.py
├── requirements.txt
│
├── callbacks/
├── pages/
├── utils/
├── data/
└── assets/
```

# Autor: Javier Sanus Ferri
Proyecto de analítica de fútbol para visualización y exploración de datos de rendimiento y valor de mercado de jugadores.