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
        colaborador = st.text_input("🧑 Colaborador(a) Responsável")

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

        obs = st.text_area("📌 Observações")

        submit_material = st.form_submit_button("💾 Salvar Registro")

        if submit_material:
            registros = []

            # Papéis
            if papel_bobina > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "P. Bobina", "Quantidade": papel_bobina, "Colaborador": colaborador, "Tipo": "Papel", "Observação": obs})
            if papel_higienico > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "P. Higiênico", "Quantidade": papel_higienico, "Colaborador": colaborador, "Tipo": "Papel", "Observação": obs})
            if papel_tolha > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Papel Tolha", "Quantidade": papel_tolha, "Colaborador": colaborador, "Tipo": "Papel", "Observação": obs})

            # Sacos
            if saco_30p > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "30p", "Quantidade": saco_30p, "Colaborador": colaborador, "Tipo": "Saco", "Observação": obs})
            if saco_50p > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "50p", "Quantidade": saco_50p, "Colaborador": colaborador, "Tipo": "Saco", "Observação": obs})
            if saco_100p > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "100p", "Quantidade": saco_100p, "Colaborador": colaborador, "Tipo": "Saco", "Observação": obs})
            if saco_200p > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "200p", "Quantidade": saco_200p, "Colaborador": colaborador, "Tipo": "Saco", "Observação": obs})
            if saco_50b > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "50b", "Quantidade": saco_50b, "Colaborador": colaborador, "Tipo": "Saco", "Observação": obs})
            if saco_100b > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "100b", "Quantidade": saco_100b, "Colaborador": colaborador, "Tipo": "Saco", "Observação": obs})
            if saco_200b > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "200b", "Quantidade": saco_200b, "Colaborador": colaborador, "Tipo": "Saco", "Observação": obs})
            if saco_50v > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "50v", "Quantidade": saco_50v, "Colaborador": colaborador, "Tipo": "Saco", "Observação": obs})
            if ramper > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Ramber", "Quantidade": ramper, "Colaborador": colaborador, "Tipo": "Saco", "Observação": obs})

            # Sabonetes
            if sabonete_neutro > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Neutro", "Quantidade": sabonete_neutro, "Colaborador": colaborador, "Tipo": "Sabonete", "Observação": obs})
            if sabonete_erva_doce > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Erva Doce", "Quantidade": sabonete_erva_doce, "Colaborador": colaborador, "Tipo": "Sabonete", "Observação": obs})
            if sabonete_clorexidina > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Clorexidina", "Quantidade": sabonete_clorexidina, "Colaborador": colaborador, "Tipo": "Sabonete", "Observação": obs})
            if alcool_gel > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Álcool Gel", "Quantidade": alcool_gel, "Colaborador": colaborador, "Tipo": "Sabonete", "Observação": obs})
            if alcool_70 > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Álcool 70", "Quantidade": alcool_70, "Colaborador": colaborador, "Tipo": "Sabonete", "Observação": obs})

            # Produtos
            if desinfetante > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Desinfetante", "Quantidade": desinfetante, "Colaborador": colaborador, "Tipo": "Produto", "Observação": obs})
            if hipoclorito > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Hipoclorito", "Quantidade": hipoclorito, "Colaborador": colaborador, "Tipo": "Produto", "Observação": obs})
            if peroxido > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Peróxido", "Quantidade": peroxido, "Colaborador": colaborador, "Tipo": "Produto", "Observação": obs})
            if detergente > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Detergente", "Quantidade": detergente, "Colaborador": colaborador, "Tipo": "Produto", "Observação": obs})
            if quartenario > 0:
                registros.append({"Data": data_uso, "Setor": setor, "Item": "Quartenário", "Quantidade": quartenario, "Colaborador": colaborador, "Tipo": "Produto", "Observação": obs})

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


# Rodapé
st.sidebar.markdown("---")
st.sidebar.info("App criado para supervisão de limpeza hospitalar")