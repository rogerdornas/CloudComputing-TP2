#!/bin/bash
URL="http://localhost:50026/api/recommend"
echo "--- Iniciando Monitoramento em $URL ---"
echo "Pressione [CTRL+C] para parar."

while true; do
    # Pega o código HTTP (ex: 200, 000 se cair)
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{"songs": ["Yesterday"]}' $URL)
    
    # Pega o corpo da resposta (JSON)
    RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d '{"songs": ["Yesterday"]}' $URL)
    
    # Extrai a versão e a data do modelo (usando grep/sed gambiarra para não depender de jq)
    VERSION=$(echo $RESPONSE | grep -o '"version":"[^"]*"' | cut -d'"' -f4)
    DATE=$(echo $RESPONSE | grep -o '"model_date":"[^"]*"' | cut -d'"' -f4)
    
    TIMESTAMP=$(date +"%H:%M:%S")
    
    if [ "$HTTP_CODE" == "200" ]; then
        echo "[$TIMESTAMP] Status: $HTTP_CODE | Ver: $VERSION | Model: $DATE"
    else
        echo "[$TIMESTAMP] Status: $HTTP_CODE | FALHA/OFFLINE"
    fi
    
    sleep 1
done
