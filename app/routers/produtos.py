from fastapi import APIRouter, HTTPException, status, Body
import app.db as db

router = APIRouter(
    prefix="/produtos",
    tags=["produtos"]
)

# ==============================================================================
# Listar todos os produtos
# ==============================================================================

@router.get("/")
def listar_produtos():
    return db.produtos

# ==============================================================================
# Buscar produto por ID
# ==============================================================================

@router.get("/{product_id}")
def obter_produto_por_id(product_id: int):
    for produto in db.produtos:
        if produto["id"] == product_id:
            return produto
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Produto não encontrado."
    ) 

# ==============================================================================
# Cadastrar um novo produto
# ==============================================================================

@router.post("/", status_code=status.HTTP_201_CREATED)
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
    
    db.qtd_produtos += 1

    novo_produto = {
        "id": db.qtd_produtos,
        "nome": nome,
        "preco_unitario": preco_unitario
    }
    db.produtos.append(novo_produto)
    return novo_produto