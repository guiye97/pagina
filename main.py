import datetime

import pandas as pd
import streamlit as st
import streamlit_antd_components as sac

from auxiliar import dias_meses, nombres_meses

st.title("Generador Fotovoltaico - Santa Fe")

sac.menu([
    sac.MenuItem('Inicio', icon='house-fill', href='https://python.guiye97.repl.co/'),
    sac.MenuItem('Historia', icon='book-fill', href='https://shorturl.at/cuIJN'),
    sac.MenuItem('Ubicación', icon='map', href='https://shorturl.at/ySTW8'),
    sac.MenuItem('Financiamiento', icon='cash-coin', href='https://shorturl.at/cuIJN', children=[
      sac.MenuItem('Empresa Sotic SA', icon='truck', href='https://shorturl.at/vwzT9'),
      sac.MenuItem('Secretaría de Estado CTI, prov. Sta. Fe', icon='building-check', href='https://shorturl.at/xDX01'),
      sac.MenuItem('Facultad Regional Santa Fe', icon='buildings', href='https://www.frsf.utn.edu.ar'),
    ]),
    sac.MenuItem('Aval', icon='Building-check', children=[
        sac.MenuItem('EPE Santa Fe', icon='lightning-charge-fill', href='https://www.epe.santafe.gov.ar/institucional/'),
        sac.MenuItem('Ex-Sub Secretaría de Energías Renovables, prov. Sta. Fe', icon='building-check'),
    ]),
    sac.MenuItem(type='divider'),
    sac.MenuItem('Consultas', icon='send', disabled=True),
    sac.MenuItem('Alumnos', type='group', children=[
        sac.MenuItem('Dropsi, Pablo', icon='binoculars-fill'),
        sac.MenuItem('Ferreyra, Guillermo', icon='usb-symbol'),
        sac.MenuItem('Montenegro, Angel', icon='universal-access'),
        sac.MenuItem('Smith, Axel', icon='xbox'),
    ]),
], format_func='title', size='large', indent=30, open_all=True, return_index=True)

sac.divider(icon='x-lg', align='center')

st.markdown("## Ecuaciones de Simulación")
# Agrega texto explicativo y ecuaciones según sea necesario

# Ecuación a mostrar la siguiente expresión obtiene la potencia eléctrica P (en kilo-Watt)
# obtenida por un GFV:
st.subheader("Potencia eléctrica obtenida por un Generador FV (kW)")
st.latex(
  r'P [kW] = N \cdot \frac{G}{G_{\text{std}}} \cdot P_{\text{pico}}' +
  r'\cdot \left[1 + k_p \cdot (T_c - T_r)\right] \eta \cdot 10^{-3}')

# Ecuación 2 a mostrar, La temperatura de la celda difiere de la temperatura ambiente:
st.subheader("Temperatura de la celda al diferir de la Temperatura Ambiente (°C)")
st.latex(
    r'{T}_{c}=T+0,031 \left[ ^\circ C \cdot {m}_{}^{2} \right / W]\cdot G')

# Ecuación 3 a mostrar, Limites de Generacion
st.subheader("Límites de Generación Técnicos (kW)")
st.latex(r'{P}_{min} [kW]= \frac{\mu (\%)}{100}\cdot {P}_{inv}')

st.latex(r'''{P}_{r} [kW]=  \left\{ \begin{array}{cl}
  0 & si \ P \leq {P}_{min} \\
  P & si \ {P}_{min} < P \leq {P}_{inv} \\
  {P}_{inv} & si \ {P}_{inv} < P
  \end{array} \right.''')

sac.divider(icon='x', align='center')

st.write("## Tabla anual 2019")
# Datos
tabla = pd.read_excel("Datos_climatologicos_Santa_Fe_2019.xlsx", index_col=0)
tabla

dia = "2019-04-25 13:50"
temp = tabla.at[dia, "Temperatura (°C)"]
st.write(f"# Temperatura del {dia}")
st.write(temp)


with st.sidebar:
  #mes = st.number_input("Mes", min_value=1, max_value=12, value=1)
  nombre_mes = st.selectbox("Mes", nombres_meses)
  mes = nombres_meses.index(nombre_mes) + 1
  dias = st.date_input("seleccionar dia",
                       value=datetime.date(2019, 1, 1),
                       min_value=datetime.date(2019, 1, 1),
                       max_value=datetime.date(2019, 12, 31))
  N = st.number_input('Nro. de paneles',
                      value=12,
                      min_value=0,
                      max_value=1000,
                      step=1)
  Ppico = st.number_input('Potencia pico del panel (W)', value=240)
  kp = st.number_input('Coef de T º',
                       value=-0.0044,
                       min_value=-0.1,
                       max_value=0.0,
                       step=0.001,
                       format="%4f")
  rend = st.number_input('Rndimiento', value=0.9)
  Gstd = 1000
  Tr = 25


tab1, tab2 = st.tabs(['Datos mensuales', 'Datos diarios'])

with tab1:
  tabla_mes = tabla.loc[f'2019-{mes}-01 00:00':
    f'2019-{mes}-{dias_meses[mes-1]}-30 23:50', :
  ]
  tabla_mes.loc[:,'potencia (kW)'] = (N*tabla_mes['Irradiancia (W/m²)']             /Gstd*Ppico*(1+kp*
    (tabla_mes['Temperatura (°C)']-Tr))*rend*1e-3
  )

st.line_chart(data=tabla_mes, y='potencia (kW)')
st.write("# Tabla anual 2019 con Potencia")
tabla_mes

st.write(f'# Tabla {nombre_mes} 2019 con Temperatura')
tabla_mes['Temperatura (°C)']
st.line_chart(data=tabla_mes, y='Temperatura (°C)')

with tab2:
  st.write('# Grafico temperatura diario')
 
  if isinstance(dias, datetime.date):
      tabla_dia = tabla.loc[f'{dias.year}-{dias.month}-{dias.day}', :]
      st.line_chart(data=tabla_dia, y='Temperatura (°C)')
  else:
      st.error("Selected date range is invalid.")
