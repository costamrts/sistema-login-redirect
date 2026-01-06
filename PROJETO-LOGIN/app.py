import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Acesso Restrito", page_icon="🔒", layout="centered")

# --- BANCO DE DADOS ---
dados_login = {
    "email": ["joao@teste.com", "maria@teste.com", "chefe@teste.com"],
    "senha": ["12345", "abcde", "admin"]
}
df_credenciais = pd.DataFrame(dados_login)

dados_links = {
    "email": ["joao@teste.com", "maria@teste.com", "chefe@teste.com"],
    "link": [
        "https://www.youtube.com/@DanielLopez",
        "https://www.youtube.com/@Teatualizei",
        "https://www.youtube.com/@SaladeGuerraSdG"
    ]
}
df_destinos = pd.DataFrame(dados_links)

# --- FUNÇÕES ---
def validar_usuario(email, senha):
    """Retorna o Link se válido, ou None se inválido"""
    usuario = df_credenciais[df_credenciais['email'] == email]
    if not usuario.empty:
        senha_registrada = usuario.iloc[0]['senha']
        if str(senha).strip() == str(senha_registrada).strip():
            # Busca o link
            destino = df_destinos[df_destinos['email'] == email]
            if not destino.empty:
                return destino.iloc[0]['link']
            return "https://www.google.com"
    return None

# --- TELA (FRONT-END) ---
st.title("🔒 Login Direto")
st.write("Digite seus dados. Se estiverem corretos, o botão de acesso aparecerá.")

# 1. Inputs (Sem st.form para validar enquanto digita)
email = st.text_input("E-mail")
senha = st.text_input("Senha", type="password")

# 2. Validação em Tempo Real
link_final = validar_usuario(email, senha)

# 3. O "Botão Mágico"
if link_final:
    # SE A SENHA ESTIVER CERTA:
    st.success("Credenciais Válidas! Pode entrar.")
    # Este botão JÁ É o link. Clicou, abriu. Sem espera.
    st.link_button("🚀 ACESSAR SISTEMA AGORA", link_final, type="primary", use_container_width=True)
else:
    # SE A SENHA ESTIVER ERRADA OU VAZIA:
    # Mostra um botão falso desabilitado só para visual
    st.button("Aguardando credenciais...", disabled=True, use_container_width=True)
    if senha: # Só avisa erro se o cara já digitou algo
        st.warning("Verificando dados...")