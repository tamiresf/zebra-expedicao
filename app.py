import streamlit as st
from supabase import create_client, Client

st.set_page_config(
    page_title="Emissor Zebra",
    page_icon="🏷️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

SUPABASE_URL = "https://tlknbjaaahfpbwjovyut.supabase.co"
SUPABASE_KEY = "sb_publishable_o1uxZ7iShu9Pk9_NLXlTVg_AP7wjf1T"

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = get_supabase()

st.subheader("🏷️ Expedição - Emissão de Etiquetas")

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

transp_selecionada = st.selectbox("Transportadora", LISTA_TRANSPORTADORAS)

transp_manual = ""
if transp_selecionada == "OUTRA":
    transp_manual = st.text_input("Qual transportadora?", placeholder="Digite o nome da transportadora")

with st.form("form_coletor", clear_on_submit=True):
    cliente = st.text_input("Cliente", placeholder="Ex: Casa do Ferrador")
    numero_pedido = st.text_input("Número do Pedido", placeholder="Ex: 3050")
    quantidade = st.number_input("Cópias (Opcional)", min_value=1, max_value=99, value=1, step=1)
    
    enviar = st.form_submit_button("🖨️ IMPRIMIR ETIQUETA", use_container_width=True)

if enviar:
    if transp_selecionada == "OUTRA":
        t = transp_manual.strip().upper()
    else:
        t = transp_selecionada.strip().upper()

    c = cliente.strip().upper()
    p = numero_pedido.strip().upper()
    q = int(quantidade) if quantidade else 1
    
    if not t:
        st.warning("Informe o nome da transportadora.")
    elif not c:
        st.warning("Informe o nome do cliente.")
    elif not p:
        st.warning("Informe o número do pedido.")
    else:
        try:
            dados = {
                "transportadora": t,
                "cliente": c,
                "numero_pedido": p,
                "quantidade": q,
                "status": "PENDENTE"
            }
            supabase.table("fila_impressao").insert(dados).execute()
            st.success(f"Pedido {p} ({q} cópias) enviado para a impressora!")
        except Exception as e:
            st.error(f"Erro de envio: {e}")
