import os, json, html, re
BASE = "https://koppe00.github.io/Accessguard/"   # bij eigen domein: https://klinq.nl/
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPDATED = "2026-11-21"
E = html.escape
NAV = [("werkwijze/","Werkwijze"),("veiligheid/","Veiligheid"),("aanleveren/","Aanleveren"),("prijs/","Prijs"),("kennisbank/","Kennisbank")]
ORG = {"@type":"Organization","@id":BASE+"#org","name":"Klinq","url":BASE,"logo":BASE+"assets/logo.svg",
       "legalName":"Koppelaar Informatieadvies","description":"Klinq maakt AccessGuard: toezicht op dossierinzage voor zorgorganisaties.",
       "identifier":{"@type":"PropertyValue","propertyID":"KvK","value":"95233784"},"areaServed":"NL","email":"info@klinq.nl"}
APP = {"@type":"SoftwareApplication","@id":BASE+"#accessguard","name":"AccessGuard","applicationCategory":"BusinessApplication","operatingSystem":"Webbrowser",
       "description":"Controleert alle dossierinzages en toegangsrechten volgens NEN 7513 en NEN 7510. Gegevens blijven op de eigen computer.",
       "publisher":{"@id":BASE+"#org"},
       "offers":{"@type":"Offer","price":"99.00","priceCurrency":"EUR","description":"Per organisatie per maand, exclusief btw. 30 dagen proefperiode."}}
pages = []

def page(path, title, desc, body, active=None, ld=None, crumbs=None, script=False):
    r = "../" * path.count("/")
    nav = "".join(f'<a href="{r}{h}"' + (' aria-current="page"' if h == active else '') + f'>{t}</a>' for h, t in NAV)
    graph = [ORG] + (ld or [])
    if crumbs:
        graph.append({"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":BASE+u} for i,(n,u) in enumerate([("Home","")]+crumbs)]})
        cr = '<nav class="crumbs" aria-label="Kruimelpad"><a href="'+r+'">Home</a>' + "".join(f' / <a href="{r}{u}">{E(n)}</a>' for n,u in crumbs[:-1]) + f' / <span>{E(crumbs[-1][0])}</span></nav>'
        body = body.replace("<!--crumbs-->", cr)
    body = body.replace('href="~/', f'href="{r}')
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
<meta name="theme-color" content="#F5F3EC" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#14191C" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{r}assets/logo.svg" type="image/svg+xml">
<link rel="preload" href="{r}assets/fonts/newsreader-500.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{r}assets/fonts/plex-sans-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r}assets/site.css">
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@graph":graph},ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Naar de inhoud</a>
<header class="top"><div class="wrap">
<a class="brand" href="{r}" aria-label="Klinq, naar de homepage"><span class="wm">klin<i>q</i></span><small>AccessGuard</small></a>
<nav class="nav" aria-label="Hoofdmenu">{nav}</nav>
<div class="acts"><a class="login" href="{r}app/">Inloggen</a><a class="btn sm" href="{r}app/">Proef starten</a></div>
</div></header>
<main id="main">
{body}
</main>
<footer><div class="wrap">
<div><a class="brand" href="{r}"><span class="wm">klin<i>q</i></span></a><p style="margin-top:12px;max-width:40ch">Toezicht op dossierinzage voor zorgorganisaties. AccessGuard controleert alle inzages, en de gegevens blijven bij jullie.</p><p style="margin-top:10px"><a href="mailto:info@klinq.nl">info@klinq.nl</a></p></div>
<div><h4>AccessGuard</h4><ul><li><a href="{r}werkwijze/">Werkwijze</a></li><li><a href="{r}veiligheid/">Veiligheid</a></li><li><a href="{r}aanleveren/">Aanleveren</a></li><li><a href="{r}prijs/">Prijs en proef</a></li><li><a href="{r}app/">Inloggen</a></li></ul></div>
<div><h4>Per sector</h4><ul><li><a href="{r}ziekenhuizen/">Ziekenhuizen</a></li><li><a href="{r}vvt/">Ouderenzorg (VVT)</a></li><li><a href="{r}ggz/">Ggz</a></li></ul></div>
<div><h4>Kennisbank</h4><ul><li><a href="{r}kennisbank/nen-7513-logging-controleren/">Logging controleren</a></li><li><a href="{r}kennisbank/noodtoegang-beoordelen/">Noodtoegang beoordelen</a></li><li><a href="{r}kennisbank/logging-en-de-wabvpz/">Logging en de Wabvpz</a></li></ul></div>
<div class="legal"><span>Klinq is een handelsnaam van Koppelaar Informatieadvies · KvK 95233784 · AccessGuard is in de pilotfase</span><a href="{r}colofon/">Colofon en privacy</a></div>
</div></footer>
{f'<script src="{r}assets/demo.js" defer></script>' if script else ''}
</body>
</html>
'''
    d = os.path.join(OUT, path); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(doc); pages.append(path)

def ch(no, label, inner, cls=""):
    return f'<section class="ch {cls}"><div class="wrap"><div class="no"><b>{no}</b>{label}</div><div class="body">{inner}</div></div></section>'

def close(title="Begin met één maand aan gegevens", text="Dertig dagen, met jullie eigen exportbestanden. Geen betaalgegevens nodig. Na de proef besluiten jullie zelf."):
    return f'<section class="close"><div class="wrap"><div style="display:flex;flex-direction:column;gap:14px"><h2>{title}</h2><p class="lede">{text}</p></div><div class="go"><a class="btn" href="~/app/">Proef starten <span class="arr">→</span></a><a class="btn line" href="mailto:info@klinq.nl">Eerst even bellen of mailen</a></div></div></section>'

def qa(items):
    h = '<dl class="qa">' + "".join(f'<div><dt>{E(q)}</dt><dd>{a}</dd></div>' for q,a in items) + '</dl>'
    ld = {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub("<[^>]+>","",a)}} for q,a in items]}
    return h, ld

def head(eyebrow_crumbs, h1, lede):
    return f'<section class="page-head"><div class="wrap"><!--crumbs--><h1>{h1}</h1><p class="lede">{lede}</p></div></section>'

# ---------- de voorbeeldlog ----------
DEMO = [
 ("09:32","M·7a21","Cardiologie","P·4f1a09","ok","polibezoek",None,None),
 ("09:35","M·19be","SEH","P·c802e1","ok","mag alles zien",None,None),
 ("09:41","M·7a21","Cardiologie","P·77d0b3","ok","opname",None,None),
 ("09:44","M·a547","Cardiologie","P·e1c9f2","flag","geen zorgcontact","Geen zorgcontact","De patiënt had in deze periode alleen een afspraak bij orthopedie. De medewerker werkt op cardiologie. Er is geen reden in de gegevens te vinden."),
 ("09:47","M·3fd8","Interne","P·0b6e5a","ok","noodtoegang + reden",None,None),
 ("09:52","M·19be","SEH","P·5aa214","ok","mag alles zien",None,None),
 ("10:03","M·c0e2","Neurologie","P·c0e2··","flag","eigen dossier","Eigen dossier","De medewerker opende zijn eigen dossier met zijn werkaccount. Dat hoort via het patiëntenportaal te gaan."),
 ("10:11","M·7a21","Cardiologie","P·91af30","ok","afspraak",None,None),
 ("10:16","M·5b0d","Radiologie","P·e1c9f2","ok","mag alles zien",None,None),
 ("10:24","M·88f1","Interne","P·2c7e44","flag","noodtoegang, reden 'x'","Noodtoegang zonder goede reden","Noodtoegang gebruikt met als reden alleen 'x'. Daaruit is niet op te maken waarom het nodig was."),
 ("10:30","M·3fd8","Interne","P·0b6e5a","ok","opname",None,None),
 ("10:38","M·41aa","Cardiologie","P·4f1a09","ok","polibezoek",None,None),
]
def demo_rows():
    out=[]
    for t,m,a,p,k,res,rule,why in DEMO:
        attrs = f' data-rule="{E(rule)}" data-why="{E(why)}"' if rule else ''
        out.append(f'<tr class="{k}"{attrs}><td>{t}</td><td>{m}</td><td class="afd">{a}</td><td class="pat">{p}</td><td><span class="res">{("✓ " if k=="ok" else "▲ ")+E(res)}</span></td></tr>')
    return "".join(out)
SHEET = f'''<div><figure class="sheet" id="demo" style="margin:0" aria-label="Voorbeeld: twaalf inzages uit een inzagelog">
<header><span><b>inzagelog.csv</b> · di 14 oktober, 12 van 20.237 regels</span><span id="demoCount" aria-live="polite">3 signalen</span></header>
<table><caption class="vh">Twaalf inzages met de uitkomst van de controle</caption><thead class="vh"><tr><th>Tijd</th><th>Medewerker</th><th>Afdeling</th><th>Patiënt</th><th>Uitkomst</th></tr></thead><tbody>{demo_rows()}</tbody></table>
<footer><span>M· en P· zijn codes; namen zie je pas als het nodig is</span><button class="btn sm" id="demoRun" type="button">Controleer deze 12 inzages</button></footer>
</figure>
<div class="why" id="demoWhy" hidden aria-live="polite"><span class="ttl"></span><span class="txt"></span><span class="opts"><button type="button" data-v="terecht">Terecht, er was een reden</button><button type="button" data-v="onterecht">Niet terecht</button><button type="button" data-v="onderzoek">Uitzoeken</button></span><span class="after" style="color:var(--soft);font-size:.88rem"></span></div></div>'''

# ---------- HOME ----------
fqh, fqld = qa([
 ("Gaan er patiëntgegevens naar Klinq?", "Nee. AccessGuard rekent in de browser van de gebruiker. Wij krijgen alleen naam en e-mailadres van gebruikers en de factuurgegevens. Test het zelf: zet het internet uit, de controles werken door."),
 ("Beslist de software of iemand fout zat?", "Nee. AccessGuard wijst aan, een mens beoordeelt. Elk oordeel krijgt een toelichting. Dat past bij artikel 22 van de AVG en bij hoe je met medewerkers wilt omgaan."),
 ("Welke systemen?", "Elk EPD of ECD dat een inzagelog kan exporteren, plus het personeelssysteem. Volgt de export onze <a href=\"aanleveren/\">specificatie</a>, dan werkt het direct. Zo niet, dan maakt de assistent een koppeling, zonder de inhoud te zien."),
 ("Is het gecertificeerd?", "Nog niet. AccessGuard is in de pilotfase. Op <a href=\"veiligheid/\">Veiligheid</a> staat per onderdeel wat er is en wat er nog komt, zoals de externe pentest."),
])
HOME = f'''<section class="open"><div class="wrap">
<div>
<h1>Wie keek in welk dossier, en <mark>waarom</mark>?</h1>
<p class="sub">AccessGuard legt elke inzage in het EPD of ECD naast de zorgcontacten. Wat klopt, laat hij liggen. Wat niet klopt, komt bij jou op tafel. De gegevens gaan nergens heen.</p>
<div class="go"><a class="btn" href="app/">Proef met eigen gegevens <span class="arr">→</span></a><a href="#hoeveel">Hoeveel controleer je nu?</a></div>
<ul class="terms"><li>€ 99 per maand per organisatie</li><li>30 dagen proef, zonder betaalgegevens</li><li>Ziekenhuis, VVT en ggz</li></ul>
</div>
{SHEET}
</div></section>
''' + ch("1","Hoeveel controleer je nu?", f'''<div class="two"><div style="display:flex;flex-direction:column;gap:18px">
<h2 id="hoeveel">Een steekproef ziet bijna niets</h2>
<p>Elke zorgorganisatie moet de logging regelmatig controleren op onrechtmatige toegang. Vaak gebeurt dat met de hand: een paar dossiers per maand, als er tijd is.</p>
<p>De Autoriteit Persoonsgegevens vond dat bij het HagaZiekenhuis niet genoeg.<a class="fn" href="#b1">1</a> Eén dossier per twee maanden was geen systematische controle. OLVG kreeg in 2021 een boete omdat de controle op wie welk dossier bekeek tekortschoot.<a class="fn" href="#b2">2</a></p>
<p class="side" id="b1">1. AP, boetebesluit HagaZiekenhuis, 18 juni 2019. <a href="kennisbank/nen-7513-logging-controleren/">Meer in de kennisbank</a>.<br><span id="b2">2. NOS, 11 februari 2021: € 440.000 boete voor OLVG.</span></p>
</div>
<form class="calc" id="calc" onsubmit="return false"><label for="cTot">Inzages per maand in jullie EPD of ECD<input id="cTot" type="number" min="0" step="1000" value="25000" inputmode="numeric"></label><label for="cMan">Inzages die jullie nu per maand nalopen<input id="cMan" type="number" min="0" step="5" value="40" inputmode="numeric"></label><output for="cTot cMan" aria-live="polite">Nu bekijk je <mark>0,16%</mark> van de inzages.</output></form>
</div>''') + ch("2","Wat er met een inzage gebeurt", f'''<h2>Elke inzage krijgt dezelfde vragen</h2>
<p class="lede">Had de patiënt zorg op de afdeling van de medewerker? Werkt de medewerker hier nog? Is het zijn eigen dossier, of dat van een collega of familielid? Was er noodtoegang, en met welke reden?</p>
<ul class="ledger">
<li><b>Geen zorgcontact</b><span>Geen afspraak, opname of traject op de afdeling van de medewerker, in een venster rond de inzage.</span><small>R1</small></li>
<li><b>Eigen dossier, collega, familie</b><span>De medewerker kijkt bij zichzelf, bij een collega-patiënt of bij iemand met dezelfde achternaam en postcode.</span><small>R2 · R3 · R4</small></li>
<li><b>Noodtoegang</b><span>Break-the-glass zonder reden of met een nietszeggende reden. Met een goede reden kun je ze steekproefsgewijs nalopen.</span><small>R5 · R5b</small></li>
<li><b>Opvallend veel</b><span>Veel meer verschillende dossiers dan collega's op dezelfde afdeling.</span><small>R6</small></li>
<li><b>Account en rechten</b><span>Inzage na uit dienst, onbekende accounts, rechten die niet bij de functie passen of al lang niet gebruikt zijn.</span><small>R0 · R7 · A1–A3</small></li>
</ul>
<p>Afdelingen die alle patiënten mogen zien, zoals een spoedeisende hulp, stel je één keer in. <a href="werkwijze/">Alle twaalf controles en hoe je signalen beoordeelt</a></p>''') + ch("3","Waar de gegevens blijven", f'''<h2>Wij willen jullie logging niet hebben</h2>
<p class="lede">AccessGuard draait in de browser van de gebruiker. Er is geen server waar de inzagelog naartoe gaat. Oordelen en logboek gaan op slot met een wachtwoordzin die alleen jullie kennen.</p>
<div class="route"><div><span class="tag">bij jullie</span><b>EPD, ECD en HR</b><span>Exportbestanden, patiëntnummers eventueel al als code</span></div><div class="here"><span class="tag">bij jullie</span><b>De browser van de gebruiker</b><span>Alle controles, oordelen en het rapport</span></div><div><span class="tag x">✕ geen patiëntgegevens</span><b>Klinq</b><span>Alleen naam, e-mail en factuur</span></div></div>
<p><mark>Test het zelf:</mark> zet tijdens de proef de wifi uit en voer de controles opnieuw uit. Werkt het, dan gaat er niets naar buiten. <a href="veiligheid/">Wat er is en wat er nog komt</a></p>''', "ink-band") + ch("4","Wat je nodig hebt", f'''<h2>Vier exportbestanden, één maand</h2>
<ul class="ledger">
<li><b>Inzagelog</b><span>Wie keek wanneer in welk dossier, en wat deed hij.</span><small>EPD/ECD · FHIR AuditEvent</small></li>
<li><b>Zorgcontacten</b><span>Afspraken, opnames, verblijf en trajecten per afdeling.</span><small>EPD/ECD · FHIR Encounter</small></li>
<li><b>Medewerkers</b><span>Wie werkt waar, en wie is uit dienst.</span><small>HR · SCIM User</small></li>
<li><b>Rechten</b><span>Welke groepen een account heeft. Aanbevolen.</span><small>EPD/ECD · SCIM Group</small></li>
</ul>
<p>Functioneel beheer krijgt vanuit de applicatie een mail met sjablonen. Heten kolommen anders? Dan vertaalt AccessGuard ze en laat hij zien wat er mist. <a href="aanleveren/">De volledige specificatie</a></p>''') + ch("5","De proef", f'''<h2>Dertig dagen om zeker te zijn</h2>
<ol class="days">
<li><b>dag 1</b><strong>Account en sleutel</strong><span>Inloggen met je werkaccount, wachtwoordzin kiezen. IT krijgt een kant-en-klare mail.</span></li>
<li><b>dag 2–7</b><strong>Bestanden</strong><span>Functioneel beheer levert één maand aan. AccessGuard toetst de kwaliteit en zegt wat er mist.</span></li>
<li><b>dag 7–25</b><strong>Beoordelen en vergelijken</strong><span>Signalen bekijken naast jullie huidige controle. Offline-test doen, FG of CISO laten meekijken.</span></li>
<li><b>dag 30</b><strong>Besluiten</strong><span>Alles groen? Dan € 99 per maand, maandelijks opzegbaar. Niets wordt automatisch afgeschreven.</span></li>
</ol>''') + ch("6","Vragen", f'''<h2>Wat FG's en CISO's ons vragen</h2>{fqh}''') + close()
page("", "AccessGuard · Toezicht op dossierinzage in de zorg · Klinq",
 "Controleer alle inzages in het EPD of ECD volgens NEN 7513, niet een steekproef. Gegevens blijven in jullie browser. € 99 per maand, 30 dagen proef.",
 HOME, ld=[APP, fqld], script=True)

# ---------- WERKWIJZE ----------
CHECKS = [("R1","Geen zorgcontact","Geen afspraak, opname of traject op de afdeling van de medewerker rond de inzage."),("R2","Eigen dossier","Een medewerker opent zijn eigen dossier met zijn werkaccount."),("R3","Dossier van een collega","De patiënt werkt zelf ook in de organisatie en er was geen zorgcontact."),("R4","Mogelijk familie","Dezelfde achternaam en postcode als de medewerker, zonder zorgcontact."),("R5","Noodtoegang zonder goede reden","Break-the-glass met geen of een nietszeggende reden."),("R5b","Noodtoegang met reden","Om af en toe na te lopen of de reden klopt."),("R6","Opvallend veel dossiers","Veel meer verschillende dossiers dan collega's op dezelfde afdeling."),("R7","Inzage na uit dienst","Een dossier geopend met het account van iemand die uit dienst is."),("R0","Onbekend account","Inzage met een account dat niet in de personeelslijst staat."),("A1","Rechten passen niet bij functie","Rechten die volgens jullie eigen norm niet bij de functie horen."),("A2","Account actief na uit dienst","Het account heeft nog rechten na uit dienst."),("A3","Lang niet gebruikt","Rechten die al lang niet gebruikt zijn.")]
rows = "".join(f'<tr><td class="m">{c}</td><td><b>{E(n)}</b></td><td>{E(d)}</td></tr>' for c,n,d in CHECKS)
page("werkwijze/", "Werkwijze: zo controleert AccessGuard dossierinzage · Klinq",
 "Van exportbestand naar oordeel: de twaalf controles op inzage en toegangsrechten, hoe je signalen beoordeelt, en wat er in het rapport voor FG en bestuur komt.",
 head("", "Van exportbestand naar oordeel", "Een inzage is in orde als er een reden voor is. AccessGuard zoekt die reden in de zorgcontacten en de personeelslijst. Waar hij ontbreekt, ontstaat een signaal. Een mens beslist.") +
 ch("1","Eerst de kwaliteit", '''<h2>Geen signalen op rommelige data</h2><p class="lede">Voordat er één signaal verschijnt, toetst AccessGuard de bestanden. Als de basis niet klopt, krijg je honderden valse meldingen, en daar heeft niemand iets aan.</p>
<ul class="ledger"><li><b>Gekoppeld aan medewerkers</b><span>Minstens 97% van de inzages hoort bij iemand uit de personeelslijst.</span><small>≥ 97%</small></li><li><b>Zorgcontact gevonden</b><span>Bij minstens 80% van de inzages is een reden te vinden.</span><small>≥ 80%</small></li><li><b>Niet te veel signalen</b><span>Hooguit 1% van de inzages wordt een signaal. Anders eerst de inrichting bijstellen.</span><small>≤ 1%</small></li></ul>''') +
 ch("2","De controles", f'''<h2>Twaalf vaste controles</h2><p class="lede">Elke controle kun je uitzetten. Wat afwijkt van de standaard, komt in het logboek en in het rapport.</p><div class="tbl"><table class="t"><thead><tr><th>Code</th><th>Controle</th><th>Wanneer een signaal</th></tr></thead><tbody>{rows}</tbody></table></div>''') +
 ch("3","Beoordelen", '''<h2>Een mens beslist, AccessGuard ordent</h2><ul class="ledger"><li><b>Risicoscore</b><span>Je begint bij wat het zwaarst weegt.</span><small></small></li><li><b>Per signaal of per medewerker</b><span>Groepsoordelen kunnen, altijd met toelichting.</span><small></small></li><li><b>Namen verborgen</b><span>Standaard zie je codes. Namen tonen vraagt een reden en wordt vastgelegd.</span><small></small></li><li><b>Vervolg</b><span>Melding aan de FG, datalekafweging, gesprek, maatregel. Afsluiten kan pas als dat is vastgelegd.</span><small></small></li><li><b>Rapport</b><span>Vast format voor FG en bestuur: reikwijdte, uitkomsten, afgeweken instellingen.</span><small></small></li></ul>''') +
 ch("4","Nieuwe bron", '''<h2>Een assistent die niets ziet</h2><p class="lede">Wijkt een export af? De assistent herkent kolommen en codes en stelt een koppeling voor. Hij krijgt alleen kolomnamen en gemaskeerde voorbeeldwaarden. Functioneel beheer keurt de koppeling goed, en die werkt daarna elke maand.</p>''') + close(),
 active="werkwijze/", ld=[APP], crumbs=[("Werkwijze","werkwijze/")])

# ---------- VEILIGHEID ----------
TR = [("Gegevensstroom en architectuur","ok","Verwerking in de browser; geen server voor jullie data."),("Netwerkgedrag","ok","Na het laden geen verbindingen nodig. Zelf te testen met de offline-test."),("Versleuteling","ok","AES-256-GCM; sleutel via PBKDF2 (200.000 rondes); codes via HMAC-SHA-256; sleutels niet uitleesbaar."),("Externe onderdelen","ok","Eén bestand, geen externe bibliotheken of lettertypen in de applicatie."),("Broncode","ok","In te zien, zodat een eigen beoordeling mogelijk is."),("Aanleverspecificatie","ok","Openbaar, gebaseerd op FHIR AuditEvent (IHE BALP) en SCIM."),("Logboek van de tool","ok","Elke handeling wordt vastgelegd en op slot bewaard."),("Externe pentest","soon","Gepland, door een onafhankelijke partij."),("Ondertekende versies","soon","Met vingerafdruk per versie, zodat je ziet wat er draait."),("Juridische toets verwerkersrol","soon","Onderbouwing waarom Klinq geen verwerker van patiëntgegevens is."),("ISO 27001 / NEN 7510","soon","Nog niet. Komt na de pilotfase.")]
trs = "".join(f'<tr><td><b>{E(a)}</b></td><td><span class="st {s}">{"aanwezig" if s=="ok" else "gepland"}</span></td><td>{E(c)}</td></tr>' for a,s,c in TR)
page("veiligheid/", "Veiligheid en privacy van AccessGuard · Klinq",
 "Hoe AccessGuard dossierinzage controleert zonder dat patiëntgegevens de organisatie verlaten: lokale verwerking, versleuteling, de offline-test en wat er nog komt.",
 head("", "De veiligste data is data die blijft waar hij is", "AccessGuard werkt op de computer van de gebruiker. Wij zien de logging nooit. Dat hoef je niet te geloven: je kunt het testen.") +
 ch("1","Gegevensstroom", '''<div class="route"><div><span class="tag">bij jullie</span><b>EPD, ECD en HR</b><span>Exportbestanden</span></div><div class="here"><span class="tag">bij jullie</span><b>Browser van de gebruiker</b><span>Controles, oordelen, rapport</span></div><div><span class="tag x">✕ geen patiëntgegevens</span><b>Klinq</b><span>Account en factuur</span></div></div>
<div class="two"><div><h3>Wat Klinq wel heeft</h3><ul class="ledger" style="margin-top:12px"><li><b>Gebruikers</b><span>Naam en e-mailadres</span><small></small></li><li><b>Organisatie</b><span>Naam en factuurgegevens</span><small></small></li><li><b>Kluis</b><span>Versleutelde oordelen, als jullie die online bewaren. Zonder wachtwoordzin onleesbaar.</span><small></small></li></ul></div>
<div><h3>Wat Klinq nooit heeft</h3><ul class="ledger" style="margin-top:12px"><li><b>Brondata</b><span>Inzagelog, zorgcontacten, personeelslijst</span><small></small></li><li><b>Patiënten</b><span>Namen of nummers</span><small></small></li><li><b>Sleutel</b><span>Jullie wachtwoordzin</span><small></small></li><li><b>Betaalkaart</b><span>Gaat rechtstreeks naar de betaalprovider</span><small></small></li></ul></div></div>''') +
 ch("2","Zelf nagaan", '''<h2>Zet de wifi uit</h2><p class="lede">Voer tijdens de proef de controles uit zonder internetverbinding. Werkt het, dan gaat er niets naar buiten. AccessGuard meet dit ook zelf en zet het in de voortgang van de proef.</p><p><b>Wat AccessGuard niet kan voorkomen:</b> een besmette werkplek, of iemand die een schermafbeelding maakt. Gebruik een beheerde werkplek. Het logboek maakt misbruik van de tool zichtbaar.</p>''', "ink-band") +
 ch("3","Voor CISO en FG", f'''<h2>Wat er is, en wat er nog komt</h2><p class="lede">AccessGuard is in de pilotfase. We zeggen eerlijk wat al aanwezig is en wat gepland staat.</p><div class="tbl"><table class="t"><thead><tr><th>Onderdeel</th><th>Status</th><th>Toelichting</th></tr></thead><tbody>{trs}</tbody></table></div><p style="color:var(--soft)">Wat jullie zelf blijven doen: een DPIA, het bewaren van de logging in het bronsysteem en het beantwoorden van verzoeken van patiënten.</p>''') + close("Ga het zelf na in de proef","Inclusief offline-test en een A4 voor bestuur en FG."),
 active="veiligheid/", ld=[APP], crumbs=[("Veiligheid","veiligheid/")])

# ---------- AANLEVEREN ----------
FILES = [
 ("inzagelog.csv","Inzagelog","EPD of ECD","FHIR AuditEvent · IHE BALP",[("tijdstip","moet","2026-10-14T09:32:10","AuditEvent.recorded"),("gebruiker","moet","JANSENA","agent.who.identifier"),("patient","moet","1004211 of code","entity.what (Patient)"),("actie","moet","inzage","action + subtype"),("reden","bij noodtoegang","Spoedopvang","purposeOfEvent"),("soort_account","aanbevolen","persoon of systeem","agent.type")]),
 ("zorgcontacten.csv","Zorgcontacten","EPD of ECD","FHIR Encounter · EpisodeOfCare",[("patient","moet","1004211 of code","Encounter.subject"),("afdeling","moet","Cardiologie","serviceProvider"),("begin","moet","2026-10-01","period.start"),("einde","aanbevolen","2026-10-03","period.end"),("soort","aanbevolen","afspraak, opname, verblijf, zorgtraject","class")]),
 ("medewerkers.csv","Medewerkers","personeelssysteem","SCIM 2.0 User",[("gebruiker","moet","JANSENA","userName"),("naam","aanbevolen","A. Jansen","name"),("afdeling","moet","Cardiologie","enterprise:department"),("functie","aanbevolen","Verpleegkundige","title"),("uit_dienst","aanbevolen","2026-09-30","active / endDate")]),
 ("rechten.csv","Rechten (aanbevolen)","EPD of ECD","SCIM 2.0 Group",[("gebruiker","moet","JANSENA","Group.members"),("groep","moet","EPD_VERPL_CARDIO","Group.displayName")]),
]
ft = "".join(f'<h3 style="margin-top:10px">{fn}</h3><p style="color:var(--soft)">{t}, uit het {b}. Standaard: {s}.</p><div class="tbl"><table class="t"><thead><tr><th>Kolom</th><th>Nodig</th><th>Voorbeeld</th><th>Standaard</th></tr></thead><tbody>'+"".join(f'<tr><td class="m">{k}</td><td>{e}</td><td class="m">{E(v)}</td><td class="m">{E(st)}</td></tr>' for k,e,v,st in fl)+'</tbody></table></div>' for fn,t,b,s,fl in FILES)
page("aanleveren/", "Aanleverspecificatie inzagelog en zorgcontacten (NEN 7513) · Klinq",
 "Welke exportbestanden AccessGuard nodig heeft voor controle op dossierinzage: kolommen, voorbeelden en de koppeling naar FHIR AuditEvent, Encounter en SCIM.",
 head("", "Vier bestanden, dicht bij open standaarden", "Streng in de kern, ruim aan de randen. Wat verplicht is ligt vast. Andere kolomnamen, codes en datumnotaties vertaalt AccessGuard, en hij zegt wat er mist. Specificatie 1.0.") +
 ch("1","Kort", '''<ul class="ledger"><li><b>Voor jou</b><span>Wie keek in welk dossier, wie was in zorg waar, wie werkt waar, en welke rechten accounts hebben. Eén maand is genoeg.</span><small></small></li><li><b>Voor functioneel beheer</b><span>CSV met kopregel, UTF-8, puntkomma of komma, datums als jjjj-mm-dd. In de applicatie staan sjablonen en een mail om door te sturen.</span><small></small></li><li><b>Voor IT en auditor</b><span>Eén model, drie routes. Niveau 1: CSV (nu). Niveau 2: FHIR NDJSON via Bulk Data (gepland). Niveau 3: live via FHIR en SCIM (gepland).</span><small></small></li></ul>''') +
 ch("2","De bestanden", ft) +
 ch("3","Waardenlijst", '''<h2>De kolom "actie"</h2><div class="tbl"><table class="t"><thead><tr><th>Waarde</th><th>Betekenis</th><th>FHIR AuditEvent</th></tr></thead><tbody><tr><td class="m">inzage</td><td>Dossier bekeken</td><td class="m">R</td></tr><tr><td class="m">wijziging</td><td>Iets veranderd of toegevoegd</td><td class="m">U / C</td></tr><tr><td class="m">afdruk</td><td>Afgedrukt</td><td class="m">R + subtype print</td></tr><tr><td class="m">export</td><td>Gegevens geëxporteerd</td><td class="m">R + subtype export</td></tr><tr><td class="m">noodtoegang</td><td>Break-the-glass</td><td class="m">R + purposeOfEvent ETREAT</td></tr><tr><td class="m">automatisch</td><td>Systeemhandeling, telt niet mee</td><td class="m">—</td></tr></tbody></table></div>
<p><mark>Patiëntnummers als code.</mark> Vervang elk nummer door een code, bijvoorbeeld met HMAC-SHA-256 en een geheime sleutel die alleen jullie kennen. Gebruik in alle bestanden dezelfde methode en sleutel. Dan blijven de bestanden te koppelen en ziet AccessGuard geen echte nummers.</p><p style="color:var(--soft)">Buiten scope: het bewaren van de logging en het beantwoorden van inzageverzoeken. Die blijven bij het bronsysteem.</p>''') + close("Controleer je bestanden in de proef","AccessGuard toetst ze direct en legt uit wat er mist, voor jou, functioneel beheer en IT."),
 active="aanleveren/", ld=[APP], crumbs=[("Aanleveren","aanleveren/")])

# ---------- PRIJS ----------
pqh, pqld = qa([
 ("Wat gebeurt er na de proef?", "Je sluit het abonnement af in de applicatie. Doe je dat niet, dan stopt de toegang. Er wordt niets automatisch afgeschreven."),
 ("Hoe betaal je?", "Per maand, via de beveiligde betaalpagina van de betaalprovider. Klinq ziet je kaartgegevens niet."),
 ("Telt het aantal gebruikers?", "Nee. Eén prijs per organisatie. Meestal werken één of twee mensen ermee, bijvoorbeeld een privacy officer en iemand van interne controle."),
 ("Hoe zeg je op?", "Maandelijks. De gegevens staan bij jullie, dus er is niets terug te halen."),
])
page("prijs/", "Prijs AccessGuard: € 99 per maand per organisatie · Klinq",
 "AccessGuard kost € 99 per maand per organisatie, exclusief btw, ongeacht het aantal gebruikers. Begin met 30 dagen proef met jullie eigen gegevens.",
 head("", "€ 99 per maand. Voor de hele organisatie.", "Geen prijs per bed, per gebruiker of per module. € 119,79 inclusief 21% btw, maandelijks opzegbaar. Begin met dertig dagen proef.") +
 ch("1","Inbegrepen", '''<ul class="ledger"><li><b>Alle controles</b><span>Twaalf controles op inzage en toegangsrechten.</span><small></small></li><li><b>Alle gebruikers</b><span>Geen limiet op het aantal accounts.</span><small></small></li><li><b>Nieuwe bronnen</b><span>De assistent voor afwijkende exports.</span><small></small></li><li><b>Rapport</b><span>Voor FG en bestuur, elke maand.</span><small></small></li></ul><p><a class="btn" href="~/app/">Proef starten <span class="arr">→</span></a></p>''') +
 ch("2","De proef", '''<h2>Dertig dagen, drie vragen</h2><ul class="ledger"><li><b>Werkt het?</b><span>Bestanden volgens de specificatie, ≥ 97% gekoppeld aan medewerkers, ≥ 80% met zorgcontact, ≤ 1% signalen.</span><small>werking</small></li><li><b>Vind je terug wat je kende?</b><span>Draai jullie huidige controle over dezelfde maand en vergelijk.</span><small>vergelijken</small></li><li><b>Durf je het aan?</b><span>Offline-test gedaan, veiligheidsinformatie besproken met FG of CISO.</span><small>veiligheid</small></li></ul>''', "ink-band") +
 ch("3","Vragen", pqh) + close(),
 active="prijs/", ld=[APP, pqld], crumbs=[("Prijs","prijs/")])

# ---------- SECTOREN ----------
SECT = {
 "ziekenhuizen/": ("Ziekenhuizen","Controle op dossierinzage in ziekenhuizen (HiX, Epic) · Klinq","Alle inzages in het ziekenhuis-EPD controleren volgens NEN 7513: spoedeisende hulp, noodtoegang en afdelingen die alles mogen zien. Gegevens blijven in het ziekenhuis.",
   "Tienduizenden inzages per maand, en toch overzicht","In een ziekenhuis kijken veel mensen in veel dossiers, meestal terecht. AccessGuard laat liggen wat verklaarbaar is en houdt over wat aandacht vraagt.",
   [("Spoedeisende hulp en ondersteuning","Afdelingen als SEH, radiologie of apotheek zien patiënten zonder eigen afspraak. AccessGuard herkent ze en vraagt of ze alles mogen zien."),("Noodtoegang","Break-the-glass met een nietszeggende reden wordt een signaal. Met een goede reden kun je ze steekproefsgewijs nalopen."),("Systeemaccounts","Interfaces en achtergrondprocessen tellen niet als persoon."),("Bronnen","Bijvoorbeeld HiX of Epic voor inzagelog en zorgcontacten, AFAS of Youforce voor medewerkers.")]),
 "vvt/": ("Ouderenzorg (VVT)","Controle op dossierinzage in de ouderenzorg (VVT) · Klinq","Inzagecontrole voor VVT-organisaties: langdurig verblijf, wijkzorg en wisselende teams. Controle volgens NEN 7513 met een ECD-export.",
   "Langdurige zorg, wisselende teams","In de VVT is een cliënt vaak maanden of jaren in zorg, en werken invallers en flexpools mee. Een zorgcontact is hier geen afspraak maar een lopend traject.",
   [("Lopend verblijf","Een verblijf of traject zonder einddatum telt als lopend. Inzages door het team rond de cliënt zijn dan verklaarbaar."),("Wijkzorg en flexpools","Medewerkers op meerdere locaties zie je terug per team. Afwijkingen vallen op tegen collega's."),("Uit dienst","Bij veel wisselingen blijven accounts soms actief. AccessGuard signaleert inzages en rechten na uit dienst."),("Bronnen","Bijvoorbeeld Nedap Ons, Ysis of een ander ECD, en het personeelssysteem.")]),
 "ggz/": ("Ggz","Controle op dossierinzage in de ggz · Klinq","Inzagecontrole voor ggz-instellingen: extra gevoelige gegevens, kleine behandelteams en lange trajecten. Controle volgens NEN 7513, gegevens blijven in huis.",
   "De gevoeligste dossiers verdienen het meeste toezicht","Gegevens over psychische gezondheid zijn bijzonder gevoelig. Een inzage zonder reden weegt hier zwaar, voor de cliënt en voor het vertrouwen in de instelling.",
   [("Behandeltrajecten","Een traject loopt vaak lang. Een lopend traject telt als reden voor inzage door het behandelteam."),("Kleine teams","Inzages buiten het team vallen snel op. Weinig ruis, duidelijke signalen."),("Collega's als cliënt","Werkt een cliënt zelf ook in de organisatie? Dan krijgt inzage zonder zorgcontact voorrang."),("Bronnen","Bijvoorbeeld Ysis of een ander EPD voor de ggz, en het personeelssysteem.")]),
}
for p,(nm,title,desc,h1,lead,pts) in SECT.items():
    led = '<ul class="ledger">' + "".join(f'<li><b>{E(a)}</b><span>{E(b)}</span><small></small></li>' for a,b in pts) + '</ul>'
    page(p, title, desc, head("", E(h1), E(lead)) + ch("1", nm, led + '<p style="color:var(--soft)">Staat jullie systeem er niet bij? AccessGuard werkt met exportbestanden. Elke bron die een inzagelog volgens NEN 7513 kan exporteren, is te koppelen. <a href="~/aanleveren/">Wat moet ik aanleveren?</a></p>') + close(), ld=[APP], crumbs=[(nm,p)])

# ---------- KENNISBANK ----------
ARTS = [
 ("nen-7513-logging-controleren/","NEN 7513: hoe controleer je de logging van dossierinzage?","Wat NEN 7513 vastlegt, waarom regelmatige controle nodig is, wat de AP zei over HagaZiekenhuis en OLVG, en hoe je controle praktisch inricht.",
 '''<p>NEN 7513 is de Nederlandse norm voor het vastleggen van acties op elektronische patiëntdossiers. De norm beschrijft wát je logt: wie, wanneer, welk dossier, welke handeling. Vastleggen alleen is niet genoeg. De logging moet ook worden gecontroleerd.</p>
<h2>Wat zegt de wet?</h2><p>De Wabvpz en het Besluit elektronische gegevensverwerking door zorgaanbieders (Begz) verplichten zorgaanbieders de logging te laten voldoen aan NEN 7513.<a class="fn" href="#s3">3</a> Daarnaast vraagt de AVG (artikel 32) passende maatregelen om ongeoorloofde toegang te voorkomen en te ontdekken.</p>
<h2>Wat zei de Autoriteit Persoonsgegevens?</h2><ul><li><b>HagaZiekenhuis (2019):</b> € 460.000 boete. De logbestanden werden niet regelmatig gecontroleerd. Eén dossier per twee maanden gaf geen systematische controle. De logging moest "regelmatig worden gecontroleerd op onrechtmatige toegang".<a class="fn" href="#s1">1</a></li><li><b>OLVG (2021):</b> € 440.000 boete. Tussen 2018 en 2020 was er onvoldoende controle op wie welk dossier bekeek.<a class="fn" href="#s2">2</a></li></ul>
<h2>Hoe richt je controle praktisch in?</h2><ol><li><b>Bepaal wat een geldige reden is.</b> Meestal: een zorgcontact op de afdeling van de medewerker, rond de inzage.</li><li><b>Leg de log naast de zorgcontacten.</b> Alles controleren is haalbaar als je het automatiseert.</li><li><b>Zoek de bekende risico's.</b> Eigen dossier, collega's, familie, noodtoegang zonder reden, inzage na uit dienst, ongewoon veel dossiers.</li><li><b>Laat een mens beoordelen</b> en leg het oordeel vast, met toelichting en vervolg.</li><li><b>Rapporteer</b> aan FG en bestuur: reikwijdte, uitkomsten, afwijkingen van de standaard.</li></ol>
<blockquote>Begin met één maand. Dan zie je snel welke afdelingen veel ruis geven, zoals een spoedeisende hulp, en kun je dat bewust inrichten.</blockquote>''',
 [("AP, boetebesluit HagaZiekenhuis, 18 juni 2019","https://www.verzekeraars.nl/media/6303/hagaziekenhuis_boetebesluit.pdf"),("NOS, 440.000 euro boete voor OLVG, 11 februari 2021","https://nos.nl/l/2368185"),("Dirkzwager, nieuwe rechten en plichten rond het EPD per 1 juli 2020","https://www.dirkzwager.nl/kennis/artikelen/per-1-juli-2020-nieuwe-rechten-en-verplichtingen-met-betrekking-tot-het-elektronisch-patientendossier"),("Nictiz, Handreiking BEIS deel II Toegangslog","https://nictiz.nl/app/uploads/2022/08/Handreiking-BEIS-deel-II-Toegangslog-definitief-201701.pdf")]),
 ("noodtoegang-beoordelen/","Noodtoegang (break-the-glass) beoordelen: zo doe je dat","Noodtoegang is nodig in de zorg, en een bekende route voor misbruik. Hoe beoordeel je redenen, en hoe houd je het werkbaar?",
 '''<p>Met noodtoegang, ook wel "break-the-glass", opent een zorgverlener een dossier waar hij normaal geen toegang toe heeft. Bijvoorbeeld bij een spoedopname 's nachts. Het systeem vraagt dan meestal om een reden.</p>
<h2>Waarom apart beoordelen?</h2><p>Noodtoegang omzeilt de gewone autorisatie. Dat is de bedoeling, maar het maakt het ook gevoelig voor misbruik. Daarom hoort elke noodtoegang terug te komen in de controle.<a class="fn" href="#s1">1</a></p>
<h2>Drie soorten redenen</h2><ul><li><b>Geen reden of nietszeggend</b>, zoals "x", "test" of ".". Altijd een signaal.</li><li><b>Algemeen</b>, zoals "zorg" of "dienst". Bespreek met de afdeling wat een goede reden is.</li><li><b>Concreet</b>, zoals "spoedopvang, patiënt niet aanspreekbaar". Loop deze steekproefsgewijs na.</li></ul>
<h2>Praktische afspraken</h2><ol><li>Leg vast wat een goede reden is, met voorbeelden.</li><li>Kijk naar patronen: veel noodtoegang door één persoon of afdeling.</li><li>Koppel terug aan teams. Het doel is gedrag verbeteren, niet mensen betrappen.</li></ol>''',
 [("Nictiz, Handreiking BEIS deel II Toegangslog","https://nictiz.nl/app/uploads/2022/08/Handreiking-BEIS-deel-II-Toegangslog-definitief-201701.pdf")]),
 ("logging-en-de-wabvpz/","Logging en de Wabvpz: het recht van de patiënt op een overzicht","Sinds 1 juli 2020 mag een patiënt een overzicht vragen van wie zijn dossier heeft ingezien. Wat betekent dat voor je logging en je controle?",
 '''<p>Sinds 1 juli 2020 gelden in de Wabvpz nieuwe rechten voor patiënten. Artikel 15d geeft recht op elektronische inzage en een kosteloos afschrift van het dossier. Artikel 15e geeft recht op een afschrift van de logging: wie het dossier heeft ingezien of gegevens heeft opgevraagd, en wanneer.<a class="fn" href="#s1">1</a></p>
<h2>Wat betekent dat voor jullie?</h2><ul><li>De logging moet volledig en leesbaar zijn, en voldoen aan NEN 7513.</li><li>Een patiënt kan zelf zien wie er keek. Staat daar een onverklaarbare inzage tussen, dan wil je dat eerder weten dan de patiënt.</li><li>Een loggingsoverzicht opvragen gaat via het bronsysteem.<a class="fn" href="#s2">2</a> Dat is iets anders dan controle.</li></ul>
<h2>Controle en inzageverzoek zijn twee dingen</h2><p>Het verzoek van de patiënt beantwoord je uit het bronsysteem, waar de logging ook bewaard wordt. Controle is actief zoeken naar inzages zonder reden, over alle patiënten. AccessGuard doet dat tweede. Bewaren en verzoeken blijven bij het EPD of ECD.</p>''',
 [("Dirkzwager, nieuwe rechten en plichten rond het EPD per 1 juli 2020","https://www.dirkzwager.nl/kennis/artikelen/per-1-juli-2020-nieuwe-rechten-en-verplichtingen-met-betrekking-tot-het-elektronisch-patientendossier"),("UMC Utrecht, aanvraagformulier inzage logging","https://www.umcutrecht.nl/en/aanvraagformulier-inzage-logging-medisch-dossier")]),
]
lst = '<ul class="ledger">' + "".join(f'<li><b><a href="~/kennisbank/{s}">{E(t)}</a></b><span>{E(d)}</span><small>nov 2026</small></li>' for s,t,d,_,_ in ARTS) + '</ul>'
page("kennisbank/", "Kennisbank: toezicht op dossierinzage en NEN 7513 · Klinq",
 "Praktische artikelen over het controleren van logging volgens NEN 7513, noodtoegang en de Wabvpz. Voor privacy officers, FG's en functioneel beheerders in de zorg.",
 head("", "Kennisbank", "Praktische kennis over toezicht op dossierinzage, voor privacy officers, FG's en functioneel beheerders. Feitelijk, met bronnen.") + ch("", "Artikelen", lst) + close(),
 active="kennisbank/", crumbs=[("Kennisbank","kennisbank/")])
for s,t,d,bodyh,src in ARTS:
    srcs = "".join(f'<li id="s{i+1}"><a href="{u}" rel="noopener">{E(n)}</a></li>' for i,(n,u) in enumerate(src))
    art = {"@type":"Article","headline":t,"description":d,"inLanguage":"nl","datePublished":UPDATED,"dateModified":UPDATED,"author":{"@id":BASE+"#org"},"publisher":{"@id":BASE+"#org"},"mainEntityOfPage":BASE+"kennisbank/"+s}
    page("kennisbank/"+s, t+" · Klinq", d,
      f'<section class="page-head"><div class="wrap"><!--crumbs--><h1 style="max-width:24ch">{E(t)}</h1><p class="lede">{E(d)}</p><p style="font:400 .82rem var(--mono);color:var(--soft)">bijgewerkt 21 november 2026 · geen juridisch advies</p></div></section>'
      f'<div class="article"><div class="wrap"><article class="prose">{bodyh}</article><aside class="aside"><h4>Bronnen</h4><ol>{srcs}</ol><h4>AccessGuard</h4><p>Controleert alle inzages tegen de zorgcontacten. <a href="~/werkwijze/">Werkwijze</a></p></aside></div></div>' + close(),
      active="kennisbank/", ld=[art], crumbs=[("Kennisbank","kennisbank/"),(t,"kennisbank/"+s)])

# ---------- COLOFON ----------
page("colofon/", "Colofon en privacy · Klinq", "Wie achter Klinq en AccessGuard zit en hoe deze website en de applicatie met persoonsgegevens omgaan.",
 head("", "Colofon en privacy", "Klinq is een handelsnaam van Koppelaar Informatieadvies, ingeschreven bij de Kamer van Koophandel onder nummer 95233784. Klinq maakt AccessGuard.") +
 ch("1","Deze website", '<ul class="ledger"><li><b>Cookies</b><span>Geen. Ook geen analytics of trackers.</span><small></small></li><li><b>Lettertypen</b><span>Worden van deze website zelf geladen, niet van een externe dienst.</span><small></small></li><li><b>Contact</b><span><a href="mailto:info@klinq.nl">info@klinq.nl</a></span><small></small></li></ul>') +
 ch("2","AccessGuard", '<p>Voor een account verwerken we naam en e-mailadres van gebruikers, de naam van de organisatie en factuurgegevens. Gegevens van patiënten en medewerkers worden op de computer van de gebruiker verwerkt en komen niet bij Klinq. Zie <a href="~/veiligheid/">Veiligheid</a>.</p><p>AccessGuard is in de pilotfase. Functionaliteit kan wijzigen. Certificering en een externe pentest zijn gepland. Algemene voorwaarden worden opgesteld voor de eerste abonnementen; tot die tijd gelden afspraken per pilot.</p>'),
 crumbs=[("Colofon","colofon/")])

# ---------- 404, robots, sitemap ----------
nf = open(os.path.join(OUT,"colofon/index.html")).read()
nf = nf.split('<main id="main">')[0].replace('href="../','href="/Accessguard/').replace('src="../','src="/Accessguard/').replace(f'<link rel="canonical" href="{BASE}colofon/">','<meta name="robots" content="noindex">')
nf += '<main id="main"><section class="page-head"><div class="wrap"><h1>Deze pagina bestaat niet</h1><p class="lede">Misschien is hij verplaatst. <a href="/Accessguard/">Naar de homepage</a> of <a href="/Accessguard/app/">inloggen bij AccessGuard</a>.</p></div></section></main></body></html>'
open(os.path.join(OUT,"404.html"),"w").write(nf)
open(os.path.join(OUT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nDisallow: /app/\nSitemap: {BASE}sitemap.xml\n")
open(os.path.join(OUT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"<url><loc>{BASE}{p}</loc><lastmod>{UPDATED}</lastmod></url>\n" for p in pages)+"</urlset>\n")
print("pages", len(pages))
