# main.py
import time
import random
from database import CLIENTES

def limpar_tela():
    # Simula a rolagem de mensagens no terminal
    print("\n" * 3)

def enviar_mensagem(texto, delay=1):
    """Simula o tempo de digitação de um bot real"""
    print(f"🤖 Bot: {texto}")
    time.sleep(delay)

def buscar_cliente_por_cpf(cpf):
    # Remove pontos e traços para evitar que pequenos erros travem a busca
    cpf_limpo = cpf.replace(".", "").replace("-", "").strip()
    
    if len(cpf_limpo) != 11:
        return None
        
    # Formata de volta para o padrão "xxx.xxx.xxx-xx" usado no dicionário
    cpf_formatado = f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
    return CLIENTES.get(cpf_formatado)

def menu_principal(cliente):
    while True:
        limpar_tela()
        enviar_mensagem(f"Olá, {cliente['nome']}! Como posso te ajudar hoje?", delay=0.5)
        print("\nDigite o número da opção desejada:")
        print("[1] - 📄 2ª Via de Fatura")
        print("[2] - 🔌 Informar Falta de Energia")
        print("[3] - 📊 Histórico de Consumo")
        print("[0] - 🚪 Sair do Atendimento")
        
        opcao = input("\nSua opção: ").strip()
        
        if opcao == "1":
            fluxo_segunda_via(cliente)
        elif opcao == "2":
            fluxo_falta_energia(cliente)
        elif opcao == "3":
            fluxo_historico(cliente)
        elif opcao == "0":
            enviar_mensagem("Obrigado por entrar em contato. Tenha um ótimo dia! 👋")
            break
        else:
            enviar_mensagem("⚠️ Opção inválida. Escolha uma opção do menu.")
            time.sleep(2)

def fluxo_segunda_via(cliente):
    limpar_tela()
    enviar_mensagem("Buscando suas faturas pendentes... 🔍", delay=1.5)
    fatura = cliente["fatura_pendente"]
    
    if fatura:
        enviar_mensagem(f"Encontrei uma fatura pendente de **{fatura['mes']}**.")
        enviar_mensagem(f"Valor: R$ {fatura['valor']:.2f}")
        enviar_mensagem("Aqui está o código de barras para pagamento: 👇")
        print(f"\n{fatura['codigo_barras']}\n")
    else:
        enviar_mensagem("Parabéns! Não encontrei nenhuma fatura pendente. Conta em dia! ✅")
    
    input("\nPressione [ENTER] para voltar ao menu principal...")

def fluxo_falta_energia(cliente):
    limpar_tela()
    enviar_mensagem(f"Entendido. Registrando ocorrência para o endereço: {cliente['endereco']}")
    enviar_mensagem("Nossa equipe técnica de campo já foi alertada. 🛠️", delay=1)
    
    protocolo = random.randint(100000, 999999)
    enviar_mensagem(f"Protocolo de atendimento: #{protocolo}")
    enviar_mensagem("Previsão para normalização: em até 4 horas.")
    
    input("\nPressione [ENTER] para voltar ao menu principal...")

def fluxo_historico(cliente):
    limpar_tela()
    enviar_mensagem("Buscando seu histórico de consumo recente: 📈", delay=1)
    for i, consumo in enumerate(cliente["historico_consumo"], 1):
        print(f"  • Mês {i}: {consumo}")
    
    input("\nPressione [ENTER] para voltar ao menu principal...")

def iniciar_atendimento():
    limpar_tela()
    print("="*45)
    print("      💡 BEM-VINDO À CONCESSIONÁRIA LUZ-TECH 💡      ")
    print("="*45)
    enviar_mensagem("Olá! Sou o assistente virtual de atendimento.")
    
    tentativas = 0
    while tentativas < 3:
        cpf_digitado = input("\nPor favor, digite seu CPF para iniciar o atendimento: ")
        cliente = buscar_cliente_por_cpf(cpf_digitado)
        
        if cliente:
            menu_principal(cliente)
            break
        else:
            tentativas += 1
            enviar_mensagem(f"⚠️ CPF não encontrado. (Tentativa {tentativas} de 3)")
            
    if tentativas == 3:
        enviar_mensagem("Número de tentativas excedido. Atendimento encerrado. Tente novamente mais tarde.")

if __name__ == "__main__":
    iniciar_atendimento()