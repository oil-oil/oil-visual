---
name: oil-visual
description: "制作统一漫画墨线风格的解释图与透明插画素材，可单独绘制眼镜线条人物、暖黄色牧羊犬、两者组合，或同风格的物件与装饰元素。当用户需要概念、机制、流程、对比的完整解释画面，或可复用的排版插图时使用；不用于普通代码图表、照片处理或无关品牌视觉。"
---

# Oil Visual

Create raster visuals in one shared manga-ink language. Choose one output mode before generating; do not mix the two production paths.

## Choose the output mode

### Mode A — explanatory image

Use when the image must explain a concept, mechanism, workflow, comparison, or tradeoff by itself.

- Deliver a complete PNG or WebP with a finished off-white scene.
- Generate every essential title and label directly inside the bitmap.
- Make the relation visible through objects, paths, states, or repeated materials; labels identify the evidence but do not replace it.
- Do not generate an unlabeled base and add essential words in a separate rendering step.

### Mode B — transparent illustration

Use when a character, object, or decorative illustration will be composed into a hero, document, card, slide, or other layout.

- Request a genuinely transparent PNG when the selected generator supports native alpha. Otherwise use a perfectly uniform chroma-key background that does not occur in the artwork. Default to `#00FF00`; use `#FF00FF` when the subject contains green.
- Do not include explanatory labels unless the user explicitly requests text inside the illustration.
- Preserve native alpha when it is clean. For a chroma-key source, remove the background with the bundled `scripts/cutout.py`. Deliver a transparent PNG in either case.
- Keep the transparent artwork as a reusable visual asset; the surrounding layout supplies the title and explanatory copy.

If the destination is unclear, choose Mode A when the image itself must communicate the idea and Mode B when another layout will carry the explanation.

## Shared visual language

- Draw confident black manga/comic ink outlines with varied line weight and restrained circular halftone screentone.
- Treat the recurring characters as optional subjects, not a required pair. When a person is selected, draw the minimal stick-figure protagonist with a round head, thin round glasses, dot eyes, a simple smile, and thin line-drawn limbs; when a dog is selected, draw the chubby warm-yellow Border Collie. Select characters only when requested or when they visibly help explain the claim; never add them merely to signal the style.
- For object-only artwork, carry the same style through clear silhouettes, varied ink line weight, restrained circular halftone, and simple material details. Do not add a person, dog, or face to make an object feel on-brand.
- When characters are present, keep them secondary to the subject's evidence or action unless the character itself is the requested subject.
- Use black, white, and halftone gray as the base. Use warm yellow for the dog when present; without the dog, warm yellow may appear as a small light patch or sparse star accent, but is not required.
- Add at most two muted semantic colors. Common mapping: blue = input/content, orange = action/warning/cost, purple = process, green = successful result.
- Avoid 3D, glossy gradients, photorealism, wobbly sketch lines, generic card grids, dashboards, unrelated clutter, and watermarks. Deliberately requested decorative elements are valid subjects.

## Mode A workflow — explanatory image

### 1. Write the visual brief

```text
viewer_question: what should be understood in 10 seconds?
concrete_claim: one-sentence conclusion
real_objects: visible objects, interfaces, documents, tools, or states
relation: comparison, transformation, causality, sequence, hierarchy, feedback, tradeoff, or pipeline
visual_evidence: what must remain understandable when labels are ignored?
scene: believable setting and 2–4 useful environmental cues
semantic_colors: what each accent color means
labels: exact short strings plus the evidence surface for each label
```

Show the input, action or relation, and result. Keep one dominant focal action and no more than three major visual regions. For multiple steps, use a simple left-to-right or top-to-bottom sequence.

### 2. Design the labels

- Prefer 2–6 labels. Use more only when the explanation truly needs them.
- Keep each label short and concrete: role, action, state, or outcome.
- Place every label on or immediately beside its evidence surface, such as a desk nameplate, task sheet, folder tab, machine, meter, lane, or result document.
- Use modern Chinese sans-serif typography, medium or bold, large enough to read at the intended display size.
- Do not turn body copy, commands, tables, or long paragraphs into image text. Use a deterministic layout method when dense or editable text is required.

Add this block to the generation prompt:

```text
Text (verbatim): Render these exact labels as part of the bitmap illustration:
"<label 1>", "<label 2>", "<label 3>".
Use each phrase exactly once. Do not translate, paraphrase, misspell, repeat,
or add any other text. Use modern sans-serif medium/bold typography, large
and readable. Place "<label 1>" on <evidence surface>; place "<label 2>" on
<evidence surface>; place "<label 3>" on <evidence surface>.
```

### 3. Build the prompt

Use this order:

1. State the concrete claim and shared task.
2. Describe the real setting, selected subjects, and any action. Include the protagonist or dog only when requested or when they visibly help explain the claim.
3. Describe the evidence objects and their geometry: aligned, nested, connected, split, transformed, repeated, or converging.
4. Assign semantic colors.
5. Quote the exact labels and specify each placement.
6. Add the Mode A style anchor.
7. End with exclusions.

Mode A style anchor:

```text
Professional editorial manga/comic ink illustration. Clean confident black ink outlines with varied line weights, expressive but controlled. Use classic circular halftone screentone for gray and shadow areas. Render only the selected characters and objects; do not add a protagonist or dog automatically. Use an off-white lightly textured real environment, not a blank white canvas. Typography is modern sans-serif, medium or bold, large and readable. Color is restrained: black, white, halftone gray, warm yellow when useful, plus at most two muted semantic accent colors. No 3D, no glossy gradients, no photorealism, no generic card grid, no dashboard, no unrelated clutter, no tiny text, no long paragraphs, no watermark.
```

### 4. Inspect and retry

1. Inspect the output at original resolution.
2. Compare every label with the brief character by character. Confirm that each appears exactly once and that no stray text was added.
3. Reject missing, duplicated, invented, or misspelled labels.
4. Regenerate with one targeted correction while repeating all scene and style invariants. Do not conceal an error with a separate text layer.

Use this retry instruction:

```text
Keep the scene, composition, characters, objects, colors, and all correct labels unchanged.
Change only the incorrect text "<wrong>" to the exact text "<right>".
Do not add, remove, translate, or repeat any other text.
```

## Mode B workflow — transparent illustration asset

### 1. Select the subject

Identify exactly which subjects are requested: the person alone, the dog alone, both together, or an object or decorative element without characters. Describe one clear action when an action is needed, and include only the props needed to establish it. For a standalone object, describe its shape, material, and distinguishing details instead. Leave generous padding around the artwork so the cutout can be composed safely.

### 2. Build the prompt

Describe the selected subjects first. State explicitly that no unrequested person, dog, face, or prop should appear. Then append the fixed style anchor and one background rule below.

```text
Style: professional manga/comic ink illustration. Clean confident ink outlines
with varying line weights, thick for contours and thin for details, not wobbly
or sketchy. Use classic circular halftone screentone dot patterns for gray and
shadow areas. Give characters and objects the same clear silhouette and ink
language. Color usage is extremely restrained: mostly black, white, and gray
halftone; warm yellow on the dog when present, or as an optional small light
patch or sparse star accent when the dog is absent. Use no more than two muted
semantic accent colors. Render only the requested subjects.
Do not let halftone, ink, props, or the subject touch the image border. Keep
generous padding. No text, no watermark. PNG format.
```

Use this background rule when the generator supports genuine transparency:

```text
Render on a genuinely transparent background with a clean alpha channel.
No backdrop, floor plane, cast shadow, or opaque pixels outside the artwork.
```

Otherwise replace `<KEY_COLOR>` with the selected hex color and use this rule:

```text
The background must be a perfectly uniform flat <KEY_COLOR> rectangle with zero
gradient, texture, noise, speckles, shadows, floor plane, or lighting variation.
```

### 3. Validate the source

- Inspect the image before removal.
- For native alpha, confirm the image is RGBA, all four corners have alpha `0`, and no opaque background or edge residue remains. Keep the alpha intact; do not run the cutout script.
- For a chroma-key source, confirm all four corners are uniform and visually match the chosen key color. Reject backgrounds with gradients, texture, shadows, speckles, or artwork touching the border.
- Preserve a chroma-key source alongside the transparent result until the output is approved.

### 4. Remove a chroma-key background only

Skip this step for clean native-alpha output. For a uniform chroma-key source, install Pillow if the active Python environment does not have it, then run:

```bash
python3 scripts/cutout.py source.png transparent.png
```

Optional tuning:

```bash
python3 scripts/cutout.py source.png transparent.png \
  --transparent-threshold 12 \
  --opaque-threshold 220
```

The script samples the image border, builds a soft alpha matte from color distance, and removes color spill from antialiased edges. It works with any uniform key color, so the key can be chosen to avoid the subject palette.

### 5. Validate the transparent result

- Confirm the output is RGBA and all four corners have alpha `0`.
- Confirm every requested subject remains complete. Check glasses and thin limbs for a person, ears and tail for a dog, and narrow contours or small details for an object.
- Check for a gray fringe at 100% zoom.
- Confirm internal white and halftone areas were not erased.
- Regenerate the source instead of forcing the algorithm when the background is visibly uneven.

## Output handling

- Save approved project assets inside the current project or output directory.
- Do not leave project-referenced images only in the generator's default storage.
- Use versioned filenames instead of overwriting an approved asset unless the user explicitly requests replacement.
- Report the final prompt, output mode, final image path, and the transparency path used. Include the chroma-key source path and any non-default cutout options when cutout was needed.

## Quality gate

For every output:

- The subject is recognizable in about 3 seconds.
- When the output explains something, the main action or relation is clear in about 10 seconds.
- Only requested characters appear; when present, they serve the subject rather than becoming generic decoration.
- Line work and halftone remain consistent; warm yellow and semantic accents follow the selected subjects and meaning.

For Mode A:

- One claim, one focal action, and no more than three major visual regions.
- The visual evidence still shows the relation when labels are ignored.
- Every required label is exact, appears once, and is integrated into the correct evidence surface.
- All labels remain readable at the intended display size.

For Mode B:

- The output has real transparency, whether supplied natively or produced by clean background removal.
- Thin details and internal halftone regions remain intact.
- No source background, fringe, shadow, or border artifact remains.
