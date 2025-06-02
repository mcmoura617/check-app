import streamlit as st
import pandas as pd
import plotly.express as px
from gspread_pandas import Spread, Client
from google.oauth2.service_account import Credentials
import gspread_pandas as gp

# === Configuração da página ===
st.set_page_config(page_title="🏥 App Limpeza Hospitalar", layout="wide")
st.title("🏥 Controle Operacional - Setor de Limpeza")

# === Funções para carregar e salvar no Google Sheets ===
def conectar_planilha(sheet_name="Materiais"):
    try:
        scope = [
            'https://spreadsheets.google.com/feeds', 
            'https://www.googleapis.com/auth/drive', 
            'https://www.googleapis.com/auth/spreadsheets' 
        ]
        credentials = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gp.Client(creds=credentials)

        # Nome da planilha
        spreadsheet_name = "Controle Limpeza Hospitalar"

        # Conectar à planilha
        spread = Spread(spreadsheet_name, client=client)

        # Listar abas existentes
        existing_sheets = [sheet.title for sheet in spread.spread.worksheets()]

        if sheet_name not in existing_sheets:
            st.warning(f"⚠️ Aba '{sheet_name}' não encontrada. Criando nova aba...")
            spread.create_sheet(sheet_name)

        return spread
    except Exception as e:
        st.error(f"❌ Erro ao conectar à planilha: {e}")
        st.info("💡 Dica: Verifique se você ativou as APIs do Google Sheets e Drive no Google Cloud Console.")
        return None


def carregar_da_planilha(sheet_name="Materiais"):
    spread = conectar_planilha(sheet_name)
    if spread:
        try:
            df = spread.sheet_to_df(sheet=sheet_name)
            if not df.empty:
                st.success(f"✅ Dados carregados da aba '{sheet_name}'")
            else:
                st.info(f"ℹ️ Aba '{sheet_name}' está vazia.")
            return df
        except Exception as e:
            st.warning(f"⚠️ Erro ao carregar '{sheet_name}': {e}")
    return pd.DataFrame()


def salvar_no_sheets(df, sheet_name="Materiais"):
    if df.empty:
        st.warning(f"⚠️ Nenhum dado para salvar na aba '{sheet_name}'")
        return
    spread = conectar_planilha(sheet_name)
    if spread:
        try:
            spread.df_to_sheet(df, sheet=sheet_name, index=False, replace=True)
            st.success(f"✅ Dados salvos na aba '{sheet_name}'")
        except Exception as e:
            st.error(f"❌ Erro ao salvar na aba '{sheet_name}': {e}")


# === Tabs do app ===
tab1, tab2, tab3, tab4 = st.tabs([
    "📦 Lançamento de Materiais",
    "🧼 Checklist Atividades",
    "🚚 Checklist Carro Funcional",
    "📊 Painel de Monitoramento"
])

# === 1. Lançamento de Materiais ===
with tab1:
    st.header("📦 Lançamento de Materiais Utilizados")
    with st.form(key="form_material"):
        data_uso = st.date_input("📅 Data de Uso")
        setores = [
            "Área Externa", "Cme", "Recepção", "Térreo Ala Norte",
            "Térreo Ala Sul", "Cc", "Cos", "3º Andar", "4º Roll",
            "Uti Neo", "Ucinco", "Ucinca", "Uti Materna", "Ambulatório",
            "6º Norte", "6º Sul", "7º Norte", "7º Sul", "8º Norte",
            "8º Sul", "Subsolo", "Casa Da Gestante", "Resíduos",
            "Nutrição", "Lactário", "Lavanderia"
        ]
        setor = st.selectbox("📍 Selecione o Setor", options=setores)
        st.markdown("### 📄 Papéis")
        papel_bobina = st.number_input("P. Bobina", min_value=0, step=1, key="p_bobina")
        papel_higienico = st.number_input("P. Higiênico", min_value=0, step=1, key="p_higienico")
        papel_tolha = st.number_input("Papel Tolha", min_value=0, step=1, key="p_tolha")
        st.markdown("### 🛍️ Sacos")
        saco_30p = st.number_input("30p", min_value=0, step=1, key="saco_30p")
        saco_50p = st.number_input("50p", min_value=0, step=1, key="saco_50p")
        saco_100p = st.number_input("100p", min_value=0, step=1, key="saco_100p")
        saco_200p = st.number_input("200p", min_value=0, step=1, key="saco_200p")
        saco_50b = st.number_input("50b", min_value=0, step=1, key="saco_50b")
        saco_100b = st.number_input("100b", min_value=0, step=1, key="saco_100b")
        saco_200b = st.number_input("200b", min_value=0, step=1, key="saco_200b")
        saco_50v = st.number_input("50v", min_value=0, step=1, key="saco_50v")
        ramper = st.number_input("Ramber", min_value=0, step=1, key="ramper")
        st.markdown("### 🧼 Sabonetes")
        sabonete_neutro = st.number_input("Neutro", min_value=0, step=1, key="sabonete_neutro")
        sabonete_erva_doce = st.number_input("Erva Doce", min_value=0, step=1, key="sabonete_erva_doce")
        sabonete_clorexidina = st.number_input("Clorexidina", min_value=0, step=1, key="sabonete_clorexidina")
        alcool_gel = st.number_input("Álcool Gel", min_value=0, step=1, key="alcool_gel")
        alcool_70 = st.number_input("Álcool 70", min_value=0, step=1, key="alcool_70")
        st.markdown("### 🧴 Produtos")
        desinfetante = st.number_input("Desinfetante", min_value=0, step=1, key="desinfetante")
        hipoclorito = st.number_input("Hipoclorito", min_value=0, step=1, key="hipoclorito")
        peroxido = st.number_input("Peróxido", min_value=0, step=1, key="peroxido")
        detergente = st.number_input("Detergente", min_value=0, step=1, key="detergente")
        quartenario = st.number_input("Quartenário", min_value=0, step=1, key="quartenario")
        st.markdown("### 🥤 Copos")
        copo_150ml = st.number_input("150ml", min_value=0, step=1, key="copo_150ml")
        copo_50ml = st.number_input("50ml", min_value=0, step=1, key="copo_50ml")
        st.markdown("### 🧹 Mops")
        mop_umido = st.number_input("Úmido", min_value=0, step=1, key="mop_umido")
        mop_po = st.number_input("Pó", min_value=0, step=1, key="mop_po")
        submit_material = st.form_submit_button("💾 Salvar Registro")
        if submit_material:
            registros = []
            def adicionar_registro(item_nome, quantidade, tipo):
                if quantidade > 0:
                    registros.append({
                        "Data": str(data_uso),
                        "Setor": setor,
                        "Item": item_nome,
                        "Quantidade": quantidade,
                        "Tipo": tipo
                    })
            # Papéis
            adicionar_registro("P. Bobina", papel_bobina, "Papel")
            adicionar_registro("P. Higiênico", papel_higienico, "Papel")
            adicionar_registro("Papel Tolha", papel_tolha, "Papel")
            # Sacos
            adicionar_registro("30p", saco_30p, "Saco")
            adicionar_registro("50p", saco_50p, "Saco")
            adicionar_registro("100p", saco_100p, "Saco")
            adicionar_registro("200p", saco_200p, "Saco")
            adicionar_registro("50b", saco_50b, "Saco")
            adicionar_registro("100b", saco_100b, "Saco")
            adicionar_registro("200b", saco_200b, "Saco")
            adicionar_registro("50v", saco_50v, "Saco")
            adicionar_registro("Ramber", ramper, "Saco")
            # Sabonetes
            adicionar_registro("Neutro", sabonete_neutro, "Sabonete")
            adicionar_registro("Erva Doce", sabonete_erva_doce, "Sabonete")
            adicionar_registro("Clorexidina", sabonete_clorexidina, "Sabonete")
            adicionar_registro("Álcool Gel", alcool_gel, "Sabonete")
            adicionar_registro("Álcool 70", alcool_70, "Sabonete")
            # Produtos
            adicionar_registro("Desinfetante", desinfetante, "Produto")
            adicionar_registro("Hipoclorito", hipoclorito, "Produto")
            adicionar_registro("Peróxido", peroxido, "Produto")
            adicionar_registro("Detergente", detergente, "Produto")
            adicionar_registro("Quartenário", quartenario, "Produto")
            # Copos
            adicionar_registro("150ml", copo_150ml, "Copo")
            adicionar_registro("50ml", copo_50ml, "Copo")
            # Mops
            adicionar_registro("Úmido", mop_umido, "Mop")
            adicionar_registro("Pó", mop_po, "Mop")
            if registros:
                df_novo = pd.DataFrame(registros)
                salvar_no_sheets(df_novo, "Materiais")
            else:
                st.warning("⚠️ Nenhum item foi preenchido.")

# === 2. Checklist de Atividades por Setor ===
with tab2:
    st.header("🧼 Checklist Diário de Atividades")
    setores = [
        "Área Externa", "Cme", "Recepção", "Térreo Ala Norte",
        "Térreo Ala Sul", "Cc", "Cos", "3º Andar", "4º Roll",
        "Uti Neo", "Ucinco", "Ucinca", "Uti Materna", "Ambulatório",
        "6º Norte", "6º Sul", "7º Norte", "7º Sul", "8º Norte",
        "8º Sul", "Subsolo", "Casa Da Gestante", "Resíduos",
        "Nutrição", "Lactário", "Lavanderia"
    ]
    turno_opcoes = ["Manhã", "Tarde", "Noite"]
    col1, col2 = st.columns(2)
    with col1:
        setor_checklist = st.selectbox("📍 Selecione o Setor", setores)
    with col2:
        turno = st.selectbox("⏰ Selecione o Turno", turno_opcoes)
    data_checklist = st.date_input("📅 Data da Atividade")
    colaborador = st.text_input("🧑‍🔧 Colaborador(a) Responsável")
    st.subheader("🗂 Itens de Limpeza")
    coluna1, coluna2 = st.columns(2)
    itens = {
        "Pisos lavados e secos": False,
        "Superfícies desinfetadas": False,
        "Vidros limpos": False,
        "Cestos esvaziados e sacos trocados": False,
        "Áreas de passagem limpas": False,
        "Produtos reabastecidos": False,
        "Sinalização adequada": False,
        "Ferramentas organizadas": False,
        "Lixeiras higienizadas": False,
        "Portas e maçanetas limpas": False,
        "Banheiros limpos e abastecidos": False,
        "EPI's utilizados corretamente": False
    }
    respostas = {}
    for i, (item, default) in enumerate(itens.items()):
        if i < len(itens) // 2:
            with coluna1:
                respostas[item] = st.checkbox(item, value=default, key=f"c_{i}_check")
        else:
            with coluna2:
                respostas[item] = st.checkbox(item, value=default, key=f"c_{i}_col2_check")
    obs_checklist = st.text_area("📌 Observações Gerais")
    imagem_upload = st.file_uploader("📷 Faça upload de uma imagem (comprovante)", type=["jpg", "jpeg", "png"])
    if st.button("💾 Salvar Checklist", key="salvar_checklist"):
        df = pd.DataFrame({
            "Data": [str(data_checklist)],
            "Setor": [setor_checklist],
            "Turno": [turno],
            "Colaborador": [colaborador],
            **{k: [v] for k, v in respostas.items()},
            "Observação": [obs_checklist],
            "Imagem": [imagem_upload.name if imagem_upload else None]
        })
        salvar_no_sheets(df, "Checklist_Atividades")
        if imagem_upload:
            st.image(imagem_upload, caption="Comprovante Enviado", use_column_width=True)

# === 3. Checklist do Carro Funcional ===
with tab3:
    st.header("🚚 Checklist do Carro Funcional")
    setores_carro = setores.copy()
    data_carro = st.date_input("📅 Data do Checklist")
    setor_carro = st.selectbox("📍 Selecione o Setor", setores_carro, key="carro_setor_selectbox")
    st.subheader("🗂 Itens do Carro")
    col1, col2 = st.columns(2)
    itens_carro = {
        "Balde com água e sabão": False,
        "Esfregão (Lt)": False,
        "Cabo Mop Pó": False,
        "Cabo Mop Úmido": False,
        "Rodo": False,
        "Escova de vaso": False,
        "Placa de sinalização": False,
        "Pa coletora": False,
        "Carro limpo e organizado": False
    }
    respostas_carro = {}
    for i, (item, default) in enumerate(itens_carro.items()):
        if i < len(itens_carro) // 2:
            with col1:
                respostas_carro[item] = st.checkbox(item, value=default, key=f"c1_{i}")
        else:
            with col2:
                respostas_carro[item] = st.checkbox(item, value=default, key=f"c2_{i}")
    obs_carro = st.text_area("📌 Observações do Carro")
    imagem_upload_carro = st.file_uploader("📷 Faça upload de uma imagem (comprovante)", type=["jpg", "jpeg", "png"], key="carro_imagem")
    if st.button("💾 Salvar Checklist do Carro", key="salvar_carro_button"):
        df = pd.DataFrame({
            "Data": [str(data_carro)],
            "Setor": [setor_carro],
            **{k: [v] for k, v in respostas_carro.items()},
            "Observação": [obs_carro],
            "Imagem": [imagem_upload_carro.name if imagem_upload_carro else None]
        })
        salvar_no_sheets(df, "Checklist_Carros")
        if imagem_upload_carro:
            st.image(imagem_upload_carro, caption="Comprovante do Carro", use_column_width=True)

# === 4. Painel de Monitoramento ===
with tab4:
    st.header("📊 Painel de Monitoramento")
    
    try:
        # Inicializar session_state se não existir
        if 'filtro_mes' not in st.session_state:
            st.session_state['filtro_mes'] = "Todos"
        if 'filtro_setor' not in st.session_state:
            st.session_state['filtro_setor'] = "Todos"

        # Carregar dados das planilhas
        df_materiais = carregar_da_planilha("Materiais")
        df_checklist = carregar_da_planilha("Checklist_Atividades")
        df_carros = carregar_da_planilha("Checklist_Carros")

        # Filtros principais
        st.markdown("### 🔍 Filtros Gerais")
        col_filtro_mes, col_filtro_setor = st.columns(2)

        with col_filtro_mes:
            meses_disponiveis = ["Todos"]
            if not df_materiais.empty and "Data" in df_materiais.columns:
                df_materiais["Data"] = pd.to_datetime(df_materiais["Data"])
                df_materiais["Mês"] = df_materiais["Data"].dt.to_period('M').astype(str)
                meses_disponiveis += list(df_materiais["Mês"].unique())
            filtro_mes = st.selectbox("📅 Selecione o Mês", options=meses_disponiveis, key="filtro_mes_atualizado")
        
        with col_filtro_setor:
            setores_unicos = ["Todos"] + list(df_materiais["Setor"].unique()) if not df_materiais.empty and "Setor" in df_materiais.columns else ["Todos"]
            filtro_setor = st.selectbox("📍 Filtrar por Setor", options=setores_unicos, key="filtro_setor_atualizado")

        # Filtro por Item Específico
        if not df_materiais.empty:
            itens_unicos = ["Todos"] + list(df_materiais["Item"].unique())
            filtro_item = st.selectbox("🧾 Filtrar por Item", options=itens_unicos)

        # Aplicar filtros
        df_materiais_filtrado = df_materiais.copy()
        df_checklist_filtrado = df_checklist.copy()
        df_carros_filtrado = df_carros.copy()

        if not df_materiais_filtrado.empty:
            if filtro_mes != "Todos":
                df_materiais_filtrado = df_materiais_filtrado[df_materiais_filtrado["Mês"] == filtro_mes]
            if filtro_setor != "Todos":
                df_materiais_filtrado = df_materiais_filtrado[df_materiais_filtrado["Setor"] == filtro_setor]
            if 'filtro_item' in locals() and filtro_item != "Todos":
                df_materiais_filtrado = df_materiais_filtrado[df_materiais_filtrado["Item"] == filtro_item]

        # === Métricas Rápidas ===
        st.markdown("### 📊 Métricas Gerais")
        col_metrica1, col_metrica2, col_metrica3 = st.columns(3)

        total_materiais = df_materiais_filtrado["Quantidade"].sum() if not df_materiais_filtrado.empty else 0
        dias_distintos = df_materiais_filtrado["Data"].nunique() if not df_materiais_filtrado.empty else 1
        media_diaria = total_materiais / dias_distintos if dias_distintos > 0 else 0

        with col_metrica1:
            st.metric(label="📦 Total de Itens Utilizados", value=f"{total_materiais:,}")

        with col_metrica2:
            st.metric(label="🧮 Média Diária", value=f"{media_diaria:.1f}/dia")

        if not df_checklist.empty:
            colunas_atividades = [col for col in df_checklist.columns if col not in ['Data', 'Setor', 'Turno', 'Colaborador', 'Observação', 'Imagem']]
            df_checklist['Itens_Concluidos'] = df_checklist[colunas_atividades].sum(axis=1)
            df_checklist['Total_Itens'] = len(colunas_atividades)
            df_checklist['Percentual_Concluido'] = (df_checklist['Itens_Concluidos'] / df_checklist['Total_Itens']) * 100
            media_conclusao_checklist = df_checklist['Percentual_Concluido'].mean() if not df_checklist.empty else 0
        else:
            media_conclusao_checklist = 0

        with col_metrica3:
            st.metric(label="✅ % de Conclusão Checklist", value=f"{media_conclusao_checklist:.1f}%")

        # === Seção: Materiais Utilizados ===
        st.markdown("## 📦 Materiais Utilizados")
        if not df_materiais_filtrado.empty:
            col1, col2 = st.columns(2)

            with col1:
                resumo_tipo = df_materiais_filtrado.groupby("Item")["Quantidade"].sum().sort_values(ascending=False).reset_index()
                fig_item = px.bar(resumo_tipo, x="Item", y="Quantidade", title="🧾 Total de Cada Item Utilizado", text_auto=True)
                st.plotly_chart(fig_item, use_container_width=True)

            with col2:
                resumo_setor = df_materiais_filtrado.groupby("Setor")["Quantidade"].sum().reset_index()
                fig_setor = px.bar(resumo_setor, x="Setor", y="Quantidade", title="📍 Total de Itens por Setor", text_auto=True)
                st.plotly_chart(fig_setor, use_container_width=True)

            st.markdown("### 🧮 Resumo Consolidado - Itens como Colunas")
            df_pivot = df_materiais_filtrado.pivot_table(
                index=["Data", "Setor"],
                columns="Item",
                values="Quantidade",
                aggfunc="sum",
                fill_value=0
            ).reset_index()
            st.dataframe(df_pivot.sort_values(by="Data", ascending=False), use_container_width=True)
        else:
            st.info("ℹ️ Não há dados de materiais para exibir.")

        # === Seção: Checklist de Atividades ===
        st.markdown("## 📋 Checklist de Atividades")
        if not df_checklist.empty:
            col1, col2 = st.columns([2, 1])

            with col1:
                colunas_itens = [col for col in df_checklist.columns if col not in ['Data', 'Setor', 'Turno', 'Colaborador', 'Observação', 'Imagem']]
                df_checklist['Itens_Concluidos'] = df_checklist[colunas_itens].sum(axis=1)
                df_checklist['Total_Itens'] = len(colunas_itens)
                df_checklist['Percentual_Concluido'] = (df_checklist['Itens_Concluidos'] / df_checklist['Total_Itens']) * 100
                resumo_setor_check = df_checklist.groupby("Setor")["Percentual_Concluido"].mean().reset_index()
                fig_check_setor = px.bar(
                    resumo_setor_check,
                    x="Setor",
                    y="Percentual_Concluido",
                    title="📈 Média de Conclusão por Setor (%)",
                    text_auto=".1f",
                    range_y=[0, 100]
                )
                st.plotly_chart(fig_check_setor, use_container_width=True)

            with col2:
                st.markdown("📌 Registros do Checklist")
                st.dataframe(df_checklist[["Data", "Setor", "Turno", "Colaborador"]], use_container_width=True, height=300)
        else:
            st.info("ℹ️ Não há registros de checklist de atividades.")

        # === Seção: Checklist de Carros ===
        st.markdown("## 🚚 Checklist do Carro Funcional")
        if not df_carros.empty:
            col1, col2 = st.columns([1, 2])

            cols_carro = [col for col in df_carros.columns if col not in ['Data', 'Setor', 'Observação', 'Imagem']]
            df_carros['Itens_Concluidos'] = df_carros[cols_carro].sum(axis=1)
            df_carros['Total_Itens'] = len(cols_carro)
            df_carros['Percentual_Concluido'] = (df_carros['Itens_Concluidos'] / df_carros['Total_Itens']) * 100
            resumo_carro_setor = df_carros.groupby("Setor")["Percentual_Concluido"].mean().reset_index()

            with col1:
                st.markdown("🚚 % de Itens nos Carros")
                st.dataframe(resumo_carro_setor, use_container_width=True)

            with col2:
                st.markdown("📌 Registros do Checklist dos Carros")
                st.dataframe(df_carros[["Data", "Setor", "Observação"]], use_container_width=True, height=300)
        else:
            st.info("ℹ️ Não há registros de carros funcionais.")

    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar painel: {e}")