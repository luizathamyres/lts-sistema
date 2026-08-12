import streamlit as st
from supabase import create_client

# Configuração da página
st.set_page_config(
    page_title="LTS Construtora",
    page_icon="🏗️",
    layout="wide"
)

# Conexão com o Supabase
SUPABASE_URL = "https://kmhnyticqfrgevcbatuw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImttaG55dGljcWZyZ2V2Y2JhdHV3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODY0ODg4ODEsImV4cCI6MjEwMjA2NDg4MX0.FUGbRuU7S_yV5DlPjSaALxTm4FvUFbLPYGKDj7m2hMo"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Menu lateral
st.sidebar.title("🏗️ LTS Construtora")
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

    # ── Aba: Novo Cliente
    with aba[0]:
        st.subheader("Cadastrar Novo Cliente")

        # Estado civil FORA do form para reagir imediatamente
        estado_civil = st.selectbox("Estado civil", [
            "Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)", "União estável"
        ])

        with st.form("form_cliente"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome completo *")
                cpf = st.text_input("CPF *")
                rg = st.text_input("RG")
                data_nascimento = st.date_input("Data de nascimento")
                telefone = st.text_input("Telefone *")
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

            # Dados do cônjuge — aparece automaticamente se casado
            conjuge_nome = conjuge_cpf = conjuge_rg = ""
            conjuge_profissao = conjuge_estado_civil = ""

            if estado_civil in ["Casado(a)", "União estável"]:
                st.markdown("---")
                st.markdown("**👫 Dados do Cônjuge**")
                col3, col4 = st.columns(2)
                with col3:
                    conjuge_nome = st.text_input("Nome do cônjuge")
                    conjuge_cpf = st.text_input("CPF do cônjuge")
                    conjuge_rg = st.text_input("RG do cônjuge")
                with col4:
                    conjuge_profissao = st.text_input("Profissão do cônjuge")
                    conjuge_estado_civil = st.text_input("Estado civil do cônjuge")

            observacoes = st.text_area("Observações")
            salvar = st.form_submit_button("💾 Salvar Cliente", use_container_width=True)

            if salvar:
                if not nome or not cpf or not telefone:
                    st.error("⚠️ Preencha os campos obrigatórios: Nome, CPF e Telefone.")
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
                resultado = supabase.table("clientes")\
                    .select("*")\
                    .ilike("nome", f"%{busca}%")\
                    .execute()

                if not resultado.data:
                    resultado = supabase.table("clientes")\
                        .select("*")\
                        .ilike("cpf", f"%{busca}%")\
                        .execute()

                if resultado.data:
                    for cliente in resultado.data:
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
                                st.write(f"**Data de nascimento:** {cliente.get('data_nascimento','—')}")
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
    st.info("Este módulo será desenvolvido em breve. Use o menu lateral para navegar.")
