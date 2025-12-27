import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash

# =========================
# DATOS
# =========================
data = {
    'Pos': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Modelo': ['BMW M135i xDrive', 'Cupra León VZ', 'Renault Megane RS', 'Subaru WRX',
               'Hyundai i30 N', 'Mazda 3 Turbo', 'Mercedes A200', 'Audi A3 35 TFSI',
               'BMW 118i', 'Peugeot 308 GT'],
    'Version': ['xDrive', 'VZ', 'Trophy', '2.4T', '2021*', '2.5 Turbo', 'AMG Line', '35 TFSI', 'M Sport', 'GT'],
    'Peso': [1525, 1395, 1430, 1585, 1429, 1496, 1365, 1395, 1320, 1290],
    'HP': [306, 300, 300, 271, 275, 227, 163, 150, 140, 130],
    'Torque': [450, 400, 400, 350, 353, 420, 250, 250, 220, 230],
    'Aceleracion': [4.8, 5.7, 5.7, 6.1, 6.1, 6.4, 8.2, 8.4, 8.5, 9.7],
    'Precio': [34.5, 27.5, 28.5, 28.5, 24.5, 23.5, 25.5, 23.5, 22.5, 22.5],
    'Traccion': ['AWD', 'Delantera', 'Delantera', 'AWD', 'Delantera', 'AWD',
                 'Delantera', 'Delantera', 'Delantera', 'Delantera'],
    'Seguridad': [5, 5, 5, 5, 5, 5, 5, 5, 5, 4],
    'Origen': ['🇩🇪 Alemania', '🇪🇸 España', '🇪🇸 España', '🇯🇵 Japón', '🇨🇿 Rep. Checa',
               '🇯🇵 Japón', '🇩🇪 Alemania', '🇩🇪 Alemania', '🇩🇪 Alemania', '🇫🇷 Francia'],
    'Motor': ['2.0L TwinPower Turbo', '2.0L TSI Turbo',
              '1.8L Turbo', '2.4L Turbo Bóxer',
              '2.0L T-GDI', '2.5L Turbo', '1.33L Turbo',
              '1.4L Turbo', '1.5L Turbo', '1.2L PureTech'],
    'Consumo': [10.5, 10.5, 8.5, 8.5, 9.5, 9.5, 14, 15, 15, 16],
    'Ensamble': ['Leipzig', 'Martorell', 'Palencia', 'Gunma', 'Nošovice',
                 'Hofu', 'Alemania/Hungría', 'Ingolstadt', 'Leipzig', 'Mulhouse'],
    'Imagen': [
        'https://photos.encuentra24.com/t_or_fh_m/f_auto/v1/cl/26/18/84/79/26188479_6e89fd',
        'https://cupra.com.mx/content/dam/public/cupra-website/myco/models/leon/overview/overview-hero.jpg/_jcr_content/renditions/original.image_file.992.558.file/overview-hero.jpg',
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfx1pCLIh18KxyJpuz7R8TQyB6oQbhlXgh-w&s',
        'https://fuelcarmagazine.com/wp-content/uploads/2023/10/Subaru-WRX-TR-2024-edicion-especial.jpg',
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_z8RItn9knBLp4jJFp8JEfKlIJxuNcwo5FQ&s',
        'https://dercocenter-api.s3.us-east-1.amazonaws.com/images/version/1700226247-aqENEQ6BuF.webp',
        'https://www.mercedes-benz.cl/content/chile/es/passengercars/models/hatchback/a-class-w177-fl/overview/_jcr_content/root/responsivegrid/simple_stage.component.damq6.3335738369871.jpg/mercedes-benz-a-class-w177-stage-3840x1440-08-2022.jpg',
        'https://acroadtrip.blob.core.windows.net/catalogo-imagenes/l/RT_V_c73dba5be6df4f2c8dc1077fcdbb3ef6.jpg',
        'https://www.bmw.cl/content/dam/bmw/marketCL/bmw_cl/all-models/1-series/5-door/2024/navigation/bmw-1-series-lci-onepager-ms-desktop.jpg',
        'https://www.autocar.co.uk/sites/autocar.co.uk/files/peugeot-308-rt-2024-02-tracking-front.jpg'
    ]
}

df = pd.DataFrame(data)

# =========================
# MÉTRICAS
# =========================
df['CalidadPrecio'] = (df['HP'] / df['Precio']) * \
    (df['Seguridad'] / 5) * (100 / df['Aceleracion'])
df['ScoreSeguridad'] = df['Seguridad'] * 20
df['ScoreVelocidad'] = (100 / df['Aceleracion']) * 10

# =========================
# APP
# =========================
app = Dash(__name__)
server = app.server  # ← IMPORTANTE para Render

# =========================
# LAYOUT
# =========================
app.layout = html.Div([
    html.H1("🏎️ Análisis Vehiculos Felipe", style={
            "color": "white", "textAlign": "center"}),

    # Gráficos
    html.Div([
        dcc.Graph(id="calidad-precio-chart"),
        dcc.Graph(id="velocidad-chart"),
    ], style={'marginBottom': '30px'}),

    # Título Carrusel
    html.H3("Explora los Modelos", style={
            'color': '#94a3b8', 'textAlign': 'center', 'marginTop': '20px'}),

    # Contenedor del Carrusel + Botones
    html.Div([
        # Botón Izquierda
        html.Button("◀", id="btn-prev", n_clicks=0, style={
            'backgroundColor': '#334155', 'color': 'white', 'border': 'none',
            'fontSize': '24px', 'padding': '10px 20px', 'cursor': 'pointer',
            'borderRadius': '8px', 'marginRight': '20px'
        }),

        # Tarjeta del Coche (Contenido dinámico)
        html.Div(id="carousel-content",
                 style={'display': 'inline-block', 'verticalAlign': 'middle'}),

        # Botón Derecha
        html.Button("▶", id="btn-next", n_clicks=0, style={
            'backgroundColor': '#334155', 'color': 'white', 'border': 'none',
            'fontSize': '24px', 'padding': '10px 20px', 'cursor': 'pointer',
            'borderRadius': '8px', 'marginLeft': '20px'
        }),
    ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}),

    # Intervalo para carrusel automático (5 segundos)
    dcc.Interval(
        id='carousel-interval',
        interval=5000,  # 5 segundos en milisegundos
        n_intervals=0
    ),

    # Tabla de Información Detallada
    html.Div([
        html.H3("📊 Tabla Comparativa Completa", style={
            'color': '#94a3b8', 'textAlign': 'center', 'marginTop': '40px', 'marginBottom': '20px'
        }),
        html.Div(id='info-table', style={'overflowX': 'auto'})
    ], style={'marginTop': '40px', 'padding': '0 20px'})

], style={
    "background": "linear-gradient(135deg, #0f172a, #1e293b)",
    "minHeight": "100vh",
    "padding": "20px",
    "fontFamily": "Arial"
})

# =========================
# CALLBACKS
# =========================

# Callback para los gráficos


@app.callback(
    Output('calidad-precio-chart', 'figure'),
    Input('calidad-precio-chart', 'id')
)
def update_calidad_precio(_):
    fig = go.Figure()
    fig.add_bar(name='Seguridad', x=df['Modelo'], y=df['ScoreSeguridad'])
    fig.add_bar(name='Velocidad', x=df['Modelo'], y=df['ScoreVelocidad'])
    fig.add_bar(name='Calidad-Precio', x=df['Modelo'], y=df['CalidadPrecio'])
    fig.update_layout(barmode='group', template='plotly_dark', height=400,
                      title="Comparación: Seguridad, Velocidad y Calidad-Precio",
                      margin=dict(l=20, r=20, t=40, b=20))
    return fig


@app.callback(
    Output('velocidad-chart', 'figure'),
    Input('velocidad-chart', 'id')
)
def update_velocidad(_):
    fig = px.bar(df, x='Aceleracion', y='Modelo', orientation='h', color='Seguridad',
                 template='plotly_dark', title="Aceleración 0-100 km/h (segundos)", height=400)
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig


# Callback para el CARRUSEL (Automático + Manual)
@app.callback(
    Output('carousel-content', 'children'),
    Input('btn-prev', 'n_clicks'),
    Input('btn-next', 'n_clicks'),
    Input('carousel-interval', 'n_intervals')
)
def update_carousel(btn_prev, btn_next, n_intervals):
    # Determinar qué input disparó el callback
    ctx = dash.callback_context

    if not ctx.triggered:
        current_index = 0
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigger_id == 'carousel-interval':
            # Avance automático cada 5 segundos
            current_index = n_intervals % len(df)
        else:
            # Avance manual con botones
            current_index = (btn_next - btn_prev) % len(df)

    car = df.iloc[current_index]

    return html.Div([
        html.Img(
            src=car['Imagen'],
            style={
                'width': '100%',
                'maxWidth': '600px',
                'height': '350px',
                'objectFit': 'cover',
                'borderRadius': '12px',
                'marginBottom': '20px'
            }
        ),
        html.H2(f"{car['Modelo']} ({car['Version']})", style={
                'color': 'white', 'marginBottom': '10px'}),
        html.P(f"🏭 {car['Origen']} ({car['Ensamble']})", style={
               'color': '#94a3b8', 'fontSize': '18px'}),
        html.P(f"🔧 {car['Motor']}", style={
               'color': '#94a3b8', 'fontSize': '16px'}),
        html.Div([
            html.Span(f"⚡ {car['HP']} HP", style={'margin': '0 15px'}),
            html.Span(f"🔄 {car['Torque']} Nm", style={'margin': '0 15px'}),
            html.Span(f"⏱️ 0-100: {car['Aceleracion']}s",
                      style={'margin': '0 15px'})
        ], style={'color': '#cbd5e1', 'fontSize': '18px', 'marginTop': '15px'}),
        html.Div([
            html.Span(f"💰 ${car['Precio']}M", style={'margin': '0 15px'}),
            html.Span(
                f"🛡️ {'⭐' * int(car['Seguridad'])}", style={'margin': '0 15px'}),
            html.Span(f"🚗 {car['Traccion']}", style={'margin': '0 15px'}),
            html.Span(f"⛽ {car['Consumo']} L/100km",
                      style={'margin': '0 15px'})
        ], style={'color': '#cbd5e1', 'fontSize': '18px', 'marginTop': '10px'})
    ], style={
        "background": "#0f172a",
        "padding": "30px",
        "borderRadius": "12px",
        "textAlign": "center",
        "border": "2px solid #334155",
        "maxWidth": "700px",
        "margin": "0 auto"
    })


# Callback para la TABLA INFORMATIVA
@app.callback(
    Output('info-table', 'children'),
    Input('info-table', 'id')
)
def update_info_table(_):
    # Crear tabla HTML estilizada
    table_header = [
        html.Thead(html.Tr([
            html.Th("Pos", style={
                    'padding': '12px', 'backgroundColor': '#1e293b', 'color': '#94a3b8'}),
            html.Th("Modelo y Versión", style={
                    'padding': '12px', 'backgroundColor': '#1e293b', 'color': '#94a3b8'}),
            html.Th("Peso (kg)", style={
                    'padding': '12px', 'backgroundColor': '#1e293b', 'color': '#94a3b8'}),
            html.Th("Motor", style={
                    'padding': '12px', 'backgroundColor': '#1e293b', 'color': '#94a3b8'}),
            html.Th("Origen", style={
                    'padding': '12px', 'backgroundColor': '#1e293b', 'color': '#94a3b8'}),
            html.Th("HP", style={
                    'padding': '12px', 'backgroundColor': '#1e293b', 'color': '#94a3b8'}),
            html.Th("Torque (Nm)", style={
                    'padding': '12px', 'backgroundColor': '#1e293b', 'color': '#94a3b8'}),
            html.Th("0-100 km/h", style={'padding': '12px',
                    'backgroundColor': '#1e293b', 'color': '#94a3b8'}),
            html.Th("Tracción", style={
                    'padding': '12px', 'backgroundColor': '#1e293b', 'color': '#94a3b8'}),
            html.Th("Seguridad", style={
                    'padding': '12px', 'backgroundColor': '#1e293b', 'color': '#94a3b8'}),
            html.Th("Consumo (L/100km)", style={'padding': '12px',
                    'backgroundColor': '#1e293b', 'color': '#94a3b8'}),
            html.Th("Precio (M)", style={
                    'padding': '12px', 'backgroundColor': '#1e293b', 'color': '#94a3b8'})
        ]))
    ]

    table_body = [html.Tbody([
        html.Tr([
            html.Td(row['Pos'], style={'padding': '12px', 'color': '#cbd5e1'}),
            html.Td(f"{row['Modelo']} ({row['Version']})", style={
                    'padding': '12px', 'color': '#cbd5e1'}),
            html.Td(row['Peso'], style={
                    'padding': '12px', 'color': '#cbd5e1'}),
            html.Td(row['Motor'], style={
                    'padding': '12px', 'color': '#cbd5e1'}),
            html.Td(f"{row['Origen']} ({row['Ensamble']})", style={
                    'padding': '12px', 'color': '#cbd5e1'}),
            html.Td(row['HP'], style={'padding': '12px', 'color': '#cbd5e1'}),
            html.Td(row['Torque'], style={
                    'padding': '12px', 'color': '#cbd5e1'}),
            html.Td(row['Aceleracion'], style={
                    'padding': '12px', 'color': '#cbd5e1'}),
            html.Td(row['Traccion'], style={
                    'padding': '12px', 'color': '#cbd5e1'}),
            html.Td('⭐' * int(row['Seguridad']),
                    style={'padding': '12px', 'color': '#cbd5e1'}),
            html.Td(row['Consumo'], style={
                    'padding': '12px', 'color': '#cbd5e1'}),
            html.Td(f"${row['Precio']}", style={
                    'padding': '12px', 'color': '#cbd5e1'})
        ], style={'backgroundColor': '#0f172a' if i % 2 == 0 else '#1e293b'})
        for i, row in df.iterrows()
    ])]

    return html.Table(
        table_header + table_body,
        style={
            'width': '100%',
            'borderCollapse': 'collapse',
            'border': '2px solid #334155',
            'borderRadius': '8px',
            'overflow': 'hidden'
        }
    )


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0', port=8050)
