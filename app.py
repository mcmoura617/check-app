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
    st.header("📦 Lançamento de Materiais Utilizados")

    with st.form(key="form_material"):
        data_uso = st.date_input("📅 Data de Uso")

        # Setores
        setores = [
            "Área Externa", "Cme", "Recepção", "Térreo Ala Norte",
            "Térreo Ala Sul", "Cc", "Cos", "3º Andar", "4º Roll",
            "Uti Neo", "Ucinco", "Ucinca", "Uti Materna", "Ambulatório",
            "6º Norte", "6º Sul", "7º Norte", "7º Sul", "8º Norte",
            "8º Sul", "Subsolo", "Casa Da Gestante", "Resíduos",
            "Nutrição", "Lactário", "Lavanderia"
        ]
        setor = st.selectbox("📍 Selecione o Setor", setores)

        st.markdown("---")
        st.subheader("🗂 Itens Utilizados")

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

            # Papéis
            if papel_bobina > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "P. Bobina", "Quantidade": papel_bobina, "Tipo": "Papel"})
            if papel_higienico > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "P. Higiênico", "Quantidade": papel_higienico, "Tipo": "Papel"})
            if papel_tolha > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Papel Tolha", "Quantidade": papel_tolha, "Tipo": "Papel"})

            # Sacos
            if saco_30p > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "30p", "Quantidade": saco_30p, "Tipo": "Saco"})
            if saco_50p > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "50p", "Quantidade": saco_50p, "Tipo": "Saco"})
            if saco_100p > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "100p", "Quantidade": saco_100p, "Tipo": "Saco"})
            if saco_200p > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "200p", "Quantidade": saco_200p, "Tipo": "Saco"})
            if saco_50b > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "50b", "Quantidade": saco_50b, "Tipo": "Saco"})
            if saco_100b > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "100b", "Quantidade": saco_100b, "Tipo": "Saco"})
            if saco_200b > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "200b", "Quantidade": saco_200b, "Tipo": "Saco"})
            if saco_50v > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "50v", "Quantidade": saco_50v, "Tipo": "Saco"})
            if ramper > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Ramber", "Quantidade": ramper, "Tipo": "Saco"})

            # Sabonetes
            if sabonete_neutro > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Neutro", "Quantidade": sabonete_neutro, "Tipo": "Sabonete"})
            if sabonete_erva_doce > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Erva Doce", "Quantidade": sabonete_erva_doce, "Tipo": "Sabonete"})
            if sabonete_clorexidina > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Clorexidina", "Quantidade": sabonete_clorexidina, "Tipo": "Sabonete"})
            if alcool_gel > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Álcool Gel", "Quantidade": alcool_gel, "Tipo": "Sabonete"})
            if alcool_70 > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Álcool 70", "Quantidade": alcool_70, "Tipo": "Sabonete"})

            # Produtos
            if desinfetante > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Desinfetante", "Quantidade": desinfetante, "Tipo": "Produto"})
            if hipoclorito > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Hipoclorito", "Quantidade": hipoclorito, "Tipo": "Produto"})
            if peroxido > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Peróxido", "Quantidade": peroxido, "Tipo": "Produto"})
            if detergente > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Detergente", "Quantidade": detergente, "Tipo": "Produto"})
            if quartenario > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Quartenário", "Quantidade": quartenario, "Tipo": "Produto"})

            # Copos
            if copo_150ml > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "150ml", "Quantidade": copo_150ml, "Tipo": "Copo"})
            if copo_50ml > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "50ml", "Quantidade": copo_50ml, "Tipo": "Copo"})

            # Mops
            if mop_umido > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Úmido", "Quantidade": mop_umido, "Tipo": "Mop"})
            if mop_po > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Pó", "Quantidade": mop_po, "Tipo": "Mop"})

            if registros:
                df_novo = pd.DataFrame(registros)
                salvar_dados(df_novo, "dados_materiais.csv")
                st.success(f"✅ {len(registros)} registro(s) salvos com sucesso!")
            else:
                st.warning("⚠️ Nenhum item foi preenchido com quantidade maior que zero.")

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
    st.header("📊 Painel de Monitoramento")

    try:
        # Carregar dados do CSV
        df_materiais = pd.read_csv("dados_materiais.csv")

        # Aplicar estilo ao cabeçalho
        st.markdown("""
        <style>
        .titulo-tabela {
            background-color: #0078D4;
            color: white;
            padding: 10px;
            font-weight: bold;
            border-radius: 5px;
        }
        </style>
        """, unsafe_allow_html=True)

        # Filtros interativos
        st.markdown('<div class="titulo-tabela">🔍 Filtros</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            filtro_data = st.date_input("Selecione a Data", value=None)
        with col2:
            filtro_setor = st.selectbox("Selecione o Setor", options=["Todos"] + list(df_materiais["Setor"].unique()))
        with col3:
            filtro_item = st.selectbox("Selecione o Item", options=["Todos"] + list(df_materiais["Item"].unique()))

        # Aplicar filtros
        df_filtrado = df_materiais.copy()

        if filtro_data:
            df_filtrado = df_filtrado[df_filtrado["Data"] == str(filtro_data)]
        if filtro_setor != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Setor"] == filtro_setor]
        if filtro_item != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Item"] == filtro_item]

        # Tabela Editável
        st.markdown('<div class="titulo-tabela">📋 Registros de Materiais</div>', unsafe_allow_html=True)
        editor_df = st.data_editor(df_filtrado.sort_values(by="Data", ascending=False).reset_index(drop=True), key="editor_1", num_rows="dynamic")
        
        # Salvar alterações feitas no editor (opcional)
        if st.button("💾 Salvar Alterações"):
            editor_df.to_csv("dados_materiais.csv", index=False)
            st.success("✅ Alterações salvas!")

        # Agrupamento: Itens como colunas, datas/setores como linhas
        st.markdown('<div class="titulo-tabela">🧮 Resumo Consolidado - Itens como Colunas</div>', unsafe_allow_html=True)

        # Pivot table: Linhas = Data/Setor, Colunas = Item, Valores = Quantidade
        df_pivot = df_filtrado.pivot_table(
            index=["Data", "Setor"],
            columns="Item",
            values="Quantidade",
            aggfunc="sum",
            fill_value=0
        ).reset_index()

        st.dataframe(df_pivot)

        # Gráfico de barras dos totais por item
        st.markdown('<div class="titulo-tabela">📈 Total de Itens Utilizados</div>', unsafe_allow_html=True)
        resumo_tipo = df_filtrado.groupby("Item")["Quantidade"].sum().reset_index()
        st.bar_chart(resumo_tipo.set_index("Item"))

    except FileNotFoundError:
        st.warning("⚠️ Ainda não há registros armazenados.")