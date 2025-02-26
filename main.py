from fastapi import FastAPI, HTTPException
from unidecode import unidecode
from api import filmes_por_genero

app = FastAPI()

def normalizar_texto(texto: str) -> str:
    """Remove acentos, transforma para minúsculas e remove espaços extras."""
    return unidecode(texto.strip().lower())

@app.get("/")
def home():
    return {"mensagem": "Bem-vindo à API de Filmes!"}

@app.get("/generos")
def listar_generos():
    """ Retorna todos os gêneros disponíveis sem acentos. """
    return {"generos_disponiveis": [normalizar_texto(g) for g in filmes_por_genero.keys()]}

@app.get("/filmes/{genero}")
def obter_filmes_por_genero(genero: str):
    """ Retorna os filmes de um gênero específico, permitindo buscas parciais. """
    genero_normalizado = normalizar_texto(genero)

    # Normaliza os gêneros disponíveis e permite buscas parciais
    generos_disponiveis = {normalizar_texto(g): g for g in filmes_por_genero.keys()}

    # Busca um gênero que contenha a palavra pesquisada
    genero_real = next((generos_disponiveis[g] for g in generos_disponiveis if genero_normalizado in g), None)

    if not genero_real:
        raise HTTPException(status_code=404, detail="Gênero não encontrado")

    return {"genero": genero_real, "filmes": filmes_por_genero[genero_real]}
