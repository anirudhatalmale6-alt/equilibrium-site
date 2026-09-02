# -*- coding: utf-8 -*-
"""
Equilibrium — captures de controle.

Le cadrage d'une capture est une AFFIRMATION : « voici la section X ». Elle est
donc verifiee avant chaque declenchement, et le script s'arrete plutot que de
produire une image qui montre autre chose. Sur un autre site de ce client, un
defilement anime avait cadre six captures sur dix sur le meme hero, et le
script s'etait termine avec succes.

On defile par paliers avant chaque prise, comme un visiteur : un saut unique en
bas de page ne declenche jamais loading="lazy" sur ce qui se trouve au milieu.

Les captures font au plus 1440 px de large et la hauteur de la fenetre. Jamais
full_page : une page longue produit une image de plusieurs milliers de pixels
de haut, que rien n'affiche correctement.

Prealable : un serveur sur le port 8861 servant la racine du site.
    python3 -m http.server 8861 --directory ..
"""
import os
import sys
from playwright.sync_api import sync_playwright
BASE="http://127.0.0.1:8861/"
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)), "captures")
os.makedirs(OUT, exist_ok=True)
OUT+=os.sep

# (fichier, ancre, largeur, hauteur, nom)
SHOTS=[("index.html",None,1280,760,"eq-01-hero"),
       ("index.html","#statement",1280,760,"eq-02-statement"),
       ("index.html","#principles",1280,760,"eq-03-principles"),
       ("index.html","#not",1280,720,"eq-04-not"),
       ("principles.html","#balance",1280,760,"eq-05-principle"),
       ("principles.html","#stability",1280,760,"eq-06-stability"),
       ("movement.html","#multipolar",1280,760,"eq-07-multipolar"),
       ("movement.html","#decisions",1280,780,"eq-08-decisions"),
       ("movement.html","#questions",1280,700,"eq-09-questions"),
       ("join.html",None,1280,780,"eq-10-join"),
       ("index.html",None,390,780,"eq-11-mobile-hero"),
       ("principles.html","#diplomacy",390,780,"eq-12-mobile-principle"),
       ("movement.html","#decisions",390,780,"eq-13-mobile-decisions"),
       # la pratique, le Cercle et le portail
       ("index.html","#two",1280,760,"eq-14-two-things"),
       ("services.html",None,1280,720,"eq-15-services-band"),
       ("services.html","#line",1280,760,"eq-16-the-line"),
       ("services.html","#assessment",1280,760,"eq-17-service-line"),
       ("services.html","#fees",1280,720,"eq-18-fees"),
       ("lobbying.html","#never",1280,780,"eq-19-refusals"),
       ("lobbying.html","#wall",1280,780,"eq-20-wall"),
       ("lobbying.html","#register",1280,720,"eq-21-registration"),
       ("circle.html","#activities",1280,800,"eq-22-activities"),
       ("portal.html","#signin",1280,780,"eq-23-portal"),
       ("portal.html","#before",1280,780,"eq-24-portal-requires"),
       ("portal-area.html","#area",1280,800,"eq-25-member-area"),
       ("services.html",None,390,780,"eq-26-mobile-services"),
       ("circle.html","#activities",390,800,"eq-27-mobile-activities"),
       ("portal.html","#signin",390,800,"eq-28-mobile-portal")]

def defiler(pg):
    h=pg.evaluate("document.body.scrollHeight"); y=0
    while y<h+600:
        pg.evaluate(f"window.scrollTo({{top:{y},behavior:'instant'}})"); pg.wait_for_timeout(70)
        y+=600; h=pg.evaluate("document.body.scrollHeight")
    pg.evaluate("window.scrollTo({top:0,behavior:'instant'})"); pg.wait_for_timeout(120)

with sync_playwright() as pw:
    b=pw.chromium.launch()
    for f,anc,w,h,nom in SHOTS:
        ctx=b.new_context(viewport={"width":w,"height":h},reduced_motion="reduce")
        pg=ctx.new_page(); pg.goto(BASE+f,wait_until="networkidle"); defiler(pg)
        if anc:
            pg.evaluate(f"""()=>{{const e=document.querySelector({anc!r});
                window.scrollTo({{top:e.getBoundingClientRect().top+window.scrollY-72,behavior:'instant'}});}}""")
            pg.wait_for_timeout(280)
            # le cadrage est une affirmation : on la verifie avant de declencher
            ok=pg.evaluate(f"""()=>{{const r=document.querySelector({anc!r}).getBoundingClientRect();
                return r.top>-160 && r.top<window.innerHeight*0.6;}}""")
            if not ok: print("  CADRAGE RATE", nom); sys.exit(2)
        pg.screenshot(path=OUT+nom+".png"); ctx.close()
        print("  ",nom)
    b.close()
