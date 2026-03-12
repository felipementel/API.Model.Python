# Usuarios API

API CRUD de usuarios criada com FastAPI, Python 3.14 e arquitetura Ports and Adapters.

O projeto foi pensado para estudo de deploy no Kubernetes, por isso inclui:

- persistencia apenas em memoria
- Swagger para exploracao da API
- testes unitarios e de endpoint
- endpoints de health check para liveness e readiness
- workflow de CI para execucao automatica dos testes

## Tecnologias

- Python 3.14
- FastAPI
- Uvicorn
- Pydantic
- Pytest
- Pytest Cov
- Black
- isort
- mypy

## Modelo de dominio

Entidade principal: `Usuario`

- `id: int`
- `nome: string`
- `dtNascimento: date`
- `status: bool`
- `telefones: string[]`

## Arquitetura

O projeto segue o modelo Ports and Adapters:

- `domain`: regras e contratos do dominio
- `application`: casos de uso e servicos
- `adapters/inbound`: entrada HTTP da aplicacao
- `adapters/outbound`: persistencia em memoria

Estrutura simplificada:

```text
src
|-- adapters
|   |-- inbound
|   |   `-- http
|   |       `-- routes
|   `-- outbound
|       `-- repositories
|-- application
|   `-- services
|-- domain
|   `-- ports
`-- main.py
```

## Pre-requisitos

- Windows com PowerShell
- Python 3.14 instalado
- `py -3.14` disponivel no terminal

Para validar a instalacao do Python:

```powershell
py -3.14 --version
```

## Como rodar o projeto

### 1. Criar o ambiente virtual

No PowerShell, dentro da pasta do projeto:

```powershell
py -3.14 -m venv .venv
```

### 2. Ativar o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a execucao de scripts, rode uma vez:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Instalar dependencias

```powershell
python -m pip install --upgrade pip
pip install -e .[dev]
```

### 4. Subir a API localmente

Opcao 1, executando diretamente o arquivo principal:

```powershell
py -3.14 .\src\main.py
```

Opcao 2, usando Uvicorn com recarga automatica:

```powershell
uvicorn main:app --app-dir src --reload
```

### 5. Acessar a aplicacao

Com a API em execucao, abra:

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## Como rodar os testes

Com o ambiente virtual ativo:

```powershell
pytest --cov=src --cov-report=term-missing
```

Resultado esperado no estado atual do projeto:

- testes unitarios do servico
- testes dos endpoints HTTP
- cobertura de 100%

## Qualidade de codigo

O projeto tambem possui ferramentas de padronizacao e analise estatica configuradas em `pyproject.toml`.

### Black

Responsavel por formatar o codigo automaticamente, mantendo um padrao consistente no projeto.

Configuracao atual:

- `line-length = 88`
- `target-version = py314`

Executar:

```powershell
black src tests
```

### isort

Responsavel por organizar os imports e manter o estilo compativel com o Black.

Configuracao atual:

- perfil `black`
- `line_length = 88`

Executar:

```powershell
isort src tests
```

### mypy

Responsavel por fazer checagem estatica de tipos para identificar inconsistencias antes da execucao.

Configuracao atual:

- `python_version = 3.14`
- `check_untyped_defs = true`
- `disallow_incomplete_defs = true`
- `no_implicit_optional = true`

Executar:

```powershell
mypy src
```

### Instalar ferramentas de qualidade

Esses pacotes fazem parte do grupo `dev`, junto com as dependencias de teste.

```powershell
pip install -e .[dev]
```

## Endpoints disponiveis

### Health checks

- `GET /health/live`
- `GET /health/ready`

Uso no Kubernetes:

- `live`: verifica se a aplicacao esta viva
- `ready`: verifica se a aplicacao esta pronta para receber trafego

### CRUD de usuarios

- `POST /usuarios`
- `GET /usuarios`
- `GET /usuarios/{usuario_id}`
- `PUT /usuarios/{usuario_id}`
- `DELETE /usuarios/{usuario_id}`

## Exemplo de payload

### Criar usuario

Requisicao:

```json
{
	"id": 1,
	"nome": "Carlos",
	"dtNascimento": "1992-03-14",
	"status": true,
	"telefones": [
		"11911112222",
		"1122223333"
	]
}
```

### Resposta esperada

```json
{
	"id": 1,
	"nome": "Carlos",
	"dtNascimento": "1992-03-14",
	"status": true,
	"telefones": [
		"11911112222",
		"1122223333"
	]
}
```

## Exemplo com curl

Criar usuario:

```bash
curl -X POST "http://127.0.0.1:8000/usuarios" \
	-H "Content-Type: application/json" \
	-d "{\"id\":1,\"nome\":\"Carlos\",\"dtNascimento\":\"1992-03-14\",\"status\":true,\"telefones\":[\"11911112222\",\"1122223333\"]}"
```

Listar usuarios:

```bash
curl "http://127.0.0.1:8000/usuarios"
```

Verificar readiness:

```bash
curl "http://127.0.0.1:8000/health/ready"
```

## Persistencia

Os dados sao armazenados somente em memoria.

Implicacoes:

- ao reiniciar a aplicacao, os dados sao perdidos
- nao existe dependencia de banco de dados
- o comportamento e ideal para estudo de API, testes e deploy em Kubernetes

## CI

O workflow de CI fica em `.github/workflows/ci.yml` e executa:

- instalacao das dependencias
- execucao dos testes
- geracao de relatorio JUnit para os testes

## Como saber quando atualizar pacotes

As versoes declaradas do projeto ficam em `pyproject.toml`.

Dependencias diretas atuais do projeto:

- `fastapi >= 0.135.1`
- `uvicorn >= 0.41.0`
- `httpx >= 0.28.1`
- `black >= 26.3.0`
- `isort >= 8.0.1`
- `mypy >= 1.19.1`
- `pytest >= 9.0.2`
- `pytest-cov >= 7.0.0`

Observacao importante:

- dependencias transitivas, como `pydantic_core`, normalmente nao devem ser atualizadas isoladamente
- para dependencias diretas, o ideal e atualizar, rodar testes e revisar changelog antes de subir para producao

Formas praticas de acompanhar isso:

- rodar `pip list --outdated` no ambiente virtual
- usar o CI para validar se a atualizacao nao quebrou nada
- acompanhar changelogs dos pacotes principais
- usar automacao para abrir PRs de atualizacao

Comando manual:

```powershell
.\.venv\Scripts\python -m pip list --outdated --format=columns
```

Automacao adicionada neste projeto:

- arquivo `.github/dependabot.yml`
- verificacao semanal de dependencias Python
- verificacao semanal de GitHub Actions
- abertura automatica de PRs para atualizacao

Recomendacao pratica:

- manter dependencias de runtime sempre dentro de faixas compativeis e testadas
- atualizar dependencias de teste com mais frequencia
- nao perseguir `latest` cegamente; perseguir `latest` validado pelos testes

## Comandos uteis

Executar a API:

```powershell
py -3.14 .\src\main.py
```

Executar a API com reload:

```powershell
uvicorn main:app --app-dir src --reload
```

Executar testes:

```powershell
pytest --cov=src --cov-report=term-missing
```

Formatar codigo:

```powershell
black src tests
isort src tests
```

Checar tipos:

```powershell
mypy src
```

Instalar dependencias novamente:

```powershell
pip install -e .[dev]
```
