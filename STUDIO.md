# STUDIO.md — Workflow 4: the studio (marketing films, stills and slides)

This file is the full routine for **Workflow 4** in `AGENTS.md`. Use it when someone asks for a marketing piece: a launch or product
film, a short clip for social, a slide deck, the images for a store listing or a launch gallery, a video cover.

The template ships **no studio**. Nothing in `studio/` exists until the first piece is asked for. The first time, the agent sets the
studio up from §2 below; after that, every new piece starts from the last one.

---

## 1. The rules (they never change)

1. **Source only. No video in git.** A film is code: HTML, CSS and SVG scenes driven by JavaScript, plus scripts for its sound. Every
   frame and every mix re-renders from the source. `studio/.gitignore` blocks videos, frames, previews, caches and render output.
2. **Published videos are links.** Every video that is uploaded gets a row in `studio/videos.md`: link, version, length, visibility,
   the source it came from and the command that re-renders it.
3. **Every published asset has its source in `studio/`.** That includes covers, thumbnails, posters and store images. Never build one
   in a scratch or temp folder: when the scratch folder is cleared, the asset can no longer be changed.
4. **No machine-only paths.** No absolute path to one person's Mac in any script. Tools are pinned in `studio/package.json`; anything
   that lives outside the repo (a browser build, a sample library, a sound font) is read from an environment variable with a
   documented default, and the film's README says how to get it.
5. **Licensed media is never committed** unless its licence allows passing it on. Sample libraries (Logic Pro, GarageBand), sound
   fonts and stock files are read from where they are installed. Record each source and its licence in the film's README.
6. **Words and facts come first.** `docs/marketing/brand.md` (positioning, voice, claims we make and don't) and the current `docs/`
   win over any film or slide. Every piece passes the honesty rules (§4) before it is published.
7. **Only the founder publishes.** An agent may prepare an upload, but it stays **private** until the founder says otherwise.

---

## 2. First use — set up the studio

Do this once, on a branch, the first time a piece is asked for. Create only what the first piece needs; the rest is added when a
piece needs it.

```
studio/
├── README.md            the rules (§1), what's here, requirements, how to make a new piece
├── .gitignore           §2.1
├── package.json         pins the renderer (§2.2)
├── videos.md            every rendered and published video (§2.3)
├── design-system/       the shared look (§2.4): README.md, tokens.css, one file per style
├── research/            the grounding pack for marketing: 01-ground-truth.md (facts as of the work)
├── films/<slug>/        one folder per film (§3)
├── stills/              store and launch images, when they are not part of a film
└── slides/<deck>/       slide decks, when asked for
```

### 2.1 `studio/.gitignore`

```gitignore
# The studio keeps SOURCE only. Every video re-renders from its source; published videos are listed in videos.md.
*.mp4
*.mov
*.m4v
*.webm
*.mkv
*.avi
*.gif
frames/
frames*/
preview/
out/
work/
work_*/
cache/
keyframes/
review*/
stems/
*.raw
*.npy
node_modules/
package-lock.json
__pycache__/
```

Render output goes in each film's `out/`, `frames/`, `preview/` or `work/`, so the ignore list catches it. Images that are source
(a poster, a contact sheet kept for reference, approved key frames) are saved as JPEG next to the film's README, not in `out/`.

### 2.2 `studio/package.json`

```json
{
  "name": "studio",
  "private": true,
  "description": "Marketing studio: deterministic HTML/CSS/SVG films rendered to frames, then encoded with ffmpeg. See README.md.",
  "engines": { "node": ">=22" },
  "dependencies": { "playwright-core": "1.55.0" }
}
```

Scripts load it with `require(process.env.PLAYWRIGHT_CORE || 'playwright-core')`, and find the matching headless browser under
`~/Library/Caches/ms-playwright/` (install it with `npx playwright-core install chromium-headless-shell`). Pin the version: a
different browser build renders text a pixel differently, and frames stop matching.

### 2.3 `studio/videos.md`

```markdown
# Videos

Every video we have rendered or published. Videos are never committed: each one re-renders from its source (the film's folder at
the commit that last changed it). Add a row whenever a video is uploaded or replaced, and keep superseded rows. They are the history.

Uploads are **private** first. Change the visibility here when it changes on the platform.

## Published

| Film | Version | Length | Picture | Link | Visibility | Uploaded | Notes |
|---|---|---|---|---|---|---|---|

## Rendered, not published

| Film | Version | Length | Picture | Status | Notes |
|---|---|---|---|---|---|

## Re-render

(the exact commands per film)
```

### 2.4 `studio/design-system/README.md`

The design system is the rule book that makes the next piece look and sound like the last one. Write it from the first approved
film, not before. Sections:

1. **The mark and the wordmark**: the SVG, the face, what may and may not animate.
2. **The cast**: how people (and any other characters) are drawn. No photos, no stock faces.
3. **Colour has a job**: each accent means one thing. Copy the values from the product's own design system into `tokens.css`.
4. **Type**: the faces and their jobs, minimum sizes (a product fact stays readable in a 600 px wide embed).
5. **Honesty rules**: §4 below, made specific to the product.
6. **Product fragments, not screens**: show stylised pieces of the real UI, never a full screen recording, never a cursor.
7. **Motion basics**: §3.2.
8. **Sound**: §3.4.
9. **Formats and delivery**: §5.
10. **The styles**: one line per style, its reference film, and when to use it.

Each style gets its own `style-<x>.md`: look, type, colour jobs, motion vocabulary, fragments, film structure, sound, do and don't,
reference frames, checklist. A style may narrow the shared rules; it never breaks them.

---

## 3. A film

### 3.1 The folder

```
films/<slug>/
├── README.md              what it is, status, what's here, requirements, commands
├── story.md               the brief (top) and the beat sheet: beats, times, picture, on-screen words, narration
├── narration-script.md    each line with its start and finish-by time, the voice, pronunciation notes
├── poster.jpg             reference images (contact sheet, storyboard) as JPEG
├── film/                  the picture
│   ├── CONTRACT.md        the scene contract (§3.2)
│   ├── index.html, engine.js, timeline.json
│   ├── shared/            kit.js (every on-screen string and sample name lives here), base.css, glyphs
│   ├── scenes/            one module per scene
│   ├── tools/runner.mjs   static server + headless browser launch, shared by preview and render
│   ├── preview.mjs, render.mjs, encode.sh
│   └── stills/            launch images built from the same kit (§5), when the film has them
└── audio/
    ├── tools/             score, effects, narration placement, mix, analysis
    ├── cues/              motion cues read from the scene code
    └── narration/         the voice clips (source: a take cannot be regenerated exactly)
```

If an earlier film exists, **copy the closest one** and keep its engine and kit. Replace the story strings, the timeline and the
scenes. Build the engine from scratch only for the first film.

### 3.2 The scene contract

- **Every frame is a pure function of time.** `render(root, t, dur)` sets every visual property from `t` alone. No CSS transitions
  or animations, no wall clock, no unseeded randomness. This is what lets any frame re-render exactly, at any resolution.
- `timeline.json` holds each scene's start, end, key-frame time (`keyT`), captions and transitions. Times are film time.
- A scene module registers `{ id, mount, render }`, builds its DOM in `mount`, and prefixes every id and class with its scene id.
- 1920×1080 CSS pixels at 60 fps. A 4K master renders the same layout at 2× device pixels.
- Every move eases, things arrive staggered, one focal point at a time. Match cuts by default; one hard cut per film at most.
- `preview.mjs` gives: `--lint` (load every scene, check caption hold times), `--keyframes --sheet` (one finished frame per beat),
  `--scene <id> --t <times> --sheet` (one scene, many moments), `--serve` (scrub in a browser).
- `render.mjs` writes numbered frames and is resumable; `encode.sh` turns frames into H.264 with ffmpeg.

### 3.3 Steps (with the founder's approval points)

1. **Brief.** Agree four things before building: who it is for and where it runs, its length, the one message, the style. Write
   them at the top of `story.md`. *(Founder approves.)*
2. **Ground.** Read `docs/marketing/brand.md`, `studio/research/01-ground-truth.md`, the current `docs/`, the design system and the
   style file. Check each fact against the product on the day.
3. **Story.** Write the beat sheet. Check every line against §4. *(Founder approves.)*
4. **Key frames.** Build each scene far enough to render one finished frame at its `keyT`, and make a contact sheet.
   *(Founder approves the frames before any motion is built.)*
5. **Build and render silent.** Animate around the approved frames. Lint and verify as you go. Render a 1080p review copy.
   *(Founder reviews.)*
6. **Sound** (§3.4).
7. **Master.** Render the final picture (4K when the platform rewards it) and encode it with the final mix.
8. **Publish.** Prepare the upload as **private**. Add the row to `studio/videos.md`. *(Only the founder makes it public.)*
9. **Commit the source** on a branch and open a pull request. Prefix `Studio:`; say what the piece is and why in the body.

### 3.4 Sound

The picture is always rendered silent first. The sound is code next to it, so it re-renders like the picture.

- **Cues.** Read the motion cues out of the scene code into `audio/cues/*.json`: time, kind (landing, press, switch, flight, light,
  typing…), weight, on-screen x.
- **Score.** Written in code (`music.py` or similar) from synthesis plus installed instruments (see §1 rule 5). Tempo locked to the
  film's bars, so cuts land on beats. Calm and warm by default: no risers, drops or "epic" swells unless the style says so.
- **Effects.** One short sound per cue, panned by its x, tuned to the score's key, ridden 3–9 dB under the music. Slow drifts stay
  silent.
- **Narration.** Write and time the script first (a calm read is about 2.3 words a second). Generate the voice with a text-to-speech
  tool, export each line as a WAV, and place each line by its start time. Commit the clips.
- **Mix.** −14 LUFS integrated, true peak at or below −1 dBTP. The voice sits about 10 dB over the bed; the music dips under each line
  only as much as it needs. The music ends in silence with the last fade.

---

## 4. Honesty rules

A film, a slide or a store image is a public claim, just like the website. Before anything is rendered for real:

- Check every claim against `docs/marketing/brand.md` and the product as it is on the day. If the product does not do it today, the
  piece does not show it.
- Every name, client and number in a product fragment is **sample data**, kept in one place per film (the kit) and labelled as
  sample data where it could be mistaken for real.
- No vendor or partner logos unless there is written permission. Name integrations in text.
- No invented testimonials, ratings, user counts or press quotes.
- No hype or superlatives: "first", "only", "best", "#1", "revolutionary", "game-changing".
- No claim we can't prove today: user counts, ratings, "trusted by", time or money saved.

Write the product-specific version of these rules into `studio/design-system/README.md` §5 when the studio is set up.

---

## 5. Formats

| Output | Spec |
|---|---|
| Film master | 3840×2160 (or 1920×1080), 60 fps, H.264, AAC, −14 LUFS. Upload 4K when the platform gives 4K uploads better encodes (YouTube does) |
| Review copy | 1920×1080, CRF 18–26, local only |
| Share copy | a small 1080p file (around 20 MB) for chat apps and social posts |
| Video cover | 1280×720 JPEG, under 2 MB, readable at thumbnail size |
| Launch gallery | the platform's current size (check it on the day; Product Hunt has used 1270×760) |
| Store listing | the store's current sizes (the Chrome Web Store uses 1280×800 screenshots, a 440×280 small tile, a 1400×560 marquee) |
| Slides | 1920×1080 HTML slides |

Stills are rendered from HTML with the same kit as the film, so type and colour match. Flatten them to RGB without alpha when the
store asks for it, and check the smallest text against the design system's minimum size.

---

## 6. Moving an existing film in

If a film was built somewhere else first (a scratch workspace), move it in as source:

1. Copy the picture, the sound scripts, the narration clips, the docs and the reference images. Leave frames, previews, stems and
   videos behind.
2. Replace every machine-only path (§1 rule 4).
3. **Check the move.** Render a few frames from the new place and compare them byte for byte with frames rendered before the move;
   rebuild the sound and compare the mix. Write the result in the commit body.
4. Add every published video to `videos.md`.
