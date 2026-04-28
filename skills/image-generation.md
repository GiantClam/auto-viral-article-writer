# image-generation — AI Image Generation (baoyu-imagine compatible)

## Triggers
`生成图片`, `create image`, `generate image`, `AI画图`, `draw`

## Input
- `--prompt`: Image description (required)
- `--ref`: Reference image path(s), multiple supported (optional)
- `--aspect-ratio`: 16:9 / 1:1 / 4:3 / 3:4 / 9:16 (default: 16:9)
- `--quality`: normal / 2k (default: 2k)
- `--gemini-image-model`: Gemini model (default: gemini-3.1-flash-image-preview)
- `--output`: Output file path (required)
- `--use-curl`: Force requests mode (required on Windows PowerShell)
- `-v`: Verbose output

## Workflow

### Step 1 — Validate Inputs

Reference image is optional; if provided, verify file exists:
```python
import os
if ref_path and not os.path.exists(ref_path):
    raise FileNotFoundError(f'Reference image not found: {ref_path}')
```

### Step 2 — Build Command

Always use `--gemini-image --use-curl` on Windows PowerShell:

```bash
python tools/nanobanana_client.py --gemini-image --use-curl \
  --prompt "Your image description" \
  --output "output/images/xxx.png"
```

With reference photo:
```bash
python tools/nanobanana_client.py --gemini-image --use-curl \
  --ref "./your-photo.jpg" \
  --prompt "Photorealistic portrait, warm tones..." \
  --aspect-ratio 16:9 \
  --output "output/images/portrait.png"
```

### Step 3 — Execute and Parse Output

Run via subprocess, parse stdout for `Image saved:` line.

## Provider Support

| Provider | Env Variable |
|----------|-------------|
| **aiberm (default)** | `AIBERM_API_KEY` |
| **Google Gemini** | `GOOGLE_AI_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| Azure | `AZURE_OPENAI_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| DashScope | `DASHSCOPE_API_KEY` |
| MiniMax | `MINIMAX_API_KEY` |
| Replicate | `REPLICATE_API_TOKEN` |
| Jimeng | `JIMENG_ACCESS_KEY_ID`, `JIMENG_SECRET_ACCESS_KEY` |
| Seedream | `ARK_API_KEY` |

Default priority: aiberm > Google Gemini > OpenAI

## Output Format

```
Image saved: output/images/xxx.png
Size: X KB
```

## Notes

- **Windows PowerShell**: `curl` is an alias for `Invoke-WebRequest` — always use `--use-curl` flag
- Reference image is converted to base64 and passed via `inlineData` to Gemini
- Without `--ref`, no reference photo is used (pure AI generation)
- Default output directory: `output/images/`