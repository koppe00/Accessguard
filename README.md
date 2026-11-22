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

**Slotbout.** `app/index.html` bevat een Content Security Policy met `connect-src 'none'`: de browser weigert elke verbinding naar buiten. De app test dit bij het starten (tabblad Veiligheid) en logt geblokkeerde pogingen. De site heeft een eigen, iets ruimere policy (alleen eigen bestanden, geen verbindingen).

Bij een eigen domein: pas `BASE` aan in het buildscript en in `sitemap.xml`, `robots.txt` en de canonical-links.

Klinq is een handelsnaam van Koppelaar Informatieadvies (KvK 95233784). AccessGuard is in de pilotfase.

## Automatisch koppelen

Afwijkende exports koppelt AccessGuard zelf, zonder AI: met vaste regels (gedeelde codes tussen bestanden, vormen van kolommen) en het gedrag in de data (wie bekijkt de patiënten van een afdelingscode, wanneer en met welke reden komt een handeling voor). Elke beslissing krijgt het bewijs erbij; bij twijfel vraagt de app het de gebruiker. Alles gebeurt op de eigen computer.

## Structuurmelding

Lukt het koppelen niet goed, dan kan de gebruiker onder Bron koppelen de opbouw van de bestanden insturen. De melding bevat kolomnamen, soorten, vulgraad, ruime klassen voor aantallen, vormen en de waarschijnlijke indeling met bewijs uit gedrag. Geen regels, nummers, namen of datums. Codelijsten en bestandsnamen alleen als de gebruiker dat aanzet. Voor versturen controleert de app of er waarden uit de bestanden in de melding staan; zo ja, dan is versturen geblokkeerd. In de Claude-versie komt de melding binnen in de eigen opslag (menu Meldingen, alleen voor de eigenaar). In de GitHub-versie is er geen verbinding: de gebruiker downloadt de melding en mailt die.
