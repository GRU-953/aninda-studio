<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Copyright 2026 Aninda Sundar Howlader -->
# The Aninda Studio Figma plugin

This plugin builds the Aninda Studio library inside a Figma file: the variables,
the styles, the marks, a small set of components, and one frame for each of the
30 cards in the system.

**Written documentation licence:** PolyForm Noncommercial 1.0.0.
**Code and tokens licence:** Apache-2.0. See `NOTICE` for the split.

---

## What it cannot do, said plainly

- **It cannot produce a `.fig` file.** Figma's file format is proprietary and
  closed, so no program outside Figma can write one. A plugin is the only way to
  put this system into Figma without drawing it by hand.
- **It cannot use the Figma REST API instead.** The Variables REST API needs an
  Enterprise plan even to read, and the REST API has no way to create a node at
  all. Checked against Figma's own documentation on 14 August 2026.
- **It cannot install fonts.** The three families have to be on your computer
  before you run it. It checks first and stops before making anything if one is
  missing, so a half-built library is not a state you can end up in.
- **It cannot guess the plugin id or the api version.** Figma issues both and
  publishes neither, so the build refuses to finish until you have copied them
  from a manifest Figma itself wrote. Step 2 below is that copy.
- **It does not know what your Figma plan allows.** Whether the Variables API
  works, and how many modes a collection may hold, are not documented facts I
  can look up. The plugin asks the file at run time and tells you the answer.

---

## Before you start

You need three fonts installed on your computer:

| Family | Style | Where it comes from |
| --- | --- | --- |
| Literata | Regular | The Latin text face. SIL Open Font License 1.1. |
| Noto Serif Bengali | Regular and Medium | The Bangla text face. SIL Open Font License 1.1. |
| Aninda Mono | Regular | The monospaced face. It is a renamed subset of IBM Plex Mono, because `IBM Plex` is a Reserved Font Name and a subset counts as a modification under the licence. |

Figma reads fonts your operating system has installed. The `.woff2` files in
this project are for the web and will not install as system fonts, so you need
an installable `.ttf` or `.otf` of each. If `Aninda Mono` is not installed under
exactly that name, the plugin stops and says so.

---

## Step by step

Every step is one action. If something does not match what you see, stop and
tell me — I would rather fix the instructions than have you guess.

### 1. Build the plugin files

1. Open the Terminal app.
2. Type `cd /Users/gru953/Claude/Cowork/Aninda_Studio/13_plugins/figma` and press Return.
3. Type `node build.mjs` and press Return.
4. Read what it prints. The first time, it will stop and say the manifest has
   not been adopted yet. That is expected. Go to step 2.

### 2. Copy the two values only Figma can give you

1. Open the Figma **desktop** app. The browser version cannot load a plugin from
   your computer.
2. Open any design file, or make a new one.
3. Click the Figma menu at the top left.
4. Click **Plugins**.
5. Click **Development**.
6. Click **New plugin...**.
7. In the window that opens, type the name `Aninda Studio`.
8. Choose **Figma design** as the editor type.
9. Click **Next**.
10. Choose the **Empty** template.
11. Click **Save as**, choose your Desktop, and click **Save**.
12. Figma has now written a folder on your Desktop with a `manifest.json` inside
    it. Note where it is.
13. Go back to Terminal.
14. Type `node scripts/adopt-scaffold.mjs ` — with a space at the end — then
    drag the `manifest.json` file from that folder onto the Terminal window,
    which types its path for you. Press Return.
15. It prints the `id` and the `api` it copied. Both are now recorded in
    `scripts/figma-api-version.txt` with today's date.

### 3. Build again

1. In Terminal, type `node build.mjs` and press Return.
2. It should finish with `Build finished.` and print the id and api it found.

### 4. Load the plugin into Figma

1. Go back to the Figma desktop app.
2. Click the Figma menu at the top left.
3. Click **Plugins**.
4. Click **Development**.
5. Click **Import plugin from manifest...**.
6. Find `13_plugins/figma/manifest.json` — the one in this folder, not the one
   on your Desktop — and click **Open**.

### 5. Check what your file allows, before changing anything

1. Open the Figma file you want the library to live in. A new, empty file is the
   safest place to start.
2. Click the Figma menu, then **Plugins**, then **Development**, then
   **Aninda Studio — build the library**, then **Probe what this file allows**.
3. Click **Start**.
4. Read the Probe list. It tells you whether variables work here, how many modes
   a collection may hold, and whether every font is present. Nothing has been
   created or changed.

### 6. Build the library

1. In the same plugin window, choose **Build the library**.
2. Click **Start**.
3. Wait. On a fresh file this takes a minute or two, most of it the 30 card
   frames.
4. When it finishes, read the Receipt table.

### 7. Check the receipt against what was expected

The **Expected** column comes from `RECEIPT-EXPECTED.json`, which `build.mjs`
wrote from the same code the plugin ran. A row where the two numbers agree is
shown in green; a row where they differ is shown in red and bold.

Anything the plugin could not do appears under **Skipped, with the reason**.
There is no silent omission: if a thing is not in the file, its reason is in
that list.

If a number is red, click **Copy the whole receipt** and send it to me.

### 8. If you want to undo it

1. Open the plugin again.
2. Choose **Remove everything this plugin made**.
3. Click **Start**.

It removes only items carrying this plugin's own tag. Anything you drew
yourself, and any page still holding your own work, is left alone and reported
as skipped.

---

## Using a different set of tokens

The token files are compiled into the plugin when you run `node build.mjs`, so
it works with no internet connection. To try a different set without rebuilding,
paste one JSON object into the **Use different tokens** box:

```json
{
  "primitive": { },
  "semantic": {
    "light": { },
    "dark": { },
    "hc-light": { },
    "hc-dark": { }
  }
}
```

All four themes must be present and must hold identical token paths. If one is
missing, the plugin says which and makes nothing.

---

## What gets made

| Thing | How many | Notes |
| --- | --- | --- |
| Variable collections | 2 | `Primitives` with one mode, `Theme` with four. |
| Variables | 127 | 110 primitives, 17 semantic roles. |
| Variable aliases | 40 | Ten roles across four themes point at a primitive rather than repeating its value. |
| Paint styles | 17 | One per semantic role, bound to the `Theme` variable so it follows the mode. |
| Text styles | 16 | Seven Latin, seven Bangla, two monospaced. |
| Effect styles | 1 | The focus ring. |
| Grid styles | 2 | A twelve-column layout and an 8 px square grid. |
| Marks | 10 | Every SVG in `04_mark/svg`, plus a two-weight `Mark` component set. |
| Components | 11 | Button, Input and Badge as variant sets, and a Card. |
| Card frames | 30 | One per card in `08_components/_cards.json`. |
| Pages | 3 | Marks, Components, Cards. |

Some things are deliberately not made, and the receipt says so each run:

- **No paint styles for the 66 ramp steps.** They are variables. A designer
  should reach for `Theme/Ink/Default`, which follows the theme, not for a fixed
  ramp step, which does not.
- **No elevation or shadow styles.** The token set has no shadow token, and
  inventing blur radii here would put numbers in the library the system never
  agreed to.
- **No line height on the Latin and monospaced text styles.** The token set
  defines a line height for Bangla only, so Figma's automatic setting is used.
- **No Bangla on 25 of the 30 card frames.** `BANGLA-STANDARD.md` holds a
  verified string for the others and none for these. Writing new Bangla to fill
  the space is not allowed, so the frame says so on its face.

---

## If it goes wrong

**"These fonts are not installed"** — install the families in the table above,
quit Figma completely, reopen it, and run the plugin again. Figma reads the font
list once at start-up.

**"Variables: not available"** — the plugin carries on in styles-only mode. Each
of the four themes becomes its own set of plain paint styles, named
`Light/Ink/Default` and so on, instead of one set that follows a mode. The
receipt says this happened and why.

**"Modes per collection: 1"** — your Figma plan allows one mode per collection,
so only the Light theme was written into the `Theme` collection. The other three
appear under Skipped with that reason.

**The build says the manifest is not adopted, after you adopted it** — check you
ran `adopt-scaffold.mjs` in this folder and not in a copy. The file it writes is
`13_plugins/figma/manifest.json`.

---

## For the record

- `manifest.json` is not committed. It holds an id issued to one person, and a
  committed one would let the build pass with a value nobody checked.
- `dist/` **is** committed, because Figma loads the built JavaScript and asking
  the owner to run a build before opening Figma is one more place to get stuck.
  Continuous integration rebuilds it and fails if it differs from what is
  committed, so the two cannot drift apart.
- Nothing generated here carries a date or a timestamp. Every artefact is a pure
  function of the token files, so a rebuild that changes nothing produces a
  byte-identical file and the comparison means something.
