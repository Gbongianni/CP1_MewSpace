# Analise de viabilidade

from kit_dados import mapa_terreno, pontos_interesse, rotas, veiculos

# CONSTANTES DE REGRA
INCLINACAO_MAX_OPERACIONAL = 15
BATERIA_MINIMA_PCT = 30
MARGEM_SEGURANCA = 1.2

# Legenda do mapa de terreno
LEGENDA_TERRENO = {0: "PERIGOSO", 1: "SEGURO", 2: "ATENCAO"}

MAX_COORD_X = 36  # maior X dos Pontos de Interesse (Cratera Sul = 31) + margem
MAX_COORD_Y = 32  # maior Y dos Pontos de Interesse (Mina B = 28) + margem

# FUNCOES DE CALCULO (indicadores)


def distancia_ida_volta(rota):
    # Indicador 1: distancia total de ida e volta
    return rota["distancia_km"] * 2


def tempo_estimado(rota, veiculo):
    # Indicador 2: tempo estimado em horas (ida e volta)
    return distancia_ida_volta(rota) / veiculo["velocidade_kmh"]


def consumo_estimado_pct(rota, veiculo):
    # Indicador 3: % de bateria consumida estimada
    if veiculo["autonomia_km"] == 0:
        return 100
    return (distancia_ida_volta(rota) / veiculo["autonomia_km"]) * 100


def distancia_euclidiana(nome1, nome2):
    # Indicador 4: distancia em linha reta entre dois pontos
    p1 = next((p["coordenada"] for p in pontos_interesse if p["nome"] == nome1), None)
    p2 = next((p["coordenada"] for p in pontos_interesse if p["nome"] == nome2), None)
    if p1 is None or p2 is None:
        return None
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def eficiencia_rota(rota):
    # Indicador 5: razao entre distancia da rota e linha reta
    d_reta = distancia_euclidiana(rota["origem"], rota["destino"])
    if d_reta is None or d_reta == 0:
        return None
    return rota["distancia_km"] / d_reta


# FUNCOES DE CLASSIFICACAO (regras)


def classificar_viabilidade(rota, veiculo):
    # Retorna VIAVEL / RESTRICAO / NAO RECOMENDADO
    if rota["inclinacao_max_graus"] > INCLINACAO_MAX_OPERACIONAL:
        return "NAO RECOMENDADO"
    if veiculo["bateria_pct"] < BATERIA_MINIMA_PCT:
        return "NAO RECOMENDADO"
    if distancia_ida_volta(rota) * MARGEM_SEGURANCA > veiculo["autonomia_km"]:
        return "NAO RECOMENDADO"
    if rota["risco"] == "alto" or rota["inclinacao_max_graus"] >= 12:
        return "RESTRICAO"
    return "VIAVEL"


def classificar_bateria(bateria_pct):
    # Classificacao de bateria: NORMAL / ATENCAO / CRITICO
    if bateria_pct >= 70:
        return "NORMAL"
    if bateria_pct >= 40:
        return "ATENCAO"
    return "CRITICO"


def classificar_risco(risco_str):
    # Normaliza o risco para exibicao.
    return {"baixo": "BAIXO", "medio": "MEDIO", "alto": "ALTO"}.get(
        risco_str, "DESCONHECIDO"
    )


def classificar_periculosidade(pct_perigoso):
    # Classifica o terreno com base no % de celulas perigosas.
    if pct_perigoso >= 25:
        return "CRITICO"
    elif pct_perigoso >= 10:
        return "ATENCAO"
    else:
        return "NORMAL"


# FUNCOES DE AGREGACAO


def contar_por_classificacao(resultados):
    # Conta quantos rovers ficaram em cada categoria.
    contagem = {"VIAVEL": 0, "RESTRICAO": 0, "NAO RECOMENDADO": 0}
    for r in resultados:
        contagem[r["classificacao"]] += 1
    return contagem


def medias_da_frota(veiculos):
    # Medias gerais da frota.
    n = len(veiculos)
    return {
        "bateria_media": sum(v["bateria_pct"] for v in veiculos) / n,
        "autonomia_media": sum(v["autonomia_km"] for v in veiculos) / n,
        "velocidade_media": sum(v["velocidade_kmh"] for v in veiculos) / n,
        "capacidade_total": sum(v["capacidade_kg"] for v in veiculos),
        "capacidade_maxima": max(v["capacidade_kg"] for v in veiculos),
        "bateria_minima": min(v["bateria_pct"] for v in veiculos),
    }


# FUNCOES DE ANALISE DA MATRIZ (mapa_terreno)


def estatisticas_terreno(matriz):
    # Conta celulas por tipo e calcula porcentagens.
    total = 0
    contagem = {0: 0, 1: 0, 2: 0}

    for linha in matriz:
        for celula in linha:
            contagem[celula] += 1
            total += 1

    if total == 0:
        return None

    return {
        "total": total,
        "seguro": contagem[1],
        "atencao": contagem[2],
        "perigoso": contagem[0],
        "pct_seguro": round(contagem[1] / total * 100, 1),
        "pct_atencao": round(contagem[2] / total * 100, 1),
        "pct_perigoso": round(contagem[0] / total * 100, 1),
    }


def consultar_celula(matriz, x, y):
    # Retorna o valor da celula (x, y) ou None se fora dos limites.
    if 0 <= y < len(matriz) and 0 <= x < len(matriz[0]):
        return matriz[y][x]
    return None


def converter_coordenada_para_celula(x, y):
    # Converte coordenada dos Pontos de Interesse para celula da matriz.

    colunas = len(mapa_terreno[0])
    linhas = len(mapa_terreno)

    cx = int(x / MAX_COORD_X * colunas)
    cy = int(y / MAX_COORD_Y * linhas)

    # garante que fica dentro dos limites
    cx = max(0, min(cx, colunas - 1))
    cy = max(0, min(cy, linhas - 1))
    return cx, cy


def analisar_entorno_pontos(matriz, pontos):
    # Para cada ponto de interesse:
    # - converte coordenada para celula da matriz
    # - verifica o valor da celula
    # - conta vizinhos perigosos (vizinhança 3x3).
    resultados = []
    for p in pontos:
        x_orig, y_orig = p["coordenada"]
        cx, cy = converter_coordenada_para_celula(x_orig, y_orig)

        valor = consultar_celula(matriz, cx, cy)
        if valor is None:
            resultados.append(
                {
                    "nome": p["nome"],
                    "coordenada": (x_orig, y_orig),
                    "celula": (cx, cy),
                    "status": "FORA DA MATRIZ",
                    "vizinhos_perigosos": 0,
                }
            )
            continue

        # conta vizinhos perigosos (0) na vizinhanca 3x3
        perigosos = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                v = consultar_celula(matriz, cx + dx, cy + dy)
                if v == 0:
                    perigosos += 1

        resultados.append(
            {
                "nome": p["nome"],
                "coordenada": (x_orig, y_orig),
                "celula": (cx, cy),
                "status": LEGENDA_TERRENO[valor],
                "vizinhos_perigosos": perigosos,
            }
        )
    return resultados


def gerar_recomendacao_terreno(stats):
    # Gera texto de recomendacao baseado nas estatisticas do terreno
    classe = classificar_periculosidade(stats["pct_perigoso"])

    if classe == "CRITICO":
        return (
            "CRITICO: mais de 25% do terreno mapeado e perigoso. "
            "Rotas devem ser replanejadas para evitar essas celulas."
        )
    elif classe == "ATENCAO":
        return (
            "ATENCAO: entre 10% e 25% do terreno e perigoso. "
            "Monitorar navegacao e evitar celulas 0 em qualquer rota."
        )
    else:
        return (
            "NORMAL: menos de 10% do terreno e perigoso. "
            "Operacao viavel com navegacao padrao."
        )


def gerar_recomendacao_ponto(resultado_ponto):
    # Recomendacao individual por ponto de interesse.
    if resultado_ponto["status"] == "PERIGOSO":
        return "EVITAR - ponto cai em celula perigosa"
    if resultado_ponto["vizinhos_perigosos"] >= 3:
        return "CAUTELA - muitos vizinhos perigosos"
    if resultado_ponto["status"] == "ATENCAO":
        return "MONITORAR - celula de atencao"
    return "OK - regiao segura"


# ANALISE COMPLETA DE UMA ROTA


def analisar_rota(rota):
    # Percorre todos os veiculos e classifica cada um para a rota
    resultados = []
    for v in veiculos:
        resultados.append(
            {
                "veiculo": v["id"],
                "modelo": v["modelo"],
                "classificacao": classificar_viabilidade(rota, v),
                "tempo_h": round(tempo_estimado(rota, v), 2),
                "consumo_pct": round(consumo_estimado_pct(rota, v), 1),
                "bateria_pct": v["bateria_pct"],
                "bateria_status": classificar_bateria(v["bateria_pct"]),
            }
        )
    return resultados


# RELATORIO


def gerar_relatorio():
    print("=" * 70)
    print(" PROGRAMA 1 — ANALISE DE VIABILIDADE DE ROTAS LUNARES")
    print("=" * 70)

    # --- Medias da frota ---
    m = medias_da_frota(veiculos)
    print("\n[INDICADORES GERAIS DA FROTA]")
    print(f"  Bateria media:      {m['bateria_media']:.1f} %")
    print(f"  Bateria minima:     {m['bateria_minima']} %")
    print(f"  Autonomia media:    {m['autonomia_media']:.1f} km")
    print(f"  Velocidade media:   {m['velocidade_media']:.1f} km/h")
    print(f"  Capacidade total:   {m['capacidade_total']} kg")
    print(f"  Capacidade maxima:  {m['capacidade_maxima']} kg")

    # --- Analise por rota ---
    total_viaveis = 0
    total_restricao = 0
    total_nao_rec = 0
    rotas_sem_opcao = []

    print("\n" + "=" * 70)
    print(" ANALISE POR ROTA")
    print("=" * 70)

    for rota in rotas:
        print(f"\n{rota['id']} | {rota['origem']} -> {rota['destino']}")
        print(
            f"  Distancia: {rota['distancia_km']} km "
            f"(ida/volta: {distancia_ida_volta(rota):.1f} km) | "
            f"Inclinacao: {rota['inclinacao_max_graus']} graus | "
            f"Risco: {classificar_risco(rota['risco'])}"
        )

        efic = eficiencia_rota(rota)
        if efic:
            print(f"  Eficiencia (rota/reta): {efic:.2f}")

        resultados = analisar_rota(rota)
        contagem = contar_por_classificacao(resultados)

        for r in resultados:
            marca = {"VIAVEL": "[OK]", "RESTRICAO": "[!]", "NAO RECOMENDADO": "[X]"}[
                r["classificacao"]
            ]
            print(
                f"    {marca} {r['veiculo']:<6} {r['modelo']:<12} "
                f"| {r['classificacao']:<15} "
                f"| tempo {r['tempo_h']:>5} h "
                f"| consumo {r['consumo_pct']:>5}% "
                f"| bateria {r['bateria_status']}"
            )

        total_viaveis += contagem["VIAVEL"]
        total_restricao += contagem["RESTRICAO"]
        total_nao_rec += contagem["NAO RECOMENDADO"]

        if contagem["VIAVEL"] == 0:
            rotas_sem_opcao.append(rota["id"])

    # --- Analise do mapa de terreno (MATRIZ) ---
    print("\n" + "=" * 70)
    print(" ANALISE DO MAPA DE TERRENO (MATRIZ)")
    print("=" * 70)

    stats = estatisticas_terreno(mapa_terreno)
    print(
        f"  Dimensoes da matriz: {len(mapa_terreno)} linhas x {len(mapa_terreno[0])} colunas"
    )
    print(f"  Total de celulas:    {stats['total']}")
    print(f"  Seguras (1):         {stats['seguro']:>3}  ({stats['pct_seguro']}%)")
    print(f"  Atencao (2):         {stats['atencao']:>3}  ({stats['pct_atencao']}%)")
    print(f"  Perigosas (0):       {stats['perigoso']:>3}  ({stats['pct_perigoso']}%)")
    print(f"  Classificacao:       {classificar_periculosidade(stats['pct_perigoso'])}")

    print("\n  Mapa visual (0=perigoso, 1=seguro, 2=atencao):")
    for i, linha in enumerate(mapa_terreno):
        print(f"    linha {i}: " + " ".join(str(c) for c in linha))

    print("\n  Entorno dos pontos de interesse (com conversao de escala):")
    for r in analisar_entorno_pontos(mapa_terreno, pontos_interesse):
        rec = gerar_recomendacao_ponto(r)
        print(
            f"    {r['nome']:<18} coord {r['coordenada']!s:<10} "
            f"-> celula {r['celula']!s:<8} "
            f"| {r['status']:<10} "
            f"| vizinhos perigosos: {r['vizinhos_perigosos']} "
            f"| {rec}"
        )

    print("\n  Recomendacao geral do terreno:")
    print(f"    {gerar_recomendacao_terreno(stats)}")

    # --- Conclusao ---
    print("\n" + "=" * 70)
    print(" CONCLUSAO E RECOMENDACOES")
    print("=" * 70)
    print(f"  Total de pares rota x veiculo avaliados: {len(rotas) * len(veiculos)}")
    print(f"  Viaveis:           {total_viaveis}")
    print(f"  Com restricao:     {total_restricao}")
    print(f"  Nao recomendados:  {total_nao_rec}")

    if rotas_sem_opcao:
        print(
            f"\n  ATENCAO: rotas sem nenhum rover viavel: {', '.join(rotas_sem_opcao)}"
        )
        print("  -> Recomendacao: revisar inclinacao, criar rota alternativa")
        print("     ou designar rover com maior capacidade de torque.")
    else:
        print("\n  Todas as rotas possuem pelo menos um rover viavel.")

    # Recomendacao baseada no terreno
    classe_terreno = classificar_periculosidade(stats["pct_perigoso"])
    print(f"\n  Terreno: {classe_terreno} ({stats['pct_perigoso']}% perigoso)")
    if classe_terreno == "CRITICO":
        print("  -> Recomendacao: suspender missoes nao essenciais; replanejar rotas.")
    elif classe_terreno == "ATENCAO":
        print("  -> Recomendacao: manter missoes com monitoramento reforcado.")
    else:
        print("  -> Recomendacao: missoes liberadas com navegacao padrao.")

    print("=" * 70)


# GERA O RELATORIO

if __name__ == "__main__":
    gerar_relatorio()
