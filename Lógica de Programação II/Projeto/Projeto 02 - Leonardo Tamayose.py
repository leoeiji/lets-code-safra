import json


def carregar_db(path: str = "db.json"):
    """Carrega o banco de dados de musicos e bandas

    Parameters
    ----------
    path : str, optional
        Caminho do arquivo json. O padrão é "db.json".

    Returns
    -------
    dict
        Dicionário com o banco de dados de musicos e bandas.
    """
    try:
        with open(path, "r", encoding="utf-8") as db:
            return json.load(db)
    except FileNotFoundError:
        # Se o arquivo não existir, cria um novo
        with open(path, "w", encoding="utf-8") as db:
            json.dump({"musicos": []}, db)
            return {"musicos": []}


def pegar_input(campos: dict, opcoes: list = None):
    """Pega os inputs do usuário

    Parameters
    ----------
    campos : dict
        Dicionário com os campos do formulário e as funções de validação
    opcoes : list, optional
        Lista de opções para o campo opção. O padrão é None.

    Returns
    -------
    tuple
        Tuple com as respostas em formato string
    """
    if opcoes is not None and len(campos) != len(opcoes):
        raise Exception("Os campos e as opções devem ter o mesmo tamanho")
    elif opcoes is None:
        opcoes = [None] * len(campos)

    output = []
    for (per, func), ops in zip(campos.items(), opcoes):
        # Mostrando o menu, se tiver
        if ops is not None:
            print("\n>> Escolha o número de uma opção:")
            for index, op in enumerate(ops, start=1):
                print(f"  {index}. {op}")

        # Validando resposta com a função dada
        res = input(f">> {per}")
        while func is not None and not func(res):
            print(">> Resposta inválida!")
            res = input(f">> {per}")

        output.append(tratar_strings(res))

    return tuple(output)


def str2lst(s: str, sep: str = ","):
    """Transforma uma string numa lista

    Parameters
    ----------
    s : str
        String com os itens separados por vírgula

    Returns
    -------
    list
        Lista dos itens separados
    """
    return [i.strip() for i in s.split(sep)]


def combinar_listas(*args):
    """Gerador que combina listas de listas

    Parameters
    ----------
    *args : list like
        Listas de listas a serem combinadas

    Yields
    ------
    tuple
        Tupla com uma combinação
    """
    listas = [tuple(lista) for lista in args]
    output = [[]]
    for sublista in listas:
        output = [x + [y] for x in output for y in sublista]
    for i in output:
        yield tuple(i)


def mostrar_musicos(lista_musicos: list[dict]):
    """Mostra os músicos na tela

    Parameters
    ----------
    lista_musicos : list
        Lista de músicos.
    """
    for musico in lista_musicos:
        generos_musicais = [i.title() for i in musico["generos_musicais"]]
        instrumentos = [i.title() for i in musico["instrumentos"]]
        print(f"\nNome: {musico['nome'].title()}")
        print(f"E-mail: {musico['email'].lower()}")
        print(f"Gêneros musicais: {', '.join(generos_musicais)}")
        print(f"Instrumentos: {', '.join(instrumentos)}")


def tratar_strings(string: "list or str"):
    """Trata as strings para guardar no banco de dados

    Parameters
    ----------
    string : list or str
        Lista de strings ou string para tratar.
    """
    if isinstance(string, str):
        return string.strip().upper()
    elif isinstance(string, list):
        return [tratar_strings(string=i) for i in string]


def cadastrar_musico(nome: str, email: str, generos_musicais: list, instrumentos: list):
    """Cadastra um novo musico no banco de dados

    Parameters
    ----------
    nome : str
        Nome do musico.
    email : str
        Email do musico.
    generos_musicais : list
        Lista de gêneros musicais do musico.
    instrumentos : list
        Lista de instrumentos do musico.
    """
    db = carregar_db()

    # Checando se o email já existe
    emails = [musico["email"] for musico in db["musicos"]]
    if email in emails:
        raise Exception(">> Email já foi cadastrado!")

    db["musicos"].append(
        {
            "nome": nome,
            "email": email,
            "generos_musicais": generos_musicais,
            "instrumentos": instrumentos,
        }
    )

    with open("db.json", "w", encoding="utf-8") as arquivo:
        json.dump(db, arquivo, indent=4, sort_keys=True, ensure_ascii=False)


def buscar_musicos(exato=True, **kwargs):
    """Busca músicos no banco de dados

    Parameters
    ----------
    exato : bool
        True se todos os parâmetros devem ser cumpridos.
    **kwargs : dict
        Dicionário com os parâmetros a serem buscados.


    Returns
    -------
    list
        Lista de músicos que atendem aos critérios de busca.
    """
    if len(kwargs) == 0:
        raise Exception(">> Deve haver pelo menos um parâmetro de busca!")

    # Carregando banco de dados
    musicos: list[dict] = carregar_db()["musicos"]

    output = []
    for musico in musicos:
        bools = []
        for param, valor_busca in kwargs.items():
            valor_db = musico.get(param)
            if valor_db is None:
                raise Exception(f">> Parâmetro {param} não encontrado!")

            if isinstance(valor_db, list):
                bools.append(valor_busca in valor_db)
            else:
                bools.append(valor_db == valor_busca)

        # Se for exato, todos os parâmetros devem ser cumpridos
        if exato and False in bools:
            continue
        else:
            output.append(musico)

    return output


def modificar_musicos(email: str, add=True, **kwargs):
    """Modifica os dados de um músico

    Parameters
    ----------
    email : str
        Email do músico.
    add : bool
        True se deve adicionar, False se deve remover.
    **kwargs : dict
        Dicionário com os parâmetros a serem modificados.
    """
    db = carregar_db()

    musico = buscar_musicos(email=email)
    if len(musico) == 0:
        raise Exception(">> Email não encontrado!")
    else:
        # Remove o músico para depois adicioná-lo
        musico = musico[0]
        db["musicos"].remove(musico)

    for param, valor in kwargs.items():
        if param in musico:
            if add:
                musico[param].append(valor)
            else:
                musico[param].remove(valor)
                if len(musico[param]) == 0:
                    raise Exception(f">> Parâmetro {param} não pode estar vazio!")

    db["musicos"].append(musico)
    with open("db.json", "w", encoding="utf-8") as arquivo:
        json.dump(db, arquivo, indent=4, sort_keys=True, ensure_ascii=False)


def montar_bandas(genero: str, instrumentos: tuple):
    """Monta as bandas de acordo com o gênero e os instrumentos

    Parameters
    ----------
    genero : str
        Gênero musical da banda.
    instrumentos : tuple
        Instrumentos que a banda precisa.

    Returns
    -------
    list
    """
    listas_musicos = []
    for instr in instrumentos:
        musicos = buscar_musicos(generos_musicais=genero, instrumentos=instr)
        if len(musicos) == 0:
            raise Exception(f">> Não há músicos de {genero} que tocam {instr}!")
        listas_musicos.append(musicos)

    # Montando as bandas
    bandas = list(combinar_listas(*listas_musicos))

    # Removendo bandas com artistas repetidos
    bandas = list(
        filter(
            lambda banda: len(set([x["email"] for x in banda])) == len(banda), bandas
        )
    )

    if len(bandas) == 0:
        raise Exception(">> Não há bandas que atendam aos critérios!")

    return bandas


def menu():
    """Menu principal do programa"""

    menu_perg = {
        "Qual operação deseja realizar? ": lambda x: x in ["1", "2", "3", "4", "5"]
    }
    menu_ops = [
        "Cadastrar músico",
        "Buscar músicos",
        "Modificar músicos",
        "Montar uma banda",
        "Sair",
    ]
    op = pegar_input(menu_perg, [menu_ops])[0]

    while op != "5":
        if op == "1":
            # Cadastrar musico
            try:
                perguntas = {
                    "Nome: ": lambda x: x.replace(" ", "").isalpha(),
                    "E-mail: ": lambda x: x.count("@") == 1,
                    "Gêneros musicais (separados por vírgula): ": lambda x: x != "",
                    "Instrumentos (separados por vírgula): ": lambda x: x != "",
                }
                dados_musico = list(pegar_input(perguntas))
                dados_musico[2] = str2lst(dados_musico[2])
                dados_musico[3] = str2lst(dados_musico[3])
                cadastrar_musico(*dados_musico)
                print(">> Músico cadastrado com sucesso!")
            except Exception as e:
                print(e)

        elif op == "2":
            # Buscar músicos
            try:
                perguntas = {
                    "A busca deve ser exata? (s/n): ": lambda x: x in ("s", "n"),
                    "Nome: ": None,
                    "E-mail: ": None,
                    "Gêneros musicais (separados por vírgula): ": None,
                    "Instrumentos (separados por vírgula): ": None,
                }
                campos = ["exato", "nome", "email", "generos_musicais", "instrumentos"]

                # Criando dicionário para a busca
                dados_busca = dict(zip(campos, pegar_input(perguntas)))
                dados_busca = {k: v for k, v in dados_busca.items() if v != ""}
                dados_busca["exato"] = dados_busca["exato"] == "S"
                musicos = buscar_musicos(**dados_busca)
                if len(musicos) == 0:
                    print(">> Nenhum músico encontrado!")
                else:
                    print(f"\n>> Músicos encontrados (total: {len(musicos)}):")
                    mostrar_musicos(musicos)

            except Exception as e:
                print(e)

        elif op == "3":
            # Modificar músico
            campos = ["Gêneros musicais", "Instrumentos"]
            opcoes = ["Adicionar", "Remover"]
            perguntas = {
                "E-mail do músico: ": lambda x: x.count("@") == 1,
                "O que deseja modificar? ": lambda x: x.isdigit() and 1 <= int(x) <= 2,
                "Adicionar ou remover? ": lambda x: x.isdigit() and 1 <= int(x) <= 2,
                "Qual o valor? ": None,
            }
            email, campo, opcao, valor = pegar_input(
                perguntas, [None, campos, opcoes, None]
            )
            campos = ["generos_musicais", "instrumentos"]
            try:
                modificar_musicos(
                    email=email, add=int(opcao) == 1, **{campos[int(campo) - 1]: valor}
                )
            except Exception as e:
                print(e)

        elif op == "4":
            # Montar bandas
            genero, n_pessoas = pegar_input(
                {
                    "Qual o gênero musical? ": None,
                    "Quantos integrantes? ": lambda x: x.isdigit() and int(x) > 0,
                }
            )

            instrumentos = pegar_input(
                {
                    f"Instrumento do integrante {i}: ": None
                    for i in range(1, int(n_pessoas) + 1)
                }
            )

            try:
                bandas = montar_bandas(genero, instrumentos)
                for i, banda in enumerate(bandas, 1):
                    print(f"\n{'-'*20} Banda {i} {'-'*20}")
                    for index, integrante in enumerate(banda):
                        print(
                            f"{instrumentos[index].title()}: {integrante['nome'].title()}, {integrante['email'].lower()}"
                        )

            except Exception as e:
                print(e)

        op = pegar_input(menu_perg, [menu_ops])[0]


if __name__ == "__main__":
    menu()
