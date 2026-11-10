# RPG Manager MCP

Servidor MCP desenvolvido em Python para demonstrar a consulta e o gerenciamento de personagens e missões de uma campanha de RPG de mesa.

O projeto utiliza o **Model Context Protocol (MCP)** para permitir que um cliente descubra e execute ferramentas disponibilizadas por um servidor. O cliente é Python convencional: não utiliza LLM nem API de inteligência artificial.

## 1. Objetivo

Disponibilizar seis ferramentas MCP para:
- Listar, consultar e cadastrar personagens.
- Listar e cadastrar missões.
- Concluir missões.

Os dados são persistidos em arquivos JSON, sem banco de dados.

## 2. Tecnologias

- Python 3.10 ou superior.
- MCP Python SDK 1.x.
- FastMCP.
- Comunicação `stdio`.
- JSON para persistência.
- `asyncio` para executar o cliente assíncrono.

> **Compatibilidade:** este projeto utiliza a linha 1.x do SDK porque a aula trabalha com `FastMCP`, `ClientSession`, `StdioServerParameters` e `stdio_client`. O arquivo `requirements.txt` limita a dependência a `mcp>=1.28,<2.0`.

## 3. Estrutura de arquivos

```text
RPG-Manager-MCP/
├── servidor.py
├── cliente.py
├── personagens.json
├── missoes.json
├── requirements.txt
└── README.md
```

- `servidor.py`: cria o servidor FastMCP, registra as ferramentas e manipula os JSON.
- `cliente.py`: inicia o servidor como subprocesso, abre a sessão MCP, lista e chama ferramentas.
- `personagens.json`: armazena os personagens.
- `missoes.json`: armazena as missões.
- `requirements.txt`: lista a dependência Python.
- `README.md`: documentação do projeto.

## 4. Instalação

Abra o terminal na pasta do projeto.

### 4.1. Verifique o Python

```bash
python --version
```

Utilize Python 3.10 ou superior.

### 4.2. Crie e ative um ambiente virtual (recomendado)

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows (CMD):

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4.3. Instale a dependência

```bash
python -m pip install -r requirements.txt
```

## 5. Como executar

Não é necessário abrir o servidor manualmente em um terminal separado. O cliente inicia `servidor.py` automaticamente por meio de `stdio_client`.

Execute:

```bash
python cliente.py
```

O cliente:
1. Inicia o processo do servidor.
2. Estabelece a comunicação por `stdio`.
3. Inicializa a sessão com `initialize()`.
4. Descobre as ferramentas com `list_tools()`.
5. Exibe nome, descrição e parâmetros.
6. Executa exemplos com `call_tool()`.
7. Encerra a sessão e o processo do servidor ao terminar.

Também é possível iniciar o servidor diretamente para integrá-lo a um host MCP compatível:

```bash
python servidor.py
```

Nesse caso, o servidor ficará aguardando a comunicação pelo transporte `stdio`. Não digite comandos no terminal enquanto ele estiver em execução.

## 6. Ferramentas disponíveis

| Ferramenta | Parâmetros | Descrição |
|---|---|---|
| `listar_personagens` | Nenhum | Lista nome, raça, classe e nível. |
| `consultar_personagem` | `nome` | Consulta os dados completos de um personagem. |
| `adicionar_personagem` | `nome`, `raca`, `classe`, `nivel` | Cadastra um personagem e impede nomes duplicados. |
| `listar_missoes` | Nenhum | Lista nome, descrição e status das missões. |
| `adicionar_missao` | `nome`, `descricao` | Cadastra uma missão com status inicial Pendente. |
| `concluir_missao` | `nome` | Altera o status de uma missão para Concluída. |

### Regras de validação

- Campos textuais não podem estar vazios.
- O nível deve ser um número inteiro entre 1 e 20.
- Não são permitidos nomes duplicados, mesmo que a diferença esteja apenas em maiúsculas e minúsculas.
- Uma missão nova começa com o status `Pendente`.
- Concluir uma missão inexistente retorna uma mensagem informativa.
- Concluir uma missão já concluída não altera os dados novamente.

## 7. Exemplos de chamadas

As chamadas abaixo ilustram os argumentos enviados pelo cliente MCP.

### Listar personagens

```python
await sessao.call_tool("listar_personagens", arguments={})
```

Resultado ilustrativo:

```text
Personagens cadastrados:
- Thorin | Raça: Anão | Classe: Guerreiro | Nível: 5
- Elaria | Raça: Elfa | Classe: Maga | Nível: 4
- Kael | Raça: Humano | Classe: Ladino | Nível: 3
```

### Consultar personagem

```python
await sessao.call_tool(
    "consultar_personagem",
    arguments={"nome": "Thorin"}
)
```

Resultado ilustrativo:

```text
Personagem: Thorin
Raça: Anão
Classe: Guerreiro
Nível: 5
```

### Adicionar personagem

```python
await sessao.call_tool(
    "adicionar_personagem",
    arguments={
        "nome": "Lyra",
        "raca": "Meia-elfa",
        "classe": "Clériga",
        "nivel": 2
    }
)
```

Resultado:

```text
Personagem "Lyra" cadastrado com sucesso.
```

### Listar missões

```python
await sessao.call_tool("listar_missoes", arguments={})
```

### Adicionar missão

```python
await sessao.call_tool(
    "adicionar_missao",
    arguments={
        "nome": "O Segredo das Ruínas",
        "descricao": "Investigar símbolos antigos encontrados nas ruínas."
    }
)
```

Resultado:

```text
Missão "O Segredo das Ruínas" cadastrada com sucesso. Status: Pendente.
```

### Concluir missão

```python
await sessao.call_tool(
    "concluir_missao",
    arguments={"nome": "O Segredo das Ruínas"}
)
```

Resultado:

```text
Missão "O Segredo das Ruínas" concluída com sucesso.
```

## 8. Persistência dos dados

Os dados ficam nos arquivos `personagens.json` e `missoes.json`.

O servidor carrega os arquivos ao iniciar. Quando um arquivo ainda não existe, ele é criado com os dados iniciais de demonstração. Toda inclusão ou atualização salva a lista novamente no respectivo JSON.

Por isso, os dados continuam disponíveis depois que o cliente e o servidor são encerrados.

**Atenção:** os exemplos do cliente adicionam a personagem Lyra e a missão O Segredo das Ruínas. Se o cliente for executado novamente, as ferramentas informarão que esses nomes já estão cadastrados. Isso é esperado e demonstra a persistência e a regra contra duplicidade.

## 9. Conceitos MCP demonstrados

- **Servidor MCP:** programa que disponibiliza funcionalidades para clientes compatíveis.
- **Tool (ferramenta):** função registrada com `@mcp.tool()` que pode ser descoberta e executada pelo cliente.
- **FastMCP:** interface simplificada do SDK para criar o servidor e registrar ferramentas.
- **Cliente MCP:** programa que estabelece a comunicação e solicita operações ao servidor.
- **`stdio`:** transporte que utiliza a entrada e a saída padrão do processo para trocar mensagens MCP.
- **`ClientSession`:** sessão responsável pela comunicação entre cliente e servidor.
- **`initialize()`:** inicializa a sessão MCP.
- **`list_tools()`:** solicita a lista de ferramentas disponíveis.
- **`call_tool()`:** solicita a execução de uma ferramenta específica.

## 10. Limitações intencionais

Este é um projeto introdutório. Ele não implementa autenticação, interface gráfica, LLM, API externa, banco de dados, múltiplos usuários ou controle de acesso. Essas funcionalidades estão fora do escopo acadêmico definido para o projeto.
