# -*- coding: utf-8 -*-
"""
Equilibrium — contenu du site, et raison de ce qui est volontairement vide.

CE QUE LE CLIENT A DONNE
  1. le nom : Equilibrium ;
  2. la direction visuelle : « sur fond noir et touche de diamant » ;
  3. une capture de son compte TikTok @equilibrium0392, dont le logo est un E
     serif taille en diamant sur pastille noire, et dont la bio dit :
     « Global political & diplomatic movement. Restoring balance through
       diplomacy, sovereignty, economic cooperation & strategic stability. » ;
  4. six paragraphes de texte fondateur, en anglais, reproduits ci-dessous
     MOT POUR MOT dans DECLARATION.

CE QU'IL N'A PAS DONNE, ET QUE JE N'INVENTE DONC PAS
  Aucun fait sur le mouvement lui-meme : date de fondation, nombre de membres,
  pays d'implantation, forme juridique, dirigeants, financement, soutiens,
  couverture de presse, partenaires. Rien de tout cela n'existe sur le site.
  Les emplacements sont la, marques « To be decided », et se remplissent en
  une minute le jour ou il me donne les valeurs.

  La raison n'est pas de la prudence de principe. Un mouvement politique qui
  affiche un chiffre invente perd toute credibilite le jour ou quelqu'un le
  verifie, et sur ce terrain-la quelqu'un verifie toujours. Le cout d'un blanc
  assume est nul ; celui d'un faux est definitif.

  Sa capture indique 3 abonnes et 13 mentions J'aime. C'est un mouvement qui
  demarre. Aucun chiffre d'audience n'apparait donc nulle part : ni celui-la,
  qui le dessert, ni un autre, qui serait faux.

CE QUE JE N'ECRIS PAS NON PLUS
  Aucune position pour ou contre un Etat, un gouvernement, un parti, une
  organisation ou un conflit reels. Aucun nom propre de pays dans le propos.
  Son texte est volontairement general — « no single power, bloc, or ideology » —
  et le rendre concret, ce serait lui faire dire ce qu'il n'a pas dit, sur le
  sujet ou cela coute le plus cher. S'il veut du concret, cela viendra de lui
  par ecrit.

DEUX REGISTRES, ET LA PAGE LE DIT
  DECLARATION est sa parole, citee. Tout le reste est ma redaction : une
  explicitation de ses cinq principes, ecrite a partir de son seul texte. La
  page distingue les deux explicitement, parce qu'un lecteur a le droit de
  savoir ce que le mouvement a dit et ce qu'un redacteur en a tire.

LA COLONNE « WHAT IT DOES NOT MEAN »
  Chaque principe porte ce que le principe ne dit pas. C'est la seule facon
  d'etoffer un texte abstrait sans inventer de programme : je delimite au lieu
  d'ajouter. Un mouvement qui n'enonce que des principes generaux se fait lire
  comme ce que le lecteur y projette ; ecrire les bornes est ce qui le rend
  lisible, et c'est aussi ce qui protege le client des lectures qu'il ne veut
  pas.
"""

MOUVEMENT = "Equilibrium"

# La bio de son compte, mot pour mot. Sert de ligne de positionnement.
LIGNE = ("Global political &amp; diplomatic movement. Restoring balance through "
         "diplomacy, sovereignty, economic cooperation &amp; strategic stability.")

CHAINE = "@equilibrium0392"

# ---------------------------------------------------------------------------
# SA PAROLE. Six paragraphes, mot pour mot, sans coupe, sans reformulation,
# sans correction. Si une virgule bouge ici, ce n'est plus une citation.
# ---------------------------------------------------------------------------
DECLARATION = [
    "Equilibrium is an independent global political movement built around the "
    "principle that lasting international stability requires balance rather "
    "than domination.",

    "The movement advocates pragmatic diplomacy, economic cooperation, national "
    "sovereignty, open markets, and constructive relations between nations with "
    "different political and cultural systems. It rejects unnecessary "
    "geopolitical confrontation and seeks to encourage dialogue whenever "
    "competing interests can be reconciled peacefully.",

    "Equilibrium promotes a multipolar approach to international affairs in "
    "which no single power, bloc, or ideology should determine the future of "
    "the international system. Instead, states should be able to pursue their "
    "own development while participating in mutually beneficial economic, "
    "diplomatic, technological, and cultural partnerships.",

    "Its philosophy is based on five core principles: balance of power, "
    "sovereignty, diplomacy, economic freedom, and long-term stability.",

    "Equilibrium ultimately seeks to contribute to an international order where "
    "competition remains possible without becoming permanent confrontation—and "
    "where influence is built through economic strength, diplomacy, innovation, "
    "and cooperation rather than coercion.",
]

# ---------------------------------------------------------------------------
# LES CINQ PRINCIPES.
#
# Ordre : celui de sa propre phrase (« balance of power, sovereignty,
# diplomacy, economic freedom, and long-term stability »). Ce n'est pas un
# detail — un mouvement enonce ses principes dans un ordre, et le reordonner
# serait deja une interpretation.
#
# cle | nom | citation tiree de SON texte | ce que cela veut dire | ce que cela
# ne veut pas dire
#
# La citation de chaque principe vient de ses propres phrases : c'est ce qui
# rend l'explicitation verifiable ligne a ligne plutot que credible sur parole.
# ---------------------------------------------------------------------------
PRINCIPES = [
    ("balance", "Balance of power",
     "No single power, bloc, or ideology should determine the future of the "
     "international system.",
     [
         "Balance is a structure, not a sentiment. It holds when several centres "
         "of decision are able to act, not when one of them chooses to restrain "
         "itself. Restraint that depends on goodwill is not balance; it is "
         "permission.",
         "Competition between states is treated as normal and permanent. The "
         "question the movement asks is not how to end competition but how to "
         "keep it from hardening into confrontation.",
     ],
     [
         "It is not the claim that every state is the same, nor a verdict on any "
         "particular government. It is a position on how the system should be "
         "ordered, not a ranking of the states inside it.",
         "It is not neutrality on the substance of a given dispute. A movement "
         "can hold that no single power should set the terms and still hold a "
         "view on a specific question.",
     ]),

    ("sovereignty", "Sovereignty",
     "States should be able to pursue their own development.",
     [
         "Decisions about a country's internal development belong to that "
         "country. A development path is not something to be granted on "
         "condition that another state's model is adopted with it.",
         "Different political and cultural systems are treated as a fact to work "
         "with, not a problem to be corrected before relations can begin.",
     ],
     [
         "It is not isolation. The same sentence that asks for sovereignty asks "
         "for participation in economic, diplomatic, technological and cultural "
         "partnerships; the two are stated together and not as a trade-off.",
         "It is not release from an agreement a state has freely entered into. "
         "Sovereignty is what makes a commitment binding in the first place.",
     ]),

    ("diplomacy", "Diplomacy",
     "Dialogue whenever competing interests can be reconciled peacefully.",
     [
         "Talking is a method, not a reward. Channels stay open with those one "
         "disagrees with, because those are the only ones where disagreement can "
         "be worked on.",
         "Confrontation that serves no purpose is treated as a cost paid for "
         "nothing. The word in the statement is unnecessary, and it is doing "
         "work: it concedes that some confrontation is not.",
     ],
     [
         "It is not the claim that every dispute yields to conversation. The "
         "statement says whenever competing interests can be reconciled "
         "peacefully, which admits plainly that sometimes they cannot.",
         "It is not a preference for process over outcome. Dialogue that settles "
         "nothing is not the objective.",
     ]),

    ("economy", "Economic freedom",
     "Influence is built through economic strength, diplomacy, innovation, and "
     "cooperation rather than coercion.",
     [
         "Trade and investment are the ordinary channel between states, not a "
         "reward for alignment and not an instrument to be switched off to "
         "obtain a political result.",
         "Open markets are named in the statement alongside cooperation, which "
         "reads them as a way of binding interests together rather than as an "
         "economic doctrine on its own.",
     ],
     [
         "It is not a position on how any state should organise its own economy. "
         "That falls under sovereignty, and the two principles are held "
         "together.",
         "It is not the claim that markets settle political questions by "
         "themselves.",
     ]),

    ("stability", "Long-term stability",
     "Competition remains possible without becoming permanent confrontation.",
     [
         "The horizon is decades, not news cycles. Predictability has a value of "
         "its own: states that can anticipate each other take fewer irreversible "
         "decisions.",
         "Lasting stability is described in the statement as requiring balance. "
         "It is presented as the result of a structure, not of a mood or of an "
         "agreement between two capitals.",
     ],
     [
         "It is not the defence of the status quo. Stability here means the "
         "absence of rupture, not the absence of change.",
         "It is not a promise of calm. A balanced system can be tense; what it "
         "is meant to avoid is the tension becoming the permanent condition.",
     ]),
]

# ---------------------------------------------------------------------------
# CE QUE LE MOUVEMENT N'EST PAS.
#
# Le bloc le plus utile du site, et le plus rare. Un mouvement qui n'enonce
# que des principes generaux se fait lire comme ce que le lecteur y projette,
# et sur ce terrain les projections sont hostiles par defaut. Ecrire les bornes
# soi-meme coute quatre lignes ; les laisser ecrire par d'autres coute le
# mouvement.
#
# Chacune de ces bornes decoule de son texte ou de l'absence de fait dans son
# texte. Aucune n'ajoute de position.
# ---------------------------------------------------------------------------
NEST_PAS = [
    ("A political party",
     "Equilibrium is described in its own statement as a movement. It does not "
     "contest elections and it does not present candidates."),
    ("Aligned with any state or bloc",
     "The statement holds that no single power, bloc or ideology should "
     "determine the international system. That position is incompatible with "
     "acting on behalf of one."),
    ("A commentary channel on live events",
     "The five principles are general by design. Applying them to a particular "
     "dispute is a separate act, and one the movement makes deliberately when it "
     "chooses to, not automatically because something happened."),
    ("A claim of authority",
     "Nothing here is presented as expertise, mandate or representation. It is "
     "an argument, offered publicly, to be judged on whether it holds."),
]

# ---------------------------------------------------------------------------
# LES DECISIONS QUI NE M'APPARTIENNENT PAS.
#
# Troisieme vocabulaire du blanc delibere, apres « a verifier » (Amarimmo :
# la valeur existe, une autorite la publie, personne ne l'a verifiee a une
# date) et « a definir » (EdenFlor : decision commerciale non prise). Ici,
# « To be decided » : ce sont des decisions politiques et juridiques que seul
# le fondateur peut prendre, et dont plusieurs ont des consequences legales
# dans le pays ou il les prendra.
#
# Elles sont AFFICHEES sur le site, dans la page Movement, et non cachees dans
# un courriel. Un visiteur qui lit « forme juridique : a decider » comprend
# qu'il regarde un mouvement qui demarre. Un visiteur a qui l'on ne dit rien
# suppose qu'on lui cache quelque chose.
# ---------------------------------------------------------------------------
# Depuis que le client a ajoute la pratique et le Cercle, le tableau est
# GROUPE. Vingt-deux lignes a plat se lisent comme une liste de courses ; en
# trois groupes, elles se lisent comme ce qu'elles sont : trois chantiers dont
# le deuxieme ne peut pas commencer avant que le premier soit tranche.
DECISIONS = [
    ("The movement", [
        ("Legal form",
         "Association, non-profit, think tank, or no legal entity at all. "
         "Determines everything below."),
        ("Country of registration",
         "Sets which law applies to funding, to declarations and to the "
         "supporter list."),
        ("Membership",
         "Whether Equilibrium has members at all, or only readers and "
         "supporters. The two are not the same thing legally."),
        ("Funding",
         "Whether the movement accepts contributions, from whom, and under "
         "which country's rules on political financing."),
        ("Spokesperson",
         "Who speaks in the movement's name, and whether that person is named "
         "publicly."),
        ("Languages",
         "The statement is in English. A movement that argues for a multipolar "
         "world in one language only is arguing against itself."),
        ("Publication rhythm",
         "How often a position is published, and in what form."),
        ("Contact channel",
         "Which address receives what the join form collects, and who is "
         "responsible for it."),
    ]),

    ("The practice", [
        ("Separation from the movement",
         "Whether the practice is a separate legal person from the movement, "
         "and which of the two signs a client engagement. Every other row in "
         "this group depends on the answer."),
        ("Registration as a representative",
         "Putting a client's position to public decision-makers is a "
         "registrable activity in most countries, and doing it for a foreign "
         "principal is registrable again under a stricter regime. Which "
         "registers apply follows from where the practice sits and from where "
         "each client sits."),
        ("Client acceptance",
         "Which entities and which states the practice will act for, and which "
         "it will refuse. This is the policy that decides what the name comes "
         "to mean, and it cannot be written by anyone but the founder."),
        ("Publication of clients",
         "Whether every mandate is published here, or only those a register "
         "already makes public."),
        ("Positions and mandates",
         "Whether the movement may publish on a question where the practice "
         "holds a mandate, and what it says about the overlap when it does."),
        ("Fees",
         "How the practice is paid, and by whom. No figure appears on this "
         "site until this is decided."),
        ("Money between the two",
         "Whether the movement may receive anything from a client of the "
         "practice. In several countries this is settled by law rather than by "
         "preference."),
        ("Professional cover",
         "Insurance, a conflicts register, and who is responsible for keeping "
         "them accurate."),
    ]),

    ("The Circle", [
        ("What membership is",
         "A legal membership carrying rights, or a subscriber circle carrying "
         "none. Only one of the two creates obligations towards the members."),
        ("Admission and exit",
         "Who is admitted, by whom, and on what grounds a membership ends."),
        ("Contribution",
         "Whether members contribute, how much, and under which country's "
         "rules on political financing."),
        ("Member data",
         "Who holds the member list, in which country, and under whose "
         "responsibility. Membership of a political movement is sensitive "
         "wherever it is held."),
        ("The directory",
         "Whether members can see one another at all. A directory of the "
         "members of a political movement is the most sensitive object "
         "anywhere in this project."),
        ("Activities",
         "Which of the formats on the Circle page actually run, how often, and "
         "where. Nothing is scheduled and nothing is announced until this is "
         "answered."),
    ]),
]

# ---------------------------------------------------------------------------
# FAQ. Uniquement des questions auxquelles son texte permet de repondre, ou
# dont la reponse honnete est « pas encore decide ».
# ---------------------------------------------------------------------------
FAQ = [
    ("Is Equilibrium a political party?",
     "No. It is a movement: a body of argument, published in public. It does "
     "not contest elections and it presents no candidates."),
    ("Which country is it based in?",
     "That has not been decided, and the site says so rather than implying an "
     "answer. When it is decided it will be stated here plainly."),
    ("Is it aligned with a particular government?",
     "No. The central position of the statement is that no single power, bloc "
     "or ideology should determine the international system, which rules out "
     "acting for one."),
    ("What does multipolar mean here?",
     "That several centres of decision are able to act, and that the future of "
     "the international system is not settled by one of them. It is a statement "
     "about structure, not a preference for any particular set of powers."),
    ("Does the movement take a position on current conflicts?",
     "The five principles are general. A position on a specific dispute is a "
     "separate act and is published as such when the movement chooses to take "
     "one. Nothing on this page should be read as one."),
    ("Is balance the same as neutrality?",
     "No. Balance is a claim about how the system should be ordered. Neutrality "
     "is a refusal to hold a view on a particular question. One does not "
     "require the other."),
    ("How is the movement funded?",
     "That has not been decided. Political financing is regulated, and the "
     "rules depend on the country of registration, which is itself still open."),
    ("Can I join?",
     "The form on this site is a mockup and sends nothing anywhere. Before it "
     "can accept a single name there has to be an identified body receiving the "
     "data and a country whose law applies to it."),
    ("Who wrote the text on this site?",
     "The statement is the movement's own words, quoted without alteration. "
     "Everything else is draft copy written from that statement, for approval."),
]

# ===========================================================================
# LA PRATIQUE — services diplomatiques et lobbying.
#
# Deuxieme demande du client : « Equilibrium sell diplomatic services for
# entities and countries. It also act as a lobbying firm. »
#
# LE PROBLEME DE STRUCTURE, ECRIT ICI PARCE QU'IL COMMANDE TOUT LE RESTE
#   Un mouvement politique qui publie des positions et un cabinet paye pour
#   porter celles de ses clients ne sont pas la meme chose en droit dans la
#   quasi-totalite des pays. Si c'est la meme personne morale, chaque position
#   publiee par le mouvement se lit comme achetee ; et l'argent d'un Etat
#   etranger vers un mouvement politique est, dans plusieurs pays, interdit
#   tout court. Je ne tranche pas cela a sa place : je construis les deux sous
#   une meme marque, j'ECRIS la separation en public comme regle de
#   gouvernance, et la forme juridique reste une decision ouverte.
#
# CE QUE JE N'ECRIS NULLE PART
#   Qu'Equilibrium est enregistre, agree, accredite, mandate ou reconnu ou que
#   ce soit. Ce n'est pas encore vrai. Aucun tarif, aucun client, aucun pays,
#   aucun register nomme : quels registres s'appliquent depend du pays ou le
#   cabinet s'etablit et du pays de chaque client, et rien de tout cela n'est
#   decide. La liste des regimes a examiner avec un avocat est dans le README,
#   qui est ma note de travail pour lui — pas la parole du mouvement.
#
# LA LIGNE QUI COMPTE
#   La diplomatie entre Etats est conduite par les Etats. Un cabinet prive
#   conseille, prepare, reunit et porte ; il n'accredite personne et n'engage
#   personne. Cette phrase est sur la page, en clair, parce que c'est celle qui
#   separe une pratique serieuse d'une usurpation.
# ===========================================================================
PRATIQUE = [
    ("assessment", "Strategic assessment",
     ["Before anything is said to anyone: a written reading of the position. "
      "Who actually decides, what they are optimising for rather than what "
      "they announce, what is negotiable, what is not, and what doing nothing "
      "costs.",
      "Most engagements that fail were lost here. A party that opens a channel "
      "without knowing which of its own objectives it is willing to trade has "
      "already conceded the sequence."],
     ["A written assessment",
      "A map of who decides and of what moves them",
      "The options, each with what it costs"]),

    ("channel", "Channels and facilitation",
     ["Opening and holding a line between parties who are not talking, or not "
      "yet talking officially. Convening, hosting, carrying a position "
      "accurately in both directions, and keeping the existence of the channel "
      "proportionate to what it is for.",
      "Talking is a method, not a reward. The practice applies that where it "
      "is useful and charges for the work, not for the principle."],
     ["A channel, and the discipline to keep it quiet",
      "Accurate carriage of positions both ways",
      "A written record of what was said, for the client"]),

    ("engagement", "Bilateral and multilateral engagement",
     ["Preparation of delegations and of the sequence around them: what is "
      "raised first, what is held back, who is met before whom, what goes in "
      "writing and what does not.",
      "Sequencing is most of the outcome. A meeting obtained too early spends "
      "the only leverage the client had for obtaining it."],
     ["Briefing material",
      "A sequence, with the reasoning attached",
      "Follow-up in writing"]),

    ("economic", "Economic diplomacy and market access",
     ["Positioning a trade or investment interest as what it is — an interest "
      "— and building the case that meeting it serves the other side too. "
      "Identifying the public decisions standing between a client and a "
      "market, and who takes them.",
      "Influence built through economic strength and cooperation rather than "
      "coercion is the movement's own line. Commercially it is also the only "
      "argument that survives a change of government."],
     ["The case, written for the other side's reader",
      "The decisions, and the bodies that take them",
      "Where a declaration is required before the case is put"]),

    ("argument", "Public argument",
     ["Where a case is better made in the open than in a room: written "
      "positions, long-form argument, and the discipline of publishing under "
      "the name of whoever is paying rather than through an obliging third "
      "party.",
      "A case put through an intermediary that hides who is paying is worth "
      "less than the same case put openly, and costs far more the day it is "
      "found out."],
     ["Written positions, signed by whoever paid for them",
      "A publication plan",
      "No placement that conceals its source"]),

    ("representation", "Declared representation",
     ["Acting formally for a client before public decision-makers, on the "
      "record, in whichever register applies.",
      "This is the line carrying the most obligations and the fewest "
      "surprises. It is set out in full on the lobbying page, together with "
      "what the practice will not do."],
     ["A declared mandate",
      "A record of every approach made",
      "The register entry, linked in public"]),
]

# Les bornes de la pratique. Meme role que NEST_PAS pour le mouvement, et le
# meme raisonnement : ce qu'un cabinet de ce type ne dit pas de lui-meme, ses
# clients et ses adversaires le disent a sa place.
PRATIQUE_NEST_PAS = [
    ("A diplomatic mission",
     "Diplomatic relations between states are conducted by states. Equilibrium "
     "holds no accreditation, no diplomatic status and no official function of "
     "any kind, does not act as an organ of any state, and binds nobody."),
    ("Legal advice",
     "Where a question is legal — and registration, sanctions, competition and "
     "procurement questions are legal — it goes to counsel admitted where it "
     "arises. The practice says so rather than answering it."),
    ("A promise of outcome",
     "No engagement is written against a result obtained from a public "
     "authority, and no fee depends on one. A practice that prices itself on "
     "decisions it does not take is selling something it does not have."),
    ("Undisclosed representation",
     "Every mandate is declared wherever declaration applies. The practice "
     "does not take work whose usefulness depends on concealing who is paying "
     "for it."),
    ("A replacement for the client's own people",
     "The practice reads, prepares, opens and carries. It does not decide, and "
     "it does not sign."),
]

LOBBYING_FAIT = [
    ("Declared advocacy",
     "Putting a client's position to the people who take a public decision, "
     "inside their own procedure, on the record."),
    ("Monitoring",
     "Following the files that affect a client early enough that a position "
     "can still be put. Most of the value of this work sits in the calendar, "
     "not in the argument."),
    ("Evidence and drafting",
     "Submissions, consultation responses, and the material a decision-maker "
     "can actually use: what changes, for whom, and what it costs."),
    ("Coalitions, named as such",
     "Bringing together parties with a shared interest under their own names. "
     "Where several clients stand behind one position, the position says so."),
    ("The compliance itself",
     "The registration, the returns that follow it, and the internal record "
     "that makes those returns accurate."),
]

# La liste la plus utile de la page. Un cabinet de lobbying credible se decrit
# par ses refus, parce que tout le monde annonce les memes services.
LOBBYING_NEFAIT = [
    "Advocacy that hides who is paying for it, in any form, including material "
    "published under somebody else's name.",
    "Anything of value to a public official, to their family or to their "
    "staff. No exception, no threshold, no hospitality that would need "
    "explaining afterwards.",
    "Front organisations. A campaign presented as spontaneous public support "
    "while being paid for by a single interest is a deception practised on the "
    "decision-maker, whatever the trade calls it.",
    "Fees contingent on a public decision. What a contingency fee buys is not "
    "persuasion.",
    "Mandates that require the client's identity to be kept out of the "
    "register.",
    "Work on a question where the movement has published a position, unless "
    "the overlap is handled by the rule below and handled in public.",
]

# LA MURAILLE. Le bloc qui rend l'ensemble credible ou ne le rend pas.
MURAILLE = [
    ("Two voices, never one",
     "The movement publishes positions in its own name. The practice speaks "
     "for clients, in theirs. Nothing is published in both capacities, under "
     "one signature, in one document."),
    ("No position is for sale",
     "A client cannot commission, edit, delay or veto anything the movement "
     "publishes. This is the clause the whole structure exists to make "
     "credible, and it is worth nothing unless it is public — which is why it "
     "is written here rather than kept in an internal note."),
    ("The movement names no client",
     "Movement publications do not name clients of the practice, and client "
     "work is never presented as a movement position."),
    ("Overlap is declared, not quietly avoided",
     "Where the practice holds a mandate on a question the movement writes "
     "about, the overlap is disclosed. Whether the movement then publishes "
     "with the disclosure attached, or stays silent, is the founder's "
     "decision and is listed as open."),
    ("Money does not cross",
     "Whether the movement may receive anything at all from a client of the "
     "practice is a question of law before it is a question of policy, and in "
     "several countries the law answers it. Open until the country is chosen."),
    ("Everything declarable is declared",
     "Every mandate is entered in whichever register applies before the work "
     "begins, and the entries are linked from this site rather than left to be "
     "found."),
]

FAQ_PRATIQUE = [
    ("Is Equilibrium registered as a lobbyist?",
     "Not yet, and this site does not suggest otherwise. Which registers apply "
     "follows from the country where the practice is set up and from where "
     "each client sits, and neither has been decided. No mandate is taken "
     "before the registration covering it exists."),
    ("Is the practice the same body as the movement?",
     "That is an open decision, and it is the first row of the practice group "
     "in the table of open questions. The separation described on this page is "
     "the rule that holds whichever way it is answered."),
    ("Can a client obtain a position from the movement?",
     "No. A client cannot commission, edit, delay or veto anything the "
     "movement publishes. Everything else on this page depends on that clause "
     "being true, which is why it is published rather than kept internally."),
    ("Does the practice act for governments?",
     "Which entities and which states the practice will act for is an open "
     "decision, and it is the policy that will decide what the name comes to "
     "mean. A website does not answer it."),
    ("Does Equilibrium conduct diplomacy?",
     "No. Diplomatic relations between states are conducted by states. The "
     "practice advises, prepares, convenes and carries. It holds no "
     "accreditation and no official function, and nothing it does binds "
     "anyone."),
    ("What does an engagement cost?",
     "No figure appears anywhere on this site, because none has been set. How "
     "the practice is paid is an open decision, and a fee contingent on a "
     "public decision is excluded whatever the answer turns out to be."),
]

# ===========================================================================
# LE CERCLE — l'adhesion, ses activites, et le portail.
#
# « Equilibrium has a membership called equilibrium circle with a login portal
# and a list of activities. »
#
# CE QUE JE PEUX ECRIRE : les FORMATS d'activite. Ce sont des contenants, et
# ils decoulent de ce que fait un mouvement de ce type.
# CE QUE JE N'ECRIS PAS : un evenement. Aucune date, aucun lieu, aucun
# intervenant, aucune periodicite. Chaque format porte « Not yet scheduled »,
# et la page dit en toutes lettres qu'elle n'annonce rien. Un mouvement de
# trois abonnes qui affiche un calendrier invente perd le seul actif qu'il a.
# ===========================================================================
CERCLE = "Equilibrium Circle"

CERCLE_QUOI = [
    ("What the Circle is",
     "The people who carry the argument: who read the material before it is "
     "public, who argue with it, and who do the work of putting it in front of "
     "others."),
    ("What the Circle is not",
     "It is not an endorsement of any member, and it confers no representative "
     "capacity. No member speaks in the movement's name, and joining makes "
     "nobody a client of the practice."),
    ("How one enters",
     "By admission rather than by payment alone. Who admits, on what grounds, "
     "and whether there is a contribution at all are open decisions, listed as "
     "such."),
]

CERCLE_ACTIVITES = [
    ("briefings", "Briefings",
     "Written analysis circulated to members before it is public, where it is "
     "made public at all."),
    ("roundtables", "Roundtables",
     "Closed sessions under a non-attribution rule: what was said may be used, "
     "who said it may not."),
    ("groups", "Working groups",
     "One per principle, each producing written work rather than minutes."),
    ("assembly", "Assembly",
     "A general meeting of the Circle, and the only place a membership can "
     "hold anyone to account."),
    ("chapters", "Chapters",
     "Members organising where they are, under one common rule about what may "
     "be said in the movement's name."),
    ("delegations", "Delegations",
     "Visits and study missions arranged for members rather than for clients, "
     "and kept apart from the practice's mandates."),
    ("translation", "Translation",
     "Carrying the statement and the positions into other languages. A "
     "movement arguing for a multipolar world in one language is arguing "
     "against itself."),
    ("directory", "Directory",
     "Members able to find one another. The most sensitive thing anywhere in "
     "this project, and the one least likely to be built first."),
]

# Ce qu'il faut AVANT qu'un portail puisse detenir un seul nom. Le tableau
# n'est pas une liste de fonctionnalites : c'est ce qui manque, et pourquoi le
# portail livre aujourd'hui n'authentifie personne.
PORTAIL_EXIGENCES = [
    ("A responsible body",
     "Somebody in law has to hold the member list. Until the legal form "
     "exists, nobody does."),
    ("A country",
     "Which country's data law applies decides the rest of this table, "
     "including which rows are optional."),
    ("Hosting",
     "Where the member list physically sits, and whose jurisdiction that puts "
     "it under."),
    ("Encryption at rest",
     "Membership of a political movement is sensitive. A member list in a "
     "plain database is a leak waiting for an occasion."),
    ("Access control",
     "Who inside the movement may see the list, and a record of who looked."),
    ("Retention",
     "How long a former member stays in the file, and what happens to them "
     "when they leave."),
    ("Breach procedure",
     "Written before it is needed, because written afterwards it is useless."),
    ("Member rights",
     "Access, correction, erasure and objection, with somebody named to answer "
     "them."),
    ("An impact assessment",
     "Processing sensitive data at scale generally requires one before a "
     "single record is created."),
    ("Authentication",
     "Passwords hashed, sessions bounded, and a second factor for anyone able "
     "to see the whole list."),
]


# ---------------------------------------------------------------------------
# page 10 — soutenir avant le lancement
# ---------------------------------------------------------------------------
# L'ADRESSE. Elle est declaree ICI et nulle part ailleurs : la page de soutien
# la lit, et le theme WordPress la lit dans une option d'administration. Deux
# copies auraient derive, et sur une adresse de portefeuille une derive d'un
# caractere envoie l'argent chez un inconnu, sans recours.
#
# ELLE EST VIDE, ET CE N'EST PAS UN OUBLI. Le client a envoye une adresse
# Bitcoin par capture d'ecran. La capture est un post Instagram d'un TIERS
# (compte monarch.stories), et l'adresse figure dans la LEGENDE de ce post.
# Le controle que j'ai fait dit seulement ceci : la chaine est une adresse
# mainnet P2SH valide, somme de controle base58 verifiee. La validite ne dit
# RIEN du proprietaire — n'importe quelle adresse valide appartient a
# quelqu'un, et rien ne dit que ce quelqu'un est lui.
#
# Une adresse fausse publiee sur une page de dons n'est pas un defaut
# d'affichage : c'est de l'argent de donateurs envoye a un inconnu, de maniere
# irreversible, sous le nom du mouvement. Le cout d'un blanc est nul ; celui
# d'une erreur est definitif et retombe sur lui.
#
# Elle se remplit donc quand, et seulement quand, il confirme PAR ECRIT que le
# portefeuille est le sien, en recollant l'adresse dans un message. Tant
# qu'elle vaut "", la page affiche « To be decided » comme partout ailleurs et
# ne peut recevoir aucun paiement.
ADRESSE_BTC = ""

# Le reseau de l'adresse ci-dessus. Ecrit en toutes lettres sur la page :
# envoyer un actif d'une autre chaine a une adresse Bitcoin le detruit, et
# c'est l'erreur de donateur la plus courante.
RESEAU_BTC = "Bitcoin mainnet (BTC)"

SOUTIEN_EST = [
    ("A gift, and nothing else.",
     "It is given to the movement. It is not a purchase, not a subscription "
     "and not an investment."),
    ("Voluntary, and of any size.",
     "No amount is suggested anywhere on this page. A movement that has "
     "published no accounts has no business naming a figure."),
    ("Sent directly.",
     "There is no platform between the giver and the movement, so nobody "
     "takes a percentage and no third party is told who gave."),
    ("Anonymous by default.",
     "This page has no form and no account. Nothing here asks who you are, "
     "and nothing here records it."),
]

SOUTIEN_NEST_PAS = [
    ("Not a membership.",
     "Giving does not admit anyone to the Circle. Admission is by decision, "
     "and how it works is itself an open question."),
    ("Not standing in the movement.",
     "It confers no title, no vote, no representative capacity and no right "
     "to speak in the movement&rsquo;s name."),
    ("Not influence over a position.",
     "No published position is for sale at any price. The rule that keeps "
     "money away from what the movement says is set out on Lobbying."),
    ("Not refundable.",
     "A payment on this network cannot be reversed by anyone, including the "
     "movement. There is no chargeback and no dispute procedure."),
]

# Ce qui n'est pas encore decide, et que la page affiche plutot que de le
# taire. Chaque ligne renvoie a une decision reelle du tableau de movement.html
# — aucune n'est inventee ici pour faire nombre.
SOUTIEN_OUVERT = [
    ("Who receives it",
     "The movement has no legal form and no country of registration yet. "
     "Until it does, a contribution is held by no institution and answers to "
     "no register."),
    ("What it pays for",
     "No budget has been published, so none is claimed. A page that promised "
     "where the money goes would be inventing it."),
    ("Whether gifts are published",
     "Whether contributions, their totals and their origins appear publicly, "
     "and at which threshold."),
    ("Which rules apply",
     "Political funding is regulated in most countries, and the rules that "
     "bind the movement follow from its legal form and its country. Anyone "
     "whose own country restricts political contributions should check "
     "before sending."),
    ("Other ways to give",
     "Bank transfer, card, or a platform. None of them exists yet, and none "
     "can exist before there is an entity to hold an account."),
    ("Receipts",
     "Whether a giver can obtain any acknowledgement at all, and from whom. "
     "A bare address issues none."),
]
