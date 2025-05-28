import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações da página
st.set_page_config(page_title="📊 Analisador de Dados", layout="wide")

# Título e descrição
st.title("📊 App Profissional de Análise de Dados")
st.markdown("Faça upload de um arquivo CSV e explore os dados com gráficos interativos!")

# Sidebar
st.sidebar.header("⚙️ Opções")
st.sidebar.write("Use esta barra para controlar as visualizações.")

# Upload de arquivo
uploaded_file = st.sidebar.file_uploader("📤 Faça upload de um arquivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Mostrar dados brutos
        st.subheader("📂 Dados Carregados")
        st.dataframe(df.head())

        # Tabs para organizar conteúdo
        tab1, tab2, tab3 = st.tabs(["📈 Gráfico de Barras", "📉 Gráfico de Linha", "📊 Estatísticas"])

        with tab1:
            st.subheader("Gráfico de Barras")
            coluna = st.selectbox("Selecione a coluna para o gráfico de barras:", df.columns)
            if df[coluna].dtype != 'O':  # Apenas numéricas
                fig, ax = plt.subplots()
                sns.barplot(x=df.index[:50], y=df[coluna][:50], ax=ax)
                st.pyplot(fig)
            else:
                st.warning("Escolha uma coluna numérica para o gráfico de barras.")

        with tab2:
            st.subheader("Gráfico de Linha")
            coluna_linha = st.selectbox("Selecione a coluna para o gráfico de linha:", df.columns, key="linha")
            if df[coluna_linha].dtype != 'O':
                st.line_chart(df[coluna_linha].head(50))
            else:
                st.warning("Escolha uma coluna numérica para o gráfico de linha.")

        with tab3:
            st.subheader("Estatísticas Descritivas")
            st.write(df.describe(include='all'))

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")

else:
    st.info("⏳ Aguardando upload de um arquivo CSV...")

# Rodapé
st.sidebar.markdown("---")
st.sidebar.info("App criado com 💻 e Streamlit")