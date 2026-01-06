import streamlit as st
import pandas as pd
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Acesso Restrito", page_icon="🔒")

# --- BANCO DE DADOS SIMULADO (DataFrames) ---

# Tabela 1: Credenciais (Quem pode entrar)
dados_login = {
    "email": ["joao@teste.com", "joaquim@teste.com", "chefe@teste.com"],
    "senha": ["12345", "abcde", "admin"]
}
df_credenciais = pd.DataFrame(dados_login)

# Tabela 2: Destinos (Para onde cada um vai)
# Note que aqui não tem senha, só o email para cruzar a informação
dados_links = {
    "email": ["joao@teste.com", "maria@teste.com", "chefe@teste.com"],
    "link": [
        "https://www.youtube.com/@DanielLopez",  # Link do João
        "https://www.youtube.com/@Teatualizei",     # Link da Maria
        "https://www.youtube.com/@SaladeGuerraSdG"          # Link do Chefe
    ]
}
df_destinos = pd.DataFrame(dados_links)

# --- FUNÇÕES ---

def verificar_login(email, senha):
    # Procura o usuário na Tabela 1
    usuario = df_credenciais[df_credenciais['email'] == email]
    
    if not usuario.empty:
        # Se achou, verifica a senha
        senha_registrada = usuario.iloc[0]['senha']
        if str(senha) == str(senha_registrada):
            return True
    return False

def pegar_link(email):
    # Procura o link na Tabela 2
    destino = df_destinos[df_destinos['email'] == email]
    if not destino.empty:
        return destino.iloc[0]['link']
    return "https://www.google.com" # Link padrão de segurança

def redirecionar(url):
    # Truque em HTML/JS para redirecionar
    html = f'<meta http-equiv="refresh" content="0; url={url}"><script>window.location.href = "{url}";</script>'
    st.markdown(html, unsafe_allow_html=True)

# --- TELA (FRONT-END) ---

st.title("🔒 Login de Redirecionamento")

with st.form("meu_form"):
    email_digitado = st.text_input("E-mail")
    senha_digitada = st.text_input("Senha", type="password")
    botao = st.form_submit_button("Entrar")

if botao:
    if verificar_login(email_digitado, senha_digitada):
        st.success("Login aprovado! Redirecionando...")
        
        # Busca o link na segunda tabela
        link_final = pegar_link(email_digitado)
        
        # Mostra link manual caso o automático falhe
        st.write(f"Se não for automático, [clique aqui]({link_final})")
        
        # Espera um pouquinho e redireciona
        time.sleep(1)
        redirecionar(link_final)
    else:
        st.error("Usuário ou senha incorretos.")