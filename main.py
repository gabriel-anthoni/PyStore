from fastapi import FastAPI, HTTPException, status, Body
from datetime import datetime

app = FastAPI()

# ==============================================================================
# Simulação de Banco de Dados em Memória
# ==============================================================================

qtd_usuarios = 1
qtd_pedidos  = 1
usuarios     = [
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

qtd_produtos = 1
produtos = [
    {
        "id": 1,
        "nome": "Teclado",
        "preco_unitario": 150.00,
    }
]

# ==============================================================================
# Listar todos os usuários
# ==============================================================================

@app.get("/usuarios")
def listar_usuarios():
    return usuarios

# ==============================================================================
# Buscar usuário por ID
# ==============================================================================

@app.get("/usuarios/{user_id}")
def obter_usuario_por_id(user_id: int):
    for usuario in usuarios:
        if usuario["id"] == user_id:
            return usuario
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
    )  

# ==============================================================================
# Listar todos os pedidos de um usuário
# ==============================================================================

@app.get("/usuarios/{user_id}/pedidos")
def listar_pedidos_do_usuario(user_id: int):
    for usuario in usuarios:
        if usuario["id"] == user_id:
            return usuario["pedidos"]
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
    )  

# ==============================================================================
# Buscar um pedido específico de um usuário por ID
# ==============================================================================

@app.get("/usuarios/{user_id}/pedidos/{order_id}")
def obter_pedido_especifico_do_usuario(user_id: int, order_id: int):
    for usuario in usuarios:
        if usuario["id"] == user_id:
            for pedido in usuario["pedidos"]:
                if pedido["id"] == order_id:
                    return pedido
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido não encontrado."
            )  
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
    )  

# ==============================================================================
# Criar um novo usuário
# ==============================================================================

@app.post("/usuarios", status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(
    nome:            str = Body(...),
    data_nascimento: str = Body(...),
    endereco:        str = Body(...)
):
    
    if not nome.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O campo 'nome' é obrigatório e não pode conter apenas espaços."
        )
    
    if not data_nascimento.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O campo 'data_nascimento' é obrigatório."
        )
    
    if not endereco.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O campo 'endereco' é obrigatório e não pode conter apenas espaços."
        )
    
    try:
        data = datetime.strptime(data_nascimento,"%d/%m/%Y")
        idade_days = datetime.now() - data
        idade      = idade_days.days // 365
        if(idade < 18):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cadastro não permitido: o usuário deve ter no mínimo 18 anos."
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de data inválido. Use o padrão DD/MM/AAAA (ex: 20/05/1998)."
        )
    
    global qtd_usuarios
    qtd_usuarios += 1
    novo_usuario = {
        "id": qtd_usuarios,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
        "pedidos": []
    }
    usuarios.append(novo_usuario)
    
    return novo_usuario

# ==============================================================================
# Adicionar um novo pedido para um usuário
# ==============================================================================

@app.post("/usuarios/{user_id}/pedidos", status_code=status.HTTP_201_CREATED)
def adicionar_pedido(
    user_id: int,
    product_id: int = Body(...),
    quantidade: int = Body(...),
):
    if not product_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O campo 'product_id' é obrigatório."
        )
    
    if (not quantidade) or (quantidade <= 0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O campo 'quantidade' é obrigatório e deve ser maior que zero."
        )

    global qtd_pedidos
    
    for produto in produtos:
        if produto["id"] == product_id:

            qtd_pedidos += 1
            data_pedido = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            valor_total = quantidade * produto["preco_unitario"]

            novo_pedido = {
                "id": qtd_pedidos,
                "data_pedido": data_pedido,
                "produto_id": product_id,
                "produto_nome": produto["nome"],
                "quantidade": quantidade,
                "valor_total": valor_total,
                "foi_entregue": False
            }

            for usuario in usuarios:
                if usuario["id"] == user_id:
                    usuario["pedidos"].append(novo_pedido)
                    return novo_pedido
    raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário não encontrado."
        )

# ==============================================================================
# Listar todos os produtos
# ==============================================================================

@app.get("/produtos")
def listar_produtos():
    return produtos

# ==============================================================================
# Buscar produto por ID
# ==============================================================================

@app.get("/produtos/{product_id}")
def obter_produto_por_id(product_id: int):
    for produto in produtos:
        if produto["id"] == product_id:
            return produto
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Produto não encontrado."
    ) 

# ==============================================================================
# Cadastrar um novo produto
# ==============================================================================

@app.post("/produtos", status_code=status.HTTP_201_CREATED)
def cadastrar_produto(
    nome:           str   = Body(...),
    preco_unitario: float = Body(...),
):

    if not nome.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O campo 'nome' é obrigatório e não pode conter apenas espaços."
        )
    
    if (not preco_unitario) or (preco_unitario <= 0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O campo 'preco_unitario' é obrigatório e deve ser maior que zero."
        )
    
    global qtd_produtos
    qtd_produtos += 1

    novo_produto = {
        "id": qtd_produtos,
        "nome": nome,
        "preco_unitario": preco_unitario
    }
    produtos.append(novo_produto)
    return novo_produto