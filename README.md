# Klinq · AccessGuard

**Toezicht op dossierinzage voor zorgorganisaties.**

AccessGuard controleert alle inzages in het EPD of ECD volgens NEN 7513, niet een steekproef. Alle verwerking gebeurt in de browser van de gebruiker; gegevens van patiënten en medewerkers gaan niet naar de leverancier.

- Website: https://koppe00.github.io/Accessguard/
- Applicatie: https://koppe00.github.io/Accessguard/app/

## Opbouw

| Pad | Inhoud |
|---|---|
| `/` en submappen | Marketingsite (statische HTML, geïndexeerd) |
| `/app/` | De applicatie AccessGuard (één bestand, `noindex`) |
| `/assets/` | Stijl, lettertypen (IBM Plex, OFL) en logo |
| `sitemap.xml`, `robots.txt` | Voor zoekmachines; `/app/` staat uitgesloten |

**Slotbout.** `app/index.html` bevat een Content Security Policy met `connect-src 'self'`: de browser weigert elke verbinding naar een andere partij; alleen het eigen adres is bereikbaar (om het lokale taalmodel op te halen). De app test dit bij het starten (tabblad Veiligheid) en logt geblokkeerde pogingen. De site heeft een eigen, iets ruimere policy (alleen eigen bestanden, geen verbindingen).

Bij een eigen domein: pas `BASE` aan in het buildscript en in `sitemap.xml`, `robots.txt` en de canonical-links.

Klinq is een handelsnaam van Koppelaar Informatieadvies (KvK 95233784). AccessGuard is in de pilotfase.

## Lokaal taalmodel

De koppel-assistent gebruikt vaste regels en kan bij twijfel een klein taalmodel raadplegen dat in de browser draait (WebLLM, WebGPU).

- Bibliotheek: `app/lib/web-llm.js` (@mlc-ai/web-llm 0.2.84, Apache 2.0)
- Modelcode: `app/model/lib/qwen05-webgpu.wasm`
- Gewichten: Qwen2.5-0.5B-Instruct, 4-bit (Apache 2.0), ca. 280 MB in `app/model/qwen05/resolve/main/`. Die worden opgehaald door de workflow **Lokaal taalmodel ophalen** (`.github/workflows/model.yml`); start die eenmalig onder Actions als hij niet vanzelf is gedraaid.

Het model krijgt alleen codes en afdelingsnamen, nooit regels uit de bestanden. Zonder WebGPU of zonder model werkt alles met de vaste regels.
