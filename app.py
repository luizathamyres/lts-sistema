import streamlit as st
from supabase import create_client
from datetime import date

st.set_page_config(
    page_title="LTS - Sistema de gestão",
    page_icon="🏗️",
    layout="wide"
)

SUPABASE_URL = "https://kmhnyticqfrgevcbatuw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImttaG55dGljcWZyZ2V2Y2JhdHV3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODY0ODg4ODEsImV4cCI6MjEwMjA2NDg4MX0.FUGbRuU7S_yV5DlPjSaALxTm4FvUFbLPYGKDj7m2hMo"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def formatar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) <= 3:
        return cpf
    elif len(cpf) <= 6:
        return f"{cpf[:3]}.{cpf[3:]}"
    elif len(cpf) <= 9:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:]}"
    else:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"

def formatar_telefone(tel):
    tel = ''.join(filter(str.isdigit, tel))
    if len(tel) <= 2:
        return f"({tel}"
    elif len(tel) <= 3:
        return f"({tel[:2]}) {tel[2:]}"
    elif len(tel) <= 7:
        return f"({tel[:2]}) {tel[2:3]} {tel[3:]}"
    elif len(tel) <= 11:
        return f"({tel[:2]}) {tel[2:3]} {tel[3:7]}-{tel[7:]}"
    else:
        return f"({tel[:2]}) {tel[2:3]} {tel[3:7]}-{tel[7:11]}"

st.sidebar.title("LUIZA THAMYRES | Construções e Serviços🏗️")
st.sidebar.markdown("---")

menu = st.sidebar.selectbox("Navegação", [
    "🏠 Início",
    "👥 Clientes",
    "🏗️ Construtora",
    "📋 Serviços Rápidos",
    "📦 Estoque",
    "📊 Relatórios"
])

# ══════════════════════════════════════════════
# PÁGINA INICIAL
# ══════════════════════════════════════════════
if menu == "🏠 Início":
    st.title("🏗️ LTS Construtora — Sistema de Gestão")
    st.markdown("---")

    try:
        total_clientes = len(supabase.table("clientes").select("id").execute().data)
    except:
        total_clientes = "—"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Clientes", total_clientes)
    with col2:
        st.metric("Obras em Andamento", "—")
    with col3:
        st.metric("Serviços Ativos", "—")

    st.info("Selecione uma opção no menu lateral para começar.")

# ══════════════════════════════════════════════
# MÓDULO CLIENTES
# ══════════════════════════════════════════════
elif menu == "👥 Clientes":
    st.title("👥 Cadastro de Clientes")
    st.markdown("---")

    aba = st.tabs(["➕ Novo Cliente", "🔍 Buscar Cliente", "📋 Todos os Clientes"])

    with aba[0]:
        st.subheader("Cadastrar Novo Cliente")

        estado_civil = st.selectbox("Estado civil", [
            "Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)", "União estável"
        ])

        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome completo *")

            cpf_raw = st.text_input("CPF * (somente números)", max_chars=11,
                                     placeholder="00000000000")
            cpf = formatar_cpf(cpf_raw)
            if cpf_raw:
                st.caption(f"✅ CPF: **{cpf}**")

            rg = st.text_input("RG")

            data_nascimento = st.date_input(
                "Data de nascimento",
                value=date(1990, 1, 1),
                min_value=date(1900, 1, 1),
                max_value=date.today(),
                format="DD/MM/YYYY"
            )

            tel_raw = st.text_input("Telefone * (somente números)", max_chars=11,
                                     placeholder="00900000000")
            telefone = formatar_telefone(tel_raw)
            if tel_raw:
                st.caption(f"✅ Telefone: **{telefone}**")

            email = st.text_input("E-mail")

        with col2:
            profissao = st.text_input("Profissão")
            escolaridade = st.selectbox("Grau de escolaridade", [
                "Fundamental incompleto", "Fundamental completo",
                "Médio incompleto", "Médio completo",
                "Superior incompleto", "Superior completo", "Pós-graduação"
            ])
            endereco = st.text_input("Endereço")
            cidade = st.text_input("Cidade")

        conjuge_nome = conjuge_cpf = conjuge_rg = ""
        conjuge_profissao = conjuge_estado_civil = conjuge_telefone = ""

        if estado_civil in ["Casado(a)", "União estável"]:
            st.markdown("---")
            st.markdown("**👫 Dados do Cônjuge**")
            col3, col4 = st.columns(2)
            with col3:
                conjuge_nome = st.text_input("Nome do cônjuge")

                conjuge_cpf_raw = st.text_input("CPF do cônjuge (somente números)",
                                                 max_chars=11, placeholder="00000000000")
                conjuge_cpf = formatar_cpf(conjuge_cpf_raw)
                if conjuge_cpf_raw:
                    st.caption(f"✅ CPF cônjuge: **{conjuge_cpf}**")

                conjuge_rg = st.text_input("RG do cônjuge")

            with col4:
                conjuge_profissao = st.text_input("Profissão do cônjuge")
                conjuge_estado_civil = st.text_input("Estado civil do cônjuge")

                conjuge_tel_raw = st.text_input("Telefone do cônjuge (somente números)",
                                                 max_chars=11, placeholder="00900000000")
                conjuge_telefone = formatar_telefone(conjuge_tel_raw)
                if conjuge_tel_raw:
                    st.caption(f"✅ Telefone cônjuge: **{conjuge_telefone}**")

        observacoes = st.text_area("Observações")
        st.markdown("---")

        if st.button("💾 Salvar Cliente", use_container_width=True, type="primary"):
            if not nome or not cpf_raw or not tel_raw:
                st.error("⚠️ Preencha os campos obrigatórios: Nome, CPF e Telefone.")
            elif len(cpf_raw) < 11:
                st.error("⚠️ CPF incompleto — digite os 11 números.")
            elif len(tel_raw) < 10:
                st.error("⚠️ Telefone incompleto — digite DDD + número.")
            else:
                try:
                    dados = {
                        "nome": nome,
                        "cpf": cpf,
                        "rg": rg,
                        "data_nascimento": str(data_nascimento),
                        "telefone": telefone,
                        "email": email,
                        "estado_civil": estado_civil,
                        "profissao": profissao,
                        "escolaridade": escolaridade,
                        "endereco": endereco,
                        "cidade": cidade,
                        "conjuge_nome": conjuge_nome,
                        "conjuge_cpf": conjuge_cpf,
                        "conjuge_rg": conjuge_rg,
                        "conjuge_profissao": conjuge_profissao,
                        "conjuge_estado_civil": conjuge_estado_civil,
                        "observacoes": observacoes
                    }
                    supabase.table("clientes").insert(dados).execute()
                    st.success(f"✅ Cliente **{nome}** cadastrado com sucesso!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")

    # ── Aba: Buscar Cliente
    with aba[1]:
        st.subheader("🔍 Buscar Cliente por CPF ou Nome")
        busca = st.text_input("Digite o CPF ou nome do cliente")

        if busca:
            try:
                todos = supabase.table("clientes").select("*").execute().data
                resultado = [
                    c for c in todos
                    if busca.lower() in c.get("nome", "").lower()
                    or busca in c.get("cpf", "")
                ]

                if resultado:
                    st.success(f"{len(resultado)} cliente(s) encontrado(s)")
                    for cliente in resultado:
                        with st.expander(f"👤 {cliente['nome']} — CPF: {cliente['cpf']}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Telefone:** {cliente.get('telefone','—')}")
                                st.write(f"**E-mail:** {cliente.get('email','—')}")
                                st.write(f"**Estado civil:** {cliente.get('estado_civil','—')}")
                                st.write(f"**Profissão:** {cliente.get('profissao','—')}")
                                st.write(f"**Escolaridade:** {cliente.get('escolaridade','—')}")
                            with col2:
                                st.write(f"**RG:** {cliente.get('rg','—')}")
                                st.write(f"**Nascimento:** {cliente.get('data_nascimento','—')}")
                                st.write(f"**Endereço:** {cliente.get('endereco','—')}")
                                st.write(f"**Cidade:** {cliente.get('cidade','—')}")
                            if cliente.get('conjuge_nome'):
                                st.markdown("---")
                                st.markdown("**👫 Cônjuge:**")
                                col3, col4 = st.columns(2)
                                with col3:
                                    st.write(f"**Nome:** {cliente.get('conjuge_nome','—')}")
                                    st.write(f"**CPF:** {cliente.get('conjuge_cpf','—')}")
                                    st.write(f"**RG:** {cliente.get('conjuge_rg','—')}")
                                with col4:
                                    st.write(f"**Profissão:** {cliente.get('conjuge_profissao','—')}")
                                    st.write(f"**Estado civil:** {cliente.get('conjuge_estado_civil','—')}")
                            if cliente.get('observacoes'):
                                st.markdown(f"**Observações:** {cliente.get('observacoes')}")
                else:
                    st.warning("Nenhum cliente encontrado.")
            except Exception as e:
                st.error(f"Erro na busca: {e}")

    # ── Aba: Todos os Clientes
    with aba[2]:
        st.subheader("📋 Lista de Clientes Cadastrados")
        try:
            todos = supabase.table("clientes")\
                .select("nome, cpf, telefone, cidade, estado_civil, profissao")\
                .order("nome")\
                .execute()
            if todos.data:
                st.dataframe(todos.data, use_container_width=True)
                st.caption(f"Total: {len(todos.data)} cliente(s) cadastrado(s)")
            else:
                st.info("Nenhum cliente cadastrado ainda.")
        except Exception as e:
            st.error(f"Erro ao carregar clientes: {e}")

# ══════════════════════════════════════════════
# MÓDULOS EM CONSTRUÇÃO
# ══════════════════════════════════════════════
else:
    st.title("🚧 Módulo em construção")
    st.info("Este módulo será desenvolvido em breve.")
