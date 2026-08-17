from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa o banco de dados ao ligar o servidor
    database.init_db()
    yield


# 1. Definição obrigatória da variável 'app'
app = FastAPI(title="LexMind-AI API", lifespan=lifespan)

# 2. Middlewares (usam a variável 'app')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# 3. Rotas da API
@app.get("/")
def home():
    return {"status": "LexMind-AI API online"}


@app.post("/api/v1/analisar-documento")
async def analisar_documento(
    tipo_doc: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        conteudo_bytes = await file.read()
        texto_extraido = conteudo_bytes.decode("utf-8", errors="ignore")

        doc_id = database.salvar_documento(file.filename, tipo_doc, texto_extraido)

        resumo_ia = f"Análise automatizada do documento {file.filename} ({tipo_doc})."
        status_ia = (
            "Conforme"
            if "cláusula" in texto_extraido.lower()
            else "Atenção Necessária"
        )
        inconsistencias_ia = (
            "Nenhuma inconsistência grave identificada."
            if status_ia == "Conforme"
            else "Ausência de cláusula padrão de rescisão."
        )

        database.salvar_analise(doc_id, resumo_ia, status_ia, inconsistencias_ia)

        return {
            "documento_id": doc_id,
            "status": status_ia,
            "resumo": resumo_ia,
            "inconsistencias": inconsistencias_ia,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))