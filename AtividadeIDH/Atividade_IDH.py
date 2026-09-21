from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PASTA_PROJETO = Path(__file__).resolve().parent
CAMINHO_CSV = PASTA_PROJETO / "Tabela4.csv"


def ler_tabela(arquivo):
    """Carrega o arquivo CSV e deixa os nomes das colunas padronizados."""
    dados = pd.read_csv(
        arquivo,
        sep=";",
        decimal=",",
        encoding="latin1",
        skiprows=1
    )

    # Remove colunas completamente vazias e espaços desnecessários.
    dados = dados.dropna(axis=1, how="all")
    dados.columns = [col.strip() for col in dados.columns]
    return dados


def converter_anos(dados):
    """Converte as colunas que representam anos para valores numéricos."""
    colunas_ano = [col for col in dados.columns if str(col).isdigit()]

    for ano in colunas_ano:
        dados[ano] = pd.to_numeric(dados[ano], errors="coerce")

    return colunas_ano


def analisar_idh(dados, anos):
    """Exibe informações gerais, ranking e evolução do IDH."""
    primeiro_ano = anos[0]
    ultimo_ano = anos[-1]

    dados["variacao"] = dados[ultimo_ano] - dados[primeiro_ano]

    print(f"\nPeríodo analisado: {primeiro_ano} até {ultimo_ano}.")
    print(f"Total de unidades federativas: {len(dados)}")

    # Ordena as UFs pelo IDH do último ano disponível.
    classificacao = (
        dados[["Sigla", "Estado", ultimo_ano]]
        .sort_values(by=ultimo_ano, ascending=False)
    )

    print(f"\nIDH das UFs em {ultimo_ano}:")
    print(classificacao.to_string(index=False))

    # Localiza a maior evolução entre o primeiro e o último ano.
    indice_maior = dados["variacao"].idxmax()
    registro = dados.loc[indice_maior]

    print(f"\nMaior crescimento: {registro['Estado']} ({registro['Sigla']})")
    print(f"Valor em {primeiro_ano}: {registro[primeiro_ano]:.3f}")
    print(f"Valor em {ultimo_ano}: {registro[ultimo_ano]:.3f}")
    print(f"Variação: {registro['variacao']:.3f}")

    quedas = dados.loc[
        dados["variacao"] < 0,
        ["Sigla", "Estado", primeiro_ano, ultimo_ano, "variacao"]
    ]

    if quedas.empty:
        print("\nNenhuma UF apresentou redução no período.")
    else:
        print("\nUFs que apresentaram redução:")
        print(quedas.to_string(index=False))


def organizar_historico(dados, anos):
    """Transforma a tabela para o formato adequado aos gráficos."""
    identificadores = [col for col in dados.columns if col not in anos]

    historico = dados.melt(
        id_vars=identificadores,
        value_vars=anos,
        var_name="Ano",
        value_name="IDH"
    )

    historico["Ano"] = historico["Ano"].astype(int)
    return historico.dropna(subset=["IDH"])


def plotar_minas(historico):
    """Cria o gráfico da evolução do IDH de Minas Gerais."""
    minas = historico.loc[historico["Sigla"].eq("MG")].sort_values("Ano")

    fig, eixo = plt.subplots(figsize=(9, 5))
    eixo.plot(minas["Ano"], minas["IDH"], marker="o")
    eixo.set_title("Evolução do IDH de Minas Gerais")
    eixo.set_xlabel("Ano")
    eixo.set_ylabel("IDH")
    eixo.set_ylim(0.3, 0.9)
    eixo.grid(alpha=0.25)

    fig.tight_layout()
    plt.show()


def plotar_todas_ufs(historico):
    """Desenha uma linha para cada unidade federativa."""
    fig, eixo = plt.subplots(figsize=(12, 7))

    for sigla, grupo in historico.groupby("Sigla"):
        grupo = grupo.sort_values("Ano")
        eixo.plot(
            grupo["Ano"],
            grupo["IDH"],
            label=sigla,
            linewidth=1.2
        )

    eixo.set_title("Evolução histórica do IDH por UF")
    eixo.set_xlabel("Ano")
    eixo.set_ylabel("IDH")
    eixo.set_ylim(0.3, 0.9)
    eixo.legend(ncol=3, bbox_to_anchor=(1.02, 1), loc="upper left")

    fig.tight_layout()
    plt.show()


def executar():
    tabela = ler_tabela(CAMINHO_CSV)
    anos = converter_anos(tabela)

    analisar_idh(tabela, anos)

    historico = organizar_historico(tabela, anos)
    plotar_minas(historico)
    plotar_todas_ufs(historico)


if __name__ == "__main__":
    executar()
