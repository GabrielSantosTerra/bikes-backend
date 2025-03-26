import requests
import psycopg2
import os
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

# Conectar ao banco de dados
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cursor = conn.cursor()

# Criar tabelas se não existirem
cursor.execute("""
CREATE TABLE IF NOT EXISTS regioes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS estados (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    sigla VARCHAR(2) NOT NULL,
    id_regiao INTEGER NOT NULL REFERENCES regioes(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cidades (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    id_estado INTEGER NOT NULL REFERENCES estados(id),
    codigo_ibge INTEGER UNIQUE NOT NULL,
    codigo_regiao INTEGER NOT NULL REFERENCES regioes(id)
);
""")

# **1. Buscar regiões**
url_regioes = "https://servicodados.ibge.gov.br/api/v1/localidades/regioes"
res = requests.get(url_regioes)
regioes = res.json()

regioes_data = [(r['id'], r['nome']) for r in regioes]

execute_values(cursor, "INSERT INTO regioes (id, nome) VALUES %s ON CONFLICT (id) DO NOTHING;", regioes_data)
conn.commit()

# **2. Buscar estados e associar às regiões**
url_estados = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
res = requests.get(url_estados)
estados = res.json()

estados_data = [(e['id'], e['nome'], e['sigla'], e['regiao']['id']) for e in estados]

execute_values(cursor, "INSERT INTO estados (id, nome, sigla, id_regiao) VALUES %s ON CONFLICT (id) DO NOTHING;", estados_data)
conn.commit()

# **3. Buscar cidades e associar corretamente**
url_municipios = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
res = requests.get(url_municipios)
municipios = res.json()

municipios_data = [(m['id'], m['nome'], m['microrregiao']['mesorregiao']['UF']['id'], m['id'], m['microrregiao']['mesorregiao']['UF']['regiao']['id']) for m in municipios]

execute_values(cursor, "INSERT INTO cidades (id, nome, id_estado, codigo_ibge, codigo_regiao) VALUES %s ON CONFLICT (id) DO NOTHING;", municipios_data)
conn.commit()

print("Dados do IBGE inseridos com sucesso!")

cursor.close()
conn.close()
