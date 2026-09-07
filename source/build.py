# -*- coding: utf-8 -*-
"""
Equilibrium — construit index.html, principles.html, movement.html, join.html.

Quatre pages qui partagent un en-tete, un pied et une feuille de style. La
coquille est ecrite une fois ici plutot que recopiee dans quatre fichiers
destines a diverger des la premiere correction.

TROIS REGLES DE FOND, TENUES DANS TOUT LE FICHIER

 1. La declaration du mouvement est citee MOT POUR MOT et typographiee
    autrement que le reste. Un lecteur doit pouvoir separer d'un coup d'oeil
    ce que le mouvement a ecrit de ce qu'un redacteur en a tire. Les pages le
    disent en toutes lettres, elles ne comptent pas sur la typographie seule.

 2. Aucun fait sur le mouvement n'est invente. Ni date, ni effectif, ni pays,
    ni forme juridique, ni dirigeant, ni financement, ni soutien, ni presse.
    Les emplacements existent, marques « To be decided », et sont AFFICHES au
    visiteur plutot que caches : un lecteur a qui l'on dit « forme juridique :
    a decider » comprend qu'il regarde un mouvement qui demarre ; un lecteur a
    qui l'on ne dit rien suppose qu'on lui cache quelque chose.

 3. Aucune position sur un Etat, un gouvernement, un parti, une organisation
    ou un conflit reels, et aucun nom propre de pays dans le propos. Son texte
    est general par construction ; le rendre concret serait lui faire dire ce
    qu'il n'a pas dit, sur le terrain ou cela coute le plus cher.

Le formulaire d'adhesion n'a pas de traitement : il n'envoie rien nulle part,
et la page l'ecrit. Une liste de sympathisants d'un mouvement politique est,
dans l'Union europeenne, une donnee revelant les opinions politiques — une
categorie particuliere au sens de l'article 9 du RGPD. Un formulaire branche
sans responsable de traitement identifie et sans pays dont la loi s'applique
serait un probleme juridique livre cle en main. Il reste donc une maquette
jusqu'a ce que le client tranche ces deux points.
"""
import os
import html

from contenu import (MOUVEMENT, LIGNE, CHAINE, DECLARATION, PRINCIPES,
                     NEST_PAS, DECISIONS, FAQ,
                     PRATIQUE, PRATIQUE_NEST_PAS, LOBBYING_FAIT, LOBBYING_NEFAIT,
                     MURAILLE, FAQ_PRATIQUE,
                     CERCLE, CERCLE_QUOI, CERCLE_ACTIVITES, PORTAIL_EXIGENCES,
                     ADRESSE_BTC, RESEAU_BTC, SOUTIEN_EST, SOUTIEN_NEST_PAS,
                     SOUTIEN_OUVERT)

_ICI = os.path.dirname(os.path.abspath(__file__))
# Dans le paquet livre, les scripts sont dans source/ et les pages un cran
# au-dessus. Sans ce reglage, relancer build.py depuis le paquet ecrirait les
# quatre pages DANS source/, laissant les vraies pages inchangees : une
# regeneration sans erreur, sans effet, et qui a l'air d'avoir marche.
RACINE = os.path.dirname(_ICI) if os.path.basename(_ICI) == "source" else _ICI

VERSION_CSS = 8     # a incrementer a chaque modification de assets/site.css
BANDEAU_DEMO = True

E = html.escape


def p(txt):
    return f"<p>{txt}</p>"


# ---------------------------------------------------------------------------
# coquille
# ---------------------------------------------------------------------------
# La navigation est GROUPEE, et le filet entre les deux groupes n'est pas une
# decoration. Tout ce site defend une distinction — le mouvement qui publie ses
# positions d'un cote, le cabinet qui porte celles de ses clients de l'autre —
# et un menu qui melangerait les sept libelles dirait le contraire du texte
# qu'il surmonte.
GROUPES = [
    ("The movement", [("index.html#statement", "Statement", "statement"),
                      ("principles.html", "Principles", "principles"),
                      ("movement.html", "The movement", "movement"),
                      ("join.html", "Join", "join"),
                      ("support.html", "Support", "support")]),
    ("The practice", [("services.html", "Services", "services"),
                      ("lobbying.html", "Lobbying", "lobbying"),
                      ("circle.html", "Circle", "circle")]),
]
LIENS = [x for _g, l in GROUPES for x in l]


def entete(courant):
    parts = []
    for i, (_g, liens) in enumerate(GROUPES):
        if i:
            parts.append('<span class="sep" aria-hidden="true"></span>')
        parts.extend(
            '<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if c == courant else "", t)
            for h, t, c in liens)
    # Le portail est un bouton distinct et non un huitieme libelle : ce n'est
    # pas une page du propos, c'est une porte. Il est aussi SORTI du <nav> —
    # a l'interieur, des que la navigation passait sur deux lignes, la pastille
    # se retrouvait seule sur la seconde, collee au filet du bas. Constate sur
    # la capture a 1280 px, corrige ici : trois enfants flex, brand | nav |
    # porte, et c'est la navigation qui se replie, pas le bouton qui s'exile.
    porte = ('<a class="signin" href="portal.html"%s>Member sign-in</a>'
             % (' aria-current="page"' if courant == "portal" else ""))
    demo = ('<div class="demo">Demonstration mockup — content awaiting the '
            'movement&rsquo;s approval. Nothing on this site is published.</div>'
            if BANDEAU_DEMO else "")
    return f'''{demo}<header class="hdr"><div class="wrap">
  <a class="brand" href="index.html">
    <img src="assets/mark.svg" alt="" width="26" height="26">
    <span class="nm">{MOUVEMENT}</span>
  </a>
  <nav class="nav">{"".join(parts)}</nav>
  {porte}
</div></header>'''


def pied():
    liens = "".join('<a href="%s">%s</a>' % (h, t) for h, t, _ in LIENS)
    return f'''<footer class="ft"><div class="wrap">
  <div class="haut">
    <div>
      <span class="brand">
        <img src="assets/mark.svg" alt="" width="26" height="26">
        <span class="nm">{MOUVEMENT}</span>
      </span>
      <p class="ligne">{LIGNE}</p>
    </div>
    <nav>{liens}</nav>
  </div>
  <div class="bas">
    <p>The statement on this site is quoted verbatim. All other text is draft
    copy written from that statement and is subject to the movement&rsquo;s
    approval.</p>
    <p>No legal form, place of registration, membership, funding, registration
    as a representative, accreditation or official status of any kind is
    claimed anywhere on this site. Those are open decisions and are listed as
    such on <a href="movement.html#decisions">The movement</a>.</p>
    <p>The movement publishes positions in its own name. The practice speaks
    for clients, in theirs. The rule that separates the two is set out on
    <a href="lobbying.html#wall">Lobbying</a>.</p>
  </div>
</div></footer>'''


def bande(surtitre, titre, sous):
    """Le bandeau des pages de la pratique et du Cercle."""
    return f'''<div class="band"><div class="wrap"><div class="in">
  <span class="eyebrow">{surtitre}</span>
  <h1>{titre}</h1>
  <p class="sub">{sous}</p>
</div></div></div>'''


def page(fichier, titre, description, courant, corps):
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(titre)}</title>
<meta name="description" content="{E(description)}">
<meta name="robots" content="noindex">
<link rel="stylesheet" href="assets/site.css?v={VERSION_CSS}">
</head>
<body>
{entete(courant)}
{corps}
{pied()}
</body>
</html>'''
    chemin = os.path.join(RACINE, fichier)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(doc)
    print("  %-18s %7d o" % (fichier, len(doc.encode("utf-8"))))


# ---------------------------------------------------------------------------
# fragments
# ---------------------------------------------------------------------------
def titre_section(sur, h2, sous=""):
    s = f'<p>{sous}</p>' if sous else ""
    return (f'<div class="sec-h"><span class="eyebrow">{sur}</span>'
            f'<h2>{h2}</h2>{s}</div>')


DECL_HTML = "".join(f"<p>{t}</p>" for t in DECLARATION)


# ---------------------------------------------------------------------------
# page 1 — accueil
# ---------------------------------------------------------------------------
cartes_principes = "".join(
    f'''<a class="card" href="principles.html#{cle}" style="text-decoration:none">
      <img src="assets/p-{cle}.svg" alt="" width="64" height="64" loading="lazy"
           style="width:64px;margin-bottom:14px">
      <h3>{nom}</h3><p>{cite}</p></a>'''
    for cle, nom, cite, _o, _n in PRINCIPES)

cartes_nest_pas = "".join(
    f'<div class="card"><h3>Not {t[0].lower()}{t[1:]}</h3><p>{d}</p></div>'
    for t, d in NEST_PAS)

accueil = f'''<main>
<div class="hero"><div class="wrap"><div class="in">
  <span class="eyebrow">Global political &amp; diplomatic movement</span>
  <h1>Balance rather than <span class="di">domination</span>.</h1>
  <p class="sub">{LIGNE}</p>
  <div class="actions">
    <a class="btn btn-plein" href="#statement">Read the statement</a>
    <a class="btn" href="principles.html">The five principles</a>
  </div>
</div></div></div>

<section id="statement"><div class="wrap">
  <div class="filet"></div>
  {titre_section("The statement", "In the movement&rsquo;s own words",
                 "Quoted in full, without alteration or abridgement. Everything "
                 "else on this site is drafted from it.")}
  <div class="decl">{DECL_HTML}</div>
  <p class="attr">&mdash; {MOUVEMENT}, founding statement</p>
</div></section>

<section id="principles"><div class="wrap">
  <div class="filet"></div>
  {titre_section("The philosophy", "Five core principles",
                 "Named in the statement, in this order. Each one is set out in "
                 "full, together with what it does not mean.")}
  <div class="grid g3">{cartes_principes}</div>
  <div class="actions"><a class="btn" href="principles.html">Read the five principles</a></div>
</div></section>

<section id="not"><div class="wrap">
  <div class="filet"></div>
  {titre_section("Boundaries", "What Equilibrium is not",
                 "A movement that states only general principles gets read as "
                 "whatever the reader projects onto it. These are the limits, "
                 "written by the movement rather than left to others.")}
  <div class="grid g4">{cartes_nest_pas}</div>
</div></section>

<section id="two"><div class="wrap">
  <div class="filet"></div>
  {titre_section("One name, two things", "The movement and the practice",
                 "Equilibrium publishes an argument. It also advises and "
                 "represents clients who pay for that work. Those are two "
                 "different activities and they are kept apart on purpose.")}
  <div class="grid g2">
    <a class="card" href="movement.html" style="text-decoration:none">
      <h3>The movement</h3>
      <p>Positions published in Equilibrium&rsquo;s own name, about how the
      international system should be ordered. Nobody pays for them and nobody
      can commission one.</p>
      <p>The statement, the five principles, and the decisions still open.</p></a>
    <a class="card" href="services.html" style="text-decoration:none">
      <h3>The practice</h3>
      <p>Diplomatic advisory and declared representation, for entities and for
      states, under mandate and on the record.</p>
      <p>What it does, what it refuses, and the rule that keeps a client from
      ever buying a movement position.</p></a>
  </div>
  <div class="avert">
    <h4>Why this is on the front page</h4>
    <p>A movement that publishes political positions and a firm paid to
    advance its clients&rsquo; positions are two different things in law almost
    everywhere. <b>Kept in one pocket, every position the movement publishes
    reads as bought.</b> The separation is therefore stated in public, on
    <a href="lobbying.html#wall">Lobbying</a>, rather than kept in an internal
    note where nobody can hold anyone to it.</p>
    <p>Whether the two are one legal person or two is <b>not yet
    decided</b>, and it is the first row of the practice group on
    <a href="movement.html#decisions">The movement</a>.</p>
  </div>
</div></section>

<section id="next"><div class="wrap">
  <div class="filet"></div>
  {titre_section("Next", "Where to go from here")}
  <div class="grid g4">
    <a class="card" href="principles.html" style="text-decoration:none">
      <h3>The five principles</h3>
      <p>Each principle set out with what it means in practice and what it does
      not mean.</p></a>
    <a class="card" href="services.html" style="text-decoration:none">
      <h3>Services</h3>
      <p>Six lines of advisory work, and the five things the practice will not
      do at any price.</p></a>
    <a class="card" href="circle.html" style="text-decoration:none">
      <h3>{CERCLE}</h3>
      <p>The membership, its activities, and the member portal.</p></a>
    <a class="card" href="join.html" style="text-decoration:none">
      <h3>Join</h3>
      <p>How to follow the movement, and what has to be settled before it can
      accept a single name.</p></a>
  </div>
</div></section>
</main>'''


# ---------------------------------------------------------------------------
# page 2 — les principes
# ---------------------------------------------------------------------------
def bloc_principe(i, cle, nom, cite, oui, non):
    lo = "".join(f"<li>{t}</li>" for t in oui)
    ln = "".join(f"<li>{t}</li>" for t in non)
    return f'''<div class="pr" id="{cle}">
  <div>
    <img class="gem" src="assets/p-{cle}.svg" alt="" width="170" height="170" loading="lazy">
    <p class="num">{i:02d}</p>
  </div>
  <div>
    <h3>{nom}</h3>
    <p class="cite">&ldquo;{cite}&rdquo;</p>
    <div class="deux">
      <div class="oui"><h4>What it means</h4><ul>{lo}</ul></div>
      <div class="non"><h4>What it does not mean</h4><ul>{ln}</ul></div>
    </div>
  </div>
</div>'''


principes_html = "".join(
    bloc_principe(i + 1, cle, nom, cite, oui, non)
    for i, (cle, nom, cite, oui, non) in enumerate(PRINCIPES))

principes = f'''<main>
<section><div class="wrap">
  <div class="filet"></div>
  {titre_section("The philosophy", "Five core principles",
                 "The statement names them in one sentence: balance of power, "
                 "sovereignty, diplomacy, economic freedom, and long-term "
                 "stability. They are set out here in that order.")}
  <div class="avert">
    <h4>Two registers on this page</h4>
    <p>The line quoted under each principle is taken from the movement&rsquo;s
    own statement. <b>Everything below it is drafted from that statement</b>
    and carries no authority of its own until the movement approves it.</p>
    <p>Each principle also carries what it <b>does not</b> mean. That column is
    not a hedge: a general principle is only legible once its limits are
    stated, and a movement that does not state them has them stated for it.</p>
  </div>
  {principes_html}
</div></section>
</main>'''


# ---------------------------------------------------------------------------
# page 3 — le mouvement
# ---------------------------------------------------------------------------
lignes_decisions = "".join(
    f'<tr class="grp"><td colspan="3">{groupe}</td></tr>' + "".join(
        f'<tr><td>{t}</td><td class="why">{d}</td>'
        f'<td><span class="tbd">To be decided</span></td></tr>'
        for t, d in lignes)
    for groupe, lignes in DECISIONS)
N_DECISIONS = sum(len(l) for _g, l in DECISIONS)

faq_html = "".join(
    f'<details><summary>{q}</summary><p class="rep">{r}</p></details>'
    for q, r in FAQ)

mouvement = f'''<main>
<section><div class="wrap">
  <div class="filet"></div>
  {titre_section("The movement", "What Equilibrium is",
                 "A body of argument, published in public, about how the "
                 "international system should be ordered.")}
  <div class="grid g3">
    <div class="card"><h3>An argument, not an office</h3>
      <p>Equilibrium exists as a position and the case made for it. It claims
      no mandate, no representation and no expertise, and asks to be judged on
      whether the argument holds.</p></div>
    <div class="card"><h3>General by design</h3>
      <p>The five principles are stated at the level of the system, not of any
      particular dispute. Applying them to a specific question is a separate
      act, taken deliberately and published as such.</p></div>
    <div class="card"><h3>Open in method</h3>
      <p>The statement is published in full. Anything drafted from it is
      marked as drafted from it. Nothing that has not been decided is
      presented as though it had been.</p></div>
  </div>
</div></section>

<section id="multipolar"><div class="wrap">
  <div class="filet"></div>
  {titre_section("The idea", "Multipolar, and what that means here",
                 "&ldquo;No single power, bloc, or ideology should determine "
                 "the future of the international system.&rdquo; The figure "
                 "below is the shape of that sentence.")}
  <figure class="figure">
    <img src="assets/multipolar.svg" alt="Seven centres of decision of equal
         weight, each linked to all the others, with nothing at the centre."
         width="1400" height="560" loading="lazy">
    <figcaption>Seven centres of equal weight, each linked to all the others,
    and nothing at the centre. The empty middle is the point: a diagram with a
    hub would state the opposite of the sentence it illustrates. No node stands
    for a real country, and none is named &mdash; attaching these points to
    actual states would attribute to the movement a position it has not
    taken.</figcaption>
  </figure>
</div></section>

<section id="decisions"><div class="wrap">
  <div class="filet"></div>
  {titre_section("Open questions", "Decisions that have not been taken",
                 "Three groups: the movement, the practice, and the Circle. "
                 "They are shown rather than hidden. Several carry legal "
                 "consequences in whichever country they are taken, and none "
                 "of them can be answered by a website.")}
  <table class="tbl">
    <thead><tr><th>Question</th><th>Why it matters</th><th>Status</th></tr></thead>
    <tbody>{lignes_decisions}</tbody>
  </table>
  <div class="avert">
    <h4>Why this table is public</h4>
    <p>A visitor who reads &ldquo;legal form: to be decided&rdquo; understands
    that this is a movement at its beginning. A visitor who is told nothing
    assumes something is being withheld. <b>The second costs more than the
    first.</b></p>
    <p>No number appears anywhere on this site: no membership figure, no
    founding date, no country, no funding, no audience. Not one of them is
    known, and a political movement that publishes a figure it cannot support
    loses the argument the first time somebody checks.</p>
  </div>
</div></section>

<section id="questions"><div class="wrap">
  <div class="filet"></div>
  {titre_section("Questions", "Questions and answers")}
  <div class="qa">{faq_html}</div>
</div></section>
</main>'''


# ---------------------------------------------------------------------------
# page 4 — rejoindre
# ---------------------------------------------------------------------------
rejoindre = f'''<main>
<section><div class="wrap">
  <div class="filet"></div>
  {titre_section("Join", "Follow the movement",
                 "Equilibrium is an argument in public. The first way to take "
                 "part in it is to read it and to argue with it.")}

  <div class="avert">
    <h4>Read this before the form</h4>
    <p><b>The form below is a mockup. It sends nothing anywhere.</b> There is
    no address behind it, no database, no script and no third-party service.
    Typing into it has no effect of any kind.</p>
    <p>That is deliberate. A list of the supporters of a political movement is,
    under European data protection law, information revealing political
    opinions &mdash; a special category, with obligations attached. Before this
    form can accept a single name there has to be an <b>identified body that
    receives the data</b> and a <b>country whose law applies to it</b>. Both
    are listed as open on <a href="movement.html#decisions">The movement</a>.</p>
    <p>The form asks for no political opinion, no affiliation and no
    identity document, and it will not, whatever it is eventually connected
    to.</p>
  </div>

  <form class="form" onsubmit="return false;">
    <div class="champ">
      <label for="nm">Name</label>
      <input id="nm" name="nm" type="text" autocomplete="name" placeholder="Your name">
    </div>
    <div class="champ">
      <label for="ct">Country</label>
      <input id="ct" name="ct" type="text" autocomplete="country-name"
             placeholder="Where you are writing from">
    </div>
    <div class="champ">
      <label for="em">How to reach you</label>
      <input id="em" name="em" type="text" autocomplete="off"
             placeholder="An address or handle you check">
    </div>
    <div class="champ">
      <label for="cb">How you would like to take part</label>
      <select id="cb" name="cb">
        <option>Follow the movement</option>
        <option>Write or translate</option>
        <option>Research and sourcing</option>
        <option>Organise locally</option>
        <option>Something else</option>
      </select>
    </div>
    <div class="champ">
      <label for="ms">Anything you want to say</label>
      <textarea id="ms" name="ms" rows="5"
                placeholder="Optional. Disagreement is as useful as agreement."></textarea>
    </div>
    <button class="btn btn-plein" type="submit" disabled>Disabled in this mockup</button>
  </form>
</div></section>

<section id="channels"><div class="wrap">
  <div class="filet"></div>
  {titre_section("Elsewhere", "Where the movement publishes",
                 "One channel is known. If there are others, they belong here.")}
  <div class="grid g3">
    <div class="card"><h3>{CHAINE}</h3>
      <p>The handle shown on the account the movement uses today. Confirm it
      and any others, and they go here as links.</p></div>
    <div class="card"><h3>Other channels</h3>
      <p><span class="tbd">To be decided</span></p>
      <p>Whether the movement publishes anywhere else, and under which
      names.</p></div>
    <div class="card"><h3>Press and enquiries</h3>
      <p><span class="tbd">To be decided</span></p>
      <p>Which address receives them, and who answers in the movement&rsquo;s
      name.</p></div>
  </div>
</div></section>
</main>'''


# ---------------------------------------------------------------------------
# page 5 — les services
# ---------------------------------------------------------------------------
def bloc_service(i, cle, nom, paras, livrables):
    ps = "".join(f"<p>{t}</p>" for t in paras)
    ls = "".join(f"<li>{t}</li>" for t in livrables)
    return f'''<div class="svc" id="{cle}">
  <div><p class="n">{i:02d}</p><h3>{nom}</h3></div>
  <div>{ps}
    <ul class="deliv"><h4>What the client receives</h4>{ls}</ul>
  </div>
</div>'''


services_html = "".join(
    bloc_service(i + 1, cle, nom, paras, liv)
    for i, (cle, nom, paras, liv) in enumerate(PRATIQUE))

cartes_pratique_non = "".join(
    f'<div class="card"><h3>Not {t[0].lower()}{t[1:]}</h3><p>{d}</p></div>'
    for t, d in PRATIQUE_NEST_PAS)

ETAPES = [
    ("Acceptance and conflicts",
     "Before anything else: does this client, on this question, pass the "
     "acceptance policy, and does the work conflict with a mandate already "
     "held or with a position the movement has published? A conflict found at "
     "this stage costs a conversation. Found later it costs the mandate."),
    ("Registration first",
     "Where putting this position requires an entry in a register, the entry "
     "is made before the first approach, not after it. There is no version of "
     "this work in which the paperwork follows the meeting."),
    ("A written engagement",
     "Scope, what is expressly excluded, who signs, what is disclosed and to "
     "whom. An engagement that cannot be described in writing is one where the "
     "two sides want different things."),
    ("The work, on the record",
     "Every approach recorded, every return filed, and the client told what "
     "was actually said rather than what would be reassuring."),
]
etapes_html = "".join(
    f'<div class="card"><h3>{i + 1}. {t}</h3><p>{d}</p></div>'
    for i, (t, d) in enumerate(ETAPES))

services = f'''<main>
{bande("The practice",
       "Advisory and declared <span class=\"di\">representation</span>.",
       "For entities and for states. Under mandate, in writing, and in "
       "whichever register applies &mdash; or not at all.")}

<section id="line"><div class="wrap">
  <div class="filet"></div>
  {titre_section("The line that matters", "What a private practice can and cannot be",
                 "This is written first because it is the sentence that "
                 "separates serious advisory work from something pretending to "
                 "be an official channel.")}
  <div class="avert">
    <h4>Read this before anything below</h4>
    <p><b>Diplomatic relations between states are conducted by states.</b>
    Equilibrium holds no accreditation, no diplomatic status and no official
    function of any kind. It is not an organ of any state, it represents no
    state as such, and nothing it does binds anybody.</p>
    <p>What a private practice can do is read a position, prepare a party,
    open and hold a channel, carry a case accurately, and act as a
    <b>declared</b> representative before public decision-makers. That is the
    whole of it, and it is a great deal of work.</p>
    <p>Equilibrium is <b>not registered anywhere as a representative today</b>,
    and this site does not suggest otherwise. Registration follows from the
    country where the practice is set up and from where each client sits.
    Neither has been decided; both are listed on
    <a href="movement.html#decisions">The movement</a>.</p>
  </div>
</div></section>

<section id="lines"><div class="wrap">
  <div class="filet"></div>
  {titre_section("Services", "Six lines of work",
                 "Each one states what the client actually receives. A service "
                 "described only by its ambition cannot be judged, and cannot "
                 "be invoiced honestly either.")}
  {services_html}
</div></section>

<section id="how"><div class="wrap">
  <div class="filet"></div>
  {titre_section("Method", "How an engagement runs",
                 "Four steps, in this order. The order is the point: three of "
                 "the four exist to be done before the work starts.")}
  <div class="grid g4">{etapes_html}</div>
</div></section>

<section id="fees"><div class="wrap">
  <div class="filet"></div>
  {titre_section("Fees", "How the practice is paid")}
  <div class="grid g2">
    <div class="card"><h3>The rate</h3>
      <p><span class="tbd">To be decided</span></p>
      <p>No figure appears anywhere on this site, because none has been set.
      A practice that publishes a number it has not decided is negotiating
      against itself before the first conversation.</p></div>
    <div class="card"><h3>What is excluded whatever the answer</h3>
      <p>No fee contingent on a public decision, in any form and under any
      name. What a contingency fee buys is not persuasion, and in several
      places it is not lawful either.</p>
      <p>No engagement written against a result obtained from a public
      authority.</p></div>
  </div>
</div></section>

<section id="not-practice"><div class="wrap">
  <div class="filet"></div>
  {titre_section("Boundaries", "What the practice is not",
                 "The same discipline as the movement&rsquo;s own boundaries: "
                 "what a firm of this kind does not say about itself, its "
                 "clients and its opponents will say for it.")}
  <div class="grid g3">{cartes_pratique_non}</div>
  <div class="actions">
    <a class="btn" href="lobbying.html">Representation, transparency and the wall</a>
  </div>
</div></section>
</main>'''


# ---------------------------------------------------------------------------
# page 6 — lobbying
# ---------------------------------------------------------------------------
cartes_lob = "".join(
    f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in LOBBYING_FAIT)
refus_lob = "".join(f"<li>{t}</li>" for t in LOBBYING_NEFAIT)
cartes_mur = "".join(
    f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in MURAILLE)
faq_pratique_html = "".join(
    f'<details><summary>{q}</summary><p class="rep">{r}</p></details>'
    for q, r in FAQ_PRATIQUE)

lobbying = f'''<main>
{bande("The practice",
       "Advocacy, <span class=\"di\">declared</span>.",
       "Putting a client&rsquo;s position to the people who take a public "
       "decision &mdash; inside their procedure, on the record, and never "
       "under somebody else&rsquo;s name.")}

<section id="does"><div class="wrap">
  <div class="filet"></div>
  {titre_section("Government relations", "What the practice does",
                 "Ordinary work, done in the open. Everything here assumes a "
                 "registration already exists for the mandate it belongs to.")}
  <div class="grid g3">{cartes_lob}</div>
</div></section>

<section id="never"><div class="wrap">
  <div class="filet"></div>
  {titre_section("Refusals", "What the practice will not do",
                 "A lobbying firm is described by its refusals, because every "
                 "firm advertises the same services. These are not "
                 "aspirations; a mandate that requires any of them is "
                 "declined.")}
  <ol class="refus">{refus_lob}</ol>
</div></section>

<section id="wall"><div class="wrap">
  <div class="filet"></div>
  {titre_section("Governance", "The wall between the movement and the practice",
                 "The movement publishes positions in its own name. The "
                 "practice speaks for clients, in theirs. Everything on this "
                 "site depends on those two things never becoming one.")}
  <figure class="figure">
    <img src="assets/wall.svg" alt="Two separate groups of four, each linked
         only within itself, divided by a line that nothing crosses."
         width="1400" height="440" loading="lazy">
    <figcaption>Two bodies of work, each connected inside itself, and a line
    that nothing crosses. The figure has no bridge because a bridge is exactly
    what is being ruled out. Whether the wall runs between two legal persons or
    inside one is <span class="tbd">To be decided</span>; the rules below hold
    either way.</figcaption>
  </figure>
  <div class="grid g3 mur">{cartes_mur}</div>
  <div class="avert">
    <h4>Why a movement and a firm cannot simply share a pocket</h4>
    <p>A movement that publishes political positions and a firm paid to
    advance its clients&rsquo; positions are treated as different things in law
    in most countries. Held in one pocket, <b>every position the movement
    publishes is read as bought</b> &mdash; and money from a foreign state to a
    political movement is, in several countries, prohibited outright rather
    than merely declared.</p>
    <p>This site therefore claims no structure at all. It states the rule the
    structure will have to satisfy, and leaves the legal form where it belongs:
    open, and listed as open.</p>
  </div>
</div></section>

<section id="register"><div class="wrap">
  <div class="filet"></div>
  {titre_section("Registration", "Declared before it is done",
                 "Putting a client&rsquo;s position to public decision-makers "
                 "is a registrable activity in most countries, and doing it "
                 "for a foreign principal is registrable again under a "
                 "stricter regime.")}
  <div class="grid g3">
    <div class="card"><h3>Registration of the practice</h3>
      <p><span class="tbd">To be decided</span></p>
      <p>Nowhere, today. No mandate is taken before the registration covering
      it exists, and this page will carry the entries as links rather than as
      claims.</p></div>
    <div class="card"><h3>Which registers apply</h3>
      <p><span class="tbd">To be decided</span></p>
      <p>It follows from where the practice is set up and from where each
      client sits. It is a legal question and it goes to counsel admitted
      there, not to a website.</p></div>
    <div class="card"><h3>Whether clients are published here</h3>
      <p><span class="tbd">To be decided</span></p>
      <p>Whether every mandate appears on this page, or only those a register
      already makes public. No client is named anywhere on this site
      today.</p></div>
  </div>
</div></section>

<section id="questions"><div class="wrap">
  <div class="filet"></div>
  {titre_section("Questions", "Questions and answers")}
  <div class="qa">{faq_pratique_html}</div>
</div></section>
</main>'''


# ---------------------------------------------------------------------------
# page 7 — le Cercle
# ---------------------------------------------------------------------------
cartes_cercle = "".join(
    f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in CERCLE_QUOI)

# Chaque format porte son etat REEL. Remplir cette grille de dates inventees
# donnerait une belle page et un mensonge verifiable en une minute.
cartes_activites = "".join(
    f'''<div class="card" id="a-{cle}"><h3>{nom}</h3><p>{d}</p>
    <p class="st"><span class="tbd">Not yet scheduled</span></p></div>'''
    for cle, nom, d in CERCLE_ACTIVITES)

cercle = f'''<main>
{bande("Membership",
       "The <span class=\"di\">Circle</span>.",
       "The people who carry the argument: who read the material before it is "
       "public, who argue with it, and who put it in front of others.")}

<section id="what"><div class="wrap">
  <div class="filet"></div>
  <img class="sceau" src="assets/seal.svg" alt="" width="480" height="480">
  {titre_section("The Circle", CERCLE,
                 "A membership, not an audience. What it is, what it is not, "
                 "and how one enters.")}
  <div class="grid g3">{cartes_cercle}</div>
</div></section>

<section id="activities"><div class="wrap">
  <div class="filet"></div>
  {titre_section("Activities", "What the Circle does",
                 "Eight formats. They are containers, and they are empty: "
                 "which ones actually run, how often and where is an open "
                 "decision.")}
  <div class="avert">
    <h4>This page announces nothing</h4>
    <p><b>No event is scheduled, and no date, place or speaker appears
    anywhere below.</b> Every format carries its real state, which is that
    nothing has been arranged yet.</p>
    <p>That is deliberate. A movement at its beginning that publishes a
    calendar it has not arranged loses the only asset it actually has, and it
    loses it the first time somebody turns up.</p>
  </div>
  <div class="grid g4 acts">{cartes_activites}</div>
</div></section>

<section id="portal-link"><div class="wrap">
  <div class="filet"></div>
  {titre_section("The portal", "Where members would sign in",
                 "Built as a mockup, and deliberately connected to nothing.")}
  <div class="grid g2">
    <div class="card"><h3>The member portal</h3>
      <p>A sign-in page and the member area behind it, laid out in full so the
      shape can be judged before anything is built.</p>
      <p>It authenticates nobody and stores nothing. What has to exist before
      it can hold a single member is listed there, in ten rows.</p></div>
    <div class="card"><h3>Why it is not connected</h3>
      <p>Membership of a political movement is sensitive information wherever
      it is held. A member list needs a body responsible for it and a country
      whose law applies before it takes a first name, not afterwards.</p>
      <p>Both are open decisions, and both are on
      <a href="movement.html#decisions">The movement</a>.</p></div>
  </div>
  <div class="actions">
    <a class="btn btn-plein" href="portal.html">Open the portal mockup</a>
    <a class="btn" href="portal-area.html">See the member area</a>
  </div>
</div></section>
</main>'''


# ---------------------------------------------------------------------------
# page 8 — le portail (maquette)
# ---------------------------------------------------------------------------
lignes_portail = "".join(
    f'<tr><td>{t}</td><td class="why">{d}</td>'
    f'<td><span class="tbd">To be decided</span></td></tr>'
    for t, d in PORTAIL_EXIGENCES)

portail = f'''<main>
{bande("Member portal",
       "Sign in to the <span class=\"di\">Circle</span>.",
       "A mockup. It authenticates nobody, stores nothing, and sends nothing "
       "anywhere.")}

<section id="signin"><div class="wrap">
  <div class="filet"></div>
  {titre_section("Sign in", "The door, drawn but not fitted")}
  <div class="duo">
    <div class="portal">
      <form class="form" onsubmit="return false;">
        <div class="champ">
          <label for="mid">Member reference</label>
          <input id="mid" name="mid" type="text" autocomplete="off"
                 placeholder="The reference on your admission notice">
        </div>
        <div class="champ">
          <label for="pw">Passphrase</label>
          <input id="pw" name="pw" type="password" autocomplete="off"
                 placeholder="Nothing typed here goes anywhere">
        </div>
        <button class="btn btn-plein" type="submit" disabled>Disabled in this mockup</button>
      </form>
      <div class="actions">
        <a class="btn" href="portal-area.html">See the member area anyway</a>
      </div>
    </div>
    <div>
      <div class="avert" style="margin-top:0">
        <h4>What this form does</h4>
        <p><b>Nothing.</b> There is no address behind it, no database, no
        script and no third-party service. The button is disabled, the form has
        no destination, and the page loads nothing from anywhere.</p>
        <p>The field asks for a <b>member reference rather than a name or an
        address</b>. That is not decoration: a sign-in page that accepts an
        email address turns every failed attempt into a statement about who is
        and is not a member of a political movement.</p>
      </div>
      <div class="avert">
        <h4>Why it is not connected yet</h4>
        <p>Membership of a political movement is sensitive information
        wherever it is held. Connecting this form would create a list of the
        members of a political movement with <b>nobody in law responsible for
        it</b> and no country whose rules apply to it.</p>
        <p>That is not a detail to sort out after launch. It is the thing that
        has to exist first.</p>
      </div>
    </div>
  </div>
</div></section>

<section id="before"><div class="wrap">
  <div class="filet"></div>
  {titre_section("Requirements", "What has to exist before it can hold one name",
                 "Ten rows. This is not a feature list &mdash; it is what is "
                 "missing, and why the portal delivered today authenticates "
                 "nobody.")}
  <table class="tbl">
    <thead><tr><th>Requirement</th><th>Why it comes first</th><th>Status</th></tr></thead>
    <tbody>{lignes_portail}</tbody>
  </table>
  <div class="avert">
    <h4>The honest order of work</h4>
    <p>Building the login first and the responsibilities afterwards is the
    usual order, and it is the wrong one. The code here is the small part; the
    rows above are the part that decides whether the code may run at
    all.</p>
    <p>Answer the first two rows &mdash; a responsible body and a country
    &mdash; and the rest becomes ordinary engineering that I can build
    quickly.</p>
  </div>
</div></section>
</main>'''


# ---------------------------------------------------------------------------
# page 9 — l'espace membre (apercu statique)
# ---------------------------------------------------------------------------
# L'apercu montre la DISPOSITION, pas un contenu. Chaque element porte son etat
# reel. Un espace membre rempli de fausses entrees ferait une belle capture
# d'ecran et serait faux des la premiere question du client.
fil_activites = "".join(
    f'''<div class="it"><h4>{nom}</h4><p>{d}</p>
    <p><span class="tbd">Not yet scheduled</span></p></div>'''
    for _cle, nom, d in CERCLE_ACTIVITES)

espace = f'''<main>
{bande("Member area",
       "Inside the <span class=\"di\">Circle</span>.",
       "A static preview. There is no session, no account and no member data "
       "on this page &mdash; it shows the shape, so the shape can be judged "
       "before anything is built.")}

<section id="area"><div class="wrap">
  <div class="filet"></div>
  {titre_section("Preview", "The member area, as it would be laid out")}
  <div class="avert">
    <h4>This is a drawing, not a session</h4>
    <p>You are not signed in, and nothing here is protected. <b>No member
    exists, no activity is scheduled and no name appears.</b> Every panel shows
    its real state rather than a sample filled in to look busy.</p>
    <p>A preview populated with invented entries photographs better and is
    worthless: the first question anyone asks about it is which of it is
    real.</p>
  </div>
  <div class="parea">
    <aside>
      <div class="who">
        <b>Member</b>
        <span>No account exists</span>
      </div>
      <a href="#area" aria-current="page">Activities</a>
      <a href="#briefings">Briefings</a>
      <a href="#groups">Working groups</a>
      <a href="#directory">Directory</a>
      <a href="#account">Account</a>
    </aside>
    <div>
      <div class="feed">
        <div class="vide"><b>Activities.</b> Nothing is scheduled. The eight
        formats below are the containers the Circle would use; which of them
        run, how often and where is an open decision.</div>
        {fil_activites}
      </div>

      <div class="feed" id="briefings" style="margin-top:24px">
        <div class="vide"><b>Briefings.</b> None published. The movement&rsquo;s
        publication rhythm has not been decided, and no briefing is written
        until there is one to write.</div>
      </div>

      <div class="feed" id="groups" style="margin-top:24px">
        <div class="vide"><b>Working groups.</b> None open. One per principle
        is the intended shape; a group with no members and no output is a
        heading, not a group.</div>
      </div>

      <div class="feed" id="directory" style="margin-top:24px">
        <div class="vide"><b>Directory.</b> Deliberately not built. A list
        showing the members of a political movement to one another is the most
        sensitive object in this whole project, and it is the last thing that
        should be built, not the first.</div>
      </div>

      <div class="feed" id="account" style="margin-top:24px">
        <div class="vide"><b>Account.</b> No account exists. What a real one
        would require &mdash; and who would answer for it &mdash; is set out in
        ten rows on <a href="portal.html#before">the portal page</a>.</div>
      </div>
    </div>
  </div>
</div></section>
</main>'''


# ---------------------------------------------------------------------------
# page 10 — soutenir avant le lancement
# ---------------------------------------------------------------------------
# La seule page du site ou une erreur d'affichage coute de l'argent a un tiers,
# et de maniere irreversible. Elle est donc ecrite a l'envers des pages de dons
# habituelles : ce qu'on ne peut pas promettre est affiche AVANT le moyen de
# payer, et le cadre de l'adresse arrive apres les avertissements, pas avant.
#
# Elle n'invente rien, comme le reste du site. Aucun montant suggere, aucun
# objectif, aucun budget, aucun total deja recu, aucun donateur : le mouvement
# n'a publie aucun compte, et une page de dons qui chiffre ce qu'elle n'a pas
# mesure est le genre de faux qui se verifie en une minute.
def ligne_deux(titre, texte):
    return f"<li><b>{titre}</b> {texte}</li>"


def valeur_adresse():
    """Le contenu du cadre d'adresse, entoure de deux marqueurs.

    Les marqueurs <!--EQ_BTC--> et <!--/EQ_BTC--> ne changent pas un pixel du
    site statique : ce sont des commentaires HTML. Ils existent pour la version
    WordPress, ou le theme remplace ce qui se trouve ENTRE eux par la valeur
    d'une option d'administration.

    C'est ce qui garantit qu'il n'y a jamais qu'UN endroit ou l'adresse est
    ecrite : cette constante quand le site est statique, l'option quand il est
    en base. Une adresse recopiee dans le contenu d'une page serait une seconde
    source, et la seconde source est toujours celle qu'on oublie de corriger.
    """
    dedans = (f'<span class="adr">{E(ADRESSE_BTC)}</span>' if ADRESSE_BTC
              else '<span class="tbd">To be decided</span>')
    return f"<!--EQ_BTC-->{dedans}<!--/EQ_BTC-->"


soutien_est = "".join(ligne_deux(t, x) for t, x in SOUTIEN_EST)
soutien_nest_pas = "".join(ligne_deux(t, x) for t, x in SOUTIEN_NEST_PAS)
soutien_ouvert = "".join(
    f'<div class="card"><h3>{t}</h3>'
    f'<p><span class="tbd">To be decided</span></p><p>{x}</p></div>'
    for t, x in SOUTIEN_OUVERT)

soutien = f'''<main>
<section><div class="wrap">
  <div class="filet"></div>
  {titre_section("Support", "Before the launch",
                 "Equilibrium has not launched. This page explains what a "
                 "contribution to it can honestly be at this stage, and what "
                 "it cannot be.")}

  <p>A movement at its beginning has no legal form, no country and no account.
  There is a period before all three exist in which the only honest way to
  accept support is directly, and to say plainly what is being given and what
  is not being promised in return. That is what this page is.</p>

  <div class="avert">
    <h4>Read this before you send anything</h4>
    <p><b>A payment on this network cannot be reversed.</b> Not by the sender,
    not by the movement, not by anyone. There is no chargeback, no dispute
    procedure and no way to recover a transfer sent to the wrong address.</p>
    <p><b>The movement has no legal form and no country of registration yet.</b>
    Both are open decisions, and so is whether the movement accepts
    contributions at all and under which rules &mdash; the three of them are
    listed on <a href="movement.html#decisions">The movement</a>. Political
    funding is regulated in most countries. Anyone whose own country restricts
    political contributions, or contributions to a body abroad, should check
    that before sending rather than after.</p>
    <p><b>Nothing on this page collects anything about you.</b> There is no
    form, no account, no list and no third-party service. This page cannot
    tell who read it or who gave.</p>
  </div>
</div></section>

<section id="address"><div class="wrap">
  <div class="filet"></div>
  {titre_section("The address", "Where a contribution goes",
                 "One address, published in one place.")}

  <div class="don">
    <span class="lab">Wallet address</span>
    <p class="val">{valeur_adresse()}</p>
    <span class="reseau">{RESEAU_BTC}</span>
    <p class="note"><b>Check the address character by character</b> against
    what is shown here before you send. It is the only check a sender has, and
    there is nothing to be done afterwards if it was wrong.</p>
    <p class="note">Send only on the network named above. An asset sent from
    another chain to this address is destroyed, not returned.</p>
    <p class="note">If you find an address for Equilibrium anywhere other than
    this page, treat it as unverified until the movement publishes it here.</p>
  </div>
</div></section>

<section id="what"><div class="wrap">
  <div class="filet"></div>
  {titre_section("What it is", "A gift, and what it does not buy",
                 "The distinction matters more here than on any other page of "
                 "this site.")}
  <div class="deux soutien">
    <div class="oui"><h4>What a contribution is</h4><ul>{soutien_est}</ul></div>
    <div class="non"><h4>What it is not</h4><ul>{soutien_nest_pas}</ul></div>
  </div>
  <p style="margin-top:26px">The rule that keeps money away from what the
  movement publishes is not a promise made on this page. It is set out, with
  what it forbids, on <a href="lobbying.html#wall">Lobbying</a>.</p>
</div></section>

<section id="open"><div class="wrap">
  <div class="filet"></div>
  {titre_section("Open", "What cannot be answered yet",
                 "Six questions a giver is entitled to ask. None of them has "
                 "an answer today, and inventing one would be the fastest way "
                 "to deserve none of this.")}
  <div class="grid g3">{soutien_ouvert}</div>
</div></section>

<section id="other"><div class="wrap">
  <div class="filet"></div>
  {titre_section("Another way", "Support that costs nothing",
                 "The movement is an argument. Money is not the only thing "
                 "that carries one, and at this stage it is not the most "
                 "useful.")}
  <div class="grid g3">
    <div class="card"><h3>Read it and argue with it</h3>
      <p>The statement and the five principles are the whole of what the
      movement has published. Disagreement with them is worth more to it now
      than a transfer.</p></div>
    <div class="card"><h3>Carry it further</h3>
      <p>Putting the argument in front of people who have not seen it, and in
      languages it has not been written in, is work the movement cannot do
      alone.</p></div>
    <div class="card"><h3>Say who you are</h3>
      <p>The join page asks how you would like to take part. It is a mockup
      today, and it says so, but it shows what will be asked.</p></div>
  </div>
  <div class="actions">
    <a class="btn btn-plein" href="join.html">Go to Join</a>
    <a class="btn" href="movement.html#decisions">See the open decisions</a>
  </div>
</div></section>
</main>'''


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Un commentaire CSS mal ferme tue silencieusement toutes les regles qui le
    # suivent : la page s'affiche, rien n'indique l'erreur, et le correctif que
    # l'on croit avoir applique ne s'applique pas. Ce controle m'a deja coute
    # deux diagnostics faux sur un autre site de ce client.
    with open(os.path.join(RACINE, "assets", "site.css"), encoding="utf-8") as f:
        css = f.read()
    assert css.count("/*") == css.count("*/"), \
        "assets/site.css : commentaires desequilibres — les regles suivantes seraient ignorees"

    print("Equilibrium — pages")
    page("index.html", f"{MOUVEMENT} — Balance rather than domination",
         "Equilibrium is an independent global political movement built around the "
         "principle that lasting international stability requires balance rather "
         "than domination.", "statement", accueil)
    page("principles.html", f"Five core principles — {MOUVEMENT}",
         "Balance of power, sovereignty, diplomacy, economic freedom and long-term "
         "stability: each principle set out with what it means and what it does not "
         "mean.", "principles", principes)
    page("movement.html", f"The movement — {MOUVEMENT}",
         "What Equilibrium is, how it acts, the decisions that remain open, and "
         "answers to the questions the statement raises.", "movement", mouvement)
    page("join.html", f"Join — {MOUVEMENT}",
         "How to follow Equilibrium, and what has to be settled before the movement "
         "can accept a single name.", "join", rejoindre)
    page("support.html", f"Support — {MOUVEMENT}",
         "How Equilibrium can honestly accept support before it has a legal form, "
         "a country or an account: what a contribution is, what it does not buy, "
         "and the six questions that have no answer yet.", "support", soutien)
    page("services.html", f"Services — {MOUVEMENT}",
         "Diplomatic advisory and declared representation for entities and states: "
         "six lines of work, how an engagement runs, and what the practice will not "
         "do at any price.", "services", services)
    page("lobbying.html", f"Lobbying — {MOUVEMENT}",
         "Declared advocacy, the refusals that define it, and the wall that keeps a "
         "client from ever buying a position published by the movement.",
         "lobbying", lobbying)
    page("circle.html", f"{CERCLE} — {MOUVEMENT}",
         "The membership: what the Circle is, the eight formats of activity it would "
         "run, and the member portal. Nothing is scheduled.", "circle", cercle)
    page("portal.html", f"Member sign-in — {MOUVEMENT}",
         "A mockup of the Circle member portal. It authenticates nobody and stores "
         "nothing, and lists in ten rows what must exist before it can.",
         "portal", portail)
    page("portal-area.html", f"Member area — {MOUVEMENT}",
         "A static preview of the Circle member area. No session, no account and no "
         "member data: it shows the shape, not a sample.", "circle", espace)
    print("termine —", RACINE)
