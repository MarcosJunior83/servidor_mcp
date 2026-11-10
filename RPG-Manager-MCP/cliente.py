# FitTrack MCP

Servidor MCP (Model Context Protocol) em Python para registrar e consultar treinos de musculação, acompanhado de um cliente MCP de testes.

## Apresentação

**Descrição:** o FitTrack MCP expõe quatro ferramentas (*tools*) que permitem registrar treinos (exercício, carga, séries, repetições e data) e consultar histórico e progressão de carga. Os dados ficam salvos em um arquivo JSON.

**Objetivo acadêmico:** demonstrar, na disciplina de Fundamentos de Inteligência Artificial, o funcionamento do MCP: criação de ferramentas, descoberta (`list_tools`), execução (`call_tool`) e comunicação padronizada entre cliente e servidor via `stdio`.

**Problema que busca resolver:** quem treina costuma anotar cargas de forma solta e perde a noção de evolução. O projeto centraliza esses registros e calcula a progressão, servindo também como exemplo simples de como expor funcionalidades por meio de um protocolo padronizado.

> Este não é um aplicativo completo de academia. O foco é o servidor MCP e o cliente de testes. Não há banco de dados externo, API externa, interface gráfica, autenticação nem uso de IA/LLM.

## Funcionalidades (ferramentas MCP)

| Ferramenta | O que faz |
|---|---|
| `listar_exercicios()` | Lista os exercícios que já possuem registros. |
| `registrar_treino(nome_exercicio, carga, series, repeticoes)` | Registra um treino com a data de hoje. Valida: nome não vazio, carga > 0, séries e repetições inteiros positivos. Preserva os registros anteriores. |
| `consultar_historico(nome_exercicio)` | Retorna todos os registros do exercício, ordenados por data. Informa quando não há histórico. |
| `consultar_progressao(nome_exercicio)` | Compara primeira e última carga, mostra a diferença e indica aumento, redução ou manutenção. Exige ao menos 2 registros. |

A busca por nome ignora maiúsculas/minúsculas (`Supino Reto` = `supino reto`).

## Tecnologias utilizadas

| Tecnologia | Função no projeto |
|---|---|
| Python | Linguagem do servidor e do cliente. |
| SDK oficial MCP para Python (`mcp[cli]>=1,<2`) | Implementa o protocolo MCP (servidor e cliente). |
| FastMCP | Cria o servidor e registra as tools com `@mcp.tool()`. |
| `ClientSession`, `StdioServerParameters`, `stdio_client` | Usados no cliente para iniciar o servidor e conversar via MCP. |
| stdio | Transporte: o cliente inicia o servidor como subprocesso e troca mensagens pela entrada/saída padrão. |
| JSON (`treinos.json`) | Armazenamento persistente dos treinos. |

## Estrutura de pastas

```
fittrack-mcp/
├── servidor_fittrack.py   # Servidor MCP: funções auxiliares + 4 ferramentas
├── treinos.json           # Armazenamento dos treinos (estrutura inicial: {"treinos": []})
├── cliente.py             # Cliente MCP: descobre e executa as ferramentas
├── requirements.txt       # Dependência: mcp[cli]>=1,<2
└── README.md              # Documentação
```

## Requisitos para execução

- **Python 3.10 ou superior** (recomendado 3.11 ou 3.12). Verifique com `python --version`.
- **VS Code** com a extensão *Python* (Microsoft).
- **Terminal** (PowerShell ou CMD; o terminal integrado do VS Code serve).
- **SDK MCP**, instalado via `requirements.txt` (precisa de internet nessa etapa).

## Como instalar e executar (Windows + VS Code)

**1. Abrir a pasta do projeto.** Baixe/extraia o projeto, abra o VS Code e use *File > Open Folder...* selecionando `fittrack-mcp`. Abra o terminal em *Terminal > New Terminal*.

**2. Criar o ambiente virtual.**

```powershell
python -m venv .venv
```
(Se `python` não for reconhecido, tente `py -m venv .venv`.)

**3. Ativar o ambiente virtual.**

PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```
Se aparecer erro de política de execução, rode apenas nesta sessão e ative de novo:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

CMD:
```cmd
.venv\Scripts\activate.bat
```
Quando ativo, o terminal mostra `(.venv)` no início da linha. No VS Code, se pedir, selecione o interpretador `.venv` em *Ctrl+Shift+P > Python: Select Interpreter*.

**4. Instalar as dependências.**

```powershell
pip install -r requirements.txt
```

**5. Executar o cliente.**

```powershell
python cliente.py
```

**6. O servidor inicia automaticamente.** Você **não** precisa executar `servidor_fittrack.py` manualmente. O cliente o inicia como subprocesso com o mesmo Python do ambiente virtual (`sys.executable`) e se conecta via stdio. Se rodar o servidor sozinho, ele ficará aguardando mensagens MCP e não mostrará nada; encerre com `Ctrl+C`.

**7. Visualizar os resultados.** Tudo é exibido no terminal: ferramentas descobertas (nome, descrição, parâmetros) e o resultado de cada teste.

## Exemplos de utilização

Saída esperada (resumida) em uma primeira execução, com o JSON vazio:

```
Conexão MCP estabelecida com o servidor FitTrack.

FERRAMENTAS DISPONÍVEIS (list_tools)
Nome: listar_exercicios
Descrição: Lista todos os exercícios que já possuem registros de treino.
Parâmetros: nenhum
...
TESTE 1 - Listar exercícios
Nenhum exercício registrado ainda.

TESTE 2 - Registrar treinos
Treino registrado: Supino Reto - 60 kg, 4x10 em AAAA-MM-DD.
Treino registrado: Supino Reto - 65 kg, 4x8 em AAAA-MM-DD.
Erro: a carga deve ser um número maior que zero.

TESTE 3 - Consultar histórico
Histórico de Supino Reto (2 registros):
AAAA-MM-DD | 60 kg | 4 séries x 10 repetições
AAAA-MM-DD | 65 kg | 4 séries x 8 repetições
Nenhum histórico encontrado para 'Exercício Inexistente'.

TESTE 4 - Consultar progressão de carga
Progressão de Supino Reto:
Primeira carga: 60 kg
Última carga: 65 kg
Diferença: +5 kg
Situação: AUMENTO de carga
```

Formato de um registro no `treinos.json`:

```json
{
  "exercicio": "Supino Reto",
  "carga": 60.0,
  "series": 4,
  "repeticoes": 10,
  "data": "AAAA-MM-DD"
}
```

Cada execução do cliente adiciona novos registros. Para zerar os dados, deixe o `treinos.json` assim:

```json
{
  "treinos": []
}
```

## Comunicação MCP

```
Usuário → Cliente MCP → Servidor MCP → Ferramenta → Resultado retornado ao cliente
```

1. O **usuário** executa `python cliente.py`.
2. O **cliente MCP** inicia o servidor (`stdio_client`) e abre a sessão (`ClientSession`).
3. `initialize()` faz o *handshake* entre cliente e servidor.
4. `list_tools()` pergunta ao **servidor MCP** quais ferramentas existem; ele responde com nome, descrição e esquema de parâmetros (gerados pelo FastMCP a partir das funções e *docstrings*).
5. `call_tool("nome", {argumentos})` envia o pedido ao servidor, que executa a **ferramenta** correspondente.
6. O **resultado** volta ao cliente como conteúdo de texto, exibido no terminal.

O cliente nunca importa nem chama as funções do servidor diretamente: todo o acesso passa pelo protocolo.

## Testes

- **Descoberta:** na seção "FERRAMENTAS DISPONÍVEIS", devem aparecer as quatro ferramentas: `listar_exercicios`, `registrar_treino`, `consultar_historico` e `consultar_progressao`.
- **Execução:** os testes 1 a 4 devem retornar as mensagens de exemplo acima, sem `[ERRO MCP]`.
- **Validação:** a tentativa com carga `0` deve retornar "Erro: a carga deve ser um número maior que zero." e **não** gravar nada.
- **Persistência:** abra o `treinos.json` após a execução e confira os novos registros; rodar o cliente de novo mantém os antigos.

## Considerações finais

O MCP padroniza como aplicações expõem ferramentas e como clientes as descobrem e usam: o cliente não precisa conhecer o código do servidor, apenas falar o protocolo. Neste projeto, isso aparece na descoberta dinâmica via `list_tools()`, na execução via `call_tool()` e na troca de mensagens por `stdio`. A mesma ideia permite que, no futuro, qualquer cliente compatível com MCP use este servidor sem alterações.
