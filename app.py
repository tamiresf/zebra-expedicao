import streamlit as st
from supabase import create_client, Client

# Configuração de página com carregamento estático e rápido
st.set_page_config(
    page_title="Emissor Zebra",
    page_icon="🏷️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Conexão direta com Supabase
SUPABASE_URL = "https://tlknbjaaahfpbwjovyut.supabase.co"
SUPABASE_KEY = "sb_publishable_o1uxZ7iShu9Pk9_NLXlTVg_AP7wjf1T"

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = get_supabase()

st.subheader("🏷️ Expedição - Emissão de Etiquetas")

with st.form("form_coletor", clear_on_submit=True):
    transportadora = st.text_input("Transportadora")
    cliente = st.text_input("Cliente")
    numero_pedido = st.text_input("Número do Pedido")
    
    enviar = st.form_submit_button("IMPRIMIR ETIQUETA", use_container_width=True)

if enviar:
    t = transportadora.strip()
    c = cliente.strip()
    p = numero_pedido.strip()
    
    if not t or not c or not p:
        st.warning("Preencha todos os campos antes de enviar.")
    else:
        try:
            supabase.table("fila_impressao").insert({
                "transportadora": t,
                "cliente": c,
                "numero_pedido": p,
                "status": "PENDENTE"
            }).execute()
            st.success(f"Pedido {p} enviado para a impressora!")
        except Exception as e:
            st.error(f"Erro de envio: {e}")
