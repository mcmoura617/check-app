import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="🏥 App Limpeza Hospitalar", layout="wide")
st.title("🏥 Controle Operacional - Setor de Limpeza")

# Tabs do app
tab1, tab2, tab3, tab4 = st.tabs([
    "📦 Lançamento de Materiais",
    "🧼 Checklist Atividades",
    "🚚 Checklist Carro Funcional",
    "📊 Painel de Monitoramento"
])

# Função para salvar dados em CSV
def salvar_dados(df, arquivo):
    if not os.path.exists(arquivo):
        df.to_csv(arquivo, index=False)
    else:
        df_existente = pd.read_csv(arquivo)
        df_final = pd.concat([df_existente, df], ignore_index=True)
        df_final.to_csv(arquivo, index=False)

# === 1. Formulário de Lançamento de Materiais ===
with tab1:
    st.header("Lançamento de Materiais Utilizados")

    with st.form(key="form_material"):
        data_uso = st.date_input("Data de Uso")
        setor = st.selectbox("Setor", ["Pré-parto", "Parto", "Recuperação", "Berçário", "UTI Neonatal"])
        produto = st.text_input("Produto Utilizado")
        quantidade = st.number_input("Quantidade", min_value=1, step=1)
        colaborador = st.text_input("Colaborador(a)")
        obs = st.text_area("Observações")

        submit_material = st.form_submit_button("Salvar Registro")

        if submit_material:
            df = pd.DataFrame({
                "Data": [data_uso],
                "Setor": [setor],
                "Produto": [produto],
                "Quantidade": [quantidade],
                "Colaborador": [colaborador],
                "Observação": [obs]
            })
            salvar_dados(df, "dados_materiais.csv")
            st.success("✅ Registro salvo com sucesso!")

# === 2. Checklist de Atividades por Setor ===
with tab2:
    st.header("Checklist Diário de Atividades")

    setor_checklist = st.selectbox("Selecione o Setor", [
        "Pré-parto", "Parto", "Recuperação", "Berçário", "UTI Neonatal"
    ])
    data_checklist = st.date_input("Data da Atividade")

    st.subheader("Itens de Limpeza")
    col1, col2 = st.columns(2)

    itens = {
        "Pisos lavados e secos": False,
        "Superfícies desinfetadas": False,
        "Vidros limpos": False,
        "Cestos esvaziados e sacos trocados": False,
        "Áreas de passagem limpas": False,
        "Produtos reabastecidos": False,
        "Sinalização adequada": False,
        "Ferramentas organizadas": False,
    }

    respostas = {}
    for i, (item, default) in enumerate(itens.items()):
        if i < len(itens) // 2:
            with col1:
                respostas[item] = st.checkbox(item, value=default)
        else:
            with col2:
                respostas[item] = st.checkbox(item, value=default)

    obs_checklist = st.text_area("Observações Gerais")

    if st.button("Salvar Checklist de Atividades"):
        df = pd.DataFrame({
            "Data": [data_checklist],
            "Setor": [setor_checklist],
            **{k: [v] for k, v in respostas.items()},
            "Observação": [obs_checklist]
        })
        salvar_dados(df, "checklists_atividades.csv")
        st.success("✅ Checklist salvo com sucesso!")

# === 3. Checklist do Carro Funcional ===
with tab3:
    st.header("Checklist do Carro Funcional")

    numero_carro = st.selectbox("Número do Carro", ["01", "02", "03", "04", "05"])
    data_carro = st.date_input("Data do Checklist")

    st.subheader("Itens do Carro")
    col1, col2 = st.columns(2)

    itens_carro = {
        "Balde com água e sabão": False,
        "Esfregão": False,
        "Panôs de chão": False,
        "Rodos e espátulas": False,
        "Luvas descartáveis": False,
        "Máscara e avental": False,
        "Desinfetante pronto uso": False,
        "Álcool gel": False,
        "Sacos plásticos": False,
        "Pinça para coleta": False,
        "Bolsa de lixo contaminado": False,
        "Carro limpo e organizado": False
    }

    respostas_carro = {}
    for i, (item, default) in enumerate(itens_carro.items()):
        if i < len(itens_carro) // 2:
            with col1:
                respostas_carro[item] = st.checkbox(item, key=f"c1_{i}", value=default)
        else:
            with col2:
                respostas_carro[item] = st.checkbox(item, key=f"c2_{i}", value=default)

    obs_carro = st.text_area("Observações do Carro")

    if st.button("Salvar Checklist do Carro"):
        df = pd.DataFrame({
            "Data": [data_carro],
            "Carro Número": [numero_carro],
            **{k: [v] for k, v in respostas_carro.items()},
            "Observação": [obs_carro]
        })
        salvar_dados(df, "checklists_carros.csv")
        st.success("✅ Checklist do carro salvo com sucesso!")

# === 4. Painel de Monitoramento ===
with tab4:
    st.header("📊 Resumo Operacional")

    try:
        df_materiais = pd.read_csv("dados_materiais.csv")
        df_atividades = pd.read_csv("checklists_atividades.csv")
        df_carros = pd.read_csv("checklists_carros.csv")

        st.subheader("Registros de Materiais")
        st.dataframe(df_materiais.tail())

        st.subheader("Atividades Realizadas")
        st.dataframe(df_atividades[["Data", "Setor"]].tail())

        st.subheader("Carros Verificados")
        st.dataframe(df_carros[["Data", "Carro Número"]].tail())

    except Exception as e:
        st.warning("⚠️ Ainda não há registros armazenados.")

---

# Rodapé
st.sidebar.markdown("---")
st.sidebar.info("App criado para supervisão de limpeza hospitalar")