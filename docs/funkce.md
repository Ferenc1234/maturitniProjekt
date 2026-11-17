# High-Precision Component Tester & Curve Tracer

Bateriově napájený, vysoce přesný tester elektronických součástek (RLC metr, charakterograf a tester polovodičů) postavený na mikrokontroléru **ESP32-S3-WROOM-1-N8**.

---

## 1. Implementované a navržené HW funkce (Aktuální stav)

### 1.1 Analogové měřicí jádro a reference
* **24bitový diferenciální $\Sigma-\Delta$ ADC:** TI ADS1220IPWR zajišťující vysoké rozlišení a šumové parametry.
* **Precizní napěťová reference:** TI REF5025AIDR ($2,5\text{ V}$) s velmi nízkým teplotním driftem.
* **Oddělovací buffer reference:** První polovina ultra-přesného Zero-Drift operačního zesilovače TI OPA2333AIDR chrání referenční zdroj před proudovým zatížením.
* **Ratiometrická koncepce:** Měřicí děliče i ADC sdílejí stejný napěťový referenční potenciál ($V_{REF} = 2,5\text{ V}$), což eliminuje absolutní chybu reference.

### 1.2 Přepínání rozsahů a Kelvinovo zapojení
* **Měřicí rozsahy $1\text{ k}\Omega$ až $1\text{ M}\Omega$:** Přepínání pomocí analogového multiplexoru TMUX1108PWR s pA svodovými proudy.
* **Nízkoodporový rozsah $100\ \Omega$:** Obejití multiplexoru přes vyhrazený Low-Side N-MOSFET (Q3.2) ke spínání zátěže přímo k zemi.
* **4vodičové (Kelvinovo) zapojení:** Oddělené proudové (`MEASURE_HIGH`, `MEASURE_LOW`) a napěťové snímací cesty pro eliminaci odporu přívodních vodičů a přechodových odporů.
* **Precizní pasivní komponenty:** Všechny kritické měřicí rezistory jsou v toleranci $0.1\%$ (řada E96).

### 1.3 Vysokonapěťový testovací modul (Zenerovy diody)
* **24V větev:** Step-up měnič MT3608L generující $24\text{ V}$ z bateriového napájení.
* **Proudové omezení:** Proudový zdroj s LM317LIPK a přesným rezistorem $619\ \Omega\ (0.1\%)$ omezující proud na tvrdé $I_{const} = 2,019\text{ mA}$.
* **Bezpečnostní dělič:** Odporový dělič $100\text{ k}\Omega / 10\text{ k}\Omega\ (0.1\%)$ převádějící napětí až $24\text{ V}$ na bezpečný rozsah $0\text{ až }2,18\text{ V}$ pro ADC.
* **Galvanická a fyzická izolace:** Kompletní odpojení 24V modulu od 3.3V logiky a měřených svorek pomocí DPDT signálového relé (GBK-2F-Y3VDC).

### 1.4 L/C měřicí obvod
* **LC oscilátor:** Integrovaný oscilační obvod s rychlým komparátorem TI TLV3201 s reakční dobou v řádu nanosekund pro přesné měření indukčností a kapacit na základě změny rezonanční frekvence.

### 1.5 Napájení a rozhraní
* **Li-Ion/Li-Pol Nabíječ:** Integrovaný obvod TP4056 s řízením nabíjení z USB-C.
* **Nízkoúbytkový LDO regulátor:** AP2112K-3.3 s vysokým PSRR pro napájení 3.3V logiky a analogové části.
* **Konektivita:** Native USB rozhraní ESP32-S3 (USB_DN, USB_DP) pro programování a přenos dat do PC.

---

## 2. Plánované funkce a HW rozšíření (Roadmap)

### 2.1 Prahová oprava DRC a optimalizace přesnosti (HW & SW Fixes)
- [ ] **Korekce spínání $100\ \Omega$ rozsahu:** Náhrada tranzistoru 2N7002 (vnitřní odpor $R_{DS(on)} \approx 1,5\text{ až }2,5\ \Omega$) za N-MOSFET s ultra-nízkým $R_{DS(on)}$ (např. IRLML2502 s $R_{DS(on)} < 45\text{ m}\Omega$) nebo jazýčkové signálové relé.
- [ ] **Softwarová kompenzace MUXu:** Algoritmus v kódové základně započítávající typický odpor TMUX1108 ($R_{ON} \approx 2,5\ \Omega$) u $1\text{ k}\Omega$ rozsahu.
- [ ] **Dynamická kompenzace proudového zdroje 24V větve:** Výpočet reálného proudu Zenerovou diodou ve firmwaru odečtením proudu protékajícího paralelnou měřicí větví $110\text{ k}\Omega$:
  $$I_{DUT} = 2,019\text{ mA} - \frac{V_{změřené}}{110000\ \Omega}$$
- [ ] **Hardware Pull-up:** Přidání $10\text{ k}\Omega$ pull-up rezistoru na `ADC_CS` pin pro zamezení plovoucího stavu SPI při bootování ESP32.

### 2.2 Rozšíření o 3. svorku – Profesionální Charakterograf (BJT & MOSFET)
- [ ] **Budič řídicí elektrody (Gate/Base):**
  * Využití druhé poloviny operačního zesilovače OPA2333 (U4B) jako sledovače napětí.
  * Generování vyhlazeného DC napětí $0\text{ až }3,3\text{ V}$ pomocí LEDC PWM z ESP32 prohnaného přes RC filtr 2. řádu ($2\times 10\text{ k}\Omega + 2\times 100\text{ nF}$).
  * Zařazení sériového rezistoru $R_B = 10\text{ k}\Omega\ (0.1\%)$ pro proudové vymezení a měření proudu báze.
- [ ] **Přímé snímání přes ADC:**
  * Odpojení pinu `AIN3` (pin 7 na ADS1220) od GND a jeho zapojení na 3. svorku (za rezistor $R_B$) pro přesný odpočet napětí na hradle/bázi $V_{AIN3}$.
- [ ] **Měřicí algoritmy pro polovodiče:**
  * **BJT ($h_{FE}$):** Měření proudů báze $I_B = \frac{V_{PWM} - V_{AIN3}}{R_B}$ a kolektoru $I_C$ s výpočtem $h_{FE} = \frac{I_C}{I_B}$.
  * **MOSFET ($V_{GS(th)}$ a $R_{DS(on)}$):** Rampa $V_{GS}$ s detekcí prahového napětí $V_{GS(th)}$ při $I_D = 250\ \mu\text{A}$ a měření $R_{DS(on)}$ v plném sepnutí.

### 2.3 Bezpečný "Soft Pre-Scan" a autodetekce vývodů
- [ ] **Snímání bez rizika:** Implementace 3 pomocných GPIO pinů s $10\text{ k}\Omega$ rezistory zapojených na svorky TP1, TP2 a TP3.
- [ ] **Identifikační sekvence:** Měření PN přechodů a hradlové kapacity s vypnutými silovými větvemi.
- [ ] **Zobrazení pinoutu a výzva:** Detekce typu součástky (NPN/PNP, N/P-MOSFET) a zobrazení správného zapojení na displeji před započetím plného 24bitového testu.

### 2.4 Ochrana proti přepětí a nabitým kondenzátorům
- [ ] **Architektura "Safe-by-Default":** Fyzické galvanické odpojení citlivého 24bitového analogového jádra v klidovém stavu pomocí izolačních relé (G6K-2F-Y).
- [ ] **Vybíjecí a detekční obvod:**
  * Připojení svorek v klidovém stavu na vybíjecí výkonové rezistory $100\ \Omega\ / 2\text{ W}$ spojené s GND.
  * Snímání zbytkového napětí na svorkách pomocí napěťového děliče zapojeného do interního ADC ESP32 (chráněného Zenerovou a Schottkyho diodou).
- [ ] **Varovná signalizace:**
  * Automatický alarm při přítomnosti napětí $U > |0,5\text{ V}|$.
  * Vybíjecí rutina s vizuální indikací (LED + displej) a blokováním spuštění testu, dokud napětí neklesne bezpečně na $0\text{ V}$.

### 2.5 Tester externích akumulátorů a baterií
- [ ] **Měření vnitřního DC odporu ($R_{i,DC}$ / ESR):**
  * Pulzní metoda zatížení akumulátoru definovaným proudovým skokem ($I_{load} = 500\text{ mA}$) po dobu $50\text{ ms}$.
  * Výpočet vnitřního odporu z poklesu svorkového napětí:
    $$R_i = \frac{V_{OC} - V_{load}}{I_{load}}$$
- [ ] **Elektronická zátěž (Constant Current Sink):**
  * Nastavitelný proudový odběratel tvořený OPA2333, výkonovým N-MOSFETem a snímačem proudu $R_{sense} = 1\ \Omega\ / 3\text{ W}\ (0.1\%)$.
- [ ] **Testování kapacity (Discharge Capacity Tester):**
  * Integrace vybíjecího proudu v čase pro stanovení kapacity v $\text{mAh}$ a odevzdané energie v $\text{Wh}$.
  * Hardwarově i softwarově ošetřené bezpečnostní vypínací napětí (Cut-off voltage) pro zamezení podbití článku.
- [ ] **Teplotní ochrana (Thermal Cutoff):**
  * Monitorování teploty chladiče elektronické zátěže pomocí $10\text{ k}\Omega$ NTC termistoru s automatickým odpojením při překročení $65\ ^\circ\text{C}$.