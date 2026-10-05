# ==============================================================================
# Simulação de Banco de Dados em Memória
# ==============================================================================

qtd_usuarios = 1
qtd_pedidos = 1
qtd_produtos = 1

usuarios = [
    {
        "id": 1,
        "nome": "Marco",
        "data_nascimento": "23/05/2000",
        "endereco": "M",
        "pedidos": [
            {
                "id": 1,
                "data_pedido": "23/05/2025 20:54:45",
                "produto_id": 1,
                "produto_nome": "Teclado",
                "quantidade": 2,
                "valor_total": 300.0,
                "foi_entregue": True
            }
        ]
    }
]

produtos = [
    {
        "id": 1,
        "nome": "Teclado",
        "preco_unitario": 150.00,
    }
]