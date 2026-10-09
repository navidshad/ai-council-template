# STUDIO.md — Workflow 4: the studio (marketing films, stills and slides)

This file is the full routine for **Workflow 4** in `AGENTS.md`. Use it when someone asks for a marketing piece: a launch or product
film, a short clip for social, a slide deck, the images for a store listing or a launch gallery, a video cover.

The template ships **no studio**. Nothing in `studio/` exists until the first piece is asked for, and then only what that piece needs
is created.

## How the studio is built: foundation → design kits → design cases

| Layer | What it is | Where |
|---|---|---|
| **Foundation** | What every piece shares, whatever it looks like: the mark, the brand colours and type, the honesty rules, the formats, and the machinery that renders and mixes | `studio/foundation/`, `studio/tools/` |
| **Design kit** | One complete look built on the foundation: its rules, its tokens, its reusable parts (cast, product fragments, stage, transitions, sound palette) and a kit sheet that shows it all on one page. A studio can have **several kits** | `studio/kits/<kit>/` |
| **Design case** | One piece made with one kit: a film, a set of store images, a cover, a deck. It holds only what is special to that piece: the brief, the story, the scenes, the strings, the narration | `studio/cases/<case>/` |

Work always goes in that order. **A case never starts before its kit exists and is approved.** A case uses its kit's parts; it does
not copy them. When a case needs a part the kit does not have, the part is added **to the kit**, so the next case can use it.

---

## 1. The rules (they never change)

1. **Source only. No video in git.** A film is code: HTML, CSS and SVG driven by JavaScript, plus scripts for its sound. Every frame
   and every mix re-renders from the source. `studio/.gitignore` blocks videos, frames, previews, caches and render output.
2. **Published videos are links.** Every upload gets a row in `studio/videos.md`: link, version, length, visibility, the case it came
   from and the command that re-renders it.
3. **Every published asset has its source in `studio/`.** Covers, thumbnails, posters and store images too. Never build one in a
   scratch or temp folder: when that folder is cleared, the asset can no longer be changed.
4. **No machine-only paths.** No absolute path to one person's computer in any script. Tools are pinned in `studio/package.json`.
   Anything outside the repo (a browser build, a sample library, a sound font) is read from an environment variable with a
   documented default, and `studio/README.md` says how to get it.
5. **Licensed media is never committed** unless its licence allows passing it on. Sample libraries, sound fonts and stock files are
   read from where they are installed. Record each source and its licence in the kit's README.
6. **Words and facts come first.** `docs/marketing/brand.md` and the current `docs/` win over any kit or case. Every case passes the
   honesty rules (§5) before it is published.
7. **Only the founder publishes.** An agent may prepare an upload, but it stays **private** until the founder says otherwise.

---

## 2. First use — set up the studio

Do this once, on a branch, the first time a piece is asked for.

```
studio/
├── README.md          the rules (§1), the three layers, the kits and cases list, requirements, how to make a new piece
├── .gitignore         §2.1
├── package.json       pins the renderer (§2.2)
├── videos.md          every rendered and published video (§2.3)
├── foundation/        §3
├── tools/             §3.2: render, preview, encode, stills, audio mix
├── kits/<kit>/        §4: one folder per design kit
├── cases/<case>/      §6: one folder per design case
└── research/          the grounding pack: 01-ground-truth.md (the product's facts as of the work)
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

Render output goes in each case's `out/`, `frames/`, `preview/` or `work/`, so the list catches it. Images that are source (a kit
sheet, approved key frames, a poster) are saved as JPEG next to the README that names them, never in `out/`.

### 2.2 `studio/package.json`

```json
{
  "name": "studio",
  "private": true,
  "description": "Marketing studio: deterministic HTML/CSS/SVG pieces rendered to frames, then encoded with ffmpeg. See README.md.",
  "engines": { "node": ">=22" },
  "dependencies": { "playwright-core": "1.55.0" }
}
```

Scripts load it with `require(process.env.PLAYWRIGHT_CORE || 'playwright-core')` and use the matching headless browser
(`npx playwright-core install chromium-headless-shell`). Pin the version: another browser build renders text a pixel differently,
and frames stop matching.

### 2.3 `studio/videos.md`

```markdown
# Videos

Every video we have rendered or published. Videos are never committed: each one re-renders from its case (at the commit that last
changed the case or its kit). Add a row whenever a video is uploaded or replaced, and keep superseded rows. They are the history.

Uploads are **private** first. Change the visibility here when it changes on the platform.

## Published

| Case | Kit | Version | Length | Picture | Link | Visibility | Uploaded | Notes |
|---|---|---|---|---|---|---|---|---|

## Rendered, not published

| Case | Kit | Version | Length | Picture | Status | Notes |
|---|---|---|---|---|---|---|

## Re-render

(the exact commands per case)
```

---

## 3. The foundation

The foundation is built with the first kit and changes rarely. Changing it touches every kit and every case.

### 3.1 `studio/foundation/`

- `README.md`, the shared rules:
  1. **The mark and the wordmark**: the SVG, the face, what may and may not animate.
  2. **Brand colours**: copied from the product's own design system into `tokens.css`, each with its job.
  3. **Type**: the faces and their jobs, and the minimum sizes (a product fact stays readable in a 600 px wide embed).
  4. **Honesty rules**: §5, made specific to the product.
  5. **Product fragments, not screens**: show stylised pieces of the real UI, never a full screen recording and never a cursor.
     Fragment labels match the product's wording on the day.
  6. **Motion basics**: §6.2.
  7. **Formats and delivery**: §7.
- `tokens.css`: the brand colours, type and spacing as CSS variables. Kits extend it; they never redefine a brand value.
- `mark.svg`: the logo and wordmark.

### 3.2 `studio/tools/`

The machinery every kit and case uses, so no case carries its own copy:

- `runner.mjs`: a small static server and the headless browser launch.
- `render.mjs`, `preview.mjs`, `encode.sh`: render a case's frames (resumable), preview key frames and contact sheets, encode with
  ffmpeg.
- `stills.mjs`: render still images from HTML at their exact size, flatten to RGB, check the smallest text.
- `audio/`: the mixer, the narration placer, the loudness check. A kit adds its own instruments and effect palette.

---

## 4. Design kits

A design kit is one complete look. Make a new kit when a piece needs a look that the existing kits cannot give without breaking
their own rules: for example a warm, hand-made kit for team stories next to a dark, kinetic kit for product depth.

### 4.1 Make a kit

1. **Brief.** Agree with the founder what the kit is for (which kinds of cases), its feel in one line, and its name.
   *(Founder approves.)*
2. **Ground.** Read `docs/marketing/brand.md`, the product's own design system and `studio/foundation/`. A kit narrows the
   foundation; it never breaks it.
3. **Build the parts** (§4.2) as code.
4. **Kit sheet.** Render one page that shows the whole kit: the stage, the type in use, each colour with its job, the cast, every
   product fragment, a transition, and a few bars of its sound. *(Founder approves the kit sheet before any case uses the kit.)*
5. **Commit** with the prefix `Studio:` on a branch, with a pull request.

### 4.2 What a kit holds

```
kits/<kit>/
├── README.md          the look: feel, stage, type use, colour jobs, motion vocabulary, sound, do and don't, checklist,
│                      and which kinds of cases it is for
├── tokens.css         the kit's additions to the foundation tokens
├── kit.js             the reusable parts as functions of time: stage and light, cast, product fragments, captions, transitions
├── base.css
├── engine.js          the scene engine: timeline, scene mounting, render(t)
├── audio/             the kit's instruments and its effect palette (one sound per kind of motion)
├── sheet.html         the kit sheet
└── kit-sheet.jpg      the approved kit sheet
```

### 4.3 Change a kit

- Add a part when a case needs it, with a line in the kit's README.
- A kit change can change cases that are already published. Before you commit one, re-render the key frames of every case that uses
  the kit and compare them with their approved frames. If a published case changes, say so in the commit body, and either keep the old
  behaviour or tell the founder.
- Retire a kit by marking it **archived** in `studio/README.md`. Keep its folder while any case still uses it.

---

## 5. Honesty rules

A film, a slide or a store image is a public claim, just like the website. Before anything is rendered for real:

- Check every claim against `docs/marketing/brand.md` and the product as it is on the day. If the product does not do it today, the
  piece does not show it.
- Every name, client and number in a product fragment is **sample data**, kept in one place per case and labelled as sample data
  where it could be mistaken for real.
- No vendor or partner logos unless there is written permission. Name integrations in text.
- No invented testimonials, ratings, user counts or press quotes.
- No hype or superlatives: "first", "only", "best", "#1", "revolutionary", "game-changing".
- No claim we can't prove today: user counts, ratings, "trusted by", time or money saved.

Write the product-specific version of these rules into `studio/foundation/README.md` when the foundation is built.

---

## 6. Design cases

A design case is one piece made with one kit. The kinds: a **film**, a **clip** (a short cut for social), a **still set** (store
listing, launch gallery), a **cover** (video cover, thumbnail, poster), a **deck**.

### 6.1 The folder

```
cases/<case>/
├── case.md            the brief (who, where, length or sizes, the one message), the kit it uses, status
├── README.md          what's here and the exact commands
├── story.md           films and clips: the beat sheet (beats, times, picture, on-screen words, narration)
├── narration-script.md  each line with its start and finish-by time, the voice, pronunciation notes
├── strings.js         every on-screen string and sample name for this case
├── timeline.json      films and clips: each scene's start, end, key-frame time, captions, transitions
├── scenes/            films and clips: one module per scene, built from kit.js parts
├── stills/            still sets and covers: one HTML page per image, built from kit.js parts
├── audio/             cues read from the scenes, the score, the narration clips (source: a take cannot be regenerated)
└── poster.jpg         approved key frames and reference images, as JPEG
```

A new case in a kit that already has a case starts by **copying the closest case**, then replacing the brief, story, strings,
timeline and scenes. The kit and the tools are used in place, never copied.

### 6.2 The scene contract (films and clips)

- **Every frame is a pure function of time.** `render(root, t, dur)` sets every visual property from `t` alone. No CSS transitions
  or animations, no wall clock, no unseeded randomness. This is what lets any frame re-render exactly, at any resolution.
- A scene registers `{ id, mount, render }`, builds its DOM in `mount`, and prefixes every id and class with its scene id.
- 1920×1080 CSS pixels at 60 fps. A 4K master renders the same layout at 2× device pixels.
- Every move eases, things arrive staggered, one focal point at a time. Match cuts by default; one hard cut per film at most.

### 6.3 Steps (with the founder's approval points)

1. **Pick the kit.** Use an existing kit if it fits the piece. If none does, make one first (§4.1).
2. **Brief.** Agree who it is for and where it runs, its length or sizes, the one message, and the kit. Write it in `case.md`.
   *(Founder approves.)*
3. **Ground.** Check each fact against `docs/marketing/brand.md`, `studio/research/01-ground-truth.md` and the product on the day.
4. **Story** (films and clips). Write the beat sheet and check every line against §5. *(Founder approves.)*
5. **Key frames.** Render one finished frame per beat (or each still at full size) and make a contact sheet.
   *(Founder approves before any motion is built.)*
6. **Build and render silent.** Animate around the approved frames. Lint and verify as you go. Render a 1080p review copy.
   *(Founder reviews.)*
7. **Sound** (§6.4).
8. **Master.** Render the final picture (4K when the platform rewards it) and encode it with the final mix.
9. **Publish.** Prepare the upload as **private** and add the row to `studio/videos.md`. *(Only the founder makes it public.)*
10. **Commit the source** on a branch and open a pull request. Prefix `Studio:`; name the case and its kit in the body.

### 6.4 Sound

The picture is always rendered silent first. The sound is code next to it, so it re-renders like the picture.

- **Cues.** Read the motion cues out of the scene code into `audio/cues/*.json`: time, kind (landing, press, switch, flight, light,
  typing…), weight, on-screen x.
- **Score.** Written in code with the kit's instruments. Tempo locked to the film's bars, so cuts land on beats.
- **Effects.** One sound per cue from the kit's palette, panned by its x, tuned to the score's key, 3–9 dB under the music.
- **Narration.** Write and time the script first (a calm read is about 2.3 words a second). Generate the voice with a text-to-speech
  tool, export each line as a WAV, and place each line by its start time. Commit the clips.
- **Mix.** −14 LUFS integrated, true peak at or below −1 dBTP. The voice sits about 10 dB over the bed; the music dips under each line
  only as much as it needs. The music ends in silence with the last fade.

---

## 7. Formats

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
store asks for it, and check the smallest text against the foundation's minimum size.

---

## 8. Moving an existing piece in

If a piece was built somewhere else first (a scratch workspace), move it in as source:

1. **Split it.** Its look (stage, cast, fragments, engine, sound palette) becomes a kit, or joins the kit it matches. Its story,
   scenes, strings and narration become a case. Shared machinery goes to `studio/tools/`.
2. Copy only source: leave frames, previews, stems and videos behind.
3. Replace every machine-only path (§1 rule 4).
4. **Check the move.** Render a few frames from the new place and compare them byte for byte with frames rendered before the move;
   rebuild the sound and compare the mix. Write the result in the commit body.
5. Add every published video to `videos.md`.
