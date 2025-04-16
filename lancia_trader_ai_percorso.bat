@echo off
REM Esegui lo script Python per aggiornare dati.json
python robert_ai_trader.py

REM Committa e pusha i nuovi dati su GitHub
git add dati.json
git commit -m "Aggiorna dati con nuovo RSI"
git push origin main

REM Apri il file HTML nel browser usando percorso assoluto
start chrome "file:///C:/Users/Utente Hp/Desktop/robert-ai-trader/index.html"
