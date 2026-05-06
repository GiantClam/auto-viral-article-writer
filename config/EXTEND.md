# Image generation preferences
default_provider: openai-compatible
default_quality: 2k
default_aspect: 16:9
default_model:
  gemini: gemini-3.1-flash-image-preview
  openai: gpt-image-2
  openai_compatible: gpt-image-2

openai_compatible:
  # Set OPENAI_COMPATIBLE_BASE_URL and OPENAI_COMPATIBLE_API_KEY in config/.env
  base_url: https://your-openai-compatible-base-url
  default_size: 1536x1024
  default_quality: high
  default_n: 1
