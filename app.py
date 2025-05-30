import streamlit as st
import pandas as pd
import plotly.express as px
from gspread_pandas import Spread, Client

# Configuração da página
st.set_page_config(page_title="🏥 App Limpeza Hospitalar", layout="wide")
st.title("🏥 Controle Operacional - Setor de Limpeza")

# === Funções para carregar e salvar dados no Google Sheets ===
def conectar_planilha(sheet_name):
    spread = Spread(sheet_name)
    return spread

def carregar_dados(sheet_name):
    try:
        spread = conectar_planilha(sheet_name)
        df = spread.sheet_to_df()
        if not df.empty:
            if "Data" in df.columns:
                df["Data"] = pd.to_datetime(df["Data"], errors='coerce')
        return df
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar '{sheet_name}': {e}")
        return pd.DataFrame()

def salvar_dados(df, sheet_name):
    try:
        spread = conectar_planilha(sheet_name)
        spread.df_to_sheet(df, index=False, sheet=sheet_name, replace=True)
        st.success(f"✅ Dados salvos na aba '{sheet_name}'")
    except Exception as e:
        st.error(f"❌ Erro ao salvar na aba '{sheet_name}': {e}")

# Abas do app
tab1, tab2, tab3, tab4 = st.tabs([
    "📦 Lançamento de Materiais",
    "🧼 Checklist Atividades",
    "🚚 Checklist Carro Funcional",
    "📊 Painel de Monitoramento"
])

# === 1. Formulário de Lançamento de Materiais ===
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
        setor = st.selectbox("📍 Selecione o Setor", setores)

        # Papéis
        st.markdown("### 📄 Papéis")
        papel_bobina = st.number_input("P. Bobina", min_value=0, step=1, key="p_bobina")
        papel_higienico = st.number_input("P. Higiênico", min_value=0, step=1, key="p_higienico")
        papel_tolha = st.number_input("Papel Tolha", min_value=0, step=1, key="p_tolha")

        # Sacos
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

        # Sabonetes
        st.markdown("### 🧼 Sabonetes")
        sabonete_neutro = st.number_input("Neutro", min_value=0, step=1, key="sabonete_neutro")
        sabonete_erva_doce = st.number_input("Erva Doce", min_value=0, step=1, key="sabonete_erva_doce")
        sabonete_clorexidina = st.number_input("Clorexidina", min_value=0, step=1, key="sabonete_clorexidina")
        alcool_gel = st.number_input("Álcool Gel", min_value=0, step=1, key="alcool_gel")
        alcool_70 = st.number_input("Álcool 70", min_value=0, step=1, key="alcool_70")

        # Produtos
        st.markdown("### 🧴 Produtos")
        desinfetante = st.number_input("Desinfetante", min_value=0, step=1, key="desinfetante")
        hipoclorito = st.number_input("Hipoclorito", min_value=0, step=1, key="hipoclorito")
        peroxido = st.number_input("Peróxido", min_value=0, step=1, key="peroxido")
        detergente = st.number_input("Detergente", min_value=0, step=1, key="detergente")
        quartenario = st.number_input("Quartenário", min_value=0, step=1, key="quartenario")

        # Copos
        st.markdown("### 🥤 Copos")
        copo_150ml = st.number_input("150ml", min_value=0, step=1, key="copo_150ml")
        copo_50ml = st.number_input("50ml", min_value=0, step=1, key="copo_50ml")

        # Mops
        st.markdown("### 🧹 Mops")
        mop_umido = st.number_input("Úmido", min_value=0, step=1, key="mop_umido")
        mop_po = st.number_input("Pó", min_value=0, step=1, key="mop_po")

        submit_material = st.form_submit_button("💾 Salvar Registro")

        if submit_material:
            registros = []

            def adicionar_registro(registros, item, tipo):
                if item > 0:
                    registros.append({
                        "Data": data_uso,
                        "Setor": setor,
                        "Item": item_nome,
                        "Quantidade": item_valor,
                        "Tipo": tipo
                    })

            # Papéis
            for item_nome, item_valor in {
                "P. Bobina": papel_bobina,
                "P. Higiênico": papel_higienico,
                "Papel Tolha": papel_tolha
            }.items():
                if item_valor > 0:
                    registros.append({"Data": data_uso, "Setor": setor, "Item": item_nome, "Quantidade": item_valor, "Tipo": "Papel"})

            # Sacos
            for item_nome, item_valor in {
                "30p": saco_30p,
                "50p": saco_50p,
                "100p": saco_100p,
                "200p": saco_200p,
                "50b": saco_50b,
                "100b": saco_100b,
                "200b": saco_200b,
                "50v": saco_50v,
                "Ramber": ramper
            }.items():
                if item_valor > 0:
                    registros.append({"Data": data_uso, "Setor": setor, "Item": item_nome, "Quantidade": item_valor, "Tipo": "Saco"})

            # Sabonetes
            for item_nome, item_valor in {
                "Neutro": sabonete_neutro,
                "Erva Doce": sabonete_erva_doce,
                "Clorexidina": sabonete_clorexidina,
                "Álcool Gel": alcool_gel,
                "Álcool 70": alcool_70
            }.items():
                if item_valor > 0:
                    registros.append({"Data": data_uso, "Setor": setor, "Item": item_nome, "Quantidade": item_valor, "Tipo": "Sabonete"})

            # Produtos
            for item_nome, item_valor in {
                "Desinfetante": desinfetante,
                "Hipoclorito": hipoclorito,
                "Peróxido": peroxido,
                "Detergente": detergente,
                "Quartenário": quartenario
            }.items():
                if item_valor > 0:
                    registros.append({"Data": data_uso, "Setor": setor, "Item": item_nome, "Quantidade": item_valor, "Tipo": "Produto"})

            # Copos
            for item_nome, item_valor in {
                "150ml": copo_150ml,
                "50ml": copo_50ml
            }.items():
                if item_valor > 0:
                    registros.append({"Data": data_uso, "Setor": setor, "Item": item_nome, "Quantidade": item_valor, "Tipo": "Copo"})

            # Mops
            for item_nome, item_valor in {
                "Úmido": mop_umido,
                "Pó": mop_po
            }.items():
                if item_valor > 0:
                    registros.append({"Data": data_uso, "Setor": setor, "Item": item_nome, "Quantidade": item_valor, "Tipo": "Mop"})

            if registros:
                df_novo = pd.DataFrame(registros)
                salvar_dados(df_novo, "Materiais")
                st.success(f"✅ {len(registros)} registro(s) salvos com sucesso!")
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

    st.subheader("✅ Itens de Limpeza")
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
        "EPI's utilizados corretamente": False,
    }

    respostas = {}
    for i, (item, default) in enumerate(itens.items()):
        if i < len(itens) // 2:
            with coluna1:
                respostas[item] = st.checkbox(item, value=default, key=f"check_{i}")
        else:
            with coluna2:
                respostas[item] = st.checkbox(item, value=default, key=f"check_{i}_col2")

    obs_checklist = st.text_area("📌 Observações Gerais")
    imagem_upload = st.file_uploader("📷 Faça upload de uma imagem (comprovante)", type=["jpg", "jpeg", "png"])

    if st.button("💾 Salvar Checklist"):
        df = pd.DataFrame({
            "Data": [data_checklist],
            "Setor": [setor_checklist],
            "Turno": [turno],
            "Colaborador": [colaborador],
            **{k: [v] for k, v in respostas.items()},
            "Observação": [obs_checklist],
            "Imagem": [imagem_upload.name if imagem_upload else None]
        })
        salvar_dados(df, "Checklist_Atividades")

        if imagem_upload:
            st.image(imagem_upload, caption="Comprovante Enviado", use_column_width=True)

# === 3. Checklist do Carro Funcional ===
with tab3:
    st.header("🚚 Checklist do Carro Funcional")

    setores = [
        "Área Externa", "Cme", "Recepção", "Térreo Ala Norte",
        "Térreo Ala Sul", "Cc", "Cos", "3º Andar", "4º Roll",
        "Uti Neo", "Ucinco", "Ucinca", "Uti Materna", "Ambulatório",
        "6º Norte", "6º Sul", "7º Norte", "7º Sul", "8º Norte",
        "8º Sul", "Subsolo", "Casa Da Gestante", "Resíduos",
        "Nutrição", "Lactário", "Lavanderia"
    ]

    data_carro = st.date_input("📅 Data do Checklist")
    setor_carro = st.selectbox("📍 Selecione o Setor", setores, key="carro_setor_selectbox")

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
            "Data": [data_carro],
            "Setor": [setor_carro],
            **{k: [v] for k, v in respostas_carro.items()},
            "Observação": [obs_carro],
            "Imagem": [imagem_upload_carro.name if imagem_upload_carro else None]
        })
        salvar_dados(df, "Checklist_Carros")
        st.success("✅ Checklist do carro salvo com sucesso!")

        if imagem_upload_carro:
            st.image(imagem_upload_carro, caption="Comprovante do Carro", use_column_width=True)

# === 4. Painel de Monitoramento ===
with tab4:
    st.header("📊 Painel de Monitoramento")

    # Inicializar variáveis do session_state para evitar erro
    if 'filtro_mes' not in st.session_state:
        st.session_state['filtro_mes'] = "Todos"
    if 'filtro_setor' not in st.session_state:
        st.session_state['filtro_setor'] = "Todos"
    if 'filtro_item' not in st.session_state:
        st.session_state['filtro_item'] = "Todos"

    try:
        # Carregar dados das planilhas
        df_materiais = carregar_dados("Materiais")
        df_checklist = carregar_dados("Checklist_Atividades")
        df_carros = carregar_dados("Checklist_Carros")

        # Filtro por mês, setor e item
        st.markdown('<div class="titulo-tabela">📅 Filtros</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            meses_disponiveis = ["Todos"]
            if not df_materiais.empty:
                df_materiais["Data"] = pd.to_datetime(df_materiais["Data"])
                meses_disponiveis += list(df_materiais["Data"].dt.to_period('M').astype(str).unique())
            filtro_mes = st.selectbox("Selecione o Mês", options=meses_disponiveis, key="filtro_mes_atualizado")

        with col2:
            setores_unicos = ["Todos"] + list(df_materiais["Setor"].unique()) if not df_materiais.empty and "Setor" in df_materiais.columns else ["Todos"]
            filtro_setor = st.selectbox("📍 Selecione o Setor", options=setores_unicos, key="filtro_setor_atualizado")

        with col3:
            itens_unicos = ["Todos"] + list(df_materiais["Item"].unique()) if not df_materiais.empty and "Item" in df_materiais.columns else ["Todos"]
            filtro_item = st.selectbox("📦 Selecione o Item", options=itens_unicos, key="filtro_item_atualizado")

        # Filtrar dados com base nos filtros
        df_materiais_filtrado = df_materiais.copy()
        df_checklist_filtrado = df_checklist.copy()
        df_carros_filtrado = df_carros.copy()

        if not df_materiais_filtrado.empty:
            df_materiais_filtrado["Data"] = pd.to_datetime(df_materiais_filtrado["Data"], errors='coerce')
            df_materiais_filtrado = df_materiais_filtrado[df_materiais_filtrado["Data"].notna()]
            df_materiais_filtrado["Mês"] = df_materiais_filtrado["Data"].dt.to_period('M').astype(str)

            if filtro_mes != "Todos":
                df_materiais_filtrado = df_materiais_filtrado[df_materiais_filtrado["Mês"] == filtro_mes]
            if filtro_setor != "Todos":
                df_materiais_filtrado = df_materiais_filtrado[df_materiais_filtrado["Setor"] == filtro_setor]
            if filtro_item != "Todos":
                df_materiais_filtrado = df_materiais_filtrado[df_materiais_filtrado["Item"] == filtro_item]

        # Gráfico de quantidade por itens
        st.markdown('<div class="titulo-tabela">🧾 Materiais Utilizados</div>', unsafe_allow_html=True)
        if not df_materiais_filtrado.empty:
            resumo_tipo = df_materiais_filtrado.groupby("Item")["Quantidade"].sum().sort_values(ascending=False).reset_index()
            fig_item = px.bar(resumo_tipo, x="Item", y="Quantidade", title="📦 Total de Cada Item Utilizado", text_auto=True)
            st.plotly_chart(fig_item, use_container_width=True)

            resumo_setor = df_materiais_filtrado.groupby("Setor")["Quantidade"].sum().reset_index()
            fig_setor = px.bar(resumo_setor, x="Setor", y="Quantidade", title="📍 Total de Itens por Setor", text_auto=True)
            st.plotly_chart(fig_setor, use_container_width=True)

            df_pivot = df_materiais_filtrado.pivot_table(
                index=["Data", "Setor"],
                columns="Item",
                values="Quantidade",
                aggfunc="sum",
                fill_value=0
            ).reset_index()
            st.markdown('<div class="titulo-tabela">🧮 Resumo Consolidado - Itens como Colunas</div>', unsafe_allow_html=True)
            st.dataframe(df_pivot.sort_values(by="Data", ascending=False), use_container_width=True)
        else:
            st.info("ℹ️ Não há registros de materiais.")

        # Checklist de atividades
        st.markdown('<div class="titulo-tabela">📋 Checklist de Atividades</div>', unsafe_allow_html=True)
        if not df_checklist_filtrado.empty:
            colunas_itens = [col for col in df_checklist_filtrado.columns if col not in ['Data', 'Setor', 'Turno', 'Colaborador', 'Observação', 'Imagem', 'Mês']]
            df_checklist_filtrado['Itens_Concluidos'] = df_checklist_filtrado[colunas_itens].sum(axis=1)
            df_checklist_filtrado['Total_Itens'] = len(colunas_itens)
            df_checklist_filtrado['Percentual_Concluido'] = (df_checklist_filtrado['Itens_Concluidos'] / df_checklist_filtrado['Total_Itens']) * 100

            resumo_setor_check = df_checklist_filtrado.groupby("Setor")["Percentual_Concluido"].mean().reset_index()
            fig_check_setor = px.bar(
                resumo_setor_check,
                x="Setor",
                y="Percentual_Concluido",
                title="📈 Média de Conclusão por Setor (%)",
                text_auto=".1f",
                range_y=[0, 100]
            )
            st.plotly_chart(fig_check_setor, use_container_width=True)

            st.markdown('<div class="titulo-tabela">📌 Registros do Checklist de Atividades</div>', unsafe_allow_html=True)
            st.dataframe(df_checklist_filtrado[["Data", "Setor", "Turno", "Colaborador", "Observação"]], use_container_width=True)

        else:
            st.info("ℹ️ Não há registros de checklist de atividades.")

        # Checklist de carros
        st.markdown('<div class="titulo-tabela">🚚 Checklist do Carro Funcional</div>', unsafe_allow_html=True)
        if not df_carros_filtrado.empty:
            cols_carro = [col for col in df_carros_filtrado.columns if col not in ['Data', 'Setor', 'Observação', 'Imagem', 'Mês']]
            df_carros_filtrado['Itens_Concluidos'] = df_carros_filtrado[cols_carro].sum(axis=1)
            df_carros_filtrado['Total_Itens'] = len(cols_carro)
            df_carros_filtrado['Percentual_Concluido'] = (df_carros_filtrado['Itens_Concluidos'] / df_carros_filtrado['Total_Itens']) * 100

            resumo_carro_setor = df_carros_filtrado.groupby("Setor")["Percentual_Concluido"].mean().reset_index()
            fig_carro_setor = px.bar(
                resumo_carro_setor,
                x="Setor",
                y="Percentual_Concluido",
                title="🚚 Percentual de Itens Concluídos no Carro por Setor (%)",
                text_auto=".1f",
                range_y=[0, 100]
            )
            st.plotly_chart(fig_carro_setor, use_container_width=True)

            st.markdown('<div class="titulo-tabela">📝 Registros do Checklist dos Carros</div>', unsafe_allow_html=True)
            st.dataframe(df_carros_filtrado[["Data", "Setor", "Observação"]], use_container_width=True)

        else:
            st.info("ℹ️ Não há registros de carros funcionais.")

    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar painel: {e}")