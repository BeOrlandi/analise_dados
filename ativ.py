import matplotlib.pyplot as plt
import seaborn as sns

###Atividade 2
reg = indicador_1[indicador_1["uf_regiao"].isin(regioes)].copy()

reg["homens"] = (reg["homem_branca"] + reg["homem_preta_parda"]) / 2
reg["mulheres"] = (reg["mulher_branca"] + reg["mulher_preta_parda"]) / 2

reg_long = reg.melt(
    id_vars="uf_regiao",
    value_vars=["homens", "mulheres"],
    var_name="sexo",
    value_name="horas"
)

fig, ax = plt.subplots(figsize=(9, 5))

sns.barplot(
    data=reg_long,
    x="uf_regiao",
    y="horas",
    hue="sexo",
    ax=ax
)

ax.set_title("Afazeres domésticos por região e sexo")
ax.set_xlabel("Região")
ax.set_ylabel("Horas / semana")

plt.tight_layout()
plt.show()

##Ativiade 3
brasil = pd.DataFrame(
    {
        "area": [
            "Graduação (total)",
            "STEM",
            "Saúde / educação"
        ],
        "homens": [
            formacao_total.loc[
                formacao_total["uf_regiao"] == "Brasil",
                "total_homens"
            ].item(),

            formacao_stem.loc[
                formacao_stem["uf_regiao"] == "Brasil",
                "homens"
            ].item(),

            formacao_saude.loc[
                formacao_saude["uf_regiao"] == "Brasil",
                "homens"
            ].item()
        ],
        "mulheres": [
            formacao_total.loc[
                formacao_total["uf_regiao"] == "Brasil",
                "total_mulheres"
            ].item(),

            formacao_stem.loc[
                formacao_stem["uf_regiao"] == "Brasil",
                "mulheres"
            ].item(),

            formacao_saude.loc[
                formacao_saude["uf_regiao"] == "Brasil",
                "mulheres"
            ].item()
        ]
    }
)

brasil_long = brasil.melt(
    id_vars="area",
    var_name="sexo",
    value_name="pessoas"
)

fig, ax = plt.subplots(figsize=(9, 5))

sns.barplot(
    data=brasil_long,
    x="area",
    y="pessoas",
    hue="sexo",
    ax=ax
)

ax.set_title("Brasil: pessoas com graduação, por área e sexo")
ax.set_xlabel("Área")
ax.set_ylabel("Pessoas")

plt.tight_layout()
plt.show()

###Atividade 4
ordem = pop_estado.sort_values("2022", ascending=False)

fig, ax = plt.subplots(figsize=(9, 8))

sns.barplot(
    data=ordem,
    y="UF",
    x="2022",
    ax=ax
)

ax.set_title("População 2022 por UF")
ax.set_xlabel("Habitantes")
ax.set_ylabel("UF")

plt.tight_layout()
plt.show()