import streamlit as st
from supabase import create_client, Client

SUPABASE_URL = "https://tlknbjaaahfpbwjovyut.supabase.co"
SUPABASE_KEY = "sb_publishable_o1uxZ7iShu9Pk9_NLXlTVg_AP7wjf1T"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("🏷️ Expedição - Emissão de Etiquetas")

# Formulário com campos comuns de formulário
with st.form("form_zebra", clear_on_submit=True):
    transportadora = st.text_area("Transportadora", height=68, placeholder="Ex: Pajucara")
    cliente = st.text_area("Cliente", height=68, placeholder="Ex: Casa do Ferrador")
    numero_pedido = st.text_area("Número do Pedido", height=68, placeholder="Ex: 3050")
    
    enviar = st.form_submit_button("🖨️ IMPRIMIR ETIQUETA", use_container_width=True)

if enviar:
    if not transportadora.strip() or not cliente.strip() or not numero_pedido.strip():
        st.warning("Preencha todos os campos.")
    else:
        dados = {
            "transportadora": transportadora.strip(),
            "cliente": cliente.strip(),
            "numero_pedido": numero_pedido.strip(),
            "status": "PENDENTE"
        }
        supabase.table("fila_impressao").insert(dados).execute()
        st.success(f"Pedido {numero_pedido.strip()} enviado com sucesso!")
