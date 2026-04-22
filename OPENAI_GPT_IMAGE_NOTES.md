# OpenAI GPT Image backend notes

## What was verified
- Fork created: `techkwon/papervizagent`
- Upstream kept as: `google-research/papervizagent`
- Branch: `feat/openai-gpt-image-2-backend`
- Local test key source: `Documents/MyApps/teacher-ai-classroom/.env.local`
- Live API verification succeeded with:
  - `gpt-image-2`
  - `gpt-image-2-2026-04-21`

## Recommended image model
Use the dated model first for reproducibility:
- `gpt-image-2-2026-04-21`

Fallback / floating latest alias:
- `gpt-image-2`

Other available image models observed in the account:
- `gpt-image-1`
- `gpt-image-1-mini`
- `gpt-image-1.5`
- `chatgpt-image-latest`

## Local config
`configs/model_config.yaml` is gitignored and currently set to:
- `model_name: gpt-4.1-mini`
- `image_model_name: gpt-image-2-2026-04-21`

API key is intentionally left blank in that file. Supply it via env:
- `OPENAI_API_KEY`

## What changed
1. `configs/model_config.template.yaml`
   - Added explicit OpenAI example comments.
2. `demo.py`
   - `refine_image_with_nanoviz(...)` now supports both:
     - Gemini image models via `generate_content`
     - OpenAI GPT Image models via `images.edit`

## Important caution
- The main diagram generation path already had `gpt-image` support in `agents/visualizer_agent.py`.
- The main missing piece was the refine/edit path in the Streamlit demo.
- This patch does **not** rename the product or imply it is an official Google/OpenAI release.

## Suggested next smoke test
From repo root:
```bash
export OPENAI_API_KEY="..."
streamlit run demo.py
```
Then check:
1. candidate generation with `gpt-image-2-2026-04-21`
2. refine tab image editing with a simple uploaded image
3. whether any Gemini-only assumptions remain in UI copy
