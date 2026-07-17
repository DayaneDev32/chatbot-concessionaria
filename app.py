import streamlit as st
import time
from database import obter_cliente, obter_fatura, obter_historico

# Configuração da página do navegador
st.set_page_config(page_title="EnergyBot - Atendimento")

st.title("⚡ EnergyBot")
st.subheader("Assistente Virtual de Concessionária de Energia")
st.write("---")

# Inicializa o histórico de mensagens na tela
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {"role": "assistant", "content": "Olá! Eu sou o EnergyBot. Para começarmos o seu atendimento, por favor, digite o seu CPF abaixo:"}
    ]

# Guarda o cliente identificado durante a conversa
if "cliente_atual" not in st.session_state:
    st.session_state.cliente_atual = None

# Guarda o CPF limpo do cliente identificado (para reusar nas funções de fatura/histórico)
if "cpf_atual" not in st.session_state:
    st.session_state.cpf_atual = None

# Exibe as mensagens antigas na tela
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Campo para o usuário interagir
if prompt := st.chat_input("Digite aqui..."):
    st.session_state.mensagens.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    resposta = ""

    # ETAPA 1: ainda não identificamos o cliente -> tenta ler como CPF
    if st.session_state.cliente_atual is None:
        cpf_limpo = "".join(filter(str.isdigit, prompt))

        if len(cpf_limpo) == 11:
            cliente = obter_cliente(cpf_limpo)

            if cliente:
                # Guarda o cliente na sessão para as próximas mensagens
                st.session_state.cliente_atual = cliente
                st.session_state.cpf_atual = cpf_limpo

                resposta = (
                    f"Olá, **{cliente['nome']}**! Identifiquei seu cadastro no nosso sistema.\n\n"
                    f"✅ Seu status de fornecimento está: **{cliente['status'].upper() if cliente['status'] == 'pendente' else 'NORMAL'}**.\n\n"
                    "O que você gostaria de consultar?\n\n"
                    "- Digite **fatura** para ver a fatura pendente\n"
                    "- Digite **histórico** para ver o consumo recente\n"
                    "- Digite **suporte** para reportar falta de energia"
                )
            else:
                # CPF não encontrado -> abre protocolo de suporte
                protocolo = f"PROT-{int(time.time())}"
                resposta = (
                    "❌ **CPF não encontrado no sistema.**\n\n"
                    "Registramos uma solicitação de **Falta de Energia / Suporte** para a sua região. "
                    f"📋 **Protocolo de atendimento técnico gerado:** `{protocolo}` "
                    "Nossa equipe de campo já foi acionada para verificar o local!"
                )
        else:
            resposta = "Por favor, digite um CPF válido com 11 dígitos para que eu possa consultar seus dados."

    # ETAPA 2: cliente já identificado -> trata o menu de opções
    else:
        opcao = prompt.strip().lower()
        cliente = st.session_state.cliente_atual
        cpf_atual = st.session_state.cpf_atual

        if "fatura" in opcao:
            fatura = obter_fatura(cpf_atual)
            if fatura:
                resposta = (
                    f"🧾 **Fatura pendente — {fatura['mes']}**\n\n"
                    f"Valor: **R$ {fatura['valor']:.2f}**\n\n"
                    f"Código de barras: `{fatura['codigo_barras']}`"
                )
            else:
                resposta = "✅ Você não possui faturas pendentes. Está tudo em dia!"

        elif "histórico" in opcao or "historico" in opcao:
            historico = obter_historico(cpf_atual)
            if historico:
                linhas = "\n".join([f"- **{mes}**: {consumo}" for mes, consumo in historico.items()])
                resposta = f"📊 **Histórico de consumo recente:**\n\n{linhas}"
            else:
                resposta = "Não encontrei histórico de consumo para o seu cadastro."

        elif "suporte" in opcao or "falta" in opcao or "energia" in opcao:
            protocolo = f"PROT-{int(time.time())}"
            resposta = (
                "Registramos uma solicitação de **Falta de Energia / Suporte** para a sua região. "
                f"📋 **Protocolo de atendimento técnico gerado:** `{protocolo}` "
                "Nossa equipe de campo já foi acionada para verificar o local!"
            )

        else:
            resposta = (
                "Não entendi sua solicitação. Você pode digitar:\n\n"
                "- **fatura** — para ver a fatura pendente\n"
                "- **histórico** — para ver o consumo recente\n"
                "- **suporte** — para reportar falta de energia"
            )

    with st.chat_message("assistant"):
        st.write(resposta)

    st.session_state.mensagens.append({"role": "assistant", "content": resposta})