
# database.py

# Simulação de banco de dados da concessionária de energia

CLIENTES = {
    "123.456.789-00": {
        "nome": "João Silva",
        "codigo_unico": "852147",
        "endereco": "Rua das Flores, 123",
        "fatura_pendente": {
            "mes": "Junho/2026",
            "valor": 187.50,
            "codigo_barras": "34191.79001 01043.513184 91020.150008 7 97560000018750"
        },
        "historico_consumo": ["150 kWh", "165 kWh", "140 kWh"]
    },
    "987.654.321-11": {
        "nome": "Maria Souza",
        "codigo_unico": "963258",
        "endereco": "Av. Brasil, 456",
        "fatura_pendente": None,
        "historico_consumo": ["210 kWh", "195 kWh", "245 kWh"]
    }
}



def _limpar_cpf(cpf):
    """Remove pontuação do CPF, mantendo só os números"""
    return "".join(filter(str.isdigit, cpf))


def _buscar_chave_cpf(cpf_busca):
    """Encontra a chave original no dicionário CLIENTES comparando só os números"""
    cpf_busca_limpo = _limpar_cpf(cpf_busca)
    for chave in CLIENTES:
        if _limpar_cpf(chave) == cpf_busca_limpo:
            return chave
    return None


def obter_cliente(cpf):
    """Busca um cliente pelo CPF"""
    chave = _buscar_chave_cpf(cpf)
    if chave:
        cliente = CLIENTES[chave]
        status = "pendente" if cliente["fatura_pendente"] else "pago"
        return {
            "nome": cliente["nome"],
            "status": status
        }
    return None


def obter_fatura(cpf):
    """Busca a fatura pendente do cliente"""
    chave = _buscar_chave_cpf(cpf)
    if chave and CLIENTES[chave]["fatura_pendente"]:
        return CLIENTES[chave]["fatura_pendente"]
    return None


def obter_historico(cpf):
    """Retorna o histórico de consumo formatado"""
    chave = _buscar_chave_cpf(cpf)
    if chave:
        consumos = CLIENTES[chave]["historico_consumo"]
        meses = ["Maio/2026", "Abril/2026", "Março/2026"]
        return dict(zip(meses, consumos))
    return {}