from kit_dados import veiculos, rotas, cargas

def mostrar_opcoes():
    print("============================================================")
    print(" SIMULADOR DE DESPACHO DE MISSAO LUNAR")
    print("============================================================")
    
    print("\n--- CARGAS ---")
    for c in cargas:
        print("[", c["id"], "]", c["tipo"], "-", c["massa_kg"], "kg")

    print("\n--- ROTAS ---")
    for r in rotas:
        print("[", r["id"], "]", r["origem"], "->", r["destino"], "(", r["distancia_km"], "km )")

    print("\n--- VEICULOS ---")
    for v in veiculos:
        print("[", v["id"], "]", v["modelo"], "(Max:", v["capacidade_kg"], "kg | Autonomia:", v["autonomia_km"], "km)")

def buscar(lista, id_desejado):
    for item in lista:
        if item["id"] == id_desejado:
            return item

def main():
    mostrar_opcoes()
    
    print("\n------------------------------------------------------------")
    id_carga = input("Digite o ID da carga: ").strip().upper()
    id_rota = input("Digite o ID da rota: ").strip().upper()
    id_veiculo = input("Digite o ID do veiculo: ").strip().upper()
    
    carga = buscar(cargas, id_carga)
    rota = buscar(rotas, id_rota)
    veiculo = buscar(veiculos, id_veiculo)
    
    if not carga or not rota or not veiculo:
        print("\nAlgum ID foi digitado incorretamente.")
        return

    print("\n============================================================")
    print(" ANALISANDO VIABILIDADE DA MISSAO...")
    print("============================================================")
    
    aprovado = True
    
    if carga["massa_kg"] > veiculo["capacidade_kg"]:
        aprovado = False
        print("-> FALHA: Carga muito pesada! Peso:", carga["massa_kg"], "kg | Suporta:", veiculo["capacidade_kg"], "kg")
    
    distancia_total = rota["distancia_km"] * 2
    bateria_necessaria = distancia_total * 1.2
    
    if bateria_necessaria > veiculo["autonomia_km"]:
        aprovado = False
        print("-> FALHA: Autonomia insuficiente. Necessario:", bateria_necessaria, "km | Disponivel:", veiculo["autonomia_km"], "km")
        
    if rota["risco"] == "alto" or rota["inclinacao_max_graus"] >= 15:
        print("-> AVISO: Rota com risco alto ou inclinacao de", rota["inclinacao_max_graus"], "graus.")

    print("------------------------------------------------------------")
    if aprovado:
        print("RESULTADO: MISSAO APROVADA! Veiculo pronto para o transporte.")
    else:
        print("RESULTADO: MISSAO REJEITADA! Ajuste os parametros.")
    print("============================================================")

if __name__ == "__main__":
    main()