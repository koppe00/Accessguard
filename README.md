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

Bij een eigen domein: pas `BASE` aan in het buildscript en in `sitemap.xml`, `robots.txt` en de canonical-links.

Klinq is een handelsnaam van Koppelaar Informatieadvies (KvK 95233784). AccessGuard is in de pilotfase.
