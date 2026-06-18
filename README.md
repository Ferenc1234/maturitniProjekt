# maturitniProjekt


Jednoduchý měřák součástek

- většina měřáků měří přesnou hodnotu součástky, což je ale prakticky k ničemu, jelikož nás většinou zajímá řád, do kterého součástka spadá (Tj. řada např E12) a její toleranci od hodnoty řady. Například resistor 2356 ohmů je pro nás absolutně nesmyslná hodnota, ale pokud víme, že rezistor bude mít kapacitu v řadě E12 s tolerancí max 10% (obvyklá hodnota), zjistíme, že rezistor je mezi hodnotami 1980 a 2420, což spadá do hodnoty 2k2.

- E12 řada má místy hodnoty které se překrývají, pokud by měřák změřil hodnotu mezi, napsal by obě hodnoty a varování o zkontrolování značení (ideálně i barevné pruhy - rgb displej potřeba)

Systém by mohl využívat:

- **ESP32** jako řídicí jednotku a UI (např. displej / web rozhraní)
- **ADS1220 24-bit ADC** pro přesné měření napětí
- přesnou **referenci napětí (např. LM4040 / ADR4525)**
- přepínatelné rezistory pro různé měřicí rozsahy
- jednoduché proudové zdroje pro testování součástek

Identifikace součástek probíhá kombinací:
- napěťových charakteristik
- proudových odezev
- časových konstant (RC)
- odporových a diodových modelů



## 📊 Očekávaná přesnost

| Měření | Přesnost (reálně) |
|--------|------------------|
| Napětí | ~0.01–0.1 % |
| Rezistory | ~0.1–0.5 % |
| Kondenzátory | ~0.5–2 % |
| Indukčnosti | ~1–5 % |
| Diody | velmi dobrá (typ + Vf) |
| Tranzistory | dobrá (typ + parametry) |
| Baterie | orientační (stav + odpor) |



## 💰 Přibližná cena projektu

| Součástka | Cena |
|------------|------|
| ESP32 vývojová deska | 4–8 € |
| ADS1220 24-bit ADC modul | 10–20 € |
| Přesná reference napětí | 2–6 € |
| Operační zesilovače + diskrétní součástky | 5–15 € |
| Přesné rezistory (0.1 %) | 5–10 € |
| Přepínání rozsahů (relé / analog switch) | 5–15 € |
| Displej (volitelný OLED/TFT - ideálně barevný) | 3–10 € |

**➡ Celkem: ~25–70 € podle kvality provedení**



## ⚠️ Omezení

- 24-bit ADC neznamená automaticky laboratorní přesnost  
- velmi závislé na kvalitě referenčního napětí a layoutu PCB  
- bez AC generátoru je L/C měření omezené  
- identifikace složitých součástek je vždy pouze odhad
