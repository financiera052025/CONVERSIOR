import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora USDT", layout="centered")
st.title("💰 Conversión USDT Personal")

# Función para cargar y limpiar datos
@st.cache_data
def cargar_y_limpiar(archivo):
    df = pd.read_csv(archivo)
    # Convertimos a numérico, lo que no sea número se vuelve NaN y lo eliminamos
    df['MONTO EN USDT'] = pd.to_numeric(df['MONTO EN USDT'], errors='coerce')
    return df.dropna(subset=['MONTO EN USDT'])

try:
    df_bancamiga = cargar_y_limpiar('bancamiga.csv')
    df_venezuela = cargar_y_limpiar('venezuela.csv')
    
    banco = st.selectbox("Selecciona el Banco:", ["Bancamiga", "Venezuela"])
    monto = st.number_input("Ingresa el monto en USDT:", min_value=0.0, format="%.2f")

    if st.button("Calcular"):
        datos = df_bancamiga if banco == "Bancamiga" else df_venezuela
        # Buscar el monto más cercano
        datos['diff'] = (datos['MONTO EN USDT'] - monto).abs()
        fila = datos.loc[datos['diff'].idxmin()]
        
        st.success(f"Resultados para {monto} USDT:")
        col1, col2 = st.columns(2)
        col1.metric("Monto Final (Bs)", f"{fila['MONTO FINAL EN BS']:,.2f}")
        col2.metric("Margen Ganancia", f"{fila['MARGEN DE GANACIA']:,.2f}")
        st.write(f"Tasa P2P utilizada: {fila['P2P']}")

except Exception as e:
    st.error(f"Error cargando archivos: {e}")
