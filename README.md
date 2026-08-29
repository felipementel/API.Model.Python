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
- flake8
- bandit
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

- Python 3.14 instalado
- Linux, macOS ou Windows (PowerShell/Bash)
- `python` ou `py -3.14` disponivel no terminal

Para validar a instalacao do Python:

No Windows:

```powershell
py -3.14 --version
```

No Linux ou macOS:

```bash
python3 --version
```

## Usando uv

Instale o `uv` caso ele ainda nao esteja disponivel.

No Windows com PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

No Linux ou macOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

e depois execute


```bash
source "$HOME/.local/bin/env"
```

Valide a instalacao:

```bash
uv --version
```

Os comandos abaixo devem ser executados dentro da pasta `source`:

```bash
cd source
```

### Preparar o ambiente

Instalar o Python 3.14 e sincronizar as dependencias da aplicacao e de
desenvolvimento:

```bash
uv python install 3.14
uv sync --extra dev
```

### Executar a API

Com recarga automatica durante o desenvolvimento:

```bash
uv run uvicorn main:app --app-dir src --reload
```

Ou executando o arquivo principal diretamente, na porta 8080:

```bash
uv run python src/main.py
```

### Executar os testes

```bash
uv run pytest
uv run pytest --cov=src --cov-report=term-missing
```

### Formatar o codigo

```bash
uv run isort --settings-path pyproject.toml src
uv run black --config pyproject.toml src
```

### Executar os checks de qualidade

```bash
uv run isort --check-only --settings-path pyproject.toml src
uv run black --check --config pyproject.toml src
uv run flake8 --toml-config pyproject.toml src
uv run mypy --config-file pyproject.toml src
uv run bandit -c pyproject.toml -r src
```

### Gerenciar dependencias

```bash
# Adicionar ou remover uma dependencia da aplicacao
uv add nome-do-pacote
uv remove nome-do-pacote

# Adicionar uma dependencia opcional ao grupo dev
uv add --optional dev nome-do-pacote

# Atualizar o lockfile e sincronizar o ambiente
uv lock
uv lock --upgrade
uv sync --upgrade

# Visualizar a arvore de dependencias
uv tree
```

> **Atencao:** o `pyproject.toml` declara `readme = "README.md"`, mas este
> arquivo esta um nivel acima da pasta `source`. Se `uv sync` falhar ao instalar
> o projeto, ajuste esse caminho ou disponibilize um README dentro de `source`.

### Criar a imagem Docker com uv

O Dockerfile usa `uv sync --frozen` e o `uv.lock` para instalar somente as
dependencias de producao. Execute os comandos na raiz do repositorio:

```bash
docker buildx build -f docker/Dockerfile -t usuarios-api .
docker run --rm -p 8080:8080 usuarios-api
```

O `uv` e usado apenas durante o build e nao e incluido na imagem final.

### Criar a imagem Docker com pip

Execute os comandos na raiz do repositorio:

```bash
docker buildx build -f docker/Dockerfile-pip -t usuarios-api-pip .
docker run --rm -p 8080:8080 usuarios-api-pip
```

## Como rodar o projeto com pip e venv

Caso prefira utilizar o fluxo tradicional com `pip` e `venv`, execute dentro da pasta `source`:

### Passos rapidos (Linux / macOS / Bash)

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .[dev]
python src/main.py
```

### Passo a passo detalhado

#### 1. Criar o ambiente virtual

No Linux / macOS (Bash):

```bash
python -m venv .venv
```

No Windows (PowerShell):

```powershell
py -3.14 -m venv .venv
```

#### 2. Ativar o ambiente virtual

No Linux / macOS (Bash):

```bash
source .venv/bin/activate
```

No Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a execucao de scripts, rode uma vez:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 3. Instalar dependencias

```bash
python -m pip install --upgrade pip
pip install -e .[dev]
```

Para instalar apenas as dependencias de producao:

```bash
pip install .
```

#### 4. Subir a API localmente

Opcao 1, executando diretamente o arquivo principal:

```bash
python src/main.py
```

Opcao 2, usando Uvicorn com recarga automatica:

```bash
uvicorn main:app --app-dir src --reload
```

### 5. Acessar a aplicacao

Com a API em execucao, abra:

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## Como rodar os testes

Com o ambiente virtual ativo:

```bash
pytest --cov=src --cov-report=term-missing
```

## Pre-checks antes do commit

Na raiz do repositorio, execute a verificacao de vulnerabilidades com Trivy:

```powershell
trivy fs --scanners vuln --format table --dependency-tree .
```

Dentro da pasta `source`, os mesmos checks de qualidade executados pelo CI sao:

```powershell
py -3.14 -m isort --check-only --settings-path ./pyproject.toml ./src
py -3.14 -m black --check --config ./pyproject.toml ./src
py -3.14 -m flake8 --toml-config ./pyproject.toml ./src
$env:MYPYPATH = './src'
py -3.14 -m mypy --config-file ./pyproject.toml ./src
py -3.14 -m bandit -c ./pyproject.toml -r ./src
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
black --config pyproject.toml src
```

### isort

Responsavel por organizar os imports e manter o estilo compativel com o Black.

Configuracao atual:

- perfil `black`
- `line_length = 88`

Executar:

```powershell
isort --settings-path pyproject.toml src
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
mypy --config-file pyproject.toml src
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

trivy fs --scanners vuln --format table --dependency-tree .
