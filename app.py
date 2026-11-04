import streamlit as st
from supabase import create_client, Client

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

# Lista de transportadoras
LISTA_TRANSPORTADORAS = [
    "PAJUÇARA",
    "EDSON",
    "JAMEF",
    "PATRUS",
    "BRASPRESS",
    "CORREIOS",
    "DISCO",
    "OUTRA"
]

# Seleção da transportadora (fora do form para reagir imediatamente ao clique)
transp_selecionada = st.selectbox("Transportadora", LISTA_TRANSPORTADORAS)

# Exibe o campo manual APENAS se escolher "OUTRA"
transp_manual = ""
if transp_selecionada == "OUTRA":
    transp_manual = st.text_input("Digite o nome da transportadora:", placeholder="Nome da transportadora")

with st.form("form_coletor", clear_on_submit=True):
    cliente = st.text_input("Cliente", placeholder="Ex: Casa do Ferrador")
    numero_pedido = st.text_input("Número do Pedido", placeholder="Ex: 3050")
    
    enviar = st.form_submit_button("🖨️ IMPRIMIR ETIQUETA", use_container_width=True)

if enviar:
    # Define o nome final da transportadora
    if transp_selecionada == "OUTRA":
        t = transp_manual.strip().upper()
    else:
        t = transp_selecionada.strip().upper()

    c = cliente.strip().upper()
    p = numero_pedido.strip().upper()
    
    if not t or not c or not p:
        st.warning("Preencha todos os campos obrigatórios antes de enviar.")
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
