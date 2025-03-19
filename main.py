import os
from fastapi import FastAPI, status, HTTPException, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from model import Aranhaverso
from typing import Optional, Any

app = FastAPI(title="API do Aranhaverso", version="0.0.1", description="Mostra os homens-aranhas do aranhaverso")

app.mount("/static", StaticFiles(directory="static"), name="static")

homens_aranhas = {
    1: {
        "nome": "Miles Morales",
        "idade": 17,
        "cores_uniforme": "Preto com detalhes em vemelho",
        "poderes": "Choques elétricos, camuflagem, sentido aranha, agilidade e superforça",
        "personalidade": "Determinado, humilde, inseguro e empatico",
        "universo": "Terra-1610 (Ultimante Marvel Universe)",
        "foto": "https://www.comboinfinito.com.br/principal/wp-content/uploads/2020/10/aranhaverso.jpg"
    },

    2: {
        "nome": "Peter Benjamin Parker",
        "idade": 25,
        "cores_uniforme": "Vermelho com detalhes em azul",
        "poderes": "Força sobre-humana, sentido aranhha, lançamento de teias e agilidade",
        "personalidade": "Responsável, humos sarcático e confiante",
        "universo": "Terra-616 (Marvel principal)",
        "foto": "https://g1.globo.com/Noticias/Cinema/foto/0,,15444595-EX,00.jpg"
    },

    3: {
        "nome": "Miguel O'Hara (Spider-Man 2099)",
        "idade": 30,
        "cores_uniforme": "Azul escuro com detalhes em vermelho brilhante",
        "poderes": "Força sobre-humana, garras, visão de águia, agilidade aprimorada e manipulação do DNA",
        "personalidade": "Determinado e resiliente, cínico, anti-herói",
        "universo": "Terra-928 (Marvel 2099)",
        "foto": "https://static.wikia.nocookie.net/liga-da-zueira-oficial/images/c/c9/Kris_anka_2099.webp/revision/latest?cb=20230623165058&path-prefix=pt-br",
    }
}

templates = Jinja2Templates(directory='templates')

def fake_db():
    try:
        print("Conectando com o banco de dados.")
    finally:
        print("Fechando a conexão com o banco de dados.")

@app.get("/aranhas")
async def get_homens_aranhas(db: Any = Depends(fake_db)):
    return homens_aranhas

@app.get("/aranhas/{homens_aranhas_id}", description="Torna um homem-aranha individual", summary="Retorna um homem-aranha")
async def get_homens_aranhas(homens_aranhas_id: int):
    if homens_aranhas_id in homens_aranhas:
        homem_aranha = homens_aranhas[homens_aranhas_id]
        return homem_aranha
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe um homem-aranha com o id {homens_aranhas_id}")

@app.get("/", response_class=HTMLResponse)
async def aranhaverso_page(request: Request, id: Optional[int] = None):
    homem_aranha = None
    erro = None
    
    if id:
        if id in homens_aranhas:
            homem_aranha = homens_aranhas[id]
        else:
            erro = f"Não existe um Homem-Aranha com o ID {id}."

    return templates.TemplateResponse("aranhaverso.html", {"request": request, "titulo": "Aranhaverso", "homem_aranha": homem_aranha, "erro": erro})


@app.post("/aranhas", status_code=status.HTTP_201_CREATED)
async def post_homens_aranhas(homem_aranha: Optional[Aranhaverso] = None):
    next_id = len(homens_aranhas) + 1
    homens_aranhas[next_id] = homem_aranha
    del homem_aranha.id
    return homem_aranha

@app.put("/aranhas/{homens_aranhas_id}", status_code=status.HTTP_202_ACCEPTED)
async def put_homens_aranhas(homens_aranhas_id: int, homem_aranha: Aranhaverso):
    if homens_aranhas_id in homens_aranhas:
        homens_aranhas[homens_aranhas_id] = homem_aranha
        homem_aranha.id = homens_aranhas_id
        del homem_aranha.id
        return homem_aranha
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe um homem-aranha com o id {homens_aranhas_id}")
    
@app.delete("/aranhas/{homens_aranhas_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_homens_aranhas(homens_aranhas_id: int):
    if homens_aranhas_id in homens_aranhas:
        del homens_aranhas[homens_aranhas_id]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
@app.patch("/aranhas/{homens_aranhas_id}", status_code=status.HTTP_202_ACCEPTED)
async def patch_homens_aranhas_id(homens_aranhas_id: int, homem_aranha: Aranhaverso):
    if homens_aranhas_id in homens_aranhas:
        existing_homem_aranha = homens_aranhas[homens_aranhas_id]

        update_data = homem_aranha.dict(exclude_unset=True)
        existing_homem_aranha.update(update_data)

        return existing_homem_aranha
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe um homem-aranha com o id {homens_aranhas_id}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)