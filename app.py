import datetime
import numpy as np

import pandas as pd
import streamlit as st
import streamlit_antd_components as sac

from auxiliar import dias_meses, nombres_meses

with st.sidebar:
  st.subheader("Seleccion de fecha")
  #mes = st.number_input("Mes", min_value=1, max_value=12, value=1)
  nombre_mes = st.selectbox("Mes", nombres_meses)
  mes = nombres_meses.index(nombre_mes) + 1
  dias = st.date_input("Seleccionar día",
                       value=datetime.date(2019, 1, 1),
                       min_value=datetime.date(2019, 1, 1),
                       max_value=datetime.date(2019, 12, 31))

  with st.expander("Opciones de los paneles e inversor:"):
    st.subheader("Paneles:")
    N = st.number_input('Número de paneles',
                        value=12,
                        min_value=0,
                        max_value=1000,
                        step=1)
    Ppico = st.number_input('Potencia pico del panel [Watts]',
                            value=240,
                            min_value=0,
                            max_value=1000,
                            step=1)
    kp = st.number_input('Coef. de potencia-temperatura [1/°C]',
                         value=-0.0044,
                         min_value=-0.1,
                         max_value=0.0,
                         step=0.0001,
                         format="%.4f")
    rend = st.number_input('Rendimiento [%]',
                           min_value=0.,
                           max_value=1.,
                           value=0.9,
                           step=0.01)

    Gstd = st.number_input('Irradiancia Estandar [W/m^2]',
                           value=1000,
                           min_value=0,
                           max_value=2000,
                           step=1)

    Tr = st.number_input('Temperatura de referencia[°C]',
                         min_value=-273.,
                         max_value=1000.,
                         value=25.,
                         step=0.01)
    st.subheader("Opciones del inversor:")
    mu = st.number_input('Umbral min. [%]',
                         value=0.010,
                         min_value=0.,
                         max_value=1.,
                         step=0.001)
    Pinv = st.number_input('Potencia inversor [Kw]',
                           value=2.5,
                           min_value=0.,
                           step=0.1)

    Pmin = (mu / 100) * Pinv

st.title("Generador Fotovoltaico - Santa Fe")

sac.menu([
    sac.MenuItem(
        'Inicio', icon='house-fill', href='https://python.guiye97.repl.co/'),
    sac.MenuItem(
        'Historia', icon='book-fill', href='https://shorturl.at/cuIJN'),
    sac.MenuItem('Ubicación', icon='map', href='https://shorturl.at/ySTW8'),
    sac.MenuItem('Financiamiento',
                 icon='cash-coin',
                 href='https://shorturl.at/cuIJN',
                 children=[
                     sac.MenuItem('Empresa Sotic S.A.',
                                  icon='truck',
                                  href='https://shorturl.at/vwzT9'),
                     sac.MenuItem('Secretaría de Estado C.T.I. prov. Sta. Fe',
                                  icon='building-check',
                                  href='https://shorturl.at/xDX01'),
                     sac.MenuItem('Facultad Regional Santa Fe',
                                  icon='buildings',
                                  href='https://www.frsf.utn.edu.ar'),
                 ]),
    sac.MenuItem(
        'Aval',
        icon='Building-check',
        children=[
            sac.MenuItem('EPE Santa Fe',
                         icon='lightning-charge-fill',
                         href='https://www.epe.santafe.gov.ar/institucional/'),
            sac.MenuItem(
                'Energías Renovables, prov. Sta. Fe',
                icon='building-check',
                href=
                "https://www.argentina.gob.ar/economia/energia/energia-electrica/renovables"
            ),
        ]),
    sac.MenuItem(type='divider'),
    sac.MenuItem('Consultas', icon='send', disabled=True),
    sac.MenuItem(
        'Alumnos',
        type='group',
        children=[
            sac.MenuItem(
                'Dropsi, Pablo',
                icon='person-standing',
                href="https://es.wikipedia.org/wiki/Juan_Rom%C3%A1n_Riquelme"),
            sac.MenuItem('Ferreyra, Guillermo',
                         icon='person-standing',
                         href="https://es.wikipedia.org/wiki/Steven_Seagal"),
            sac.MenuItem('Montenegro, Angel',
                         icon='person-standing',
                         href="https://es.wikipedia.org/wiki/John_C._Reilly"),
            sac.MenuItem('Smith, Axel',
                         icon='person-standing ',
                         href="https://es.wikipedia.org/wiki/Lionel_Messi"),
        ]),
],
         format_func='title',
         size='large',
         indent=30,
         open_all=True,
         return_index=True)

sac.divider(icon='x-lg', align='center')

st.markdown("## Ecuaciones de Simulación")
# Agrega texto explicativo y ecuaciones según sea necesario

# Ecuación a mostrar la siguiente expresión obtiene la potencia eléctrica P (en kilo-Watt)
# obtenida por un GFV:
st.subheader("Potencia eléctrica obtenida por un Generador FV (kW)")
st.latex(r'P [kW] = N \cdot \frac{G}{G_{\text{std}}} \cdot P_{\text{pico}}' +
         r'\cdot \left[1 + k_p \cdot (T_c - T_r)\right] \eta \cdot 10^{-3}')

# Ecuación 2 a mostrar, La temperatura de la celda difiere de la temperatura ambiente:
st.subheader(
    "Temperatura de la celda al diferir de la Temperatura Ambiente (°C)")
st.latex(
    r'{T}_{c}=T+0,031 \left[ ^\circ C \cdot {m}_{}^{2} \right / W]\cdot G')

# Ecuación 3 a mostrar, Limites de Generacion
st.subheader("Límites de Generación Técnicos (kW)")
st.latex(r'{P}_{\min} [kW]= \frac{\mu (\%)}{100}\cdot {P}_{inv}')

st.latex(r'''{P}_{r} [kW]=  \left\{ \begin{array}{cl}
  0 & si \ P \leq {P}_{\min} \\
  P & si \ {P}_{\min} < P \leq {P}_{inv} \\
  {P}_{inv} & si \ {P}_{inv} < P
  \end{array} \right.''')

sac.divider(icon='x', align='center')

st.write("## Tabla anual 2019")
# Datos
tabla = pd.read_excel("Datos_climatologicos_Santa_Fe_2019.xlsx", index_col=0)
tabla

# dia = "2019-04-25 13:50"
temp = tabla.at[f'{dias.year}-{dias.month}-{dias.day} 12:00',
                "Temperatura (°C)"]
st.write(f"# Temperatura del {dias} al mediodía")
st.info(temp)

tab1, tab2 = st.tabs(['Datos mensuales', 'Datos diarios'])

with tab1:
  tabla_mes = tabla.loc[
      f'2019-{mes}-01 00:00':f'2019-{mes}-{dias_meses[mes-1]}-30 23:50', :]
  tabla_mes.loc[:, 'potencia (kW)'] = (N * tabla_mes['Irradiancia (W/m²)'] /
                                       Gstd * Ppico *
                                       (1 + kp *
                                        (tabla_mes['Temperatura (°C)'] - Tr)) *
                                       rend * 1e-3)

  st.line_chart(data=tabla_mes, y='potencia (kW)')
  st.write("# Tabla anual 2019 con potencia")
  tabla_mes

  st.write(f'# Tabla {nombre_mes} 2019 con temperatura')
  tabla_mes['Temperatura (°C)']
  st.line_chart(data=tabla_mes, y='Temperatura (°C)')

  ##

  # Calcular Pr acotado entre Pmin y Pinv
  tabla_mes['Pr (kW)'] = np.clip(tabla_mes['potencia (kW)'], 0, Pinv)

  # Graficar Potencia y Pr
  st.write("# Tabla anual 2019 con potencia disponible y potencia generada:")
  st.write(tabla_mes[['Temperatura (°C)', 'potencia (kW)', 'Pr (kW)']])
  st.write(f'# Grafico de potencia generada en {nombre_mes}')
  st.line_chart(data=tabla_mes, y='Pr (kW)')
##

with tab2:
  st.write('# Grafico temperatura diario')

  if isinstance(dias, datetime.date):
    tabla_dia = tabla.loc[f'{dias.year}-{dias.month}-{dias.day}', :]
    st.line_chart(data=tabla_dia, y='Temperatura (°C)')
  else:
    st.error("Rango de datos invalido")
