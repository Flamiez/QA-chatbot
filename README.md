# iToDev QA chatbot
---
## Įsirašymo gidas
### 1. Įsirašyti uv
Dokumentacija: https://docs.astral.sh/uv/getting-started/installation/#standalone-installer
#### Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# arba neturing curl
wget -qO- https://astral.sh/uv/install.sh | sh
```
#### Windows
```bash
pip install uv
```
---
### 2. Turėti įsirašius bet kurią dockerizavimo programą, jei neturite galite įsirašyti docker desktop nurodytą žemiau
- Windows dokumentacija: https://docs.docker.com/desktop/setup/install/windows-install/
- Linux dokumentacija: https://docs.docker.com/desktop/setup/install/linux/

### 3. bibliotekų įdiegimas
- Atsidaryti pagrindinį projekto aplanką kuriame yra "uv.lock" ir "pyproject.toml" failai
- šiame aplanke atsidaryti cmd
- Paleisti komandą kuri įrašys visas projektui reikalingas bilbiotekas su specifinėmis versijomis:
```bash
uv sync
```
---
### 4. Sutvarkyti .env failą
Pagrindiniame aplanke yra pavyzdinis .env failas pavadintas .env.example
Failą pervadinti į .env ir pridėti savo GROQ_API_KEY iš https://console.groq.com/keys. (šiuo raktu su niekuo nesidalinti)
- Jei dar neturite paskyros, galima prisijungti naudojant savo GitHub paskyrą
- Jei dar neturite rakto, jį susikurti paspaudus "+ Create API Key" ir įvedus pavadinimą.
---
### 5. Projekto paleidimas
1. Paleisti duombazę
```bash
docker compose up
```
2. Paleisti API
```bash
uv run uvicorn app.main:app
```
---
### 6. Įrankių nuorodos
- API: http://127.0.0.1:8000/docs
- Qdrant: http://localhost:6333/dashboard
---
## Testavimas
Testavimui naudojami tie patys duomenų failai, tačiau pervadinti siekiant įrodyti jog jei nekeičiamas failo turinys, vektorinėje duombazėje saugomi taškai nesiduplikuos.

### Dokumentų nuorodų įvedimo pavyzdžiai /ingest endpoint
```json
{
  "paths": [
    "docs/EAU-EANM-ESTRO-ESUR-ISUP-SIOG-Guidelines-on-Prostate-Cancer-2025_updated.pdf",
    "docs/EAU-Guidelines-on-Testicular-Cancer-2025.pdf",
    "docs/EAU-Guidelines-on-Upper-Urinary-Tract-Urothelial-Carcinoma-2025_2025-06-02-054038_pezz.pdf"
  ]
}
```
arba

```json
{
  "paths": [
    "docs/file1.pdf",
    "docs/file2.pdf",
    "docs/file3.pdf"
  ]
}
```
### Klausimų pavyzdžiai /query endpoint
```json
{
  "query_text": "When can biopsy be omitted after a negative MRI?",
  "k": 4
}
```
```json
{
  "query_text": "When is PSMA-PET/CT recommended for staging?",
  "k": 4
}
```
```json
{
  "query_text": "What are the serum tumour markers used before and after orchidectomy?",
  "k": 4
}
```
```json
{
  "query_text": "How many cycles of BEP are recommended for poor-prognosis NSGCT?",
  "k": 4
}
```
```json
{
  "query_text": "When is kidney-sparing surgery preferred in UTUC?",
  "k": 4
}
```
```json
{
  "query_text": "What factors define high-risk versus low-risk UTUC?",
  "k": 4
}
```
```json
{
  "query_text": "What is the cost of PSMA-PET in Lithuania?",
  "k": 4
}
```
```json
{
  "query_text": "What are the national reimbursement rules for UTUC?",
  "k": 4
}
```
---
### Chunking/embedding choices & trade-offs
Naudojant RecursiveCharacterTextSplitter su table-aware skaitymu
Pliusai
- Nekarpo lentelių į kelias dalis todėl nepraranda lentelės konteksto
- Skaido pagal paragrafus ir sakinius minimizuojant konteksto karpyma vidury minties
Minusai
- Nors lentelės išsaugomos, lentelių struktūra ne visada aiški
- Didelės saugomos skiltys, mažiau embeddings
### Known limitations
- Paragrafas arba lentelė einanti per kelis puslapius vis tiek bus suskaidyta ir galimas konteksto praradimas
- Lentelių ir paragrafo konteksto susiejimas neimplementuotas, reikėtų paduoti ir lenteles esančias prieš/po konteksto pagla puslapį siekiant pilnai jas panaudoti
- Mažesni modeliai negali apdoroti tokių didelių chunks dėl mažo context window
