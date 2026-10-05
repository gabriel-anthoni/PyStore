from fastapi import APIRouter, HTTPException, status, Body
from datetime import datetime
import app.db as db

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

# ==============================================================================
# Listar todos os usuários
# ==============================================================================

@router.get("/")
def listar_usuarios():
    return db.usuarios

# ==============================================================================
# Buscar usuário por ID
# ==============================================================================

@router.get("/{user_id}")
def obter_usuario_por_id(user_id: int):
    for usuario in db.usuarios:
        if usuario["id"] == user_id:
            return usuario
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
    )  

# ==============================================================================
# Listar todos os pedidos de um usuário
# ==============================================================================

@router.get("/{user_id}/pedidos")
def listar_pedidos_do_usuario(user_id: int):
    for usuario in db.usuarios:
        if usuario["id"] == user_id:
            return usuario["pedidos"]
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
    )  

# ==============================================================================
# Buscar um pedido específico de um usuário por ID
# ==============================================================================

@router.get("/{user_id}/pedidos/{order_id}")
def obter_pedido_especifico_do_usuario(user_id: int, order_id: int):
    for usuario in db.usuarios:
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

@router.post("/", status_code=status.HTTP_201_CREATED)
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
    
    db.qtd_usuarios += 1
    novo_usuario = {
        "id": db.qtd_usuarios,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
        "pedidos": []
    }
    db.usuarios.append(novo_usuario)
    
    return novo_usuario

# ==============================================================================
# Adicionar um novo pedido para um usuário
# ==============================================================================

@router.post("/{user_id}/pedidos", status_code=status.HTTP_201_CREATED)
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
    
    for produto in db.produtos:
        if produto["id"] == product_id:

            db.qtd_pedidos += 1
            data_pedido = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            valor_total = quantidade * produto["preco_unitario"]

            novo_pedido = {
                "id": db.qtd_pedidos,
                "data_pedido": data_pedido,
                "produto_id": product_id,
                "produto_nome": produto["nome"],
                "quantidade": quantidade,
                "valor_total": valor_total,
                "foi_entregue": False
            }

            for usuario in db.usuarios:
                if usuario["id"] == user_id:
                    usuario["pedidos"].append(novo_pedido)
                    return novo_pedido
    raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário não encontrado."
        )