import pandas as pd
from fpgrowth_py import fpgrowth
import pickle
import os

DATASET_FILE = '/home/datasets/spotify/2023_spotify_ds1.csv' 
MODEL_FILE = 'model.pkl'

MIN_SUP_RATIO = 0.05  
MIN_CONF = 0.5

N_ROWS_TO_READ = 15000 

def main():
    print(f"--- Iniciando Gerador de Regras ---")
    
    if not os.path.exists(DATASET_FILE):
        print(f"ERRO: Arquivo '{DATASET_FILE}' não encontrado.")
        return

    print(f"Lendo apenas as primeiras {N_ROWS_TO_READ} linhas de: {DATASET_FILE}")
    
    try:
        df = pd.read_csv(DATASET_FILE, nrows=N_ROWS_TO_READ)
        
        # Limpeza básica: remove nomes de músicas vazios
        df = df.dropna()
        
    except Exception as e:
        print(f"Erro ao ler CSV: {e}")
        return

    print("Agrupando playlists...")
    try:
        col_pid = 'pid' if 'pid' in df.columns else df.columns[0]
        col_track = 'track_name' if 'track_name' in df.columns else df.columns[1]
        
        # Agrupa
        transactions = df.groupby(col_pid)[col_track].apply(list).tolist()
        
        # 1. Corta playlists gigantes: pega só as 10 primeiras músicas de cada uma.
        # Isso reduz drasticamente o consumo de RAM do algoritmo.
        transactions = [t[:10] for t in transactions]
        
        # 2. Filtra: Mantém apenas playlists que tenham pelo menos 2 músicas (para ter regra A->B)
        transactions = [t for t in transactions if len(t) >= 2]       
 
    except Exception as e:
        print(f"Erro ao processar colunas: {e}")
        return

    print(f"Processando {len(transactions)} cestas válidas...")

    if len(transactions) == 0:
        print("Nenhuma transação válida encontrada. Aumente o N_ROWS_TO_READ.")
        return

    print(f"Executando FP-Growth (MinSup: {MIN_SUP_RATIO})...")
    try:
        freqItemSet, rules = fpgrowth(transactions, minSupRatio=MIN_SUP_RATIO, minConf=MIN_CONF)
        print(f"Sucesso! Regras geradas: {len(rules)}")
    except Exception as e:
        print(f"Erro ao executar fpgrowth (provavelmente memória): {e}")
        return

    print(f"Salvando modelo em '{MODEL_FILE}'...")
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(rules, f)
    print("Concluído com sucesso.")

if __name__ == "__main__":
    main()
