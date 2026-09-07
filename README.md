# Equilibrium — site mockup

Ten static pages. No framework, no build step to install, no database, no
JavaScript, no cookie, no tracker, and **no outbound request of any kind** —
verified, not asserted (see below).

```
THE MOVEMENT
  index.html        the statement, the five principles in brief, the boundaries,
                    and the front-page explanation of the two things under one name
  principles.html   the five principles in full, each with what it does not mean
  movement.html     what the movement is, the multipolar figure, the twenty-two
                    open decisions in three groups, Q&A
  join.html         how to follow, and the mockup form with its warning

THE PRACTICE
  services.html     what a private practice can and cannot be, six lines of
                    advisory work, how an engagement runs, fees, boundaries
  lobbying.html     declared advocacy, the six refusals, THE WALL between the
                    movement and the practice, registration, Q&A

THE CIRCLE
  circle.html       the membership, the eight formats of activity, the portal
  portal.html       the sign-in mockup, and the ten things that must exist first
  portal-area.html  a static preview of the member area — no session, no data

assets/           site.css and eleven generated SVGs
brand/            the wordmark on its own, small and large, for other supports
source/           the scripts that generate everything above
tests/            the verification suite and the control captures
```

Open `index.html` in a browser. That is the whole installation.

---

## The structural point, first

A political movement that publishes positions, and a firm paid to advance its
clients' positions, are **treated as two different things in law in almost
every country**. Held in one pocket, every position the movement publishes
reads as bought — and money from a foreign state to a political movement is,
in several countries, prohibited outright rather than merely declarable.

So the site is built as two faces of one name, with the separation **written in
public** as a rule of governance (`lobbying.html#wall`), and the legal
arrangement left where it belongs: open, and listed as open. A governance rule
kept in an internal note is worth nothing, because nobody can hold anyone to
it.

**Nothing on this site claims that Equilibrium is registered, licensed,
accredited, mandated or recognised anywhere.** It is not, yet. Putting a
client's position to public decision-makers is a registrable activity in most
countries, and doing it for a foreign principal is registrable again under a
stricter regime; which regimes apply follows from where the practice is set up
and from where each client sits.

Those regimes are a question for counsel admitted in whichever country you
choose — foreign-agent registration, lobbying registers, gifts and hospitality
rules, and political-financing law all bite here, and several of them carry
criminal penalties rather than fines. That advice has to come from a lawyer in
that country, not from a website and not from me. What I have done is make sure
the site never asserts compliance you do not yet have.

---

## What this mockup does not contain, and why

**No fact about the movement is invented.** Not a founding date, a membership
figure, a country, a legal form, an officer, a budget, an endorsement or a line
of press coverage. Nothing of that kind is known to me, and a political
movement that publishes a figure it cannot support loses the argument the first
time somebody checks. The twenty-two decisions that are genuinely open are
**shown on the site**, in a table on `movement.html`, in three groups — the
movement, the practice, the Circle — each marked `To be decided`.

That table is public on purpose. A visitor who reads "legal form: to be
decided" understands they are looking at a movement at its beginning. A visitor
who is told nothing assumes something is being withheld.

**No client, no mandate and no fee appears anywhere.** No figure of any kind is
attached to the practice, because none has been set.

**No event is announced.** The Circle page carries eight *formats* of activity
— containers — and every one of them is marked `Not yet scheduled`. There is no
date, no place and no speaker anywhere on this site. A movement at its
beginning that publishes a calendar it has not arranged loses the only asset it
has, and loses it the first time somebody turns up.

**No position is taken on any real state, government, party, organisation or
conflict**, and no country is named anywhere in the argument. The founding
statement is general by construction; making it concrete would be putting words
in the movement's mouth on the subject where that costs the most. The
verification suite searches all ten pages for a list of states, blocs and
organisations and fails if one appears.

**No audience figure appears anywhere.** Not the one on the account, not
another.

---

## Two registers, and the site says which is which

The founding statement is quoted **word for word**, in a different typeface,
behind a rule, labelled as quoted in full without alteration. Everything else
is copy I drafted from that statement, and the pages say so in as many words.

The verification suite compares every quoted paragraph against `source/contenu.py`
**character by character**, after normalising whitespace only. If a word of the
statement ever drifts, the suite fails and names the paragraph.

Each principle carries a **"What it does not mean"** column. That is not
hedging. A general principle is only legible once its limits are stated, and a
movement that does not state its own limits has them stated for it by other
people. Every line in that column is derived from the statement itself — it
delimits, it never adds a policy.

The same discipline runs through the practice pages: six lines of service, each
saying what the client actually receives, and five boundaries saying what the
practice is **not** — starting with the sentence that matters most, that
diplomatic relations between states are conducted by states, and that a private
practice holds no accreditation, no diplomatic status and no official function
of any kind.

---

## Both forms are mockups

Neither the join form nor the portal sign-in has an `action`, a `method`, a
script behind it or an enabled button. They send nothing anywhere.

That is deliberate and it should stay that way until two decisions are taken. A
list of the supporters — or the members — of a political movement is, under
European data protection law, information revealing political opinions: a
special category under Article 9 of the GDPR, with obligations attached. Before
either form can accept a single name there has to be:

1. an identified body that receives the data, and
2. a country whose law applies to it.

Both are on the open-decisions table, and `portal.html` sets out ten further
requirements that come before a login screen is worth writing: hosting,
encryption at rest, access control and access logging, retention, breach
procedure, member rights, an impact assessment, and authentication itself.
Building the login first and the responsibilities afterwards is the usual
order, and it is the wrong one.

Two details worth naming:

- **The sign-in field asks for a member reference, not an e-mail address.** A
  login page that accepts an address turns every failed attempt into a
  statement about who is and is not a member of a political movement. The suite
  checks there is no e-mail field.
- **The member directory is deliberately not built.** A list showing the
  members of a political movement to one another is the most sensitive object
  in this whole project, and it is the last thing that should exist, not the
  first.

---

## Privacy, built in rather than declared

No web font, no analytics, no embed, no CDN. A political site that loads a font
from a third-party server hands that third party the IP address of every one of
its readers. Avoiding it costs nothing.

This is **measured**: the suite listens to every network request the browser
makes while loading all ten pages at fourteen widths, and fails if a single one
leaves `127.0.0.1`.

---

## Regenerating

The scripts live in `source/`. Run them **from `source/`**; they write one
level up, into the site root.

```sh
cd source
python3 gen_visuals.py     # rewrites assets/*.svg and brand/*.svg
python3 build.py           # rewrites the ten .html pages
```

Both are deterministic. Every generated image has a fixed seed, so
regenerating does not move a pixel of anything already approved — the three
visuals added with the practice and the Circle have their own seeds, and adding
them left the five principle gems and the hero byte-identical.

`build.py` refuses to run if `assets/site.css` has unbalanced comment markers.
An unterminated CSS comment silently kills every rule after it: the page still
renders, nothing reports an error, and a fix you believe you applied is not
applied. That check costs one line.

To edit the wording, edit `source/contenu.py`, not the HTML. The ten pages are
generated; hand-edits to them are overwritten by the next build.

To remove the amber demonstration banner, set `BANDEAU_DEMO = False` at the top
of `source/build.py` and rebuild.

---

## Verification

```sh
cd tests
python3 -m http.server 8861 --directory ..    # in one terminal, from the site root
python3 verif.py                              # in another
```

**1498 checks, 0 failures**, across 10 pages × 14 viewport widths from 320 px to
1440 px. The suite measures the page a browser actually draws — never the
source files. Among what it proves rather than assumes:

- every quoted paragraph of the statement, word for word against the source;
- the five principles in the order the statement names them, each with its
  quote, its "means" list, its "does not mean" list and its own gem;
- the six service lines in order, each with the list of what the client
  receives — a service described only by its ambition cannot be judged and
  cannot be invoiced honestly either;
- the six refusals on the lobbying page, word for word, and the six clauses of
  the wall, including the central one: a client cannot commission, edit, delay
  or veto anything the movement publishes;
- the twenty-two open decisions in their three groups, every one marked
  `To be decided`, with no figure;
- the eight Circle activity formats, each carrying `Not yet scheduled`, on both
  the Circle page and the member-area preview;
- **no claim of status anywhere**: no "is registered", "accredited by",
  "licensed by", "official status" — while the *negated* forms stay allowed,
  because saying plainly that nothing is claimed is the point;
- no invented year, month, weekday, headcount, amount, percentage, telephone
  number, e-mail address or registered office, on any page — with the Q&A
  entries forced open first, because closed `<details>` hide their text;
- no first person plural anywhere: a "we" would make an organisation speak
  whose legal form does not exist yet, and on a page selling services it would
  imply a team;
- no state, bloc or organisation named;
- no outbound network request, and no `<script>` element;
- neither form has an `action` or a `method`, both buttons are disabled, and
  no field asks for an opinion, an affiliation, an identity document or an
  e-mail address;
- the declared `width`/`height` of every image match its real proportions —
  **and the box it is actually drawn in matches them too**;
- every in-page anchor lands *below* the sticky header, at 390 px as well as
  1280 px;
- **the hero title and the practice band are legible at every width.** Not
  judged — measured: the text is hidden, the background that was behind it is
  photographed, and the contrast is computed against the brightest pixel of
  that background.

Measured contrast, worst case to best: hero title **5.23:1 at 1024 px**, 9.5–13
through the middle widths, 16.91 wide. Practice band **5.49:1 at 1024 px**,
10.9–13 through the middle, 16.81 wide. Both bottom out one step above the
1000 px breakpoint, which is the width worth watching on this design.

### Four things the measurement caught that looking would not have

**The brand name was being clipped to "Equilibriu" at six widths between 768 and
1440 px.** The menu had gone from four labels to seven plus a sign-in button,
and the wordmark — a flex item like any other — was being compressed. A word
short of one letter reads as a design choice, not a bug, which is exactly why
nobody would have reported it.

**The two figures were letterboxed, not scaled.** `.figure img` had `width:100%`
but no `height:auto`, so the `height` attribute in the template kept the box
tall and the SVG centred itself inside it with empty space above and below. The
existing check compared the *attribute* to the file and passed. Comparing the
**drawn box** to the file is what found it — and that check is now permanent.
The multipolar figure had been in that state since it was built.

**Anchors were landing behind the sticky header on mobile.** Invisible on a
desktop, where the header is 70 px tall; obvious at 390 px, where it is 167 px
and the section title you clicked towards is simply not there.

**The band's contrast bottoms out at 1024 px, exactly as the hero's does.** That
was not luck: the veil on the new band is painted at every width from its first
version, because the hero taught that a breakpoint chosen by estimate is a
breakpoint in the wrong place — the earlier one was scoped to 1000 px and
measured 2.56:1 at 1024.

### The suite is proved able to fail

A green suite means nothing until you have seen it go red. Five mutations were
applied and each was **first confirmed to have reached the rendered page**, not
merely the file:

| Mutation | Result |
|---|---|
| the CSS veil removed from the practice band | **25 failures**, contrast down to **1.01:1** |
| `Next session on Thursday, in March.` added to one activity | **4 failures** — month and weekday, on both pages carrying it |
| "not registered anywhere" changed to "is registered … and is accredited by the competent authority" | **3 failures** — status claim, accreditation claim, and the explicit check |
| `height:auto` removed from `.figure img` | **2 failures**, both figures, naming drawn size against natural ratio |
| `scroll-margin-top` set to zero | **11 failures**, all at 390 px, none at 1280 px |

The first attempt at the veil mutation **did not apply at all** — the selector
appears twice, inside and outside a media query, and I had replaced one. The
render-proof caught it before the green suite could be misread as a weak check.
That is the same trap as the earlier quotation mutation, which had landed on
the `<meta name="description">` in the head rather than the visible paragraph:
grepping the file proves the *file* changed; only reading the element back out
of the DOM proves the *page* did.

---

## The support page

`support.html` is the tenth page. It exists so the movement can accept support
**before** it has a legal form, a country or an account — the stage it is at
today.

It is the only page on this site where a display error costs a third party
money, irreversibly, so it is written the other way round from the usual
donation page: **what cannot be promised is shown before the means of paying.**
The warning box — the payment cannot be reversed, the movement has no legal
form or country yet, political funding is regulated in most countries, nothing
on the page collects anything about the reader — comes above the address
panel, and the verification suite checks that this order survives in the
rendered page.

As everywhere else on this site: no suggested amount, no target, no budget, no
total already received, no donor. Six questions a giver is entitled to ask are
shown with their true answer for today, `To be decided`.

### The address lives in one place, and it is empty

`ADRESSE_BTC` in `source/contenu.py` is the only place a wallet address is
written. It is `""`, and that is not an oversight: an address that arrived as a
screenshot of a **third party's** social post has been checked only for base58
validity, and validity says nothing about who owns the wallet. A wrong address
on a donation page is not a display defect, it is donors' money sent to a
stranger under the movement's name, with no way back. It is filled in when the
owner of the movement confirms in writing that the wallet is his.

While it is empty the page shows the same `To be decided` badge as everywhere
else and can receive no payment. The WordPress build reads the same value from
a single admin option rather than from the page content, for the same reason:
one place, so there is never a half-corrected copy.

The suite has two branches for this, and the inactive one is written rather
than silently skipped — with the address empty it proves that **no string
resembling a wallet address** appears anywhere in the rendered text; with an
address set it compares the rendered address **character by character** to the
source, and requires it to appear once on this page and on none of the other
nine.

---

## Still needed from you

### For the movement

1. **The original logo file.** The E is a vector reconstruction drawn from your
   screenshot, where the mark is 230 px wide. If you have the real file — a
   large PNG, or better an SVG or AI — it replaces mine in two minutes.
2. **Any other channel** the movement publishes on. One handle is on the site,
   taken from your screenshot; confirm it and add the rest.
3. **Whether the site should exist in more than one language.** A movement that
   argues for a multipolar world in one language only is arguing against
   itself.
4. **Written confirmation that the donation wallet is yours**, and the address
   pasted back so it can be compared character by character. Until then the
   support page shows `To be decided` where the address goes. This one is not
   caution for its own sake: a payment on that network cannot be reversed by
   anyone.

### For the practice — the two that block everything else

4. **One legal person or two?** Whether the practice is separate from the
   movement, and which of them signs a client engagement. Every other row in
   the practice group depends on this answer.
5. **Which country.** It decides which registers apply, which political
   financing rules apply, and whether money may pass between the two at all.

Then: the client acceptance policy — which entities and which states the
practice will act for, and which it will refuse. That is the policy that
decides what the name comes to mean, and no one but you can write it.

### For the Circle

6. **Is membership legal membership, or a subscriber circle?** Only one of the
   two creates obligations towards the members.
7. **Who holds the member list, in which country, under whose responsibility.**
   Nothing in the portal can be connected before this.
8. **Which of the eight activity formats actually run**, and how often.

All twenty-two are on the table at `movement.html#decisions`, so you can read
them in one place rather than out of this file.
