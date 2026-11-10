import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP


# Os arquivos ficam na mesma pasta deste servidor.
PASTA_PROJETO = Path(__file__).resolve().parent
ARQUIVO_PERSONAGENS = PASTA_PROJETO / "personagens.json"
ARQUIVO_MISSOES = PASTA_PROJETO / "missoes.json"

mcp = FastMCP("RPG Manager")


def carregar_dados(caminho: Path, dados_iniciais: list) -> list:
    """Carrega uma lista de dados ou cria o JSON com dados iniciais."""
    if not caminho.exists():
        salvar_dados(caminho, dados_iniciais)
        return dados_iniciais.copy()

    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        if not isinstance(dados, list):
            raise ValueError(f"O conteúdo de {caminho.name} deve ser uma lista.")

        return dados
    except json.JSONDecodeError as erro:
        raise ValueError(
            f"O arquivo {caminho.name} contém JSON inválido."
        ) from erro


def salvar_dados(caminho: Path, dados: list) -> None:
    """Salva os dados no arquivo JSON indicado."""
    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)


def texto_obrigatorio(valor: str, campo: str) -> str:
    """Valida um texto obrigatório e devolve o valor sem espaços externos."""
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"O campo '{campo}' é obrigatório.")
    return valor.strip()


def buscar_por_nome(lista: list, nome: str) -> dict | None:
    """Busca um registro pelo nome, sem diferenciar maiúsculas de minúsculas."""
    nome_normalizado = nome.strip().casefold()

    for item in lista:
        if item["nome"].casefold() == nome_normalizado:
            return item

    return None


PERSONAGENS_INICIAIS = [
    {
        "nome": "Thorin",
        "raca": "Anão",
        "classe": "Guerreiro",
        "nivel": 5
    },
    {
        "nome": "Elaria",
        "raca": "Elfa",
        "classe": "Maga",
        "nivel": 4
    },
    {
        "nome": "Kael",
        "raca": "Humano",
        "classe": "Ladino",
        "nivel": 3
    }
]

MISSOES_INICIAIS = [
    {
        "nome": "O Goblin Desaparecido",
        "descricao": "Investigar o desaparecimento de um viajante próximo à floresta.",
        "status": "Pendente"
    },
    {
        "nome": "A Torre Abandonada",
        "descricao": "Explorar uma antiga torre e descobrir o que aconteceu com seus habitantes.",
        "status": "Pendente"
    },
    {
        "nome": "Proteção da Vila",
        "descricao": "Ajudar os moradores a proteger a vila de uma ameaça.",
        "status": "Concluída"
    }
]

# Os dados são carregados quando o servidor é iniciado.
personagens = carregar_dados(ARQUIVO_PERSONAGENS, PERSONAGENS_INICIAIS)
missoes = carregar_dados(ARQUIVO_MISSOES, MISSOES_INICIAIS)


@mcp.tool()
def listar_personagens() -> str:
    """Lista os personagens cadastrados com nome, raça, classe e nível."""
    if not personagens:
        return "Nenhum personagem cadastrado."

    linhas = ["Personagens cadastrados:"]

    for personagem in personagens:
        linhas.append(
            f"- {personagem['nome']} | Raça: {personagem['raca']} | "
            f"Classe: {personagem['classe']} | Nível: {personagem['nivel']}"
        )

    return "\n".join(linhas)


@mcp.tool()
def consultar_personagem(nome: str) -> str:
    """Consulta todas as informações de um personagem pelo nome."""
    nome = texto_obrigatorio(nome, "nome")
    personagem = buscar_por_nome(personagens, nome)

    if personagem is None:
        return f'O personagem "{nome}" não foi encontrado.'

    return (
        f"Personagem: {personagem['nome']}\n"
        f"Raça: {personagem['raca']}\n"
        f"Classe: {personagem['classe']}\n"
        f"Nível: {personagem['nivel']}"
    )


@mcp.tool()
def adicionar_personagem(nome: str, raca: str, classe: str, nivel: int) -> str:
    """Cadastra um personagem, validando os campos e evitando nomes duplicados."""
    nome = texto_obrigatorio(nome, "nome")
    raca = texto_obrigatorio(raca, "raca")
    classe = texto_obrigatorio(classe, "classe")

    if isinstance(nivel, bool) or not isinstance(nivel, int):
        raise ValueError("O nível deve ser um número inteiro.")
    if not 1 <= nivel <= 20:
        raise ValueError("O nível deve estar entre 1 e 20.")

    if buscar_por_nome(personagens, nome) is not None:
        return f'Já existe um personagem cadastrado com o nome "{nome}".'

    novo_personagem = {
        "nome": nome,
        "raca": raca,
        "classe": classe,
        "nivel": nivel
    }

    personagens.append(novo_personagem)
    salvar_dados(ARQUIVO_PERSONAGENS, personagens)

    return f'Personagem "{nome}" cadastrado com sucesso.'


@mcp.tool()
def listar_missoes() -> str:
    """Lista as missões cadastradas com nome, descrição e status."""
    if not missoes:
        return "Nenhuma missão cadastrada."

    linhas = ["Missões cadastradas:"]

    for missao in missoes:
        linhas.append(
            f"- {missao['nome']} | Descrição: {missao['descricao']} | "
            f"Status: {missao['status']}"
        )

    return "\n".join(linhas)


@mcp.tool()
def adicionar_missao(nome: str, descricao: str) -> str:
    """Cadastra uma missão com status inicial Pendente, sem nomes duplicados."""
    nome = texto_obrigatorio(nome, "nome")
    descricao = texto_obrigatorio(descricao, "descricao")

    if buscar_por_nome(missoes, nome) is not None:
        return f'Já existe uma missão cadastrada com o nome "{nome}".'

    nova_missao = {
        "nome": nome,
        "descricao": descricao,
        "status": "Pendente"
    }

    missoes.append(nova_missao)
    salvar_dados(ARQUIVO_MISSOES, missoes)

    return f'Missão "{nome}" cadastrada com sucesso. Status: Pendente.'


@mcp.tool()
def concluir_missao(nome: str) -> str:
    """Altera o status de uma missão existente para Concluída."""
    nome = texto_obrigatorio(nome, "nome")
    missao = buscar_por_nome(missoes, nome)

    if missao is None:
        return f'A missão "{nome}" não foi encontrada.'

    if missao["status"] == "Concluída":
        return f'A missão "{nome}" já está concluída.'

    missao["status"] = "Concluída"
    salvar_dados(ARQUIVO_MISSOES, missoes)

    return f'Missão "{nome}" concluída com sucesso.'


if __name__ == "__main__":
    # O protocolo MCP utiliza stdout para a comunicação.
    # Por isso, não adicione prints de depuração neste arquivo.
    mcp.run(transport="stdio")
