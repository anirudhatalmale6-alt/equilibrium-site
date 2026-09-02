# -*- coding: utf-8 -*-
"""
Equilibrium — generation des visuels, en SVG, sans aucune dependance.

POURQUOI DU VECTORIEL GENERE, ET PAS DES IMAGES
  1. La seule image que possede le client est une capture d'ecran de 886 px de
     large ou son logo occupe 230 px. Agrandie a la taille d'un en-tete de
     page, elle est floue. Un vectoriel est net a toute taille, y compris sur
     un ecran a haute densite et sur une affiche.
  2. Un mouvement politique ne peut pas illustrer ses pages avec des photos
     dont il ne detient pas les droits, et il ne peut surtout pas illustrer un
     propos sur l'ordre international avec des photos de lieux, de foules ou de
     personnes reelles : chaque photo dirait quelque chose que le texte ne dit
     pas. Des formes taillees ne disent rien de plus que ce qu'elles sont.
  3. Le poids. Les neuf visuels du site tiennent dans quelques dizaines de
     kilo-octets, sans requete externe, sans police distante, sans traceur.

LA TAILLE DIAMANT
  Une facette n'est pas un degrade. Ce qui fait lire « pierre taillee » plutot
  que « vitre depolie », c'est que chaque face est PLATE et que deux faces
  voisines ont un ecart de valeur net. Le maillage est donc un quadrillage
  jitte, coupe en triangles, chaque triangle rempli d'un aplat unique, sans
  aucun degrade a l'interieur d'une face. Les eclats speculaires sont quelques
  faces poussees au blanc, pas un halo.

GRAINES FIXES
  Chaque scene a sa graine. Regenerer ne bouge pas un pixel de ce qui a deja
  ete approuve : c'est ce qui permet de refaire tourner ce script pour ajouter
  une seule image sans avoir a re-valider les huit autres.
"""
import os
import random

_ICI = os.path.dirname(os.path.abspath(__file__))
# Dans le paquet livre, les scripts sont dans source/ et les pages un cran
# au-dessus. Sans ce reglage, relancer le script depuis le paquet ecrirait les
# SVG dans source/assets/, laissant les vrais visuels inchanges — une
# regeneration qui n'affiche aucune erreur et ne met rien a jour.
RACINE = os.path.dirname(_ICI) if os.path.basename(_ICI) == "source" else _ICI
SORTIE = os.path.join(RACINE, "assets")
os.makedirs(SORTIE, exist_ok=True)

# --- palette ---------------------------------------------------------------
# Trois points seulement : l'ombre de la pierre, sa teinte, l'eclat. Tout le
# reste est interpole. Une palette a trois points reste coherente quand on
# ajoute une scene ; une palette a douze couleurs choisies a la main ne le
# reste jamais.
OMBRE = (26, 37, 50)
TEINTE = (167, 214, 236)
ECLAT = (255, 255, 255)
VIOLET = (206, 192, 246)   # la refraction, employee sur une face sur sept


def melange(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def hexa(c):
    return "#%02X%02X%02X" % c


def face(t, refraction=False):
    """t dans [0,1] : 0 = face dans l'ombre, 1 = eclat."""
    base = melange(OMBRE, TEINTE, t / 0.55) if t < 0.55 else melange(TEINTE, ECLAT, (t - 0.55) / 0.45)
    if refraction:
        base = melange(base, VIOLET, 0.42)
    return hexa(base)


# --- maillage --------------------------------------------------------------
def facettes(x0, y0, x1, y1, cols, lignes, rng, clair=0.55, ampleur=0.34):
    """Quadrillage jitte coupe en triangles. Retourne une liste de polygones.

    `clair` est la valeur moyenne, `ampleur` l'ecart entre faces voisines.
    Deux triangles issus du meme quadrilatere recoivent volontairement deux
    valeurs eloignees : c'est l'arete entre eux qui fait la taille.
    """
    pas_x = (x1 - x0) / cols
    pas_y = (y1 - y0) / lignes
    noeuds = {}
    for i in range(cols + 1):
        for j in range(lignes + 1):
            gx = 0 if i in (0, cols) else rng.uniform(-0.34, 0.34) * pas_x
            gy = 0 if j in (0, lignes) else rng.uniform(-0.34, 0.34) * pas_y
            noeuds[(i, j)] = (x0 + i * pas_x + gx, y0 + j * pas_y + gy)

    sortie = []
    for i in range(cols):
        for j in range(lignes):
            a, b = noeuds[(i, j)], noeuds[(i + 1, j)]
            c, d = noeuds[(i + 1, j + 1)], noeuds[(i, j + 1)]
            # la lumiere vient du haut a gauche : la valeur decroit vers le bas
            # a droite, sinon la pierre est plate quel que soit le maillage
            incline = 1 - (i / max(1, cols - 1) * 0.5 + j / max(1, lignes - 1) * 0.5)
            for tri, biais in ((( a, b, c), +1), ((a, c, d), -1)):
                t = clair + (incline - 0.5) * 0.9 + biais * ampleur * rng.uniform(0.45, 1.0)
                t = max(0.03, min(0.99, t))
                sortie.append((tri, t, rng.random() < 0.14))
    return sortie


def polys(liste):
    return "".join(
        '<polygon points="%s" fill="%s"/>' % (
            " ".join("%.1f,%.1f" % p for p in tri), face(t, r))
        for tri, t, r in liste)


# --- la lettre E -----------------------------------------------------------
# Un E a empattements pleins, dessine en coordonnees 0..100. Le trace suit
# celui de la capture : barres epaisses, contre-formes courtes, aucun contraste
# de graisse a l'interieur d'un fut.
E_POINTS = [(14, 8), (86, 8), (86, 21), (52, 21), (52, 43.5), (74, 43.5),
            (74, 56.5), (52, 56.5), (52, 79), (86, 79), (86, 92), (14, 92),
            (14, 79), (34, 79), (34, 21), (14, 21)]
E_TRACE = " ".join("%.1f,%.1f" % p for p in E_POINTS)


def lettre(nom, taille, cols, lignes, graine, trait=1.15, clair=0.58, ampleur=0.30,
           dossier=None):
    rng = random.Random(graine)
    tris = facettes(14, 8, 86, 92, cols, lignes, rng, clair=clair, ampleur=ampleur)
    cid = "cE%d" % graine
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="{taille}" height="{taille}" role="img" aria-label="Equilibrium">
<defs><clipPath id="{cid}"><polygon points="{E_TRACE}"/></clipPath></defs>
<g clip-path="url(#{cid})">{polys(tris)}</g>
<polygon points="{E_TRACE}" fill="none" stroke="#FFFFFF" stroke-opacity=".55" stroke-width="{trait}" stroke-linejoin="miter"/>
</svg>'''
    ecrire(nom, svg, dossier)


# --- gemmes des principes --------------------------------------------------
FORMES = {
    # equilibre : un losange large, symetrique sur l'axe horizontal
    "balance":    [(40, 240), (240, 108), (440, 240), (240, 372)],
    # souverainete : un ecu, large en haut, pointe en bas
    "sovereignty": [(240, 62), (404, 176), (330, 420), (150, 420), (76, 176)],
    # diplomatie : deux moities qui se rejoignent sur une couture verticale
    "diplomacy":  [(240, 60), (420, 170), (420, 310), (240, 420), (60, 310), (60, 170)],
    # liberte economique : une taille ouverte, plus large en haut qu'en bas
    "economy":    [(56, 116), (424, 116), (330, 414), (150, 414)],
    # stabilite : une taille emeraude, a gradins, la plus statique des cinq
    "stability":  [(182, 58), (298, 58), (392, 152), (392, 328), (298, 422),
                   (182, 422), (88, 328), (88, 152)],
}


def gemme(cle, graine):
    pts = FORMES[cle]
    trace = " ".join("%d,%d" % p for p in pts)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    rng = random.Random(graine)
    tris = facettes(min(xs), min(ys), max(xs), max(ys), 6, 6, rng, clair=0.54, ampleur=0.32)
    cid = "cg" + cle
    couture = ""
    if cle == "diplomacy":
        # la couture est le sujet de la forme, pas une decoration : deux blocs
        # distincts qui tiennent ensemble par leur arete commune
        couture = ('<line x1="240" y1="60" x2="240" y2="420" stroke="#FFFFFF" '
                   'stroke-opacity=".92" stroke-width="9"/>')
    if cle == "stability":
        # gradins : trois aretes horizontales, la lecture d'une taille emeraude
        couture = "".join(
            f'<line x1="{88 + 26}" y1="{y}" x2="{392 - 26}" y2="{y}" '
            f'stroke="#FFFFFF" stroke-opacity=".78" stroke-width="5"/>'
            for y in (150, 240, 330))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 480" width="480" height="480" role="img" aria-hidden="true">
<defs><clipPath id="{cid}"><polygon points="{trace}"/></clipPath></defs>
<g clip-path="url(#{cid})">{polys(tris)}{couture}</g>
<polygon points="{trace}" fill="none" stroke="#FFFFFF" stroke-opacity=".62" stroke-width="2.2" stroke-linejoin="miter"/>
</svg>'''
    ecrire("p-%s.svg" % cle, svg)


# --- fond de banniere ------------------------------------------------------
def banniere(nom, graine, largeur=1800, hauteur=900):
    """Le fond du hero.

    Contrainte de conception : le titre se pose DESSUS. Le fond doit donc
    rester sombre la ou le texte tombe, c'est-a-dire a gauche. La pierre est
    poussee a droite et le voile la recouvre a gauche. Ce n'est pas un reglage
    esthetique, c'est ce qui rend le titre lisible, et la lisibilite est
    mesuree dans la suite de verification.
    """
    rng = random.Random(graine)
    cx, cy, r = largeur * 0.775, hauteur * 0.5, hauteur * 0.415
    pierre = [(cx, cy - r), (cx + r * 0.80, cy - r * 0.34), (cx + r * 0.62, cy + r * 0.66),
              (cx, cy + r), (cx - r * 0.62, cy + r * 0.66), (cx - r * 0.80, cy - r * 0.34)]
    trace = " ".join("%.0f,%.0f" % p for p in pierre)
    xs = [p[0] for p in pierre]
    ys = [p[1] for p in pierre]
    # une pierre a 0.40 sur fond noir se lit comme un caillou gris : la valeur
    # moyenne du hero est plus haute que celle des gemmes, parce qu'elle est
    # vue de loin et a travers le voile.
    tris = facettes(min(xs), min(ys), max(xs), max(ys), 7, 7, rng, clair=0.58, ampleur=0.32)

    # caustiques : deux fuseaux tres pales, la lumiere que la pierre renvoie
    caust = ""
    for k in range(3):
        y = hauteur * (0.18 + 0.3 * k) + rng.uniform(-40, 40)
        caust += (f'<path d="M{largeur} {y:.0f} L{largeur * 0.22:.0f} {y + rng.uniform(-90, 90):.0f}" '
                  f'stroke="#BFE9FF" stroke-opacity="0.075" stroke-width="{rng.uniform(6, 22):.1f}"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largeur} {hauteur}" width="{largeur}" height="{hauteur}" role="img" aria-hidden="true">
<defs>
  <clipPath id="cb{graine}"><polygon points="{trace}"/></clipPath>
  <linearGradient id="voile{graine}" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#07080A" stop-opacity="1"/>
    <stop offset="0.46" stop-color="#07080A" stop-opacity="0.96"/>
    <stop offset="0.64" stop-color="#07080A" stop-opacity="0.55"/>
    <stop offset="0.82" stop-color="#07080A" stop-opacity="0.06"/>
    <stop offset="1" stop-color="#07080A" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect width="{largeur}" height="{hauteur}" fill="#07080A"/>
{caust}
<g clip-path="url(#cb{graine})">{polys(tris)}</g>
<polygon points="{trace}" fill="none" stroke="#FFFFFF" stroke-opacity=".30" stroke-width="2"/>
<rect width="{largeur}" height="{hauteur}" fill="url(#voile{graine})"/>
</svg>'''
    ecrire(nom, svg)


# --- figure multipolaire ---------------------------------------------------
def multipolaire(nom, graine, n=7):
    """Sept centres de meme poids, reliés, et RIEN au milieu.

    Le vide central est le sujet. Une figure a moyeu dirait exactement le
    contraire du texte qu'elle illustre. Aucun noeud n'est nomme, aucune carte
    n'est dessinee : rattacher ces points a des pays reels serait leur preter
    une position que le mouvement n'a pas prise.
    """
    rng = random.Random(graine)
    # 1400x560 et non 1400x700 : a la premiere version l'anneau occupait le
    # tiers central et la figure etait surtout du vide. Une figure qui doit
    # dire « sept centres et rien au milieu » doit remplir son cadre, sinon le
    # vide qu'on lit est celui des marges, pas celui du centre.
    L, H = 1400, 560
    cx, cy = L / 2, H / 2
    import math
    noeuds = []
    for k in range(n):
        a = -math.pi / 2 + 2 * math.pi * k / n
        rx, ry = 560 + rng.uniform(-26, 26), 205 + rng.uniform(-16, 16)
        noeuds.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))

    liens = ""
    for i in range(n):
        for j in range(i + 1, n):
            liens += ('<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke="#BFE9FF" '
                      'stroke-opacity="0.20" stroke-width="1.2"/>'
                      % (noeuds[i][0], noeuds[i][1], noeuds[j][0], noeuds[j][1]))

    gemmes = ""
    for k, (x, y) in enumerate(noeuds):
        t = 40
        pts = [(x, y - t), (x + t * 0.85, y), (x, y + t), (x - t * 0.85, y)]
        tr = " ".join("%.0f,%.0f" % p for p in pts)
        cid = "cm%d_%d" % (graine, k)
        sub = facettes(x - t, y - t, x + t, y + t, 3, 3, random.Random(graine + k), clair=0.6, ampleur=0.3)
        gemmes += (f'<defs><clipPath id="{cid}"><polygon points="{tr}"/></clipPath></defs>'
                   f'<g clip-path="url(#{cid})">{polys(sub)}</g>'
                   f'<polygon points="{tr}" fill="none" stroke="#FFFFFF" stroke-opacity=".6" stroke-width="1.6"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {L} {H}" width="{L}" height="{H}" role="img" aria-label="Seven centres of decision of equal weight, linked to one another, with no centre.">
<rect width="{L}" height="{H}" fill="#07080A"/>
{liens}{gemmes}
</svg>'''
    ecrire(nom, svg)


# --- banniere de la pratique ------------------------------------------------
def banniere_deux(nom, graine, largeur=1800, hauteur=520):
    """Le bandeau des pages de la pratique : DEUX pierres, pas une.

    Le hero du mouvement porte une pierre : un propos, tenu par un. Les pages
    de la pratique en portent deux, de tailles inegales et separees par un
    vide : deux parties qui se font face. Rien ne les relie graphiquement,
    parce que ce que vend le cabinet est precisement le canal qui n'existe pas
    encore.

    Meme contrainte que la banniere du mouvement : le titre se pose a gauche,
    donc la moitie gauche reste noire, et la lisibilite est mesuree.
    """
    rng = random.Random(graine)
    stones = ""
    contours = ""
    # la grande a droite, la petite plus a gauche et plus basse ; l'ecart
    # entre les deux est le sujet
    # Premiere version : la petite pierre etait posee a 0,635 de la largeur,
    # c'est-a-dire en plein dans la rampe du voile, qui vaut encore 0,55
    # d'opacite a cet endroit. Elle sortait grise et morte a cote de l'autre.
    # Le probleme n'etait pas sa valeur — elle etait deja plus claire que la
    # grande — mais l'endroit ou je l'avais posee. Les deux pierres sont
    # maintenant apres la rampe.
    for k, (fx, fy, fr) in enumerate(((0.865, 0.46, 0.40), (0.695, 0.63, 0.215))):
        cx, cy, r = largeur * fx, hauteur * fy, hauteur * fr
        pts = [(cx, cy - r), (cx + r * 0.80, cy - r * 0.34), (cx + r * 0.62, cy + r * 0.66),
               (cx, cy + r), (cx - r * 0.62, cy + r * 0.66), (cx - r * 0.80, cy - r * 0.34)]
        trace = " ".join("%.0f,%.0f" % p for p in pts)
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        # la petite pierre est plus claire : vue comme plus proche, et sans
        # elle l'oeil ne lit qu'une pierre et un accident sombre
        tris = facettes(min(xs), min(ys), max(xs), max(ys), 6, 6,
                        random.Random(graine + k * 7),
                        clair=0.56 + 0.10 * k, ampleur=0.32)
        cid = "cd%d_%d" % (graine, k)
        stones += (f'<defs><clipPath id="{cid}"><polygon points="{trace}"/></clipPath></defs>'
                   f'<g clip-path="url(#{cid})">{polys(tris)}</g>')
        contours += (f'<polygon points="{trace}" fill="none" stroke="#FFFFFF" '
                     f'stroke-opacity=".30" stroke-width="2"/>')

    caust = ""
    for k in range(3):
        y = hauteur * (0.2 + 0.28 * k) + rng.uniform(-30, 30)
        caust += (f'<path d="M{largeur} {y:.0f} L{largeur * 0.28:.0f} {y + rng.uniform(-70, 70):.0f}" '
                  f'stroke="#BFE9FF" stroke-opacity="0.07" stroke-width="{rng.uniform(5, 18):.1f}"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largeur} {hauteur}" width="{largeur}" height="{hauteur}" role="img" aria-hidden="true">
<defs>
  <linearGradient id="vd{graine}" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#07080A" stop-opacity="1"/>
    <stop offset="0.42" stop-color="#07080A" stop-opacity="0.96"/>
    <stop offset="0.56" stop-color="#07080A" stop-opacity="0.52"/>
    <stop offset="0.70" stop-color="#07080A" stop-opacity="0.07"/>
    <stop offset="1" stop-color="#07080A" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect width="{largeur}" height="{hauteur}" fill="#07080A"/>
{caust}{stones}{contours}
<rect width="{largeur}" height="{hauteur}" fill="url(#vd{graine})"/>
</svg>'''
    ecrire(nom, svg)


# --- sceau du Cercle --------------------------------------------------------
def sceau(nom, graine, taille=480):
    """Un anneau octogonal taille. Le sceau du Cercle.

    Un anneau et non un disque : le Cercle est ce qui entoure le propos, pas
    le propos. Le vide au milieu est le meme argument que la figure
    multipolaire — rien n'occupe le centre.
    """
    import math
    rng = random.Random(graine)
    c = taille / 2

    def octo(r):
        return [(c + r * math.cos(math.pi / 8 + 2 * math.pi * k / 8),
                 c + r * math.sin(math.pi / 8 + 2 * math.pi * k / 8)) for k in range(8)]

    ext, inte = octo(taille * 0.46), octo(taille * 0.30)
    d = ("M" + " L".join("%.1f,%.1f" % p for p in ext) + " Z "
         "M" + " L".join("%.1f,%.1f" % p for p in inte) + " Z")
    tris = facettes(c - taille * 0.46, c - taille * 0.46,
                    c + taille * 0.46, c + taille * 0.46, 8, 8, rng,
                    clair=0.58, ampleur=0.30)
    cid = "cs%d" % graine
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {taille} {taille}" width="{taille}" height="{taille}" role="img" aria-hidden="true">
<defs><clipPath id="{cid}" clip-rule="evenodd"><path d="{d}" clip-rule="evenodd"/></clipPath></defs>
<g clip-path="url(#{cid})">{polys(tris)}</g>
<path d="{d}" fill="none" fill-rule="evenodd" stroke="#FFFFFF" stroke-opacity=".55" stroke-width="2" stroke-linejoin="miter"/>
</svg>'''
    ecrire(nom, svg)


# --- la muraille ------------------------------------------------------------
def muraille(nom, graine):
    """Deux groupes, une separation, AUCUN lien qui la traverse.

    La figure de gouvernance de la page lobbying. Elle dit une seule chose, et
    elle doit la dire sans legende : a gauche le mouvement et ses positions, a
    droite le cabinet et ses mandats, et rien ne passe. Une figure ou un seul
    trait traverserait dirait le contraire du texte qu'elle illustre — c'est la
    meme discipline que le vide au centre de la figure multipolaire.
    """
    import math
    # 1400x440 et non 1400x520 : a la premiere version les deux grappes
    # occupaient la bande centrale et la figure etait surtout de la marge
    # haute et basse. Une figure qui doit dire « deux groupes et une
    # separation » doit remplir son cadre, sinon ce qu'on lit d'abord est le
    # vide autour.
    L, H = 1400, 440
    rng = random.Random(graine)
    groupes = []
    for k, cx in enumerate((L * 0.245, L * 0.755)):
        pts = []
        for i in range(4):
            a = -math.pi / 2 + 2 * math.pi * i / 4
            pts.append((cx + 182 * math.cos(a) + rng.uniform(-14, 14),
                        H / 2 + 132 * math.sin(a) + rng.uniform(-12, 12)))
        groupes.append(pts)

    liens = ""
    for pts in groupes:
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                liens += ('<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke="#BFE9FF" '
                          'stroke-opacity="0.22" stroke-width="1.2"/>'
                          % (pts[i][0], pts[i][1], pts[j][0], pts[j][1]))

    gemmes = ""
    for g, pts in enumerate(groupes):
        for k, (x, y) in enumerate(pts):
            t = 34
            p = [(x, y - t), (x + t * 0.85, y), (x, y + t), (x - t * 0.85, y)]
            tr = " ".join("%.0f,%.0f" % q for q in p)
            cid = "cw%d_%d_%d" % (graine, g, k)
            sub = facettes(x - t, y - t, x + t, y + t, 3, 3,
                           random.Random(graine + g * 11 + k), clair=0.60, ampleur=0.30)
            gemmes += (f'<defs><clipPath id="{cid}"><polygon points="{tr}"/></clipPath></defs>'
                       f'<g clip-path="url(#{cid})">{polys(sub)}</g>'
                       f'<polygon points="{tr}" fill="none" stroke="#FFFFFF" stroke-opacity=".6" stroke-width="1.6"/>')

    mur = (f'<line x1="{L / 2:.0f}" y1="34" x2="{L / 2:.0f}" y2="{H - 34}" '
           f'stroke="#E7B98C" stroke-opacity="0.55" stroke-width="2" '
           f'stroke-dasharray="10 9"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {L} {H}" width="{L}" height="{H}" role="img" aria-label="Two separate groups of four, each linked only within itself, divided by a line that nothing crosses.">
<rect width="{L}" height="{H}" fill="#07080A"/>
{liens}{mur}{gemmes}
</svg>'''
    ecrire(nom, svg)


def ecrire(nom, svg, dossier=None):
    cible = dossier or SORTIE
    os.makedirs(cible, exist_ok=True)
    chemin = os.path.join(cible, nom)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(svg)
    print("  %-22s %6d o" % (nom, len(svg.encode("utf-8"))))


if __name__ == "__main__":
    print("Equilibrium — visuels")
    # le sigle : deux tailles, deux maillages. Le maillage fin du grand format
    # devient du bruit a 26 px ; le format d'en-tete a donc SIX faces, pas cent,
    # et une valeur moyenne bien plus claire — a cette taille, sur fond noir,
    # une lettre a 0.58 se lit comme une tache grise. Constate sur la planche
    # de controle a 26 px, corrige ici et remesure.
    lettre("mark.svg", 100, 2, 3, 101, trait=2.0, clair=0.80, ampleur=0.16)
    # Le grand sigle n'est pas un visuel de page : c'est un fichier de marque,
    # a fournir au client pour ses supports. Le laisser dans assets/ en ferait
    # un orphelin permanent, et un controle d'orphelins que l'on apprend a
    # ignorer ne sert plus a rien. Il part donc dans brand/, avec une copie du
    # petit format.
    MARQUE = os.path.join(RACINE, "brand")
    lettre("mark-lg.svg", 480, 7, 9, 111, trait=1.0, clair=0.62, ampleur=0.30, dossier=MARQUE)
    lettre("mark.svg", 100, 2, 3, 101, trait=2.0, clair=0.80, ampleur=0.16, dossier=MARQUE)
    banniere("hero.svg", 121)
    multipolaire("multipolar.svg", 131)
    # les trois visuels ajoutes avec la pratique et le Cercle. Graines
    # distinctes : regenerer ne bouge pas un pixel des cinq gemmes ni du hero
    # deja valides.
    banniere_deux("hero-practice.svg", 151)
    sceau("seal.svg", 161)
    muraille("wall.svg", 171)
    for k, (cle, *_rest) in enumerate([("balance",), ("sovereignty",), ("diplomacy",),
                                       ("economy",), ("stability",)]):
        gemme(cle, 141 + k * 10)
    print("termine —", SORTIE)
