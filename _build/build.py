import os, json, html, shutil
BASE = "https://koppe00.github.io/Accessguard/"   # later: https://klinq.nl/
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPDATED = "2026-11-21"
E = html.escape
LOGO = '<svg viewBox="0 0 32 32" aria-hidden="true"><rect x="2.5" y="9" width="17" height="14" rx="7" fill="none" stroke="currentColor" stroke-width="3" opacity=".55"/><rect x="12.5" y="9" width="17" height="14" rx="7" fill="none" stroke="var(--accent)" stroke-width="3"/></svg>'
NAV = [("hoe-het-werkt/","Hoe het werkt"),("veiligheid/","Veiligheid"),("aanleveren/","Aanleveren"),("prijs/","Prijs"),("kennisbank/","Kennisbank")]
ORG = {"@type":"Organization","@id":BASE+"#org","name":"Klinq","url":BASE,"logo":BASE+"assets/logo.svg",
       "legalName":"Koppelaar Informatieadvies","description":"Klinq maakt AccessGuard: toezicht op dossierinzage voor zorgorganisaties.",
       "identifier":{"@type":"PropertyValue","propertyID":"KvK","value":"95233784"},"areaServed":"NL"}
APP = {"@type":"SoftwareApplication","@id":BASE+"#accessguard","name":"AccessGuard","applicationCategory":"BusinessApplication","operatingSystem":"Webbrowser",
       "description":"Controleert alle dossierinzages en toegangsrechten volgens NEN 7513 en NEN 7510. Gegevens blijven op de eigen computer.",
       "publisher":{"@id":BASE+"#org"},
       "offers":{"@type":"Offer","price":"99.00","priceCurrency":"EUR","description":"Per organisatie per maand, exclusief btw. 30 dagen gratis proefperiode."}}
pages = []

def page(path, title, desc, body, active=None, ld=None, crumbs=None):
    depth = path.count("/")
    r = "../" * depth
    nav = "".join(f'<a href="{r}{h}"{" aria-current=\"page\"" if h==active else ""}>{t}</a>' for h,t in NAV)
    graph = [ORG] + (ld or [])
    if crumbs:
        graph.append({"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":BASE+u} for i,(n,u) in enumerate([("Home","")]+crumbs)]})
        cr = '<nav class="crumbs" aria-label="Kruimelpad"><a href="'+r+'">Home</a>'+"".join(f' › <a href="{r}{u}">{E(n)}</a>' for n,u in crumbs[:-1])+f' › <span>{E(crumbs[-1][0])}</span></nav>'
        body = body.replace("<!--crumbs-->", cr)
    canon = BASE + path
    doc = f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website"><meta property="og:locale" content="nl_NL"><meta property="og:site_name" content="Klinq">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}">
<meta name="theme-color" content="#10262A">
<link rel="icon" href="{r}assets/logo.svg" type="image/svg+xml">
<link rel="preload" href="{r}assets/fonts/plex-sans-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r}assets/site.css">
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@graph":graph},ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Naar de inhoud</a>
<header class="top"><div class="wrap">
<a class="brand" href="{r}" aria-label="Klinq, naar de homepage">{LOGO}klinq<small>AccessGuard</small></a>
<nav class="nav" aria-label="Hoofdmenu">{nav}</nav>
<div class="cta"><a class="btn small" href="{r}app/">Inloggen</a><a class="btn small primary" href="{r}app/">Proefperiode starten</a></div>
</div></header>
<main id="main">
{body}
</main>
<footer><div class="wrap">
<div class="stack"><a class="brand" href="{r}">{LOGO}klinq</a><p>Toezicht op dossierinzage voor zorgorganisaties. Ons product AccessGuard controleert alle inzages, en de gegevens blijven bij jullie.</p></div>
<div><h4>Product</h4><ul><li><a href="{r}hoe-het-werkt/">Hoe het werkt</a></li><li><a href="{r}veiligheid/">Veiligheid</a></li><li><a href="{r}aanleveren/">Aanleveren</a></li><li><a href="{r}prijs/">Prijs en proefperiode</a></li><li><a href="{r}app/">Inloggen</a></li></ul></div>
<div><h4>Sectoren</h4><ul><li><a href="{r}ziekenhuizen/">Ziekenhuizen</a></li><li><a href="{r}vvt/">Ouderenzorg (VVT)</a></li><li><a href="{r}ggz/">Ggz</a></li></ul></div>
<div><h4>Kennisbank</h4><ul><li><a href="{r}kennisbank/nen-7513-logging-controleren/">NEN 7513: logging controleren</a></li><li><a href="{r}kennisbank/noodtoegang-beoordelen/">Noodtoegang beoordelen</a></li><li><a href="{r}kennisbank/logging-en-de-wabvpz/">Logging en de Wabvpz</a></li></ul></div>
<div class="legal"><span>Klinq is een handelsnaam van Koppelaar Informatieadvies · KvK 95233784</span><span><a href="{r}colofon/">Colofon, privacy en voorwaarden</a></span></div>
</div></footer>
</body>
</html>
'''
    d = os.path.join(OUT, path)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(doc)
    pages.append(path)

def cta(r, title="Probeer het 30 dagen met jullie eigen gegevens", text="Zonder betaalgegevens. Je test met één maand aan gegevens, en je gaat zelf na of het veilig is."):
    return f'<section class="cta-band"><div class="wrap"><div class="stack"><h2>{title}</h2><p>{text}</p></div><div class="row" style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn" href="{r}app/">Proefperiode starten</a><a class="btn ghost" href="{r}hoe-het-werkt/">Hoe het werkt</a></div></div></section>'

def faq(items):
    return "".join(f'<details class="faq"><summary>{E(q)}</summary><p>{a}</p></details>' for q,a in items), {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":html.unescape(__import__("re").sub("<[^>]+>","",a))}} for q,a in items]}

LOGSTREAM = '''<figure class="log" aria-label="Voorbeeld: een deel van de inzagelog, met één signaal">
<div class="bar"><span>inzagelog · oktober 2026</span><span>20.237 inzages · alle gecontroleerd</span></div>
<ol>
<li><span class="t"><span class="d">14-10 </span>09:32</span><span>M·7a21c4</span><span class="p">P·4f1a09…</span><span class="why">zorgcontact ✓</span></li>
<li><span class="t"><span class="d">14-10 </span>09:35</span><span>M·19be0d</span><span class="p">P·c802e1…</span><span class="why">opname ✓</span></li>
<li><span class="t"><span class="d">14-10 </span>09:41</span><span>M·7a21c4</span><span class="p">P·77d0b3…</span><span class="why">afspraak ✓</span></li>
<li class="flag"><span class="t"><span class="d">14-10 </span>09:44</span><span>M·a54753</span><span class="p">P·e1c9f2…</span><span class="why">geen zorgcontact</span></li>
<li><span class="t"><span class="d">14-10 </span>09:47</span><span>M·3fd880</span><span class="p">P·0b6e5a…</span><span class="why">noodtoegang, reden ✓</span></li>
<li><span class="t"><span class="d">14-10 </span>09:52</span><span>M·19be0d</span><span class="p">P·5aa214…</span><span class="why">zorgtraject ✓</span></li>
</ol>
<div class="foot"><span>M· = medewerker, P· = patiënt, als code</span><span>1 signaal → een mens beoordeelt</span></div>
</figure>'''

# ---------------- HOME ----------------
fq, fqld = faq([
 ("Gaan patiëntgegevens naar Klinq?", "Nee. AccessGuard verwerkt alles op de computer van de gebruiker. Gegevens van patiënten en medewerkers gaan niet naar ons. Je kunt dat zelf testen: de controles werken ook zonder internetverbinding."),
 ("Welke systemen worden ondersteund?", "AccessGuard werkt met exportbestanden uit het EPD of ECD en het personeelssysteem. Bestanden volgens onze <a href=\"aanleveren/\">aanleverspecificatie</a> werken direct. Wijken de kolommen af, dan maakt de assistent een koppeling. Die ziet alleen de opbouw van de bestanden, geen namen of nummers."),
 ("Beslist AccessGuard of een medewerker iets fout deed?", "Nee. AccessGuard maakt signalen. Een mens beoordeelt elk signaal en legt het oordeel vast, met een toelichting. Dat past bij de AVG (artikel 22)."),
 ("Wat kost het?", "€ 99 per maand per organisatie, exclusief btw, ongeacht het aantal gebruikers. De eerste 30 dagen zijn gratis."),
 ("Is AccessGuard al gecertificeerd?", "Nog niet. AccessGuard is in de pilotfase. Een externe pentest en ondertekende versies staan gepland. Op de pagina <a href=\"veiligheid/\">Veiligheid</a> zie je per onderdeel wat er al is en wat er nog komt."),
])
page("", "Klinq · Toezicht op dossierinzage voor de zorg met AccessGuard",
 "AccessGuard controleert alle dossierinzages volgens NEN 7513, niet een steekproef. Gegevens blijven bij jullie. € 99 per maand, 30 dagen gratis proberen.",
 f'''<section class="hero"><div class="wrap grid2">
<div class="stack">
<span class="eyebrow">Toezicht op dossierinzage · NEN 7513</span>
<h1>Wie keek in welk dossier, en had daar een reden voor?</h1>
<p class="lead">AccessGuard controleert álle inzages in het EPD of ECD, niet een steekproef. Je ziet alleen wat aandacht vraagt. En de gegevens verlaten jullie organisatie niet.</p>
<div class="btns"><a class="btn primary" href="app/">Start 30 dagen gratis</a><a class="btn" href="hoe-het-werkt/">Bekijk hoe het werkt</a></div>
<p class="note">€ 99 per maand per organisatie · geen betaalgegevens nodig voor de proef</p>
</div>
{LOGSTREAM}
</div></section>

<section style="padding-top:0"><div class="wrap"><div class="facts">
<div><b>100%</b><span>van de inzages gecontroleerd, elke maand</span></div>
<div><b>0</b><span>patiëntgegevens naar de leverancier</span></div>
<div><b>12</b><span>controles op inzage en toegangsrechten</span></div>
<div><b>€ 99</b><span>per maand, voor de hele organisatie</span></div>
</div></div></section>

<section class="band"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Het probleem</span><h2>Een steekproef laat bijna alles liggen</h2><p class="lead">Zorgorganisaties moeten de logging regelmatig controleren op onrechtmatige toegang. In de praktijk gaat dat vaak met de hand, met een paar dossiers per maand.</p></div>
<div class="grid3">
<div class="card"><span class="num">01</span><h3>Te veel inzages</h3><p>Een ziekenhuis heeft al snel tienduizenden inzages per maand. Met de hand controleer je daar een fractie van.</p></div>
<div class="card"><span class="num">02</span><h3>Toezichthouder kijkt mee</h3><p>De Autoriteit Persoonsgegevens beboette het HagaZiekenhuis in 2019 onder meer omdat de logging niet regelmatig werd gecontroleerd. OLVG kreeg in 2021 een boete omdat de controle op wie welk dossier bekeek tekortschoot.</p></div>
<div class="card"><span class="num">03</span><h3>Patiënten vragen ernaar</h3><p>Sinds 2020 hebben patiënten recht op een overzicht van wie hun dossier heeft ingezien (Wabvpz). Dan wil je zelf al weten wat erin staat.</p></div>
</div>
<p class="note" style="margin-top:20px">Bronnen: <a href="kennisbank/nen-7513-logging-controleren/">Kennisbank: logging controleren</a></p>
</div></section>

<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">Zo werkt het</span><h2>In drie stappen van exportbestand naar oordeel</h2></div>
<ol class="steps">
<li><h3>Aanleveren</h3><p>Functioneel beheer haalt vier soorten gegevens uit jullie systemen, zoals de auditlog uit het EPD. Het formaat maakt weinig uit: AccessGuard maakt zelf de koppeling.</p></li>
<li><h3>Controleren</h3><p>AccessGuard legt elke inzage naast de zorgcontacten en de personeelslijst. Geen zorgcontact, eigen dossier, collega, noodtoegang of uit dienst? Dan volgt een signaal.</p></li>
<li><h3>Beoordelen</h3><p>Een privacy officer bekijkt de signalen, legt een oordeel vast en maakt een rapport voor FG en bestuur. Namen zie je pas als je ze nodig hebt.</p></li>
</ol>
</div></section>

<section style="padding-top:0"><div class="wrap grid2">
<div class="stack"><span class="eyebrow">Veiligheid</span><h2>Gegevens blijven waar ze horen</h2>
<p class="lead">AccessGuard draait in de browser, op de computer van de gebruiker. Er is geen server waar jullie logging naartoe gaat.</p>
<ul class="checks"><li>Zelf te testen: zet het internet uit en de controles werken gewoon.</li><li>Oordelen en logboek gaan op slot met een wachtwoordzin die alleen jullie kennen (AES-256).</li><li>Patiëntnummers kunnen al bij de bron in codes worden omgezet.</li><li>De slimme assistent voor nieuwe bronnen ziet alleen kolomnamen, nooit inhoud.</li></ul>
<p><a href="veiligheid/">Meer over veiligheid →</a></p></div>
<div class="flow" aria-label="Gegevensstroom">
<div class="node"><b>EPD / ECD en HR</b><span>Exportbestanden, bij jullie</span></div>
<div class="arr">↓ exportbestand</div>
<div class="node home"><b>Browser van de gebruiker</b><span>Alle controles en oordelen</span></div>
<div class="arr stop">✕ geen gegevens naar buiten</div>
<div class="node out"><b>Klinq</b><span>Alleen naam, e-mail en factuur</span></div>
</div>
</div></section>

<section class="band"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Voor elke zorgsector</span><h2>Ziekenhuis, ouderenzorg of ggz</h2><p class="lead">De controles zijn dezelfde. Wat een "zorgcontact" is, verschilt per sector. AccessGuard gaat daarmee om.</p></div>
<div class="grid3 sectors">
<a class="card" href="ziekenhuizen/"><h3>Ziekenhuizen</h3><p>Hoge volumes, spoedeisende hulp en noodtoegang. Afdelingen die alles mogen zien worden apart behandeld.</p><span class="more">Ziekenhuizen →</span></a>
<a class="card" href="vvt/"><h3>Ouderenzorg (VVT)</h3><p>Langlopend verblijf en wijkzorg. Een cliënt in zorg blijft "in zorg" zolang het traject loopt.</p><span class="more">VVT →</span></a>
<a class="card" href="ggz/"><h3>Ggz</h3><p>Extra gevoelige gegevens en kleine behandelteams. Juist daar telt elke inzage zonder reden.</p><span class="more">Ggz →</span></a>
</div></div></section>

<section><div class="wrap grid2">
<div class="stack"><span class="eyebrow">Veelgestelde vragen</span><h2>Wat je waarschijnlijk wilt weten</h2><p class="lead">Staat je vraag er niet bij? Mail naar <a href="mailto:info@klinq.nl">info@klinq.nl</a>.</p></div>
<div>{fq}</div>
</div></section>
{cta("")}''', ld=[APP, fqld])

# ---------------- HOE HET WERKT ----------------
CHECKS = [
 ("R1","Geen zorgcontact","Er was rond de inzage geen afspraak, opname of traject op de afdeling van de medewerker."),
 ("R2","Eigen dossier","Een medewerker opent zijn eigen dossier met zijn werkaccount."),
 ("R3","Dossier van een collega","De patiënt werkt zelf ook in de organisatie, en er was geen zorgcontact."),
 ("R4","Mogelijk familie","Dezelfde achternaam en postcode als de medewerker, zonder zorgcontact."),
 ("R5","Noodtoegang zonder goede reden","Break-the-glass gebruikt, maar geen of een nietszeggende reden."),
 ("R5b","Noodtoegang met reden","Om af en toe na te lopen of de reden klopt."),
 ("R6","Opvallend veel dossiers","Veel meer verschillende dossiers dan collega's op dezelfde afdeling."),
 ("R7","Inzage na uit dienst","Een dossier geopend met het account van iemand die uit dienst is."),
 ("R0","Onbekend account","Inzage met een account dat niet in de personeelslijst staat."),
 ("A1","Rechten passen niet bij functie","Rechten die volgens de eigen norm niet bij de functie horen."),
 ("A2","Account actief na uit dienst","Het account heeft nog rechten na uit dienst."),
 ("A3","Lang niet gebruikt","Rechten die al lang niet gebruikt zijn."),
]
rows = "".join(f'<tr><td class="mono">{c}</td><td><b>{E(n)}</b></td><td>{E(d)}</td></tr>' for c,n,d in CHECKS)
page("hoe-het-werkt/", "Hoe AccessGuard dossierinzage controleert · Klinq",
 "Van exportbestand naar oordeel: welke controles AccessGuard doet op inzages en toegangsrechten, hoe signalen worden beoordeeld en wat er in het rapport komt.",
 f'''<section class="hero"><div class="wrap stack">
<!--crumbs--><span class="eyebrow">Hoe het werkt</span><h1>Alle inzages naast de zorg leggen</h1>
<p class="lead">De kern is eenvoudig: een inzage is in orde als er een reden voor is. AccessGuard zoekt die reden in de zorgcontacten en de personeelslijst. Waar hij ontbreekt, ontstaat een signaal.</p></div></section>
<section style="padding-top:0"><div class="wrap">
<ol class="steps">
<li><h3>Gegevens klaarzetten</h3><p>Inzagelog, zorgcontacten, medewerkers en (aanbevolen) rechten, zoals het bronsysteem ze exporteert. Eén maand is genoeg. Zie <a href="../aanleveren/">Aanleveren</a>.</p></li>
<li><h3>Kwaliteit controleren</h3><p>Voordat er signalen komen, toetst AccessGuard de bestanden: zijn inzages aan medewerkers te koppelen, is er bij de meeste inzages een zorgcontact, blijft het aantal signalen beperkt?</p></li>
<li><h3>Signalen beoordelen</h3><p>Per signaal een oordeel (terecht, onterecht, nader onderzoek) met verplichte toelichting. Vervolg zoals melding aan de FG en datalekafweging wordt vastgelegd.</p></li>
</ol></div></section>
<section class="band"><div class="wrap">
<div class="sec-head"><span class="eyebrow">De controles</span><h2>Twaalf vaste controles, in gewone taal uitgelegd</h2><p class="lead">Elke controle kun je aan- of uitzetten. Afwijkingen van de standaard komen in het logboek en in het rapport.</p></div>
<div class="tbl" style="background:transparent;border-color:var(--band-line)"><table style="color:var(--band-ink)"><thead><tr><th style="background:transparent;color:var(--band-muted)">Code</th><th style="background:transparent;color:var(--band-muted)">Controle</th><th style="background:transparent;color:var(--band-muted)">Wanneer een signaal</th></tr></thead><tbody>{rows.replace("<td>","<td style=\"border-color:var(--band-line)\">").replace("<td class","<td style=\"border-color:var(--band-line)\" class")}</tbody></table></div>
</div></section>
<section><div class="wrap grid2">
<div class="stack"><span class="eyebrow">Signalen beoordelen</span><h2>Een mens beslist, AccessGuard ordent</h2>
<ul class="checks"><li>Signalen krijgen een risicoscore, zodat je begint bij wat het meest telt.</li><li>Bekijk per signaal of per medewerker. Groepsoordelen kunnen, met toelichting.</li><li>Namen zijn standaard verborgen. Tonen vraagt een reden en wordt gelogd.</li><li>Een vast rapport voor FG en bestuur: reikwijdte, uitkomsten, afgeweken instellingen.</li></ul></div>
<div class="stack"><span class="eyebrow">Nieuwe bron koppelen</span><h2>Een assistent die geen gegevens ziet</h2>
<p class="lead">Wijkt een export af van de standaard? De assistent herkent kolommen en codes en stelt een koppeling voor. Hij krijgt alleen kolomnamen en een paar voorbeeldwaarden die eerst worden gemaskeerd. Functioneel beheer keurt de koppeling goed.</p></div>
</div></section>
{cta("../")}''', active="hoe-het-werkt/", ld=[APP], crumbs=[("Hoe het werkt","hoe-het-werkt/")])

# ---------------- VEILIGHEID ----------------
TR = [("Gegevensstroom en architectuur","ok","Verwerking in de browser; geen server voor jullie data."),
 ("Netwerkgedrag","ok","Na het laden geen verbindingen nodig. Zelf te testen met de offline-test."),
 ("Versleuteling","ok","AES-256-GCM; sleutel via PBKDF2 (200.000 rondes); codes via HMAC-SHA-256; sleutels niet uitleesbaar."),
 ("Externe onderdelen","ok","Eén bestand, geen externe bibliotheken of lettertypen in de applicatie."),
 ("Broncode","ok","In te zien, zodat een eigen beoordeling mogelijk is."),
 ("Aanleverspecificatie","ok","Openbaar, gebaseerd op FHIR AuditEvent (IHE BALP) en SCIM."),
 ("Logboek van de tool","ok","Elke handeling wordt vastgelegd en op slot bewaard."),
 ("Externe pentest","soon","Gepland, door een onafhankelijke partij."),
 ("Ondertekende versies","soon","Met vingerafdruk per versie, zodat je kunt controleren wat er draait."),
 ("Juridische toets verwerkersrol","soon","Onderbouwing waarom Klinq geen verwerker van patiëntgegevens is."),
 ("Certificering (ISO 27001 / NEN 7510)","soon","Nog niet. Komt na de pilotfase.")]
trs = "".join(f'<tr><td><b>{E(a)}</b></td><td>{"<span class=\"tag\">aanwezig</span>" if s=="ok" else "<span class=\"tag soon\">gepland</span>"}</td><td>{E(c)}</td></tr>' for a,s,c in TR)
page("veiligheid/", "Veiligheid en privacy van AccessGuard · Klinq",
 "Hoe AccessGuard dossierinzage controleert zonder dat patiëntgegevens de organisatie verlaten: lokale verwerking, versleuteling, offline-test en een eerlijk overzicht van wat er nog komt.",
 f'''<section class="hero"><div class="wrap grid2"><div class="stack">
<!--crumbs--><span class="eyebrow">Veiligheid</span><h1>Wij willen jullie gegevens niet hebben</h1>
<p class="lead">De veiligste manier om patiëntgegevens te beschermen is ze niet te verplaatsen. AccessGuard werkt daarom op de computer van de gebruiker. Wij zien de logging nooit.</p></div>
<div class="flow" aria-label="Gegevensstroom"><div class="node"><b>Bronsystemen</b><span>EPD, ECD, HR</span></div><div class="arr">↓ exportbestand</div><div class="node home"><b>Jullie werkplek</b><span>Controles, oordelen, rapport</span></div><div class="arr stop">✕ geen gegevens naar buiten</div><div class="node out"><b>Klinq</b><span>Alleen account en factuur</span></div></div>
</div></section>
<section style="padding-top:0"><div class="wrap split">
<div><h3>Wat Klinq wel heeft</h3><ul class="checks"><li>Naam en e-mailadres van gebruikers</li><li>Naam van de organisatie en factuurgegevens</li><li>De versleutelde kluis met oordelen, als jullie die online bewaren. Zonder jullie wachtwoordzin is die onleesbaar.</li></ul></div>
<div><h3>Wat Klinq nooit heeft</h3><ul class="checks nope"><li>Inzagelog, zorgcontacten of personeelslijst</li><li>Namen of nummers van patiënten</li><li>Jullie wachtwoordzin</li><li>Betaalkaartgegevens (die gaan rechtstreeks naar de betaalprovider)</li></ul></div>
</div></section>
<section class="band"><div class="wrap grid2">
<div class="stack"><span class="eyebrow">Zelf nagaan</span><h2>Vertrouw ons niet, test het</h2><p class="lead">Zet tijdens de proefperiode de internetverbinding uit en voer de controles opnieuw uit. Werkt het? Dan gaat er niets naar buiten. AccessGuard meet dit ook zelf en laat het zien.</p></div>
<div class="stack"><span class="eyebrow">Wat AccessGuard niet kan voorkomen</span><p class="lead">Een besmette werkplek of iemand die een schermafbeelding maakt. Gebruik daarom een beheerde werkplek. Het logboek maakt misbruik van de tool zichtbaar.</p></div>
</div></section>
<section><div class="wrap">
<div class="sec-head"><span class="eyebrow">Voor CISO en FG</span><h2>Wat er is, en wat er nog komt</h2><p class="lead">AccessGuard is in de pilotfase. We laten eerlijk zien wat al aanwezig is en wat gepland staat.</p></div>
<div class="tbl"><table><thead><tr><th>Onderdeel</th><th>Status</th><th>Toelichting</th></tr></thead><tbody>{trs}</tbody></table></div>
<p class="note" style="margin-top:14px">Wat jullie zelf blijven doen: een DPIA, het bewaren van de logging in het bronsysteem en het beantwoorden van verzoeken van patiënten.</p>
</div></section>
{cta("../","Ga het zelf na in de proefperiode","Inclusief offline-test en een A4 voor bestuur en FG.")}''', active="veiligheid/", ld=[APP], crumbs=[("Veiligheid","veiligheid/")])

# ---------------- AANLEVEREN ----------------
FILES = [
 ("inzagelog.csv","Inzagelog","EPD of ECD","FHIR AuditEvent · IHE BALP",[("tijdstip","moet","2026-10-14T09:32:10","AuditEvent.recorded"),("gebruiker","moet","JANSENA","agent.who.identifier"),("patient","moet","1004211 of code","entity.what (Patient)"),("actie","moet","inzage","action + subtype"),("reden","bij noodtoegang","Spoedopvang","purposeOfEvent"),("soort_account","aanbevolen","persoon of systeem","agent.type"),("resultaat","optioneel","gelukt of geweigerd","outcome · EventOutcomeIndicator"),("noodknop","optioneel","ja of nee","purposeOfEvent ETREAT"),("rol","optioneel","Verpleegkundige","agent.role · RoleIDCode"),("gegevenscategorie","optioneel","heel dossier","entity.type"),("behandelrelatie","optioneel","ja of nee","Nictiz Controle.behandelrelatie")]),
 ("zorgcontacten.csv","Zorgcontacten","EPD of ECD","FHIR Encounter · EpisodeOfCare",[("patient","moet","1004211 of code","Encounter.subject"),("afdeling","moet","Cardiologie","serviceProvider"),("begin","moet","2026-10-01","period.start"),("einde","aanbevolen","2026-10-03","period.end"),("soort","aanbevolen","afspraak, opname, verblijf, zorgtraject","class")]),
 ("medewerkers.csv","Medewerkers","Personeelssysteem","SCIM 2.0 User",[("gebruiker","moet","JANSENA","userName"),("naam","aanbevolen","A. Jansen","name"),("afdeling","moet","Cardiologie","enterprise:department"),("functie","aanbevolen","Verpleegkundige","title"),("uit_dienst","aanbevolen","2026-09-30","active / endDate"),("personeelsnummer","optioneel","104233","enterprise:employeeNumber"),("soort","optioneel","intern of extern","userType")]),
 ("rechten.csv","Rechten (aanbevolen)","EPD of ECD","SCIM 2.0 Group",[("gebruiker","moet","JANSENA","Group.members"),("groep","moet","EPD_VERPL_CARDIO","Group.displayName")]),
 ("afdelingen.csv","Afdelingen (optioneel)","eigen lijst","FHIR ConceptMap",[("bron_afdeling","moet","CARD-POLI","group.element.code"),("afdeling","moet","Cardiologie","element.target.code")]),
]
ftabs = "".join(f'<h3 style="margin-top:28px">{fn} <span class="note">· {t} · uit {b} · {s}</span></h3><div class="tbl"><table><thead><tr><th>Kolom</th><th>Nodig</th><th>Voorbeeld</th><th>Standaard</th></tr></thead><tbody>'+"".join(f'<tr><td class="mono">{k}</td><td>{e}</td><td class="mono">{E(v)}</td><td class="mono">{E(st)}</td></tr>' for k,e,v,st in fl)+'</tbody></table></div>' for fn,t,b,s,fl in FILES)
page("aanleveren/", "Aanleverspecificatie inzagelog en zorgcontacten (NEN 7513) · Klinq",
 "Welke exportbestanden AccessGuard nodig heeft voor controle op dossierinzage: kolommen, voorbeelden en de koppeling naar FHIR AuditEvent, Encounter en SCIM.",
 f'''<section class="hero"><div class="wrap stack">
<!--crumbs--><span class="eyebrow">Aanleveren</span><h1>Vier soorten gegevens. Het formaat maakt weinig uit.</h1>
<p class="lead">Exporteer de gegevens zoals jullie systemen ze geven. AccessGuard herkent de kolommen, maakt zelf een koppeling en vraagt het als iets niet duidelijk is. Functioneel beheer keurt de koppeling één keer goed; daarna werkt het elke maand vanzelf.</p></div></section>
<section style="padding-top:0"><div class="wrap grid3">
<div class="card"><span class="num">Voor jou</span><h3>Wat er nodig is</h3><p>Wie keek in welk dossier, wie was in zorg waar, wie werkt waar. En welke rechten accounts hebben. Eén maand is genoeg.</p></div>
<div class="card"><span class="num">Voor functioneel beheer</span><h3>CSV met kopregel</h3><p>UTF-8, puntkomma of komma, datums als jjjj-mm-dd. In de applicatie staan sjablonen en een mail die je zo kunt doorsturen.</p></div>
<div class="card"><span class="num">Voor IT en auditor</span><h3>Eén model, drie routes</h3><p>Niveau 1: CSV (nu). Niveau 2: FHIR NDJSON via Bulk Data (gepland). Niveau 3: live via FHIR en SCIM (gepland).</p></div>
</div></section>
<section style="padding-top:0"><div class="wrap">
<div class="sec-head"><h2>Wat je aanlevert, en waar je het haalt</h2></div>
<div class="tbl"><table><thead><tr><th>Gegevens</th><th>Wat staat erin</th><th>Waar haal je het?</th></tr></thead><tbody>
<tr><td><b>1. Inzagelog</b></td><td>Wie heeft wanneer welk dossier geopend, en wat deed hij.</td><td>De auditlog of inzagelogging (NEN 7513) uit het EPD of ECD. Soms heet dit toegangslog of logging.</td></tr>
<tr><td><b>2. Zorgcontacten</b></td><td>Afspraken, opnames, verblijf en zorgtrajecten, met patiënt, afdeling en datum.</td><td>Een overzicht of rapport uit het EPD of ECD.</td></tr>
<tr><td><b>3. Medewerkers</b></td><td>Inlognaam, afdeling, functie en datum uit dienst.</td><td>De personeelslijst uit het HR-systeem, met de inlognaam van het EPD of ECD.</td></tr>
<tr><td><b>4. Rechten</b> <span class="note">aanbevolen</span></td><td>Welke gebruikersgroepen of rollen elk account heeft.</td><td>Het autorisatieoverzicht uit het EPD of ECD.</td></tr>
</tbody></table></div>
<p class="note" style="margin-top:12px"><b>Aanleveren betekent hier: openen op je eigen computer.</b> Je opent de bestanden in AccessGuard zoals je een bestand opent in Excel. Er wordt niets geüpload. Tijdens het openen laat AccessGuard live zien waar de bestanden staan en dat er nul verbindingen naar buiten zijn.</p><p class="note" style="margin-top:8px">Formaat: CSV of tekstbestand met kopregel (vanuit Excel: Opslaan als CSV). Eén maand is genoeg. Gebruikt het EPD andere afdelingsnamen dan de personeelslijst? Een lijstje met beide namen helpt.</p>
</div></section>
<section style="padding-top:0"><div class="wrap">
<div class="sec-head"><h2>Standaardformaat: niet verplicht, wel sneller</h2><p class="lead">Met deze kolomnamen is er geen koppeling nodig. Ze sluiten aan op NEN 7513, de Nictiz-handreiking voor de toegangslog, FHIR en SCIM. Specificatie 1.1.</p></div>
{ftabs}
<h3 style="margin-top:28px">Waardenlijst voor "actie"</h3>
<div class="tbl"><table><thead><tr><th>Waarde</th><th>Betekenis</th><th>FHIR AuditEvent</th></tr></thead><tbody>
<tr><td class="mono">inzage</td><td>Dossier bekeken</td><td class="mono">R</td></tr><tr><td class="mono">wijziging</td><td>Iets veranderd of toegevoegd</td><td class="mono">U / C</td></tr><tr><td class="mono">afdruk</td><td>Afgedrukt</td><td class="mono">R + subtype print</td></tr><tr><td class="mono">export</td><td>Gegevens geëxporteerd</td><td class="mono">R + subtype export</td></tr><tr><td class="mono">noodtoegang</td><td>Break-the-glass</td><td class="mono">R + purposeOfEvent ETREAT</td></tr><tr><td class="mono">automatisch</td><td>Systeemhandeling, telt niet mee</td><td class="mono">—</td></tr>
</tbody></table></div>
<div class="callout" style="margin-top:28px"><b>Patiëntnummers als code</b><p>Vervang elk patiëntnummer door een code, bijvoorbeeld met HMAC-SHA-256 en een geheime sleutel die alleen jullie kennen. Gebruik in alle bestanden dezelfde methode en sleutel. Dan blijven de bestanden aan elkaar te koppelen, en ziet AccessGuard geen echte nummers.</p></div>
<p class="note" style="margin-top:16px">Gebruikt de inzagelog personeelsnummers in plaats van inlognamen? Lever dan de kolom personeelsnummer mee in medewerkers.csv; AccessGuard koppelt daar dan op. Buiten scope: het bewaren van de logging en het beantwoorden van inzageverzoeken van patiënten. Die blijven bij het bronsysteem.</p>
</div></section>
{cta("../","Controleer je bestanden in de proefperiode","AccessGuard toetst ze direct en geeft uitleg voor jou, functioneel beheer en IT.")}''', active="aanleveren/", ld=[APP], crumbs=[("Aanleveren","aanleveren/")])

# ---------------- PRIJS ----------------
pfq, pfqld = faq([
 ("Wat gebeurt er na de proefperiode?", "Je sluit het abonnement af in de applicatie. Doe je dat niet, dan stopt de toegang. Er wordt niets automatisch afgeschreven."),
 ("Hoe wordt betaald?", "Per maand, via de beveiligde betaalpagina van de betaalprovider. Klinq ziet je kaartgegevens niet."),
 ("Telt het aantal gebruikers mee?", "Nee. Eén prijs per organisatie. Meestal werken één of twee mensen met AccessGuard, bijvoorbeeld een privacy officer en iemand van interne controle."),
 ("Hoe zeg ik op?", "Maandelijks. Je gegevens staan bij jullie, dus er is niets om terug te halen."),
])
page("prijs/", "Prijs en proefperiode AccessGuard · € 99 per maand · Klinq",
 "AccessGuard kost € 99 per maand per organisatie, exclusief btw, ongeacht het aantal gebruikers. Begin met 30 dagen gratis met jullie eigen gegevens.",
 f'''<section class="hero"><div class="wrap grid2"><div class="stack">
<!--crumbs--><span class="eyebrow">Prijs</span><h1>Eén prijs voor de hele organisatie</h1>
<p class="lead">Geen prijs per bed, per gebruiker of per module. Begin met een proefperiode en beslis op basis van jullie eigen gegevens.</p></div>
<div class="card" style="padding:32px"><span class="tag">AccessGuard</span><div class="price"><b>€ 99</b><span class="note">per maand, excl. btw</span></div><p>€ 119,79 inclusief 21% btw. Maandelijks opzegbaar.</p>
<ul class="checks"><li>Alle 12 controles op inzage en rechten</li><li>Onbeperkt aantal gebruikers</li><li>Assistent voor nieuwe bronnen</li><li>Rapport voor FG en bestuur</li></ul>
<a class="btn primary" href="../app/">Start 30 dagen gratis</a></div>
</div></section>
<section class="band"><div class="wrap">
<div class="sec-head"><span class="eyebrow">De proefperiode</span><h2>Dertig dagen om zeker te zijn</h2><p class="lead">De proef is in de applicatie ingebouwd. Je ziet steeds wat al groen is.</p></div>
<div class="grid3">
<div class="card"><span class="num">Werking</span><h3>Klopt het?</h3><p>Bestanden volgens de specificatie, inzages gekoppeld aan medewerkers (≥ 97%), zorgcontact gevonden (≥ 80%), niet te veel signalen (≤ 1%).</p></div>
<div class="card"><span class="num">Vergelijken</span><h3>Vind je terug wat je al wist?</h3><p>Draai jullie huidige controle over dezelfde maand. Vul in wat je vond, en wat AccessGuard extra vond.</p></div>
<div class="card"><span class="num">Veiligheid</span><h3>Durf je het aan?</h3><p>Offline-test gedaan en de veiligheidsinformatie besproken met FG of CISO.</p></div>
</div></div></section>
<section><div class="wrap grid2"><div class="stack"><span class="eyebrow">Vragen over de prijs</span><h2>Geen kleine lettertjes</h2></div><div>{pfq}</div></div></section>
{cta("../")}''', active="prijs/", ld=[APP, pfqld], crumbs=[("Prijs","prijs/")])

# ---------------- SECTOREN ----------------
SECT = {
 "ziekenhuizen/": ("Ziekenhuizen","Controle op dossierinzage voor ziekenhuizen (HiX, Epic) · Klinq",
   "Alle inzages in het ziekenhuis-EPD controleren volgens NEN 7513: spoedeisende hulp, noodtoegang en afdelingen die alles mogen zien, zonder dat gegevens het ziekenhuis verlaten.",
   "Tienduizenden inzages per maand, elke maand gecontroleerd",
   "In een ziekenhuis kijken veel mensen in veel dossiers, vaak terecht. AccessGuard filtert wat verklaarbaar is en houdt over wat aandacht vraagt.",
   [("Spoedeisende hulp en ondersteunende afdelingen","Afdelingen als SEH, radiologie of apotheek zien vaak patiënten zonder eigen afspraak. AccessGuard herkent ze en vraagt of ze alle patiënten mogen zien."),
    ("Noodtoegang","Break-the-glass met een nietszeggende reden wordt een signaal. Met een goede reden kun je ze steekproefsgewijs nalopen."),
    ("Systeemaccounts en koppelingen","Interfaces en achtergrondprocessen worden herkend en tellen niet als persoon."),
    ("Bronnen","Bijvoorbeeld HiX of Epic voor de inzagelog en zorgcontacten, en AFAS of Youforce voor medewerkers. Een vaste koppeling per systeem maak je met de assistent.")]),
 "vvt/": ("Ouderenzorg (VVT)","Controle op dossierinzage in de ouderenzorg (VVT) · Klinq",
   "Inzagecontrole voor VVT-organisaties: cliënten in langdurig verblijf en wijkzorg, met teams die wisselen. Controle volgens NEN 7513 met een ECD-export.",
   "Langdurige zorg, wisselende teams",
   "In de VVT is een cliënt vaak maanden of jaren in zorg, en werken invallers en flexpools mee. Een zorgcontact is hier geen afspraak maar een lopend traject.",
   [("Lopend verblijf en trajecten","Een verblijf of zorgtraject zonder einddatum telt als lopend. Inzages door het team rond de cliënt zijn dan verklaarbaar."),
    ("Wijkzorg en flexpools","Medewerkers die op meerdere locaties werken, zie je terug per afdeling of team. Afwijkingen vallen op tegen collega's."),
    ("Uit dienst en tijdelijke contracten","Bij veel wisselingen blijven accounts soms actief. AccessGuard signaleert inzages en rechten na uit dienst."),
    ("Bronnen","Bijvoorbeeld Nedap Ons, Ysis of een ander ECD, en het personeelssysteem. Een vaste koppeling per systeem maak je met de assistent.")]),
 "ggz/": ("Ggz","Controle op dossierinzage in de ggz · Klinq",
   "Inzagecontrole voor ggz-instellingen: extra gevoelige gegevens, kleine behandelteams en zorgtrajecten. Controle volgens NEN 7513, gegevens blijven in huis.",
   "De gevoeligste dossiers verdienen het meeste toezicht",
   "Gegevens over psychische gezondheid zijn bijzonder gevoelig. Een inzage zonder reden weegt daar zwaar, voor de cliënt en voor het vertrouwen in de instelling.",
   [("Zorgtrajecten","Een behandeltraject loopt vaak lang. AccessGuard telt een lopend traject als reden voor inzage door het behandelteam."),
    ("Kleine teams, duidelijk patroon","Omdat teams klein zijn, vallen inzages buiten het team snel op. Dat geeft weinig ruis en duidelijke signalen."),
    ("Collega's als cliënt","Werkt een cliënt zelf ook in de organisatie? Dan krijgt inzage zonder zorgcontact een hogere prioriteit."),
    ("Bronnen","Bijvoorbeeld Ysis of een ander EPD voor de ggz, en het personeelssysteem. Een vaste koppeling per systeem maak je met de assistent.")]),
}
for p,(nm,title,desc,h1,lead,pts) in SECT.items():
    cards = "".join(f'<div class="card"><h3>{E(a)}</h3><p>{E(b)}</p></div>' for a,b in pts)
    page(p, title, desc, f'''<section class="hero"><div class="wrap grid2"><div class="stack">
<!--crumbs--><span class="eyebrow">{E(nm)}</span><h1>{E(h1)}</h1><p class="lead">{E(lead)}</p>
<div class="btns" style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn primary" href="../app/">Start 30 dagen gratis</a><a class="btn" href="../aanleveren/">Wat moet ik aanleveren?</a></div></div>
{LOGSTREAM}</div></section>
<section style="padding-top:0"><div class="wrap"><div class="grid2" style="grid-template-columns:1fr 1fr">{cards}</div>
<p class="note" style="margin-top:18px">Kun je jullie systeem niet vinden? AccessGuard werkt met exportbestanden. Elke bron die een inzagelog volgens NEN 7513 kan exporteren, is te koppelen.</p></div></section>
{cta("../")}''', ld=[APP], crumbs=[(nm,p)])

# ---------------- KENNISBANK ----------------
ARTS = [
 ("nen-7513-logging-controleren/","NEN 7513: hoe controleer je de logging van dossierinzage?","Wat NEN 7513 vastlegt, waarom regelmatige controle nodig is, wat de AP zei in de zaken HagaZiekenhuis en OLVG, en hoe je controle praktisch inricht.",
 '''<p>NEN 7513 is de Nederlandse norm voor het vastleggen van acties op elektronische patiëntdossiers. De norm beschrijft wát je moet loggen: wie, wanneer, welk dossier, welke handeling. Vastleggen alleen is niet genoeg. De logging moet ook worden gecontroleerd.</p>
<h2>Wat zegt de wet?</h2>
<p>De Wabvpz en het Besluit elektronische gegevensverwerking door zorgaanbieders (Begz) verplichten zorgaanbieders om de logging te laten voldoen aan NEN 7513. Daarnaast vraagt de AVG (artikel 32) passende maatregelen om ongeoorloofde toegang te voorkomen en te ontdekken.</p>
<h2>Wat zei de Autoriteit Persoonsgegevens?</h2>
<ul><li><b>HagaZiekenhuis (2019):</b> boete van € 460.000. De AP stelde onder meer dat de logbestanden niet regelmatig werden gecontroleerd. Het eigen beleid van één dossier per twee maanden gaf geen systematische controle. Het ziekenhuis moest zorgen dat de logging "regelmatig wordt gecontroleerd op onrechtmatige toegang".</li>
<li><b>OLVG (2021):</b> boete van € 440.000. Er was tussen 2018 en 2020 onvoldoende controle op wie welk dossier bekeek.</li></ul>
<h2>Hoe richt je controle praktisch in?</h2>
<ol><li><b>Bepaal wat een geldige reden is.</b> Meestal: een zorgcontact op de afdeling van de medewerker, in een venster rond de inzage.</li>
<li><b>Leg de log naast de zorgcontacten.</b> Alles controleren is haalbaar als je het automatiseert. Een steekproef mist vrijwel alles.</li>
<li><b>Zoek de bekende risico's.</b> Eigen dossier, collega's, familie, noodtoegang zonder reden, inzage na uit dienst, ongewoon veel dossiers.</li>
<li><b>Laat een mens beoordelen</b> en leg het oordeel vast, met toelichting en vervolg (FG, datalekafweging, gesprek).</li>
<li><b>Rapporteer</b> aan FG en bestuur: reikwijdte, uitkomsten en wat je anders deed dan de standaard.</li></ol>
<blockquote>Tip: begin met één maand. Dan zie je snel welke afdelingen veel "ruis" geven, bijvoorbeeld een spoedeisende hulp, en kun je dat bewust inrichten.</blockquote>''',
 [("Boetebesluit AP HagaZiekenhuis (2019)","https://www.verzekeraars.nl/media/6303/hagaziekenhuis_boetebesluit.pdf"),("NOS: 440.000 euro boete voor OLVG (2021)","https://nos.nl/l/2368185"),("Nictiz: Handreiking BEIS deel II Toegangslog","https://nictiz.nl/app/uploads/2022/08/Handreiking-BEIS-deel-II-Toegangslog-definitief-201701.pdf")]),
 ("noodtoegang-beoordelen/","Noodtoegang (break-the-glass) beoordelen: zo doe je dat","Noodtoegang is nodig in de zorg, maar ook een bekende route voor misbruik. Hoe beoordeel je redenen en hoe voorkom je dat het een sleepwet wordt?",
 '''<p>Met noodtoegang, ook wel "break-the-glass", opent een zorgverlener een dossier waar hij normaal geen toegang toe heeft. Bijvoorbeeld bij een spoedopname 's nachts. Het systeem vraagt dan meestal om een reden.</p>
<h2>Waarom apart beoordelen?</h2>
<p>Noodtoegang omzeilt de gewone autorisatie. Dat is precies de bedoeling, maar het maakt het ook gevoelig voor misbruik. Daarom hoort elke noodtoegang terug te komen in de controle.</p>
<h2>Drie soorten redenen</h2>
<ul><li><b>Geen reden of nietszeggend</b>, zoals "x", "test" of ".". Dit is altijd een signaal.</li>
<li><b>Algemeen</b>, zoals "zorg" of "dienst". Bespreek met de afdeling wat een goede reden is.</li>
<li><b>Concreet</b>, zoals "spoedopvang, patiënt niet aanspreekbaar". Loop deze steekproefsgewijs na.</li></ul>
<h2>Praktische afspraken</h2>
<ol><li>Leg vast wat een goede reden is, met voorbeelden.</li><li>Kijk ook naar patronen: veel noodtoegang door één persoon of afdeling.</li><li>Koppel terug aan teams. Het doel is gedrag verbeteren, niet mensen betrappen.</li></ol>''',
 [("Nictiz: Handreiking BEIS deel II Toegangslog","https://nictiz.nl/app/uploads/2022/08/Handreiking-BEIS-deel-II-Toegangslog-definitief-201701.pdf")]),
 ("logging-en-de-wabvpz/","Logging en de Wabvpz: het recht van de patiënt op een overzicht","Sinds 1 juli 2020 mag een patiënt een overzicht vragen van wie zijn dossier heeft ingezien. Wat betekent dat voor je logging en je controle?",
 '''<p>Sinds 1 juli 2020 gelden in de Wabvpz nieuwe rechten voor patiënten. Artikel 15d geeft recht op elektronische inzage en een kosteloos afschrift van het dossier. Artikel 15e geeft recht op een afschrift van de logging: wie het dossier heeft ingezien of gegevens heeft opgevraagd, en wanneer.</p>
<h2>Wat betekent dat voor jullie?</h2>
<ul><li>De logging moet volledig en leesbaar zijn, en voldoen aan NEN 7513.</li><li>Een patiënt kan zelf zien wie er keek. Als daar een onverklaarbare inzage tussen staat, wil je dat eerder weten dan de patiënt.</li><li>Een loggingsoverzicht opvragen gaat via het bronsysteem (EPD of ECD). Dat is iets anders dan de controle.</li></ul>
<h2>Controle en inzageverzoek: twee verschillende dingen</h2>
<p>Het inzageverzoek van de patiënt beantwoord je uit het bronsysteem, waar de logging ook bewaard wordt. Controle is het actief zoeken naar inzages zonder reden, over alle patiënten. AccessGuard doet dat tweede. Het bewaren van de logging en het beantwoorden van verzoeken blijven bij het EPD of ECD.</p>''',
 [("Dirkzwager: per 1 juli 2020 nieuwe rechten en verplichtingen rond het EPD","https://www.dirkzwager.nl/kennis/artikelen/per-1-juli-2020-nieuwe-rechten-en-verplichtingen-met-betrekking-tot-het-elektronisch-patientendossier"),("UMC Utrecht: aanvraagformulier inzage logging","https://www.umcutrecht.nl/en/aanvraagformulier-inzage-logging-medisch-dossier")]),
]
lst = "".join(f'<a class="card" href="../kennisbank/{s}" style="text-decoration:none;color:inherit"><span class="num">Artikel</span><h3>{E(t)}</h3><p>{E(d)}</p><span class="more" style="color:var(--accent);font-weight:600;margin-top:auto">Lees verder →</span></a>' for s,t,d,_,_ in ARTS)
page("kennisbank/", "Kennisbank: toezicht op dossierinzage en NEN 7513 · Klinq",
 "Praktische artikelen over het controleren van logging volgens NEN 7513, noodtoegang en de Wabvpz. Voor privacy officers, FG's en functioneel beheerders in de zorg.",
 f'''<section class="hero"><div class="wrap stack"><!--crumbs--><span class="eyebrow">Kennisbank</span><h1>Toezicht op dossierinzage, uitgelegd</h1><p class="lead">Praktische kennis voor privacy officers, FG's en functioneel beheerders. Feitelijk, met bronnen.</p></div></section>
<section style="padding-top:0"><div class="wrap grid3 sectors">{lst}</div></section>{cta("../")}''', active="kennisbank/", crumbs=[("Kennisbank","kennisbank/")])
for s,t,d,bodyh,src in ARTS:
    srcs = "".join(f'<li><a href="{u}" rel="noopener">{E(n)}</a></li>' for n,u in src)
    art = {"@type":"Article","headline":t,"description":d,"inLanguage":"nl","datePublished":UPDATED,"dateModified":UPDATED,"author":{"@id":BASE+"#org"},"publisher":{"@id":BASE+"#org"},"mainEntityOfPage":BASE+"kennisbank/"+s}
    page("kennisbank/"+s, t+" · Klinq", d, f'''<section class="hero"><div class="wrap"><article class="prose">
<!--crumbs--><span class="eyebrow">Kennisbank · bijgewerkt november 2026</span><h1 style="font-size:clamp(1.8rem,4vw,2.6rem)">{E(t)}</h1><p class="lead">{E(d)}</p>
{bodyh}
<h2>Bronnen</h2><ul>{srcs}</ul>
<p class="note">Dit artikel is informatief en geen juridisch advies.</p>
</article></div></section>{cta("../../")}''', active="kennisbank/", ld=[art], crumbs=[("Kennisbank","kennisbank/"),(t,"kennisbank/"+s)])

# ---------------- COLOFON ----------------
page("colofon/", "Colofon, privacy en voorwaarden · Klinq", "Wie achter Klinq en AccessGuard zit, hoe we met persoonsgegevens omgaan en de belangrijkste voorwaarden.",
 '''<section class="hero"><div class="wrap"><div class="prose"><!--crumbs--><span class="eyebrow">Colofon</span><h1>Wie zit er achter Klinq?</h1>
<p>Klinq is een handelsnaam van Koppelaar Informatieadvies, ingeschreven bij de Kamer van Koophandel onder nummer 95233784. Klinq ontwikkelt AccessGuard, software voor toezicht op dossierinzage in de zorg.</p>
<p>Contact: <a href="mailto:info@klinq.nl">info@klinq.nl</a></p>
<h2>Privacy op deze website</h2>
<ul><li>Deze website gebruikt geen cookies, geen analytics en geen trackers.</li><li>Lettertypen worden vanaf deze website zelf geladen, niet van een externe dienst.</li><li>Er worden geen gegevens van bezoekers verzameld.</li></ul>
<h2>Privacy in AccessGuard</h2>
<p>Voor een account verwerken we naam en e-mailadres van gebruikers, de naam van de organisatie en factuurgegevens. Gegevens van patiënten en medewerkers worden op de computer van de gebruiker verwerkt en komen niet bij Klinq. Zie ook <a href="../veiligheid/">Veiligheid</a>.</p>
<h2>Status</h2>
<p>AccessGuard is in de pilotfase. Functionaliteit kan nog wijzigen. Certificering en een externe pentest zijn gepland en nog niet afgerond.</p>
<h2>Voorwaarden</h2>
<p>Het abonnement is maandelijks opzegbaar. Algemene voorwaarden worden opgesteld voor de start van de eerste abonnementen. Tot die tijd gelden afspraken per pilot.</p>
</div></div></section>''', crumbs=[("Colofon","colofon/")])

# 404
open(os.path.join(OUT,"404.html"),"w").write(open(os.path.join(OUT,"colofon/index.html")).read().split("<main id=\"main\">")[0].replace('href="../','href="/Accessguard/').replace('src="../','src="/Accessguard/').replace('<link rel="canonical" href="'+BASE+'colofon/">','<meta name="robots" content="noindex">')+'<main id="main"><section class="hero"><div class="wrap stack"><span class="eyebrow">404</span><h1>Deze pagina bestaat niet</h1><p class="lead">Misschien is hij verplaatst. <a href="/Accessguard/">Ga naar de homepage</a> of <a href="/Accessguard/app/">log in bij AccessGuard</a>.</p></div></section></main></body></html>')
# robots, sitemap
open(os.path.join(OUT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nDisallow: /app/\nSitemap: {BASE}sitemap.xml\n")
open(os.path.join(OUT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"<url><loc>{BASE}{p}</loc><lastmod>{UPDATED}</lastmod></url>\n" for p in pages)+"</urlset>\n")
print("pages", len(pages))
