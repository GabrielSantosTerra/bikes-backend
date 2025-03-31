from validate_docbr import CPF, CNPJ
from fastapi import HTTPException

def validar_cpf_cnpj_sem_mascara(valor: str):
    if not valor.isdigit():
        raise HTTPException(status_code=400, detail="Documento deve conter apenas números")

    if len(valor) == 11:
        if not CPF().validate(valor):
            raise HTTPException(status_code=400, detail="CPF inválido")
    elif len(valor) == 14:
        if not CNPJ().validate(valor):
            raise HTTPException(status_code=400, detail="CNPJ inválido")
    else:
        raise HTTPException(status_code=400, detail="Documento inválido (esperado CPF ou CNPJ)")
