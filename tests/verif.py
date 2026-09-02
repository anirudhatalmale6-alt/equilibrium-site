# -*- coding: utf-8 -*-
"""
Equilibrium — verification de la maquette rendue.

On mesure la page telle qu'un navigateur la dessine, jamais le fichier source.
Lire une feuille de style ne dit pas quelle regle a gagne, et lire un gabarit
ne dit pas ce que le visiteur voit.

CE SITE FAIT HUIT AFFIRMATIONS. CHACUNE EST PROUVEE ICI, PAS SUPPOSEE.
(Les six premieres sont celles du mouvement ; les deux dernieres sont
arrivees avec la pratique et le Cercle.)

 1. « La declaration est citee mot pour mot. » Verifie caractere par caractere
    contre contenu.py, apres normalisation des espaces uniquement. C'est
    l'affirmation centrale du site : si elle tombe, tout le reste tombe.

 2. « Aucun fait n'est invente sur le mouvement. » Aucun millesime, aucun
    effectif, aucun montant, aucune anciennete, aucun telephone, aucune
    adresse electronique nulle part.

 3. « Aucune position sur un Etat reel. » Une liste de pays, de blocs et
    d'organisations est cherchee dans le texte des neuf pages.

 4. « Vingt-deux decisions restent ouvertes, en trois groupes. » Autant de
    lignes que dans la source, une pastille par ligne, et pas un chiffre dans
    la colonne d'etat.

 5. « Le formulaire n'envoie rien. » Pas d'attribut action, pas de methode,
    bouton desactive, et surtout : AUCUNE requete sortante mesuree pendant le
    chargement des neuf pages. Le portail membre obeit a la meme regle, et son
    champ demande une reference et non une adresse : une page de connexion qui
    accepte une adresse transforme chaque tentative ratee en information sur
    qui est membre d'un mouvement politique et qui ne l'est pas.

 6. « Le titre du hero est lisible. » Mesure, pas jugee : on cache le texte, on
    photographie le fond qui etait derriere lui, et on prend le pixel le plus
    clair. A 390 px la premiere version affichait un titre blanc en plein sur
    la pierre — le fond de hero grave en SVG ne connait pas la largeur de la
    fenetre, et `cover` lui rognait sa partie sombre. Le bandeau des pages de
    la pratique est mesure de la meme facon, aux memes quatorze largeurs.

 7. « Rien n'est revendique qui ne soit vrai. » Le site vend desormais des
    services diplomatiques et se presente comme cabinet de lobbying. Aucun
    enregistrement, aucun agrement, aucune accreditation, aucun statut
    officiel, aucun client, aucun tarif — et les formes NIEES restent
    autorisees, puisque c'est precisement ce que la page doit dire.

 8. « La separation entre le mouvement et la pratique est publique. » Une
    regle de gouvernance rangee dans une note interne ne vaut rien : personne
    ne peut l'opposer a personne. Les six clauses sont sur la page, la clause
    centrale — un client ne peut ni commander ni corriger ni retarder ni
    opposer son veto a une position du mouvement — est verifiee mot pour mot.
"""
import io
import os
import re
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8861/"
PAGES = ["index.html", "principles.html", "movement.html", "join.html",
         "services.html", "lobbying.html", "circle.html", "portal.html",
         "portal-area.html"]
LARGEURS = [320, 360, 375, 390, 414, 480, 560, 640, 768, 900, 1024, 1200, 1366, 1440]

_ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(_ICI)
sys.path.insert(0, RACINE)
sys.path.insert(0, os.path.join(RACINE, "source"))
from contenu import (DECLARATION, PRINCIPES, DECISIONS, FAQ, NEST_PAS,  # noqa: E402
                     PRATIQUE, PRATIQUE_NEST_PAS, LOBBYING_FAIT, LOBBYING_NEFAIT,
                     MURAILLE, FAQ_PRATIQUE, CERCLE_QUOI, CERCLE_ACTIVITES,
                     PORTAIL_EXIGENCES)

echecs = []
n = 0


def verif(nom, cond, detail=""):
    global n
    n += 1
    if not cond:
        echecs.append(f"{nom}   [{detail}]")
        print(f"  ECHEC  {nom}   [{detail}]")


def norm(s):
    """Espaces normalises, rien d'autre. Une citation dont on corrigerait la
    ponctuation ne serait plus une citation."""
    return re.sub(r"\s+", " ", s).replace("’", "'").strip()


def dit(corps, phrase):
    """Contenance insensible a la casse.

    `inner_text` rend le texte TEL QUE DESSINE, donc il applique
    text-transform. Les titres des encadres et les pastilles sont en
    majuscules dans la feuille de style : y chercher « This page announces
    nothing » echoue toujours, et l'echec ressemble a une phrase absente
    plutot qu'a une casse transformee. Quatre de mes controles sont tombes
    la-dessus d'un coup.
    """
    return phrase.lower() in corps.lower()


def pastilles(pg):
    """Le texte reel des pastilles, lu dans le DOM et non dans le rendu.

    Meme cause que ci-dessus : `.tbd` est en majuscules a l'ecran.
    textContent donne la chaine du document, qui est celle de la source.
    """
    return pg.evaluate(
        "() => [...document.querySelectorAll('.tbd')].map(e => e.textContent.trim())")


def defiler(pg):
    """Par paliers, comme un visiteur. Un saut unique en bas de page ne
    declenche jamais loading="lazy" sur ce qui se trouve au milieu."""
    h = pg.evaluate("document.body.scrollHeight")
    y = 0
    while y < h + 600:
        pg.evaluate(f"window.scrollTo({{top:{y}, behavior:'instant'}})")
        pg.wait_for_timeout(60)
        y += 600
        h = pg.evaluate("document.body.scrollHeight")
    pg.evaluate("window.scrollTo({top:0, behavior:'instant'})")
    pg.wait_for_timeout(110)


def lum(r, g, b):
    def canal(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * canal(r) + 0.7152 * canal(g) + 0.0722 * canal(b)


L_TEXTE = lum(0xE9, 0xEC, 0xF0)   # --txt, la valeur la plus claire du titre,
                                  # donc le pire cas contre un fond clair


def contraste_sur_fond(pg, selecteur):
    """Cache l'element, photographie le fond qui etait derriere, retourne le
    contraste contre le pixel le plus clair de ce fond.

    Mesurer le contraste sur une capture ou le texte est encore present ne
    marche pas : on ne sait plus quel pixel est le glyphe et quel pixel est le
    fond. Cacher le texte enleve l'ambiguite."""
    r = pg.evaluate(f"""() => {{
        const e = document.querySelector({selecteur!r});
        if (!e) return null;
        const b = e.getBoundingClientRect();
        return {{x:b.x, y:b.y, w:b.width, h:b.height}};
    }}""")
    if not r or r["w"] < 4 or r["h"] < 4:
        return None
    pg.evaluate(f"document.querySelector({selecteur!r}).style.visibility='hidden'")
    pg.wait_for_timeout(60)
    buf = pg.screenshot(clip={"x": max(0, r["x"]), "y": max(0, r["y"]),
                              "width": r["w"], "height": r["h"]})
    pg.evaluate(f"document.querySelector({selecteur!r}).style.visibility=''")
    im = Image.open(io.BytesIO(buf)).convert("RGB")
    lums = sorted(lum(*px) for px in im.getdata())
    pire = lums[int(len(lums) * 0.98)]           # le fond le plus clair
    return (max(pire, L_TEXTE) + 0.05) / (min(pire, L_TEXTE) + 0.05)


# Etats, blocs et organisations. Si l'un d'eux apparait, le site a pris une
# position que le mouvement n'a pas prise.
INTERDITS = [
    "United States", "America", "Russia", "Russian", "China", "Chinese",
    "India", "Iran", "Israel", "Palestine", "Ukraine", "Taiwan", "Turkey",
    "France", "Germany", "Britain", "United Kingdom", "Japan", "Korea",
    "Algeria", "Egypt", "Saudi", "Syria", "Venezuela", "Cuba", "Canada",
    "NATO", "BRICS", "United Nations", "European Union", "Kremlin",
    "Washington", "Beijing", "Moscow", "Brussels", "G7", "G20",
]

with sync_playwright() as pw:
    b = pw.chromium.launch()

    # ---- 1. structure, a toutes les largeurs ------------------------------
    for largeur in LARGEURS:
        ctx = b.new_context(viewport={"width": largeur, "height": 800}, reduced_motion="reduce")
        pg = ctx.new_page()
        erreurs = []
        externes = []
        pg.on("console", lambda m: erreurs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: erreurs.append(str(e)))
        pg.on("request", lambda r: externes.append(r.url) if not r.url.startswith(BASE) else None)

        for f in PAGES:
            erreurs.clear()
            externes.clear()
            pg.goto(BASE + f, wait_until="networkidle")
            defiler(pg)

            d = pg.evaluate("""() => ({s: document.documentElement.scrollWidth,
                                       c: document.documentElement.clientWidth})""")
            verif(f"{f} @{largeur} : pas de debordement horizontal",
                  d["s"] <= d["c"] + 1, f'{d["s"]} > {d["c"]}')

            img = pg.evaluate("""() => [...document.images]
                .filter(i => !i.complete || i.naturalWidth === 0)
                .map(i => i.getAttribute('src'))""")
            verif(f"{f} @{largeur} : toutes les images chargees", not img, str(img))

            verif(f"{f} @{largeur} : aucune erreur console", not erreurs, " | ".join(erreurs[:2]))

            # Un site politique qui charge une police ou un script distant
            # communique l'adresse IP de chacun de ses lecteurs a ce tiers.
            verif(f"{f} @{largeur} : aucune requete sortante",
                  not externes, str(sorted(set(externes))[:3]))

            coupes = pg.evaluate("""() => [...document.querySelectorAll('.hdr a, .nav a')]
                .filter(x => x.scrollWidth > x.clientWidth + 1)
                .map(x => x.textContent.trim())""")
            verif(f"{f} @{largeur} : aucun libelle d'en-tete rogne", not coupes, str(coupes))

            visible = pg.evaluate("""() => {
                const n = document.querySelector('.nav');
                if (!n) return false;
                const r = n.getBoundingClientRect();
                return r.width > 0 && r.height > 0;
            }""")
            verif(f"{f} @{largeur} : la navigation est visible", visible)

        # ---- 6. lisibilite du hero ET du bandeau, a CETTE largeur ----------
        # Le bandeau des pages de la pratique est mesure exactement comme le
        # hero, et des sa premiere version. Sur le hero, le defaut n'avait ete
        # trouve qu'apres coup, sur une capture a 390 px ; puis la BORNE de mon
        # correctif s'est revelee fausse a 1024 px. Un deuxieme fond a texte
        # pose dessus qui ne serait pas mesure aux quatorze largeurs referait
        # les deux erreurs.
        for fichier, prefixe, base in (("index.html", "hero", ".hero"),
                                       ("services.html", "bandeau", ".band")):
            pg.goto(BASE + fichier, wait_until="networkidle")
            pg.wait_for_timeout(140)
            for suffixe, seuil, quoi in ((" h1", 4.5, "le titre"),
                                         (" .sub", 4.5, "le sous-titre"),
                                         (" .eyebrow", 4.5, "le sur-titre")):
                c = contraste_sur_fond(pg, base + suffixe)
                verif(f"{prefixe} @{largeur} : {quoi} est lisible sur son fond",
                      c is not None and c >= seuil, f"{c:.2f}:1" if c else "introuvable")

        ctx.close()

    # ---- reste des controles a une seule largeur --------------------------
    ctx = b.new_context(viewport={"width": 1280, "height": 900}, reduced_motion="reduce")
    pg = ctx.new_page()

    # ---- liens internes ---------------------------------------------------
    for f in PAGES:
        pg.goto(BASE + f, wait_until="networkidle")
        for h in set(pg.evaluate("""() => [...document.querySelectorAll('a[href]')]
                .map(a => a.getAttribute('href')).filter(h => h && h !== '#')""")):
            if h.startswith("#"):
                verif(f"{f} : ancre {h} existe",
                      pg.evaluate(f"() => !!document.querySelector({h!r})"))
            elif ".html" in h:
                fich, _, frag = h.partition("#")
                verif(f"{f} : la page {fich} existe", fich in PAGES, h)
                if frag:
                    p2 = ctx.new_page()
                    p2.goto(BASE + fich, wait_until="domcontentloaded")
                    verif(f"{f} : {h} pointe sur une ancre existante",
                          p2.evaluate(f"() => !!document.getElementById({frag!r})"))
                    p2.close()
            else:
                verif(f"{f} : lien externe interdit ({h})", False, h)

    # ---- 1. la declaration est citee MOT POUR MOT -------------------------
    pg.goto(BASE + "index.html", wait_until="networkidle")
    paras = pg.evaluate("""() => [...document.querySelectorAll('.decl p')]
        .map(p => p.textContent)""")
    verif("declaration : autant de paragraphes que dans la source",
          len(paras) == len(DECLARATION), f"{len(paras)} vs {len(DECLARATION)}")
    for i, attendu in enumerate(DECLARATION):
        rendu = norm(paras[i]) if i < len(paras) else ""
        verif(f"declaration : paragraphe {i + 1} cite mot pour mot",
              rendu == norm(attendu), f"rendu={rendu[:70]!r}")
    verif("declaration : elle est typographiee autrement que le reste",
          pg.evaluate("""() => {
              const d = getComputedStyle(document.querySelector('.decl p')).fontFamily;
              const c = getComputedStyle(document.querySelector('.card p')).fontFamily;
              return d !== c && /Georgia|serif/i.test(d);
          }"""))
    verif("declaration : la page dit qu'elle est citee sans alteration",
          "without alteration" in pg.inner_text("body"))

    # ---- 2. aucun fait invente sur le mouvement ---------------------------
    MOTIFS = [
        (r"\b(19|20)\d{2}\b", "un millesime"),
        (r"\b\d[\d ,.]*\s*(members|supporters|signatories|followers|countries|chapters)\b", "un effectif"),
        (r"\bfounded\b|\bestablished in\b|\bsince \d", "une date de fondation"),
        (r"[€$£]\s?\d", "un montant"),
        (r"\b\d+\s?%", "un pourcentage"),
        (r"\+\d[\d ().-]{8,}", "un telephone"),
        (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "une adresse electronique"),
        (r"\bheadquartered\b|\bregistered in\b|\bbased in [A-Z]", "un siege"),
        # Ajoute avec le Cercle. Le risque propre a une page « activites » est
        # la date d'evenement inventee, et elle ne ressemble pas aux autres
        # faux : elle a l'air anodine. « May » est volontairement absent de la
        # liste — c'est un verbe modal courant en anglais, et le motif est
        # applique sans tenir compte de la casse.
        (r"\b(January|February|March|April|June|July|August|September|October"
         r"|November|December)\b", "un mois"),
        (r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b",
         "un jour de semaine"),
        # Depuis que le site vend des services : aucune revendication
        # d'enregistrement, d'agrement ou d'accreditation. Les formes NIEES
        # (« is not registered », « holds no accreditation ») ne matchent pas,
        # parce que le motif exige l'adjacence.
        (r"\b(is|are|has been|have been)\s+(registered|accredited|licensed"
         r"|certified|recognised|recognized|authorised|authorized|mandated)\b",
         "une revendication de statut"),
        (r"\b(accredited|licensed|certified|authorised|authorized|mandated)\s+by\b",
         "une revendication d'agrement"),
        # Premiere version : `\bofficial status\b` tout court. Elle a echoue
        # sur les NEUF pages, a cause de ma propre phrase de pied de page
        # « ... nor official status of any kind is claimed anywhere on this
        # site » — c'est-a-dire sur la negation meme que le motif est cense
        # proteger. Un motif qui interdit un mot plutot qu'une affirmation
        # interdit aussi de dire qu'on ne le revendique pas.
        (r"\b(has|holds|enjoys|carries|granted|with)\s+official status\b"
         r"|\bdiplomatic status of\b|\bon behalf of the government\b",
         "une revendication officielle"),
        # Le site parle a la troisieme personne d'un bout a l'autre. Un « we »
        # ferait parler une organisation dont la forme juridique n'existe pas
        # encore, et sur une page qui vend des services il ferait croire a une
        # equipe dont je ne sais rien.
        (r"\b(we|our|us)\b(?!\w)", "une premiere personne du pluriel"),
    ]
    for f in PAGES:
        pg.goto(BASE + f, wait_until="networkidle")
        defiler(pg)
        # les <details> fermes cachent leur reponse au inner_text : on ouvre
        pg.evaluate("() => document.querySelectorAll('details').forEach(d => d.open = true)")
        pg.wait_for_timeout(80)
        corps = pg.inner_text("body")
        for motif, quoi in MOTIFS:
            trouve = re.findall(motif, corps, re.I)
            verif(f"{f} : aucun fait invente — {quoi}", not trouve, str(trouve[:3]))

        # ---- 3. aucune position sur un Etat reel --------------------------
        cites = [x for x in INTERDITS if re.search(r"\b" + re.escape(x), corps, re.I)]
        verif(f"{f} : aucun Etat, bloc ou organisation nomme", not cites, str(cites))

        # ---- coquille commune ---------------------------------------------
        verif(f"{f} : le bandeau de demonstration est present",
              "Demonstration mockup" in corps)
        verif(f"{f} : la langue du document est l'anglais",
              pg.evaluate("() => document.documentElement.lang") == "en")
        verif(f"{f} : un titre et une description sont renseignes",
              bool(pg.title()) and bool(pg.evaluate(
                  "() => document.querySelector('meta[name=description]')?.content")))
        verif(f"{f} : aucun script sur la page",
              pg.evaluate("() => document.querySelectorAll('script').length") == 0)
        verif(f"{f} : le pied rappelle qu'aucun statut n'est revendique",
              "No legal form" in corps)

        # Les attributs width/height d'une image reservent sa place avant
        # qu'elle arrive. S'ils mentent sur ses proportions, la page saute au
        # chargement. Ils sont ecrits a la main dans le gabarit et le fichier,
        # lui, est regenere : ils se desynchronisent des qu'un visuel change de
        # format, sans que rien ne le signale.
        faux = pg.evaluate("""() => [...document.images].filter(i => {
            const w = +i.getAttribute('width'), h = +i.getAttribute('height');
            if (!w || !h || !i.naturalWidth) return false;
            return Math.abs((w / h) - (i.naturalWidth / i.naturalHeight)) > 0.02;
        }).map(i => `${i.getAttribute('src')} declare ${i.getAttribute('width')}x`
            + `${i.getAttribute('height')}, reel ${i.naturalWidth}x${i.naturalHeight}`)""")
        verif(f"{f} : les proportions declarees des images sont exactes",
              not faux, str(faux))

        # L'attribut peut etre exact et la BOITE fausse quand meme. `.figure
        # img{width:100%}` sans `height:auto` laisse la hauteur de l'attribut
        # en place : un SVG a viewBox ne se deforme pas, il se centre dans une
        # boite trop haute et se retrouve encadre de vide. Les deux figures du
        # site etaient dans ce cas, et le controle ci-dessus les declarait
        # justes — parce qu'il compare l'attribut au fichier, jamais la boite
        # dessinee au fichier. C'est la meme famille d'erreur que « lire la
        # feuille de style ne dit pas quelle regle a gagne ».
        boite = pg.evaluate("""() => [...document.images].filter(i => {
            const r = i.getBoundingClientRect();
            if (!i.naturalWidth || !i.naturalHeight || r.width < 4 || r.height < 4)
                return false;
            const a = r.width / r.height, b = i.naturalWidth / i.naturalHeight;
            return Math.abs(a / b - 1) > 0.02;
        }).map(i => {
            const r = i.getBoundingClientRect();
            return `${i.getAttribute('src')} dessine ${Math.round(r.width)}x`
                 + `${Math.round(r.height)}, rapport naturel ${i.naturalWidth}x`
                 + `${i.naturalHeight}`;
        })""")
        verif(f"{f} : la boite dessinee de chaque image respecte son rapport",
              not boite, str(boite))

    # ---- les cinq principes -----------------------------------------------
    pg.goto(BASE + "principles.html", wait_until="networkidle")
    defiler(pg)
    blocs = pg.evaluate("""() => [...document.querySelectorAll('.pr')].map(b => ({
        id: b.id,
        titre: b.querySelector('h3').textContent.trim(),
        cite: b.querySelector('.cite').textContent.trim(),
        oui: [...b.querySelectorAll('.oui li')].length,
        non: [...b.querySelectorAll('.non li')].length,
        gem: b.querySelector('img.gem')?.getAttribute('src')}))""")
    verif("principes : cinq blocs", len(blocs) == 5, str(len(blocs)))
    for i, (cle, nom, cite, oui, non) in enumerate(PRINCIPES):
        bl = blocs[i] if i < len(blocs) else {}
        verif(f"principes : le bloc {i + 1} est « {nom} » et dans l'ordre de la declaration",
              bl.get("id") == cle and bl.get("titre") == nom, str(bl.get("titre")))
        verif(f"principes : {nom} cite la declaration",
              norm(cite) in norm(bl.get("cite", "")), bl.get("cite", "")[:60])
        verif(f"principes : {nom} porte ce qu'il veut dire", bl.get("oui") == len(oui))
        # la colonne « ce que cela ne veut pas dire » est la raison d'etre de
        # la page : sans elle, la page ne fait qu'allonger le texte du client
        verif(f"principes : {nom} porte ce qu'il NE veut PAS dire", bl.get("non") == len(non))
        verif(f"principes : {nom} a sa propre gemme",
              bl.get("gem") == f"assets/p-{cle}.svg", str(bl.get("gem")))
    verif("principes : cinq gemmes distinctes",
          len({bl["gem"] for bl in blocs}) == 5)
    verif("principes : la page distingue la citation de la redaction",
          "drafted from that statement" in pg.inner_text("body"))

    # ---- 4. les huit decisions ouvertes -----------------------------------
    pg.goto(BASE + "movement.html", wait_until="networkidle")
    defiler(pg)
    t = pg.evaluate("""() => {
        const tr = [...document.querySelectorAll('table.tbl tbody tr')];
        const g = tr.filter(r => r.classList.contains('grp'));
        const d = tr.filter(r => !r.classList.contains('grp'));
        return {groupes: g.map(r => r.textContent.trim()),
                lignes: d.length,
                titres: d.map(r => r.children[0].textContent.trim()),
                etats: d.map(r => r.children[2].textContent.trim()),
                pastilles: document.querySelectorAll('table.tbl .tbd').length};
    }""")
    GROUPES_D = [g for g, _l in DECISIONS]
    TITRES_D = [x[0] for _g, l in DECISIONS for x in l]
    verif("decisions : les trois groupes sont ceux de la source",
          t["groupes"] == GROUPES_D, str(t["groupes"]))
    verif("decisions : autant de lignes que dans la source",
          t["lignes"] == len(TITRES_D), f'{t["lignes"]} vs {len(TITRES_D)}')
    verif("decisions : une pastille par ligne", t["pastilles"] == len(TITRES_D),
          str(t["pastilles"]))
    verif("decisions : la colonne d'etat ne dit qu'une chose",
          set(t["etats"]) == {"To be decided"}, str(set(t["etats"])))
    verif("decisions : les intitules sont ceux de la source",
          t["titres"] == TITRES_D, str(t["titres"]))
    verif("decisions : la page dit POURQUOI le tableau est public",
          "assumes something is being withheld" in pg.inner_text("body"))

    # la figure multipolaire n'a pas de moyeu, et la page le dit
    verif("multipolaire : le vide central est explique",
          "nothing at the centre" in pg.inner_text("body"))
    verif("multipolaire : aucun noeud n'est nomme",
          "none is named" in pg.inner_text("body"))

    # ---- questions --------------------------------------------------------
    qs = pg.evaluate("""() => [...document.querySelectorAll('.qa details')].map(d => ({
        q: d.querySelector('summary').textContent.trim(),
        r: d.querySelector('.rep').textContent.trim()}))""")
    verif("questions : autant que dans la source", len(qs) == len(FAQ), str(len(qs)))
    for i, (q, r) in enumerate(FAQ):
        verif(f"questions : « {q[:38]}… » est posee et repondue",
              i < len(qs) and norm(qs[i]["q"]) == norm(q) and norm(qs[i]["r"]) == norm(r))

    # ---- ce que le mouvement n'est pas ------------------------------------
    pg.goto(BASE + "index.html", wait_until="networkidle")
    defiler(pg)
    cartes = pg.evaluate("""() => [...document.querySelectorAll('#not .card h3')]
        .map(h => h.textContent.trim())""")
    verif("bornes : autant de cartes que dans la source",
          len(cartes) == len(NEST_PAS), str(len(cartes)))
    verif("bornes : chacune est formulee en negatif",
          all(c.startswith("Not ") for c in cartes), str(cartes))

    # ---- 5. le formulaire n'envoie rien -----------------------------------
    pg.goto(BASE + "join.html", wait_until="networkidle")
    defiler(pg)
    fm = pg.evaluate("""() => {
        const f = document.querySelector('form');
        return {action: f.getAttribute('action'), method: f.getAttribute('method'),
                champs: [...f.querySelectorAll('input,select,textarea')]
                          .map(e => (e.labels[0]?.textContent || e.name || '').trim()),
                bouton: f.querySelector('button')?.disabled};
    }""")
    verif("formulaire : aucun attribut action", fm["action"] is None, str(fm["action"]))
    verif("formulaire : aucune methode d'envoi", fm["method"] is None, str(fm["method"]))
    verif("formulaire : le bouton est desactive", fm["bouton"] is True)
    verif("formulaire : la page dit qu'il n'envoie rien",
          "sends nothing anywhere" in pg.inner_text("body"))
    verif("formulaire : la categorie particuliere est expliquee",
          "revealing political opinions" in pg.inner_text("body"))
    # Aucun champ ne demande une opinion, une appartenance ou une piece
    # d'identite : c'est ce que la page promet, et une promesse se verifie.
    interdits_champs = ("opinion", "party", "religion", "ethnic", "passport",
                        "id number", "date of birth", "vote")
    verif("formulaire : aucun champ d'opinion, d'appartenance ou d'identite",
          not [c for c in fm["champs"] if any(m in c.lower() for m in interdits_champs)],
          str(fm["champs"]))

    # =======================================================================
    # LA PRATIQUE — services diplomatiques et lobbying.
    #
    # Le site vend desormais des services a des entites et a des Etats, et se
    # presente comme cabinet de lobbying. Deux affirmations de plus a prouver :
    #  A. rien n'est revendique qui ne soit vrai — ni enregistrement, ni
    #     agrement, ni statut, ni client, ni tarif ;
    #  B. la separation entre le mouvement et la pratique est ECRITE en public,
    #     parce qu'une regle de gouvernance gardee dans une note interne ne vaut
    #     rien et ne peut etre opposee a personne.
    # =======================================================================
    pg.goto(BASE + "services.html", wait_until="networkidle")
    defiler(pg)
    corps_s = pg.inner_text("body")
    blocs_s = pg.evaluate("""() => [...document.querySelectorAll('.svc')].map(b => ({
        id: b.id,
        titre: b.querySelector('h3').textContent.trim(),
        paras: [...b.querySelectorAll('p')].filter(p => !p.classList.contains('n')).length,
        livr: [...b.querySelectorAll('.deliv li')].length}))""")
    verif("services : autant de lignes de service que dans la source",
          len(blocs_s) == len(PRATIQUE), f"{len(blocs_s)} vs {len(PRATIQUE)}")
    for i, (cle, nom, paras, livr) in enumerate(PRATIQUE):
        bl = blocs_s[i] if i < len(blocs_s) else {}
        verif(f"services : la ligne {i + 1} est « {nom} » et dans l'ordre de la source",
              bl.get("id") == cle and bl.get("titre") == nom, str(bl.get("titre")))
        # « ce que le client recoit » est ce qui distingue un service d'une
        # ambition : sans cette liste la page ne peut ni etre jugee ni facturee
        verif(f"services : {nom} dit ce que le client recoit",
              bl.get("livr") == len(livr), f'{bl.get("livr")} vs {len(livr)}')
    verif("services : la ligne qui compte est ecrite en clair",
          "Diplomatic relations between states are conducted by states" in corps_s)
    verif("services : l'absence d'accreditation est ecrite",
          "no accreditation" in corps_s)
    verif("services : l'absence d'enregistrement est ecrite, pas sous-entendue",
          "not registered anywhere as a representative today" in corps_s)
    verif("services : aucun tarif, la case est marquee a decider",
          "To be decided" in pastilles(pg) and dit(corps_s, "no figure appears"))
    verif("services : les honoraires de resultat sont exclus",
          "contingent on a public decision" in corps_s)
    cartes_pn = pg.evaluate("""() => [...document.querySelectorAll('#not-practice .card h3')]
        .map(h => h.textContent.trim())""")
    verif("services : autant de bornes que dans la source",
          len(cartes_pn) == len(PRATIQUE_NEST_PAS), str(len(cartes_pn)))
    verif("services : chaque borne est formulee en negatif",
          all(c.startswith("Not ") for c in cartes_pn), str(cartes_pn))

    pg.goto(BASE + "lobbying.html", wait_until="networkidle")
    defiler(pg)
    pg.evaluate("() => document.querySelectorAll('details').forEach(d => d.open = true)")
    pg.wait_for_timeout(80)
    corps_l = pg.inner_text("body")
    verif("lobbying : autant de lignes d'activite que dans la source",
          pg.evaluate("() => document.querySelectorAll('#does .card').length")
          == len(LOBBYING_FAIT))
    refus = pg.evaluate("""() => [...document.querySelectorAll('.refus li')]
        .map(l => l.textContent.trim())""")
    verif("lobbying : autant de refus que dans la source",
          len(refus) == len(LOBBYING_NEFAIT), f"{len(refus)} vs {len(LOBBYING_NEFAIT)}")
    for i, r in enumerate(LOBBYING_NEFAIT):
        verif(f"lobbying : le refus {i + 1} est celui de la source",
              i < len(refus) and norm(refus[i]) == norm(r), refus[i][:60] if i < len(refus) else "")
    # LA MURAILLE. Sans ce bloc, le reste du site n'est pas defendable : un
    # mouvement qui publie des positions et un cabinet paye pour porter celles
    # de ses clients, tenus dans la meme poche, font lire chaque position comme
    # achetee.
    verif("lobbying : la muraille a sa propre ancre", pg.evaluate(
          "() => !!document.getElementById('wall')"))
    verif("lobbying : autant de clauses de separation que dans la source",
          pg.evaluate("() => document.querySelectorAll('#wall .mur .card').length")
          == len(MURAILLE))
    verif("lobbying : la clause centrale est publique, pas interne",
          "cannot commission, edit, delay or veto" in corps_l)
    verif("lobbying : la page dit pourquoi la clause est publiee",
          "kept in an internal note" in corps_l)
    verif("lobbying : la figure de la muraille ne comporte aucun pont",
          "a line that nothing crosses" in pg.evaluate(
              "() => document.querySelector('#wall .figure img').alt"))
    verif("lobbying : aucun registre nomme, l'etat est a decider",
          pastilles(pg).count("To be decided") >= 3, str(pastilles(pg)))
    qs_p = pg.evaluate("""() => [...document.querySelectorAll('.qa details')].map(d => ({
        q: d.querySelector('summary').textContent.trim(),
        r: d.querySelector('.rep').textContent.trim()}))""")
    verif("lobbying : autant de questions que dans la source",
          len(qs_p) == len(FAQ_PRATIQUE), str(len(qs_p)))
    for i, (q, r) in enumerate(FAQ_PRATIQUE):
        verif(f"lobbying : « {q[:36]}… » est posee et repondue",
              i < len(qs_p) and norm(qs_p[i]["q"]) == norm(q)
              and norm(qs_p[i]["r"]) == norm(r))

    # =======================================================================
    # LE CERCLE — et la seule chose qu'une page d'activites peut rater.
    # Un evenement invente. Aucune date, aucun lieu, aucun intervenant : c'est
    # verifie ici en plus des motifs generaux appliques a toutes les pages.
    # =======================================================================
    pg.goto(BASE + "circle.html", wait_until="networkidle")
    defiler(pg)
    corps_c = pg.inner_text("body")
    verif("cercle : autant de cartes de definition que dans la source",
          pg.evaluate("() => document.querySelectorAll('#what .card').length")
          == len(CERCLE_QUOI))
    acts = pg.evaluate("""() => [...document.querySelectorAll('.acts .card')].map(c => ({
        id: c.id, titre: c.querySelector('h3').textContent.trim(),
        etat: c.querySelector('.st .tbd')?.textContent.trim()}))""")
    verif("cercle : autant d'activites que dans la source",
          len(acts) == len(CERCLE_ACTIVITES), f"{len(acts)} vs {len(CERCLE_ACTIVITES)}")
    for i, (cle, nom, _d) in enumerate(CERCLE_ACTIVITES):
        a = acts[i] if i < len(acts) else {}
        verif(f"cercle : l'activite {i + 1} est « {nom} »",
              a.get("id") == f"a-{cle}" and a.get("titre") == nom, str(a.get("titre")))
        verif(f"cercle : « {nom} » porte son etat reel",
              a.get("etat") == "Not yet scheduled", str(a.get("etat")))
    verif("cercle : la page dit qu'elle n'annonce rien",
          dit(corps_c, "This page announces nothing"))
    verif("cercle : le sceau est present",
          pg.evaluate("() => !!document.querySelector('img.sceau')"))

    # =======================================================================
    # LE PORTAIL. Meme regle que le formulaire d'adhesion, et un cran plus
    # haut : une liste de membres d'un mouvement politique est une donnee
    # sensible, et la brancher sans responsable identifie serait livrer le
    # probleme juridique cle en main.
    # =======================================================================
    pg.goto(BASE + "portal.html", wait_until="networkidle")
    defiler(pg)
    corps_p = pg.inner_text("body")
    fp = pg.evaluate("""() => {
        const f = document.querySelector('form');
        return {action: f.getAttribute('action'), method: f.getAttribute('method'),
                bouton: f.querySelector('button')?.disabled,
                champs: [...f.querySelectorAll('input,select,textarea')]
                          .map(e => ((e.labels[0]?.textContent || '') + ' ' + e.type).trim())};
    }""")
    verif("portail : aucun attribut action", fp["action"] is None, str(fp["action"]))
    verif("portail : aucune methode d'envoi", fp["method"] is None, str(fp["method"]))
    verif("portail : le bouton est desactive", fp["bouton"] is True)
    verif("portail : la page dit qu'il n'authentifie personne",
          "authenticates nobody" in corps_p)
    # Une page de connexion qui accepte une adresse electronique transforme
    # chaque tentative ratee en information sur qui est membre et qui ne l'est
    # pas. Le champ demande donc une reference, et la page l'explique.
    verif("portail : aucun champ d'adresse electronique",
          not [c for c in fp["champs"] if "email" in c.lower()], str(fp["champs"]))
    verif("portail : le choix de la reference plutot que du nom est explique",
          "member reference rather than a name" in corps_p)
    lp = pg.evaluate("""() => {
        const tr = [...document.querySelectorAll('table.tbl tbody tr')];
        return {n: tr.length, titres: tr.map(r => r.children[0].textContent.trim()),
                etats: [...new Set(tr.map(r => r.children[2].textContent.trim()))]};
    }""")
    verif("portail : autant d'exigences que dans la source",
          lp["n"] == len(PORTAIL_EXIGENCES), f'{lp["n"]} vs {len(PORTAIL_EXIGENCES)}')
    verif("portail : les exigences sont celles de la source",
          lp["titres"] == [x[0] for x in PORTAIL_EXIGENCES], str(lp["titres"]))
    verif("portail : aucune exigence n'est presentee comme satisfaite",
          lp["etats"] == ["To be decided"], str(lp["etats"]))

    pg.goto(BASE + "portal-area.html", wait_until="networkidle")
    defiler(pg)
    corps_a = pg.inner_text("body")
    verif("espace membre : autant d'entrees que de formats dans la source",
          pg.evaluate("() => document.querySelectorAll('.feed .it').length")
          == len(CERCLE_ACTIVITES))
    n_prog = pg.evaluate("""() => [...document.querySelectorAll('.feed .it')]
        .filter(i => i.textContent.includes('Not yet scheduled')).length""")
    verif("espace membre : chaque entree porte « Not yet scheduled »",
          n_prog == len(CERCLE_ACTIVITES), f"{n_prog} vs {len(CERCLE_ACTIVITES)}")
    # un chapeau sur le fil d'activites, plus quatre panneaux vides qui
    # annoncent leur propre vide au lieu d'etre remplis de faux echantillons
    verif("espace membre : cinq panneaux disent leur etat reel",
          pg.evaluate("() => document.querySelectorAll('.feed .vide').length") == 5)
    verif("espace membre : la page dit qu'il n'y a pas de session",
          dit(corps_a, "This is a drawing, not a session"))
    verif("espace membre : aucun nom de membre invente",
          "No account exists" in corps_a)
    verif("espace membre : aucun formulaire, donc rien a soumettre",
          pg.evaluate("() => document.querySelectorAll('form').length") == 0)

    # ---- en-tete : les deux groupes et la porte ---------------------------
    for f in PAGES:
        pg.goto(BASE + f, wait_until="domcontentloaded")
        verif(f"{f} : l'en-tete separe le mouvement de la pratique",
              pg.evaluate("() => document.querySelectorAll('.nav .sep').length") == 1)
        # La porte est un enfant de l'en-tete et NON du <nav> : dans le menu,
        # des que la navigation passait sur deux lignes, elle se retrouvait
        # seule sur la seconde. Ce controle verifie les deux choses a la fois —
        # qu'elle existe, et qu'elle est bien hors du menu.
        verif(f"{f} : la porte du portail est un bouton distinct, hors du menu",
              pg.evaluate("""() => {
                  const a = document.querySelector('.hdr a.signin');
                  return !!a && a.getAttribute('href') === 'portal.html'
                         && !a.closest('nav');
              }"""))

    # ---- une ancre doit atterrir SOUS l'en-tete collant --------------------
    # L'en-tete est en position:sticky. Sans marge de defilement, le navigateur
    # amene la cible en haut de la fenetre, c'est-a-dire DERRIERE l'en-tete :
    # le titre de la section visee est cache et le visiteur croit avoir atterri
    # au mauvais endroit. Le defaut est invisible sur un bureau, ou l'en-tete
    # fait 70 px, et flagrant sur un telephone, ou il en fait 167.
    for largeur in (390, 1280):
        ctx2 = b.new_context(viewport={"width": largeur, "height": 800})
        p3 = ctx2.new_page()
        for f in PAGES:
            p3.goto(BASE + f, wait_until="networkidle")
            ancres = p3.evaluate("""() => [...document.querySelectorAll('a[href^="#"]')]
                .map(a => a.getAttribute('href')).filter(h => h && h.length > 1)""")
            for frag in sorted(set(ancres)):
                p3.goto(BASE + f + frag, wait_until="networkidle")
                p3.wait_for_timeout(220)
                ok = p3.evaluate(f"""() => {{
                    const e = document.querySelector({frag!r});
                    const h = document.querySelector('.hdr');
                    if (!e || !h) return null;
                    return e.getBoundingClientRect().top
                           >= h.getBoundingClientRect().bottom - 2;
                }}""")
                verif(f"{f}{frag} @{largeur} : l'ancre atterrit sous l'en-tete collant",
                      ok is True, str(ok))
        ctx2.close()

    # ---- visuels : aucun orphelin, aucun manquant -------------------------
    dossier = os.path.join(RACINE, "assets")
    presents = {f for f in os.listdir(dossier) if f.endswith(".svg")}
    utilises = set()
    # Les <img> NE SUFFISENT PAS. hero.svg est pose en background-image par la
    # feuille de style : la premiere version de ce controle ne regardait que
    # document.images et declarait donc le fond du hero « jamais utilise »,
    # alors qu'il est la premiere chose que le visiteur voit. Un inventaire qui
    # ne connait qu'une facon de poser une image invente des orphelins.
    for f in PAGES:
        pg.goto(BASE + f, wait_until="domcontentloaded")
        for src in pg.evaluate("() => [...document.images].map(i => i.getAttribute('src'))"):
            if src and src.endswith(".svg"):
                utilises.add(src.split("/")[-1])
        for u in pg.evaluate("""() => [...document.querySelectorAll('*')]
                .flatMap(e => {
                    const s = getComputedStyle(e);
                    return [s.backgroundImage, s.getPropertyValue('content')];
                })
                .filter(v => v && v.includes('url('))"""):
            for m in re.findall(r'url\(["\']?([^"\')]+)', u):
                if m.endswith(".svg"):
                    utilises.add(m.split("/")[-1])
    verif("visuels : aucun present mais jamais utilise",
          not (presents - utilises), str(sorted(presents - utilises)))
    verif("visuels : aucun utilise mais absent",
          not (utilises - presents), str(sorted(utilises - presents)))

    ctx.close()
    b.close()

print(f"\n{n} verifications, {len(echecs)} echec(s)")
for e in echecs:
    print("  -", e)
sys.exit(1 if echecs else 0)
