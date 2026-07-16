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
        "fatura_pendente": None,  # Indica que a conta já está paga
        "historico_consumo": ["210 kWh", "195 kWh", "205 kWh"]
    }
}