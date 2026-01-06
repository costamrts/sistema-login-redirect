import streamlit as st
import pandas as pd
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
# layout="centered" deixa o login bonitinho no meio da tela
st.set_page_config(page_title="Acesso Restrito", page_icon="🔒", layout="centered")

# --- BANCO DE DADOS (Corrigido e Unificado) ---

# Tabela 1: Credenciais
dados_login = {
    "email": ["joao@teste.com", "maria@teste.com", "chefe@teste.com"],
    "senha": ["12345", "abcde", "admin"]
}
df_credenciais = pd.DataFrame(dados_login)

# Tabela 2: Destinos
dados_links = {
    "email": ["joao@teste.com", "maria@teste.com", "chefe@teste.com"],
    "link": [
        "https://www.youtube.com/@DanielLopez",      # Link do João
        "https://www.youtube.com/@Teatualizei",      # Link da Maria
        "https://www.youtube.com/@SaladeGuerraSdG"   # Link do Chefe
    ]
}
df_destinos = pd.DataFrame(dados_links)

# --- FUNÇÕES ---

def verificar_login(email, senha):
    """Verifica se email e senha batem com o banco de dados"""
    usuario = df_credenciais[df_credenciais['email'] == email]
    
    if not usuario.empty:
        senha_registrada = usuario.iloc[0]['senha']
        # Remove espaços em branco extras que podem causar erro
        if str(senha).strip() == str(senha_registrada).strip():
            return True
    return False

def pegar_link(email):
    """Busca o link específico do usuário"""
    destino = df_destinos[df_destinos['email'] == email]
    if not destino.empty:
        return destino.iloc[0]['link']
    return "https://www.google.com" # Fallback de segurança

def redirecionar_js(url):
    """
    Injeta JavaScript para forçar a mudança de página.
    Funciona melhor que st.switch_page para links externos.
    """
    js = f"""
        <script>
            window.top.location.href = "{url}";
        </script>
        <meta http-equiv="refresh" content="1;url={url}">
    """
    st.components.v1.html(js, height=0, width=0)

# --- TELA (FRONT-END) ---

st.title("🔒 Portal de Acesso")
st.markdown("Entre com suas credenciais para ser redirecionado.")

# Usar st.form evita que a página recarregue a cada letra digitada
with st.form("form_login"):
    email_digitado = st.text_input("E-mail", placeholder="seu@email.com")
    senha_digitada = st.text_input("Senha", type="password")
    
    # O botão de envio fica dentro do formulário
    botao_entrar = st.form_submit_button("Acessar Sistema", use_container_width=True)

# Lógica pós-clique
if botao_entrar:
    if verificar_login(email_digitado, senha_digitada):
        
        # 1. Busca o link
        link_final = pegar_link(email_digitado)
        
        # 2. Feedback visual
        st.success(f"Login aprovado! Redirecionando para: {link_final}")
        
        # 3. Botão de emergência (caso o automático falhe no navegador do usuário)
        st.link_button("👉 Clique aqui se não for redirecionado", link_final, type="primary")
        
        # 4. Aguarda e executa o redirecionamento automático
        time.sleep(2) # Tempo para o usuário ler a mensagem
        redirecionar_js(link_final)
        
    else:
        st.error("🚫 Acesso negado! Verifique usuário e senha.")