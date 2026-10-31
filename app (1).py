from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Painel de dados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
RNG = np.random.default_rng(42)


def criar_dados():
    categorias = ["Eletrônicos", "Roupas", "Casa", "Esportes"]
    regioes = ["Norte", "Sul", "Sudeste", "Centro-Oeste"]
    barras = pd.DataFrame([
        {"categoria": categoria, "regiao": regiao,
         "vendas_medias": int(RNG.integers(120, 520))}
        for categoria in categorias for regiao in regioes
    ])

    departamentos = ["TI", "Vendas", "RH", "Financeiro"]
    boxplot = pd.DataFrame({
        "departamento": RNG.choice(departamentos, 80),
        "salario": RNG.normal(5200, 1400, 80).clip(2200, 12000),
    })

    dispersao = pd.DataFrame({
        "sexo": RNG.choice(["Feminino", "Masculino"], 70),
        "altura_cm": RNG.normal(170, 9, 70),
    })
    dispersao["peso_kg"] = (dispersao["altura_cm"] - 100) * 0.85 + RNG.normal(0, 7, 70)

    distribuicao = pd.DataFrame({"idade": RNG.integers(18, 72, 100)})
    frequencia = pd.DataFrame({
        "tipo_atendimento": RNG.choice(
            ["Dúvida", "Reclamação", "Solicitação", "Elogio"],
            120,
            p=[0.34, 0.22, 0.31, 0.13],
        )
    })

    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    horarios = ["08h", "10h", "12h", "14h", "16h", "18h"]
    heatmap = pd.DataFrame([
        {"dia_semana": dia, "horario": horario,
         "movimento_clientes": int(RNG.integers(10, 110))}
        for dia in dias for horario in horarios
    ])

    datas = pd.date_range("2025-01-01", periods=30, freq="D")
    linhas = pd.DataFrame([
        {"data": data, "loja": loja, "vendas": int(RNG.integers(80, 400))}
        for loja in ["Loja A", "Loja B", "Loja C"] for data in datas
    ])

    pizza = pd.DataFrame({
        "canal_venda": ["Loja física", "E-commerce", "Marketplace", "Televendas"],
        "faturamento": [42000, 68000, 31000, 12000],
    })

    regressao = pd.DataFrame({"renda_mensal": RNG.integers(1800, 15000, 80)})
    regressao["gasto_mensal"] = regressao["renda_mensal"] * 0.31 + RNG.normal(0, 650, 80)

    return barras, boxplot, dispersao, distribuicao, frequencia, heatmap, linhas, pizza, regressao


def configurar_grafico(fig, ax):
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def grafico_barras(df):
    categorias = list(df["categoria"].unique())
    regioes = list(df["regiao"].unique())
    fig, ax = plt.subplots(figsize=(6, 3.8))
    largura = 0.2
    x = np.arange(len(categorias))
    for i, regiao in enumerate(regioes):
        valores = [df[(df["categoria"] == categoria) & (df["regiao"] == regiao)]["vendas_medias"].iloc[0] for categoria in categorias]
        ax.bar(x + (i - 1.5) * largura, valores, largura, label=regiao)
    ax.set_xticks(x)
    ax.set_xticklabels(categorias, rotation=15)
    ax.set_title("Vendas médias por categoria e região")
    ax.set_xlabel("Categoria")
    ax.set_ylabel("Vendas médias")
    ax.legend(fontsize=7)
    return configurar_grafico(fig, ax)


def grafico_boxplot(df):
    departamentos = list(df["departamento"].unique())
    valores = [df[df["departamento"] == departamento]["salario"] for departamento in departamentos]
    fig, ax = plt.subplots(figsize=(6, 3.8))
    ax.boxplot(valores)
    ax.set_xticklabels(departamentos, rotation=15)
    ax.set_title("Salário por departamento")
    ax.set_xlabel("Departamento")
    ax.set_ylabel("Salário (R$)")
    return configurar_grafico(fig, ax)


def grafico_dispersao(df):
    fig, ax = plt.subplots(figsize=(6, 3.8))
    for sexo, marcador in zip(df["sexo"].unique(), ["o", "x"]):
        dados = df[df["sexo"] == sexo]
        ax.scatter(dados["altura_cm"], dados["peso_kg"], marker=marcador, label=sexo, alpha=0.8)
    ax.set_title("Altura x Peso")
    ax.set_xlabel("Altura (cm)")
    ax.set_ylabel("Peso (kg)")
    ax.legend(fontsize=8)
    return configurar_grafico(fig, ax)


def grafico_distribuicao(df):
    fig, ax = plt.subplots(figsize=(6, 3.8))
    ax.hist(df["idade"], bins=10, edgecolor="black", color="#4C78A8")
    ax.set_title("Distribuição da idade dos clientes")
    ax.set_xlabel("Idade")
    ax.set_ylabel("Frequência")
    return configurar_grafico(fig, ax)


def grafico_frequencia(df):
    contagem = df["tipo_atendimento"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 3.8))
    ax.bar(contagem.index, contagem.values, edgecolor="black", color="#F58518")
    for i, valor in enumerate(contagem.values):
        ax.text(i, valor + 1, str(valor), ha="center", fontsize=9)
    ax.set_title("Frequência por tipo de atendimento")
    ax.set_xlabel("Tipo de atendimento")
    ax.set_ylabel("Quantidade")
    ax.tick_params(axis="x", rotation=15)
    return configurar_grafico(fig, ax)


def grafico_heatmap(df):
    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    tabela = df.pivot(index="dia_semana", columns="horario", values="movimento_clientes").reindex(dias)
    fig, ax = plt.subplots(figsize=(6, 3.8))
    imagem = ax.imshow(tabela.values, cmap="YlOrRd", aspect="auto")
    ax.set_xticks(range(len(tabela.columns)), tabela.columns)
    ax.set_yticks(range(len(tabela.index)), tabela.index)
    for i in range(tabela.shape[0]):
        for j in range(tabela.shape[1]):
            ax.text(j, i, int(tabela.values[i, j]), ha="center", va="center", fontsize=8)
    fig.colorbar(imagem, ax=ax, label="Movimento de clientes")
    ax.set_title("Movimento de clientes por dia e horário")
    ax.set_xlabel("Horário")
    ax.set_ylabel("Dia da semana")
    return configurar_grafico(fig, ax), tabela


def grafico_linhas(df):
    df = df.sort_values("data")
    fig, ax = plt.subplots(figsize=(6, 3.8))
    for loja in sorted(df["loja"].unique()):
        dados = df[df["loja"] == loja]
        ax.plot(dados["data"], dados["vendas"], marker="o", markersize=3, label=loja)
    ax.set_title("Vendas ao longo do tempo")
    ax.set_xlabel("Data")
    ax.set_ylabel("Vendas")
    ax.legend(fontsize=8)
    fig.autofmt_xdate()
    return configurar_grafico(fig, ax)


def grafico_pizza(df):
    fig, ax = plt.subplots(figsize=(6, 3.8))
    ax.pie(df["faturamento"], labels=df["canal_venda"], autopct="%1.1f%%", startangle=90)
    ax.set_title("Faturamento por canal de venda")
    return configurar_grafico(fig, ax)


def grafico_regressao(df):
    m, b = np.polyfit(df["renda_mensal"], df["gasto_mensal"], 1)
    r2 = np.corrcoef(df["renda_mensal"], df["gasto_mensal"])[0, 1] ** 2
    x = np.linspace(df["renda_mensal"].min(), df["renda_mensal"].max(), 100)
    fig, ax = plt.subplots(figsize=(6, 3.8))
    ax.scatter(df["renda_mensal"], df["gasto_mensal"], alpha=0.7, label="Dados")
    ax.plot(x, m * x + b, color="red", label=f"y = {m:.3f}x + {b:.1f} (R² = {r2:.3f})")
    ax.set_title("Renda mensal x Gasto mensal")
    ax.set_xlabel("Renda mensal (R$)")
    ax.set_ylabel("Gasto mensal (R$)")
    ax.legend(fontsize=7)
    return configurar_grafico(fig, ax), r2


st.markdown("""
<style>
.main-title {font-size: 2.35rem; font-weight: 750; color: #17324d; margin-bottom: .1rem;}
.subtitle {color: #5f6f7f; font-size: 1.05rem; margin-bottom: 1.2rem;}
.analysis {background: #f2f6fa; border-left: 4px solid #2f80ed; padding: .7rem .8rem; border-radius: 0 8px 8px 0; min-height: 78px; color: #334e68; font-size: .9rem;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Seus dados")
    nome = st.text_input("Nome", "Felipe Lloyd")
    chamada = st.text_input("Número da chamada", "12")
    turma = st.text_input("Turma", "3D2")

st.markdown('<div class="main-title">Painel de dados</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Uma visão geral dos principais resultados</div>', unsafe_allow_html=True)
st.caption(f"Aluno: **{nome}** · Chamada: **{chamada}** · Turma: **{turma}**")

barras, boxplot, dispersao, distribuicao, frequencia, heatmap, linhas, pizza, regressao = criar_dados()

graficos = [
    ("Vendas por categoria", grafico_barras(barras), "A categoria com maior média de vendas é **" + barras.groupby("categoria")["vendas_medias"].mean().idxmax() + "**."),
    ("Salários por departamento", grafico_boxplot(boxplot), "A comparação mostra as medianas e a variação dos salários em cada departamento."),
    ("Altura e peso", grafico_dispersao(dispersao), f"A correlação entre altura e peso é **{dispersao['altura_cm'].corr(dispersao['peso_kg']):.2f}**, indicando a tendência observada nos dados."),
    ("Faixa etária", grafico_distribuicao(distribuicao), f"A idade mediana dos clientes é **{distribuicao['idade'].median():.0f} anos**."),
    ("Tipos de atendimento", grafico_frequencia(frequencia), "O gráfico mostra quais tipos de atendimento aparecem com maior frequência."),
]
heatmap_fig, heatmap_table = grafico_heatmap(heatmap)
graficos.append(("Movimento de clientes", heatmap_fig, "As áreas mais escuras indicam os dias e horários com maior movimento de clientes."))
graficos.append(("Gráfico de linhas", grafico_linhas(linhas), "A evolução temporal permite comparar o desempenho das três lojas ao longo do período."))
graficos.append(("Gráfico de pizza", grafico_pizza(pizza), "O e-commerce representa o maior percentual do faturamento total."))
regressao_fig, r2 = grafico_regressao(regressao)
graficos.append(("Regressão linear", regressao_fig, f"A reta mostra a relação entre renda e gasto mensal. O coeficiente R² calculado é **{r2:.2f}**."))

for inicio in range(0, len(graficos), 3):
    colunas = st.columns(3, gap="medium")
    for coluna, (titulo, figura, analise) in zip(colunas, graficos[inicio:inicio + 3]):
        with coluna:
            st.subheader(titulo)
            st.pyplot(figura, clear_figure=False)
            st.markdown(f'<div class="analysis"><b>Análise:</b> {analise}</div>', unsafe_allow_html=True)
            plt.close(figura)
    if inicio + 3 < len(graficos):
        st.divider()

st.divider()
st.caption("Use os gráficos para comparar os resultados, perceber tendências e encontrar os pontos que mais chamam atenção.")
