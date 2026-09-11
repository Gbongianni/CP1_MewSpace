# KIT DE DADOS — MOBILIDADE
# Bases para projetos de transporte, exploração, seleção de veículos e análise de rotas.

veiculos = [
    {"id": "RV-01", "modelo": "Scout", "capacidade_kg": 180, "autonomia_km": 22.0, "bateria_pct": 94, "velocidade_kmh": 8},
    {"id": "RV-02", "modelo": "Cargo X1", "capacidade_kg": 480, "autonomia_km": 15.0, "bateria_pct": 86, "velocidade_kmh": 6},
    {"id": "RV-03", "modelo": "Cargo X2", "capacidade_kg": 650, "autonomia_km": 11.5, "bateria_pct": 78, "velocidade_kmh": 5},
    {"id": "RV-04", "modelo": "Explorer", "capacidade_kg": 120, "autonomia_km": 28.0, "bateria_pct": 91, "velocidade_kmh": 10},
    {"id": "RV-05", "modelo": "Crew Rover", "capacidade_kg": 300, "autonomia_km": 18.5, "bateria_pct": 83, "velocidade_kmh": 7},
    {"id": "RV-06", "modelo": "Utility", "capacidade_kg": 360, "autonomia_km": 16.0, "bateria_pct": 89, "velocidade_kmh": 6}
]

rotas = [
    {"id": "RT-01", "origem": "Base Alpha", "destino": "Mina A", "distancia_km": 7.2, "inclinacao_max_graus": 8, "risco": "baixo"},
    {"id": "RT-02", "origem": "Base Alpha", "destino": "Mina B", "distancia_km": 10.8, "inclinacao_max_graus": 14, "risco": "medio"},
    {"id": "RT-03", "origem": "Mina A", "destino": "Deposito", "distancia_km": 5.4, "inclinacao_max_graus": 10, "risco": "baixo"},
    {"id": "RT-04", "origem": "Deposito", "destino": "Base Alpha", "distancia_km": 6.1, "inclinacao_max_graus": 17, "risco": "alto"},
    {"id": "RT-05", "origem": "Base Alpha", "destino": "Cratera Sul", "distancia_km": 13.5, "inclinacao_max_graus": 12, "risco": "medio"},
    {"id": "RT-06", "origem": "Mina B", "destino": "Deposito", "distancia_km": 8.6, "inclinacao_max_graus": 19, "risco": "alto"}
]

cargas = [
    {"id": "CG-01", "tipo": "regolito", "massa_kg": 120, "prioridade": 2},
    {"id": "CG-02", "tipo": "gelo extraido", "massa_kg": 260, "prioridade": 1},
    {"id": "CG-03", "tipo": "baterias", "massa_kg": 180, "prioridade": 1},
    {"id": "CG-04", "tipo": "pecas mecanicas", "massa_kg": 310, "prioridade": 2},
    {"id": "CG-05", "tipo": "alimentos", "massa_kg": 95, "prioridade": 1},
    {"id": "CG-06", "tipo": "equipamentos cientificos", "massa_kg": 220, "prioridade": 3}
]

pontos_interesse = [
    {"nome": "Base Alpha", "coordenada": (10, 12)},
    {"nome": "Mina A", "coordenada": (18, 21)},
    {"nome": "Mina B", "coordenada": (25, 28)},
    {"nome": "Deposito", "coordenada": (15, 18)},
    {"nome": "Cratera Sul", "coordenada": (31, 9)},
    {"nome": "Estacao Energia", "coordenada": (8, 16)}
]

leituras_operacionais = [
    {"ciclo": 1, "veiculo": "RV-02", "bateria_pct": 86, "temp_motor_c": 42, "consumo_pct_km": 4.1},
    {"ciclo": 2, "veiculo": "RV-02", "bateria_pct": 78, "temp_motor_c": 45, "consumo_pct_km": 4.4},
    {"ciclo": 3, "veiculo": "RV-02", "bateria_pct": 69, "temp_motor_c": 47, "consumo_pct_km": 4.6},
    {"ciclo": 4, "veiculo": "RV-02", "bateria_pct": 61, "temp_motor_c": 51, "consumo_pct_km": 4.9},
    {"ciclo": 5, "veiculo": "RV-02", "bateria_pct": 54, "temp_motor_c": 54, "consumo_pct_km": 5.1},
    {"ciclo": 6, "veiculo": "RV-02", "bateria_pct": 46, "temp_motor_c": 56, "consumo_pct_km": 5.3}
]

# 0 = perigoso | 1 = seguro | 2 = atencao
mapa_terreno = [
    [1, 1, 1, 2, 2, 0],
    [1, 1, 2, 2, 1, 0],
    [1, 2, 2, 1, 1, 1],
    [1, 1, 1, 1, 2, 2],
    [2, 2, 1, 1, 1, 0],
    [0, 2, 2, 1, 1, 1]
]

# Referencia historica NASA/LROC: distancias percorridas por rovers lunares.
historico_rovers_lunares = [
    {"veiculo": "Lunokhod 1", "ano": 1970, "distancia_km": 10.54},
    {"veiculo": "Apollo 15 LRV", "ano": 1971, "distancia_km": 27.80},
    {"veiculo": "Apollo 16 LRV", "ano": 1972, "distancia_km": 26.70},
    {"veiculo": "Apollo 17 LRV", "ano": 1972, "distancia_km": 35.74},
    {"veiculo": "Lunokhod 2", "ano": 1973, "distancia_km": 42.15}
]
