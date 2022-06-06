import json
import os.path
import sys


def obter_dados() -> list:
    """
    Essa função carrega os dados dos produtos e retorna uma lista de dicionários, onde cada dicionário representa um produto.
    NÃO MODIFIQUE essa função.
    """
    with open(os.path.join(sys.path[0], "dados.json"), "r") as arq:
        dados = json.loads(arq.read())
    return dados


def listar_categorias(dados: list) -> list:
    """
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    Essa função deverá retornar uma lista contendo todas as categorias dos diferentes produtos.
    Cuidado para não retornar categorias repetidas.
    """
    categorias = []
    for product in dados:
        if product["categoria"] not in categorias:
            categorias.append(product["categoria"])

    return categorias


def listar_por_categoria(dados: list, categoria: str) -> list:
    """
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    O parâmetro "categoria" é uma string contendo o nome de uma categoria.
    Essa função deverá retornar uma lista contendo todos os produtos pertencentes à categoria dada.
    """
    output = []
    for product in dados:
        if product["categoria"] == categoria:
            output.append(product)

    return output


def produto_mais_caro(dados: list, categoria: str) -> dict:
    """
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    O parâmetro "categoria" é uma string contendo o nome de uma categoria.
    Essa função deverá retornar um dicionário representando o produto mais caro da categoria dada.
    """
    produtos = listar_por_categoria(dados, categoria)
    produtos = sorted(produtos, key=lambda produto: produto["preco"])

    return produtos[-1]


def produto_mais_barato(dados: list, categoria: str) -> dict:
    """
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    O parâmetro "categoria" é uma string contendo o nome de uma categoria.
    Essa função deverá retornar um dicionário representando o produto mais caro da categoria dada.
    """
    produtos = listar_por_categoria(dados, categoria)
    produtos = sorted(produtos, key=lambda produto: produto["preco"])

    return produtos[0]


def top_10_caros(dados: list) -> list:
    """
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    Essa função deverá retornar uma lista de dicionários representando os 10 produtos mais caros.
    """
    dados = sorted(
        dados, key=lambda produto: float(produto["preco"]), reverse=True
    )
    return dados[:10]


def top_10_baratos(dados: list) -> list:
    """
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    Essa função deverá retornar uma lista de dicionários representando os 10 produtos mais baratos.
    """
    dados = sorted(dados, key=lambda produto: float(produto["preco"]))
    return dados[:10]


def mostrar_opcoes(opcoes: "dict or list", titulo: str) -> None:
    """
    O parâmetro "options" deve ser um dicionário representando as opções do menu ou uma lista de strings representando as opções do menu.
    O parâmetro "title" é uma string contendo o título do menu.
    Essa função exibe as opções do menu.
    """
    titulo = f"\n-------- {titulo} --------"
    print(titulo)

    if type(opcoes) == dict:
        for key, opcao in opcoes.items():
            print(f"[{key}]. {opcao}")

    elif type(opcoes) == list:
        for index, opcao in enumerate(opcoes):
            print(f"[{index}]. {opcao}")

    print("-" * (len(titulo) - 1) + "\n")


def mostrar_produtos(produtos: list, titulo: str) -> None:
    """
    O parâmetro "produtos" deve ser uma lista de dicionários representando os produtos.
    O parâmetro "titulo" é uma string contendo o título a ser exibido antes dos produtos.
    Essa função exibe os produtos na tela.
    """
    titulo = f"\n-------- {titulo} --------"
    print(titulo)

    for index, produto in enumerate(produtos):
        print(f"[{index}]. ID: {produto['id']} - R${produto['preco']}")

    print("-" * (len(titulo) - 1) + "\n")


def escolher_opcao_dict(opcoes: "dict") -> str:
    """
    O parâmetro "opcoes" deve ser um dicionário representando as opções do menu.
    Essa função exibe as opções do menu e retorna a opção escolhida pelo usuário.
    """
    mostrar_opcoes(opcoes, "Opções Disponíveis")

    opcao = None
    while opcao not in opcoes:
        opcao = input(">> Digite a opção desejada: ")
        if opcao not in opcoes:
            print("Opção inválida! Escolha novamente.")
        print()

    return opcao


def escolher_opcao_list(opcoes: "list") -> str:
    """
    O parâmetro "opcoes" deve ser uma lista representando as opções do menu.
    Essa função exibe as opções do menu e retorna a opção escolhida pelo usuário.
    """
    mostrar_opcoes(opcoes, "Opções Disponíveis")

    index_opcao = None
    lista_verificar = [str(i) for i in range(len(opcoes))]
    while index_opcao not in lista_verificar:
        index_opcao = input(">> Digite o número da opção desejada: ")
        if index_opcao not in lista_verificar:
            print("Opção inválida! Escolha novamente.")
        print()

    return opcoes[int(index_opcao)]


def menu(dados: list) -> None:
    """
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    Essa função deverá, em loop, realizar as seguintes ações:
    - Exibir as seguintes opções:
        1. Listar categorias
        2. Listar produtos de uma categoria
        3. Produto mais caro por categoria
        4. Produto mais barato por categoria
        5. Top 10 produtos mais caros
        6. Top 10 produtos mais baratos
        0. Sair
    - Ler a opção do usuário.
    - No caso de opção inválida, imprima uma mensagem de erro.
    - No caso das opções 2, 3 ou 4, pedir para o usuário digitar a categoria desejada.
    - Chamar a função adequada para tratar o pedido do usuário e salvar seu retorno.
    - Imprimir o retorno salvo.
    O loop encerra quando a opção do usuário for 0.
    """
    options = {
        "1": "Listar categorias",
        "2": "Listar produtos de uma categoria",
        "3": "Produto mais caro por categoria",
        "4": "Produto mais barato por categoria",
        "5": "Top 10 produtos mais caros",
        "6": "Top 10 produtos mais baratos",
        "0": "Sair",
    }

    option = None
    while option != "0":
        option = escolher_opcao_dict(options)

        # Call function
        if option == "1":
            lista = listar_categorias(dados)
            mostrar_opcoes(lista, "Categorias")
        elif option == "2":
            categoria = escolher_opcao_list(listar_categorias(dados))
            lista = listar_por_categoria(dados, categoria)
            mostrar_produtos(lista, f"Produtos da categoria '{categoria}'")
        elif option == "3":
            categoria = escolher_opcao_list(listar_categorias(dados))
            produto = produto_mais_caro(dados, categoria)
            print(f"O produto mais caro da categoria '{categoria}':")
            print(f"\tID: {produto['id']}")
            print(f"\tPreço: {produto['preco']}")
        elif option == "4":
            categoria = escolher_opcao_list(listar_categorias(dados))
            produto = produto_mais_barato(dados, categoria)
            print(f"O produto mais barato da categoria '{categoria}':")
            print(f"\tID: {produto['id']}")
            print(f"\tPreço: {produto['preco']}")
        elif option == "5":
            lista = top_10_caros(dados)
            mostrar_produtos(lista, "Top 10 produtos mais caros")
        elif option == "6":
            lista = top_10_baratos(dados)
            mostrar_produtos(lista, "Top 10 produtos mais baratos")

    else:
        print("Até logo!")


# Programa Principal - não modificar!
dados = obter_dados()
menu(dados)
