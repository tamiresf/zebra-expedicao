import streamlit as st
from supabase import create_client, Client

# Configurações do Supabase
SUPABASE_URL = "https://tlknbjaaahfpbwjovyut.supabase.co"
SUPABASE_KEY = "sb_publishable_o1uxZ7iShu9Pk9_NLXlTVg_AP7wjf1T"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(
    page_title="Emissor Zebra", 
    page_icon="🏷️", 
    layout="centered"
)

st.title("🏷️ Expedição - Emissão de Etiquetas")
st.caption("Preencha os dados abaixo para imprimir na Zebra.")

with st.form("form_etiqueta", clear_on_submit=True):
    transportadora = st.text_input("Transportadora", placeholder="Ex: Pajucara, Jamef")
    cliente = st.text_input("Cliente", placeholder="Ex: Casa do Ferrador")
    numero_pedido = st.text_input("Número do Pedido", placeholder="Ex: 3050")
    
    botao_enviar = st.form_submit_button("🖨️ IMPRIMIR ETIQUETA", use_container_width=True)

if botao_enviar:
    if not transportadora or not cliente or not numero_pedido:
        st.error("Preencha todos os campos obrigatórios.")
    else:
        try:
            dados = {
                "transportadora": transportadora.strip(),
                "cliente": cliente.strip(),
                "numero_pedido": numero_pedido.strip(),
                "status": "PENDENTE"
            }
            supabase.table("fila_impressao").insert(dados).execute()
            st.success(f"Pedido {numero_pedido} enviado para a fila de impressão com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar na fila: {e}")
