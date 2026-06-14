# cover-image

## Purpose

Generate a polished article cover image aligned with the package's article workflow.

## Use Cases

- cover generation for a completed article
- reference-photo-based thumbnail composition
- WeChat article cover with 10 composition style options

## Trigger Examples

- `生成封面`
- `文章封面`
- `cover image`

## Inputs

- article path or slug
- optional explicit title
- reference image path (defaults to `img/20260423-140003.jpg` if not provided)
- style: 10 composition styles (see below)

## Outputs

- final cover image in `output/images/wechat/{slug}-cover-final.png`

## 10 Composition Styles

| # | Style | Best For |
|---|--------|---------|
| 1 | **深色渐变风** | 人物居中，大字覆盖后方，深色渐变背景，高对比强冲击 |
| 2 | **纯色扁平风** | 人物抠图感，纯色背景，干净清爽 |
| 3 | **产品主视觉风** | UI截图/产品占主体，人物做引导手势 |
| 4 | **对比卡片风** | 前后对比、好坏对比，人物手持两张卡片推向镜头 |
| 5 | **极简留白风** | 大面积留白，标题是唯一焦点，克制感强 |
| 6 | **海报拼贴风** | 多张素材叠加，有前中后景纵深，叙事丰富 |
| 7 | **人物侧置留白风** | 人物偏一侧，另一边全给标题，版面大气 |
| 8 | **背影构图风** | 人物背对镜头，适合励志、启发类内容 |
| 9 | **局部出镜风** | 只露手或半张脸，产品是绝对主角 |
| 10 | **正面对视风** | 人物直视镜头，眼神接触，情绪直接强烈 |

## Workflow (Ask One Question at a Time)

1. Ask which style (1-10)
2. Ask if they have a face reference photo
3. Ask expression (skip for Style 8 背影构图风)
4. Ask if they have extra materials (product screenshots etc.)
5. Ask background color
6. Ask font style
7. Ask font color effect
8. Ask for title confirmation or modification
9. Generate prompt from selected style template
10. Call `tools/nanobanana_client.py --openai-compatible-image --ref <path>`

## Generation Pathways

| Situation | Endpoint | Notes |
|---|---|---|
| `--article-title` alone | `generations` | Best text rendering; uses built-in portrait prompt |
| `--ref` (img2img) | `edits` | Max likeness when title written directly in `--prompt` |
| Custom `--prompt` + `--ref` | `edits` | Best balance of likeness + title legibility |

## Reference-Photo Prompt Rule

When using `--ref`, prompt for editorial recomposition rather than pasted placement.

Good prompt traits:
- preserve identity from reference photo
- recompose into a half-body editorial portrait
- naturally integrated lighting and depth
- explicit negatives for `collage`, `cutout edge`, and `sticker effect`

If the provider call fails, treat it as a provider/auth/endpoint issue first. Do not silently swap in a locally pasted photo and present it as generated output.

## Artifact Convention

Prefer the same slug family as the brief and article draft, for example `output/images/wechat/{slug}-cover-final.png`. If a brief or draft already exists, inherit its slug exactly.

## Boundary

This skill is for the hero cover image, not for inline article illustrations.

## Prompt Templates

Each of the 10 styles has its own full prompt template. See the main SKILL.md for the complete Chinese-language prompt templates for all 10 styles.
