"""Generate the static HTML for a video script section.

Usage: python3 -I gen_video.py <index.html> <video-id>
Replaces the block between <!-- {ID}:START --> and <!-- {ID}:END -->,
or inserts it before the "Sections ... are added" placeholder.
"""
import html
import re
import sys

ICON_WAVE = ('<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M2 10h2M6 6v8M10 3v14M14 7v6M18 10h0" '
             'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>')
ICON_MIC = ('<svg viewBox="0 0 20 20" aria-hidden="true"><rect x="7" y="2" width="6" height="10" rx="3" fill="none" '
            'stroke="currentColor" stroke-width="1.8"/><path d="M4 9.5a6 6 0 0 0 12 0M10 15.5V18" fill="none" '
            'stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>')
ICON_EYE = ('<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M1.5 10S4.5 4 10 4s8.5 6 8.5 6-3 6-8.5 6S1.5 10 1.5 10z" '
            'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><circle cx="10" cy="10" '
            'r="2.5" fill="currentColor"/></svg>')


def fmt(t):
    return f"{t:02d}" if t < 100 else str(t)


def rich(text):
    """Escape, then turn [[ON-SCREEN TEXT]] into styled on-screen chips."""
    out = html.escape(text, quote=False)
    # Short chips never break; long ones may wrap across lines.
    out = re.sub(r"\[\[(.+?)\]\]",
                 lambda m: f'<span class="ost{" ost--nw" if len(m.group(1)) <= 30 else ""}">{m.group(1)}</span>', out)
    return out


VIDEOS = {
    "video-01": {
        "v": "v1",
        "num": "02",
        "label": "Video 01",
        "title": "The Second Moment",
        "lens": "Executive lens",
        "runtime": 129,
        "next": ("#video-02", "Video 02 · The Question That Keeps Coming Back"),
        "meta": ["LinkedIn 4:5 (assumed)", "~129s", "VO 115–125 wpm + silent visual beats"],
        "stats": [("212", "VO words"), ("118", "wpm average"), ("21s", "music + SFX only"), ("8", "beats")],
        "mood": "Calm, candid, restrained. A small kitchen-table mystery becomes an information-design reveal, not a dramatic medical story.",
        "theme": "Correct, complete information in the room may be difficult to use alone at home.",
        "concept": "A complete written instruction needs an explanation designed for <mark>the second moment</mark>: when a patient must use it.",
        "question": "Which multi-step home instructions need explanations designed for the moment of use, beyond complete written instructions?",
        "visual_sys": ["Warm dotted cream", "Handwriting-display headlines", "Clean sans labels", "Black outlines",
                       "Orange accents", "Yellow paper", "Simple figures", "Progressive reveals over complex morphs"],
        "audio_sys": ["Calm VO ~115–125 wpm", "Light music", "Paper & pencil SFX", "Silent beats marked in the audio column",
                      "Ends on a 3s logo"],
        "swatches": [("#FBF3E4", "Cream"), ("#0F172A", "Outline"), ("#FF9333", "Orange"), ("#FFD45C", "Yellow paper")],
        "rows": [
            {
                "t": (0, 12), "name": "Cold open",
                "vo": (0, 10, "Day three. Eight p.m. The instruction is right there. So why is the next step still hard to find?"),
                "sfx": [(10, 12, "Paper settles; question-mark ink draws.")],
                "shots": [("0–3s", "Show the kitchen table, complete instruction sheet and series label [[PATIENT EDUCATION]]. Hook text [[DAY 3 · 8 PM]] / [[NOTHING IS MISSING.]] appears immediately."),
                          ("3–12s", "The patient searches the written sections; an orange line stops at a question mark. Match the sheet’s position to the consultation scene.")],
            },
            {
                "t": (12, 27), "name": "Rewind",
                "vo": (12, 25, "Three days earlier, everything made sense. The clinician explained each step. The patient asked their question, got an answer, and took the complete written instructions home."),
                "sfx": [(25, 27, "Paper lifts and the patient exits.")],
                "shots": [("12–20s", "Match-cut on the same printed sheet to a consultation three days earlier. Clinician explains abstract steps A/B/C, marked with orange ticks."),
                          ("20–27s", "The patient asks a question, nods and takes the complete sheet home. On-screen: [[THREE DAYS EARLIER.]]")],
            },
            {
                "t": (27, 41), "name": "Three days pass",
                "vo": (27, 39, "Day one. Day two. Day three. The written instructions stayed exactly as they were. But the explanation around them was harder to bring home."),
                "sfx": [(39, 41, "Calendar taps; orange connection fades.")],
                "shots": [(None, "The instruction sheet stays in view as [[DAY 1 → DAY 2 → DAY 3]] appears. Its printed information remains unchanged while one orange connection from the consultation fades. Return to the original kitchen-table composition.")],
            },
            {
                "t": (41, 59), "name": "Kitchen table",
                "vo": (41, 56, "Back at the kitchen table, nothing is missing. The written version is complete. But it was organized for reading. The patient needs it for doing. Right now. On their own."),
                "sfx": [(56, 59, "Pencil stops at the question mark.")],
                "shots": [("41–50s", "Stay in ONE kitchen-table composition. The patient searches the complete [[OVERVIEW]], [[TIMING]] and [[NOTES]] sections."),
                          ("50–59s", "Reveal the contrast as text over the same image: [[CORRECT IN THE ROOM.]] / [[HARD TO USE AT HOME.]] The question mark leads into the design demonstration.")],
            },
            {
                "t": (59, 84), "name": "The second moment",
                "vo": (59, 77, "That’s the second moment we design for at F.Learning. We start with the patient, the task, and the moment of use. What must they see? What comes next? What needs explaining – not just listing?"),
                "sfx": [(77, 84, "Pencil draws the patient-use sequence; yellow WHY note opens; text holds.")],
                "shots": [("59–70s", "Keep the complete written instructions on the left. On the right, a patient-education animation begins taking shape from the same A/B/C information. Orange lines connect each illustrated step to its source; a small F.Learning label marks the design transition."),
                          ("70–84s", "The animated steps reveal [[WHAT NOW?]], [[WHAT NEXT?]] and a yellow [[WHY?]] note, using simple motion to explain rather than just list. The music/SFX-only hold lets the sequence finish and remain readable.")],
            },
            {
                "t": (84, 101), "name": "Same facts, new order",
                "vo": (84, 100, "The facts are the same. So are the medical steps. What changes is the explanation. Now the steps are easy to find in the order they’re needed. And the why is visible."),
                "sfx": [(100, 101, "Underline finishes; two layouts hold side by side.")],
                "shots": [("84–93s", "Continue the SAME two-column composition, adding [[AS WRITTEN]] and [[AS USED]]. On the left, the complete A/B/C information remains across [[OVERVIEW / TIMING / NOTES]]. On the right, the animated explanation shows A → B → C in the unchanged required clinical sequence, with visual cues."),
                          ("93–101s", "Add [[WHY IT MATTERS]] beside the relevant step. Finish on [[SAME INFORMATION. DIFFERENT EXPLANATION.]]")],
            },
            {
                "t": (101, 113), "name": "Where it earns its cost",
                "vo": (101, 113, "A simple instruction? A leaflet may be enough. But several steps, days later, at home, alone? That’s when this work earns its cost."),
                "under": "Music continues low; soft paper ticks under the four labels.",
                "sfx": [],
                "shots": [(None, "A simple one-step leaflet appears as a valid option. Beside it, a multi-step home instruction gains the labels [[SEVERAL STEPS]], [[DAYS LATER]], [[AT HOME]], [[ALONE]]. An orange underline links those conditions to the need for a designed explanation.")],
            },
            {
                "t": (113, 129), "name": "Call to action",
                "vo": (113, 125, "The consultation ends. The explanation still has to work. Book a 30-minute call with a learning designer about one instruction patients keep getting wrong."),
                "sfx": [(125, 129, "CTA holds for 1s; then F logo and flearning wordmark animate over 3s.")],
                "shots": [("113–120s", "Return to the clinic and kitchen-table illustrations, joined by the orange information line. On-screen: [[DESIGN FOR THE SECOND MOMENT.]]"),
                          ("120–126s", "CTA [[BOOK A 30-MINUTE PATIENT EDUCATION CALL]] / [[ONE INSTRUCTION PATIENTS KEEP GETTING WRONG]] / [[NO DECK REQUIRED]]."),
                          ("126–129s", "Animated F then flearning wordmark.")],
            },
        ],
        "why": [
            ("Narrative choice", "The visual mystery begins with a complete page at the kitchen table, rewinds to a clear consultation, and returns to the same facts presented for use. The payoff is communication design, not distribution or a saved clinical outcome."),
            ("Raw Content Source Proof", "Direct source fit: “The written version is complete”; the same preparation information in the order written versus the order used; explanation of what and why; a leaflet is enough for a simple one-off. “This work earns its cost when…” under multi-step, days-later, home-alone conditions."),
            ("Selection / exclusion", "Keep only one patient journey, one editorial written-versus-used comparison, and a short buyer cost-fit insight."),
        ],
    },
}


VIDEOS["video-02"] = {
    "v": "v2",
    "num": "03",
    "label": "Video 02",
    "title": "The Question That Keeps Coming Back",
    "lens": "Project Lead lens",
    "runtime": 132,
    "next": ("#rationale", "Content Rationale"),
    "meta": ["LinkedIn 4:5 (assumed)", "~132s", "VO 115–125 wpm + silent visual beats"],
    "stats": [("217", "VO words"), ("118", "wpm average"), ("22s", "music + SFX only"), ("9", "beats")],
    "mood": "Dry editorial wit, short contrasts, and purposeful restraint. The repeated answer card brings a question into focus.",
    "theme": "An answer can exist in the materials without reaching every patient in a useful form.",
    "concept": "<mark>One clinical source. Different patient needs.</mark> Diagnose the gap before choosing the format.",
    "question": "How can F.Learning adapt one clinical explanation to different patient needs while keeping clinical accuracy under our team’s review?",
    "visual_sys": ["Same cream / black / orange system", "Series label", "Paper cards", "Orange question & tally",
                   "Yellow brief", "Simple Project Lead figure", "Mostly progressive reveals", "One question-to-magnifier morph"],
    "audio_sys": ["Calm VO ~115–125 wpm", "Music", "Paper & pencil SFX", "Silent beats marked in the audio column",
                  "Ends on a 3s logo"],
    "swatches": [("#FBF3E4", "Cream"), ("#0F172A", "Outline"), ("#FF9333", "Orange"), ("#FFD45C", "Yellow brief")],
    "rows": [
        {
            "t": (0, 12), "name": "Same question, again",
            "pre": [(0, 6, "Three paper slides, three pencil tally strokes.")],
            "vo": (6, 12, "Same answer. Same question. Again. Why does it keep coming back?"),
            "under": "Final light paper tap.",
            "sfx": [],
            "shots": [("0–3s", "Show the series label [[PATIENT EDUCATION]], the recurring answer card and the headline [[THE SAME QUESTION. AGAIN.]] immediately, before VO begins."),
                      ("3–12s", "The same answer card is filed repeatedly on the Project Lead’s desk; orange tally marks accumulate beside the still-open question. The orange question mark carries into the next scene.")],
        },
        {
            "t": (12, 27), "name": "A better question",
            "vo": (12, 26, "The answer is in the materials. Clinicians have explained it. More pages may not help. So the Project Lead asks a better question: who is this explanation reaching?"),
            "sfx": [(26, 27, "Magnifier line completes.")],
            "shots": [("12–20s", "Project Lead places the recurring question next to the complete source material."),
                      ("20–27s", "The orange question mark becomes a magnifying glass, drawing attention to three patient silhouettes. On-screen: [[WHO IS THIS REACHING?]] The magnifier carries into the next beat.")],
        },
        {
            "t": (27, 43), "name": "Where people get stuck",
            "vo": (27, 41, "Some patients need clearer words. Others need to see what is happening, not just read it. Some can’t rely on written English. Where, exactly, are people getting stuck?"),
            "sfx": [(41, 43, "Last observation lands on yellow note.")],
            "shots": [("27–35s", "Beneath the magnifier, introduce [[WORDING]] (dense phrase) and [[WHAT NEEDS SHOWING?]] (visual cue)."),
                      ("35–43s", "Add [[LANGUAGE]] with narration waves; all three remain questions to investigate. Move the cards onto the yellow Project Lead note.")],
        },
        {
            "t": (43, 60), "name": "The brief",
            "vo": (43, 57, "At F.Learning, we begin with your patients. Not a production format. What must they understand? Where do they get stuck? And what could make them more anxious?"),
            "sfx": [(57, 60, "Pencil connects three brief questions, then holds.")],
            "shots": [("43–51s", "The note becomes a [[COMMUNICATION BRIEF]] as F.Learning joins the process."),
                      ("51–60s", "Reveal [[WHAT MUST THEY UNDERSTAND?]], [[WHERE DO THEY GET STUCK?]], [[WHAT ADDS ANXIETY?]] and connect them to the audience cards. Hold the completed brief for the music/SFX-only moment.")],
        },
        {
            "t": (60, 78), "name": "One core, different needs",
            "vo": (60, 75, "Start with one clinical source. Keep the facts. Adapt the explanation for each audience: what they need to see, how much detail, and which language. Different versions. Same core."),
            "sfx": [(75, 78, "Final aligned source dots reveal and hold.")],
            "shots": [("60–68s", "Present one [[CLINICAL SOURCE]] card with fixed information points."),
                      ("68–78s", "Build possible audience-specific explanations underneath – visual sequence, simpler wording, narrated version – each connected to the unchanged source by orange lines. On-screen: [[ONE CORE. DIFFERENT NEEDS.]] Hold the completed comparison.")],
        },
        {
            "t": (78, 92), "name": "Proof: AMD",
            "vo": (78, 91, "For the Association of Migraine Disorders, a menstrual-migraine explainer helped patients understand their pattern. Clinicians spent less time re-explaining basics and more on care decisions."),
            "sfx": [(91, 92, "Proof card holds; soft paper placement.")],
            "shots": [(None, "An AMD proof card appears: [[ASSOCIATION OF MIGRAINE DISORDERS – Menstrual migraine]], with a simple calendar illustration. Reveal the two supported takeaways in sequence: [[LESS RE-EXPLAINING BASICS]] and [[MORE ON CARE DECISIONS.]] The case stays clearly identified.")],
        },
        {
            "t": (92, 106), "name": "Proof: NYU Langone",
            "vo": (92, 104, "For NYU Langone Health, multilingual colonoscopy-preparation videos made the steps easier to understand. Visual guidance and narration helped patients who couldn’t rely on written English."),
            "sfx": [(104, 106, "Second proof card settles beside AMD.")],
            "shots": [(None, "A separate NYU Langone Health proof card joins AMD. It shows a colonoscopy-preparation sequence, visual cues and multilingual narration waves. On-screen: [[MULTILINGUAL VISUAL GUIDANCE.]] Keep both case cards visible as distinct examples.")],
        },
        {
            "t": (106, 119), "name": "Two reviews",
            "vo": (106, 118, "Your clinical team reviews medical accuracy. We review whether a patient can still follow it. Two separate reviews. One explanation your team can check."),
            "sfx": [(118, 119, "Two review annotations sit in place.")],
            "shots": [(None, "The proof cards give way to script and storyboard sheets. Two reviewer annotations appear: [[MEDICAL ACCURACY – CLIENT CLINICAL TEAM]] and [[CAN A PATIENT STILL FOLLOW IT? – F.LEARNING]]. Beneath them, a simple process line reads [[BRIEF → SCRIPT → STORYBOARD → ANIMATION]].")],
        },
        {
            "t": (119, 132), "name": "Call to action",
            "vo": (119, 129, "Which instruction do patients keep getting wrong? Bring it to a 30-minute call with a learning designer. No deck required."),
            "sfx": [(129, 132, "F draws first; ‘flearning’ wordmark resolves.")],
            "shots": [(None, "Return to the opening desk and answer cards. The Project Lead places the recurring question on the yellow brief and circles it in orange. CTA: [[WHICH INSTRUCTION DO PATIENTS KEEP GETTING WRONG?]] / [[BOOK A 30-MINUTE PATIENT EDUCATION CALL]] / [[NO DECK REQUIRED]]. Hold the CTA; final 3s: F animation followed by the flearning wordmark.")],
        },
    ],
    "why": [
        ("Narrative choice", "A recurring answer card slides into the stack three times. Each return adds an orange tally beside the same question. The Project Lead changes the task: examine whom the explanation reaches, then build an audience-led brief. At CTA the question is circled instead of being presented as solved."),
        ("Raw Content Source Proof", "Step 1 identifies confusion; later design choices reflect literacy, language, emotional context and use. AMD qualitatively reports less time spent re-explaining basics and more on care decisions. NYU shows visual and multilingual colonoscopy-preparation guidance. The source assigns medical accuracy to client clinicians and the “can a patient still follow it” review to F.Learning."),
        ("Selection / exclusion", "The story uses one familiar, fictional question that keeps coming back. It first asks which patients are getting stuck, then shows one clinical source adapted to their different needs, and backs this up with two real cases from the raw content source: AMD and NYU Langone Health."),
    ],
}


def arc(vid, d):
    total = d["runtime"]
    segs = []
    for i, r in enumerate(d["rows"], 1):
        a, b = r["t"]
        vo_a, vo_b, _ = r["vo"]
        # VO share and silent share inside the segment, as percentages of the segment.
        vo_l = (vo_a - a) / (b - a) * 100
        vo_w = (vo_b - vo_a) / (b - a) * 100
        segs.append(f'''              <li class="arc__seg" style="--w:{(b - a) / total * 100:.3f}">
                <a href="#{vid}-r{i}" class="arc__link" aria-label="Beat {i}: {html.escape(r['name'])}, {a}–{b}s">
                  <span class="arc__bar"><span class="arc__vo" style="left:{vo_l:.2f}%;width:{vo_w:.2f}%"></span></span>
                  <span class="arc__n">{i:02d}</span>
                  <span class="arc__name">{html.escape(r['name'])}</span>
                  <span class="arc__tc">{a}–{b}s</span>
                </a>
              </li>''')
    return "\n".join(segs)


def row(vid, i, r):
    a, b = r["t"]
    vo_a, vo_b, vo = r["vo"]
    sfx = "".join(
        f'''
                  <div class="sfx">
                    <p class="sfx__tag">{ICON_WAVE}Music + SFX only · {fmt(sa)}–{fmt(sb)}s</p>
                    <p class="sfx__txt">{html.escape(t)}</p>
                  </div>''' for sa, sb, t in r["sfx"])
    pre = "".join(
        f'''
                  <div class="sfx sfx--pre">
                    <p class="sfx__tag">{ICON_WAVE}Music + SFX only · {fmt(sa)}–{fmt(sb)}s</p>
                    <p class="sfx__txt">{html.escape(t)}</p>
                  </div>''' for sa, sb, t in r.get("pre", []))
    if r.get("under"):
        sfx += f'''
                  <div class="sfx sfx--under">
                    <p class="sfx__tag">{ICON_WAVE}Under the VO</p>
                    <p class="sfx__txt">{html.escape(r["under"])}</p>
                  </div>'''
    shots = "".join(
        f'''
                    <li{' class="shots__one"' if t is None else ''}>{f'<span class="shots__t">{t}</span>' if t else ''}<p>{rich(txt)}</p></li>'''
        for t, txt in r["shots"])
    return f'''
            <article class="srow reveal" id="{vid}-r{i}" data-row="{i - 1}">
              <div class="srow__time">
                <span class="srow__n">{i:02d}</span>
                <span class="srow__tc">{fmt(a)}–{fmt(b)}s</span>
                <span class="srow__name">{html.escape(r["name"])}</span>
              </div>
              <div class="srow__cell srow__audio">
                <p class="srow__mlabel">{ICON_MIC}Narration / Audio</p>{pre}
                <p class="vo__tag">VO · {fmt(vo_a)}–{fmt(vo_b)}s</p>
                <blockquote class="vo">“{html.escape(vo)}”</blockquote>{sfx}
              </div>
              <div class="srow__cell srow__visual">
                <p class="srow__mlabel">{ICON_EYE}Visual / On-screen action</p>
                <ul class="shots">{shots}
                </ul>
              </div>
            </article>'''


def section(vid, d):
    chips = "".join(f'<li>{html.escape(c)}</li>' for c in d["visual_sys"])
    achips = "".join(f'<li>{html.escape(c)}</li>' for c in d["audio_sys"])
    sw = "".join(f'<li><span class="sw" style="background:{c}"></span>{n}</li>' for c, n in d["swatches"])
    meta = "".join(f'<li>{html.escape(m)}</li>' for m in d["meta"])
    stats = "".join(f'<div><dt>{l}</dt><dd>{v}</dd></div>' for v, l in d["stats"])
    rows = "".join(row(vid, i, r) for i, r in enumerate(d["rows"], 1))
    prog = "".join(
        f'<span class="sprog__seg" style="--w:{(r["t"][1] - r["t"][0]) / d["runtime"] * 100:.3f}" data-seg="{i}"></span>'
        for i, r in enumerate(d["rows"]))
    why = "".join(f'''
            <article class="why__card reveal" style="--d:{i}">
              <span class="why__n">{i + 1}</span>
              <h4 class="why__title">{t}</h4>
              <p>{html.escape(x)}</p>
            </article>''' for i, (t, x) in enumerate(d["why"]))
    return f'''    <!-- {vid.upper()}:START -->
    <section class="section section--video section--{d["v"]}" id="{vid}" aria-labelledby="{vid}-title" data-video>
      <div class="container">
        <header class="section__head reveal">
          <p class="section__kicker"><span class="section__num">{d["num"]}</span> {d["label"]}</p>
          <h2 class="section__title" id="{vid}-title">{d["title"]}</h2>
          <ul class="vmeta"><li class="vmeta__lens">{d["lens"]}</li>{meta}</ul>
        </header>

        <!-- A · Script header -->
        <div class="block">
          <h3 class="block__title reveal"><span class="block__tag">A</span> Script header</h3>
          <div class="sheader">
            <article class="sheader__card sheader__card--concept reveal">
              <p class="sheader__label">Core concept</p>
              <p class="sheader__concept">{d["concept"]}</p>
            </article>
            <article class="sheader__card reveal" style="--d:1">
              <p class="sheader__label">Mood</p>
              <p>{html.escape(d["mood"])}</p>
            </article>
            <article class="sheader__card reveal" style="--d:2">
              <p class="sheader__label">Theme</p>
              <p>{html.escape(d["theme"])}</p>
            </article>
            <article class="sheader__card sheader__card--question reveal" style="--d:3">
              <p class="sheader__label">Buyer question</p>
              <blockquote>{html.escape(d["question"])}</blockquote>
            </article>
          </div>
          <div class="system reveal">
            <div class="system__col">
              <p class="sheader__label">Visual system</p>
              <ul class="system__swatches">{sw}</ul>
              <ul class="tags">{chips}</ul>
            </div>
            <div class="system__col">
              <p class="sheader__label">Audio system</p>
              <ul class="tags">{achips}</ul>
            </div>
          </div>
        </div>

        <!-- B · Story arc -->
        <div class="block">
          <h3 class="block__title reveal"><span class="block__tag">B</span> Story arc</h3>
          <p class="block__lead reveal">{len(d["rows"])} beats over ~{d["runtime"]} seconds. Solid = voice-over, light = music + SFX only. Tap a beat to jump to it.</p>
          <div class="arc reveal">
            <ol class="arc__track">
{arc(vid, d)}
            </ol>
            <div class="arc__scale" aria-hidden="true"><span>0s</span><span>{d["runtime"]}s</span></div>
          </div>
          <dl class="vstats reveal">{stats}</dl>
        </div>

        <!-- C · Dual-column script -->
        <div class="block">
          <h3 class="block__title reveal"><span class="block__tag">C</span> The script</h3>
          <div class="script" data-script>
            <div class="script__bar" aria-hidden="true">
              <div class="script__cols">
                <span>Time</span>
                <span>{ICON_MIC}Narration / Audio</span>
                <span>{ICON_EYE}Visual / On-screen action</span>
              </div>
              <div class="sprog">{prog}</div>
            </div>{rows}
          </div>
        </div>

        <!-- D · Why this direction -->
        <div class="block">
          <h3 class="block__title reveal"><span class="block__tag">D</span> Why this direction</h3>
          <div class="why">{why}
          </div>
        </div>
        <a class="next reveal" href="{d["next"][0]}"><span>Next</span>{html.escape(d["next"][1])}<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M8.5 3.5L13 8l-4.5 4.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
      </div>
    </section>
    <!-- {vid.upper()}:END -->
'''


def main():
    path, vid = sys.argv[1], sys.argv[2]
    s = open(path, encoding="utf-8").read()
    block = section(vid, VIDEOS[vid])
    start, end = f"    <!-- {vid.upper()}:START -->", f"<!-- {vid.upper()}:END -->\n"
    if start in s:
        a = s.index(start)
        b = s.index(end) + len(end)
        s = s[:a] + block + s[b:]
    else:
        m = re.search(r"    <!-- Sections (\d\d)–05 are added one by one after review\. -->", s)
        assert m, "placeholder not found"
        nxt = f"{int(m.group(1)) + 1:02d}"
        s = s.replace(m.group(0), block + "\n" + m.group(0).replace(m.group(1) + "–05", nxt + "–05"))
    open(path, "w", encoding="utf-8").write(s)
    print("ok", vid)


if __name__ == "__main__":
    main()
