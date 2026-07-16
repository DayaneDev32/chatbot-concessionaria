import streamlit as st
import time
from database import obter_cliente, obter_fatura, obter_historico

# Configuração da página do navegador
st.set_page_config(page_title="EnergyBot - Atendimento", page_icon="⚡", layout="centered")

st.title("⚡ EnergyBot")
st.subheader("Assistente Virtual de Concessionária de Energia")
st.write("---")

# Inicializa o histórico de mensagens na tela
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {"role": "assistant", "content": "Olá! Eu sou o EnergyBot. Para começarmos o seu atendimento, por favor, digite o seu CPF abaixo:"}
    ]

# Exibe as mensagens antigas na tela
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Campo para o usuário interagir
if prompt := st.chat_input("Digite aqui..."):
    # Mostra a mensagem que o usuário digitou
    st.session_state.mensagens.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Processa a resposta do Bot com simulação de "digitando..."
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("*Digitando...*")
        time.sleep(1.5) # Simula o tempo de resposta humana

        # Limpa caracteres do CPF
        cpf_limpo = "".join(filter(str.isdigit, prompt))
        
        # Verifica se o que foi digitado parece um CPF
        if len(cpf_limpo) == 11:
            cliente = obter_cliente(cpf_limpo)
            if cliente:
                nome = cliente["nome"]
                status = cliente["status"]
                
                resposta = f"Olá, **{nome}**! Identifiquei seu cadastro no nosso sistema. \n\n"
                
                if status == "pendente":
                    fatura = obter_fatura(cpf_limpo)
                    resposta += f"⚠️ Consta uma fatura em aberto no valor de **R$ {fatura['valor']}** (Vencimento: {fatura['vencimento']}).\n\n"
                    resposta += f"🔑 **Linha Digitável para pagamento:**\n`{fatura['codigo_barras']}`"
                else:
                    historico = obter_historico(cpf_limpo)
                    resposta += f"✅ Seu status de fornecimento está: **NORMAL**.\n\n"
                    resposta += f"📊 **Histórico de consumo recente:**\n"
                    for mes, consumo in historico.items():
                        resposta += f"* **{mes}:** {consumo}\n"
            else:
                protocolo = f"PROT-{int(time.time())}"
                resposta = f"❌ **CPF não encontrado no sistema.**\n\n"
                resposta += f"Registramos uma solicitação de **Falta de Energia / Suporte** para a sua região.\n"
                resposta += f"📋 **Protocolo de atendimento técnico gerado:** `{protocolo}`\n"
                resposta += f"Nossa equipe de campo já foi acionada para verificar o local!"
        else:
            resposta = "Por favor, digite um CPF válido com 11 dígitos para que eu possa consultar seus dados."

        # Atualiza a tela com a resposta real
        placeholder.markdown(resposta)
        st.session_state.mensagens.append({"role": "assistant", "content": resposta})