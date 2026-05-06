#!/usr/bin/env python3
"""
Google Nano Banana Image Generation Client
Uses curl for reliable API calls
"""

import argparse
import json
import subprocess
import sys
import base64
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config_loader import load_config, validate_config


def generate_with_gemini_image(
    api_key,
    prompt,
    model="gemini-3.1-flash-image-preview",
    output_path="output.png",
    verbose=False,
    use_curl=False,
    base_url=None,
    ref_images=None,
):
    """Generate image using Gemini image generation models"""

    if verbose:
        print(f"Generating with Gemini Image...")
        print(f"  Model: {model}")
        print(f"  Prompt: {prompt[:80]}...")
        if ref_images:
            print(f"  Ref images: {ref_images}")

    if use_curl:
        return generate_with_curl(
            api_key, prompt, model, output_path, verbose, base_url, ref_images
        )

    try:
        from google import genai
        from google.genai import types

        client_kwargs = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url
        client = genai.Client(**client_kwargs)

        # Build content parts: reference images + text prompt
        from pathlib import Path
        import base64 as _b64
        parts = []
        if ref_images:
            for img_path in ref_images:
                with open(img_path, "rb") as f:
                    img_data = f.read()
                ext = Path(img_path).suffix.lower()
                mime = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
                b64 = _b64.b64encode(img_data).decode()
                parts.append(types.Part(inline_data=types.Blob(mime_type=mime, data=b64)))
        parts.append(types.Part(text=f"Generate an image of: {prompt}"))

        response = client.models.generate_content(
            model=model,
            contents=types.Content(role="user", parts=parts),
            config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"]),
        )

        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "inline_data") and part.inline_data:
                    image_data = part.inline_data.data

                    output_path = Path(output_path)
                    output_path.parent.mkdir(parents=True, exist_ok=True)

                    if isinstance(image_data, str):
                        image_data = base64.b64decode(image_data)

                    with open(output_path, "wb") as f:
                        f.write(image_data)

                    print(f"Image saved: {output_path}")
                    if verbose:
                        print(f"  Size: {len(image_data) / 1024:.2f} KB")
                    return True

        print("No image data found in response")
        return False

    except Exception as e:
        print(f"Error with Gemini Image SDK: {str(e)}")
        if "Server disconnected" in str(e):
            print("Falling back to curl...")
            return generate_with_curl(api_key, prompt, model, output_path, verbose, ref_images=ref_images)
        return False


def generate_with_openai_images(
    api_key,
    prompt,
    model="gpt-image-2",
    output_path="output.png",
    verbose=False,
    base_url="https://api.openai.com",
    size="1024x1024",
    quality="high",
    background="opaque",
    output_format="png",
    moderation="auto",
    n=1,
    ref_images=None,
    mask_path=None,
):
    """Generate image using OpenAI Images-compatible API."""

    if verbose:
        print("Generating with OpenAI-compatible Images API...")
        print(f"  Model: {model}")
        print(f"  Prompt: {prompt[:80]}...")
        print(f"  Size: {size}, Quality: {quality}")

    import os as _os
    for _k in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"]:
        _os.environ.pop(_k, None)

    import requests as _req

    try:
        if ref_images:
            url = f"{base_url.rstrip('/')}/v1/images/edits"
            headers = {"Authorization": f"Bearer {api_key}"}
            data = {
                "model": model,
                "prompt": prompt,
                "size": size,
                "quality": quality,
                "background": background,
                "output_format": output_format,
                "moderation": moderation,
            }
            files = {"image": open(ref_images[0], "rb")}
            if mask_path:
                files["mask"] = open(mask_path, "rb")
            try:
                resp = _req.post(url, headers=headers, data=data, files=files, timeout=180, proxies={"http": None, "https": None})
            finally:
                for f in files.values():
                    f.close()
        else:
            url = f"{base_url.rstrip('/')}/v1/images/generations"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            }
            payload = {
                "model": model,
                "prompt": prompt,
                "size": size,
                "quality": quality,
                "background": background,
                "output_format": output_format,
                "moderation": moderation,
                "n": n,
            }
            resp = _req.post(url, headers=headers, json=payload, timeout=180, proxies={"http": None, "https": None})
        resp.raise_for_status()
        response = resp.json()

        if "error" in response:
            print(f"API error: {response['error']}")
            return False

        # Extract image data (base64 or url)
        image_data = None
        if "data" in response and len(response["data"]) > 0:
            item = response["data"][0]
            if "b64_json" in item:
                image_data = base64.b64decode(item["b64_json"])
            elif "url" in item:
                # Download from URL
                img_resp = _req.get(item["url"], timeout=60, proxies={"http": None, "https": None})
                img_resp.raise_for_status()
                image_data = img_resp.content

        if not image_data:
            print("No image data found in response")
            return False

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(image_data)

        print(f"Image saved: {output_path}")
        if verbose:
            print(f"  Size: {len(image_data) / 1024:.2f} KB")
        return True

    except _req.exceptions.Timeout:
        print("Request timed out")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def generate_with_curl(
    api_key, prompt, model, output_path, verbose=False, base_url=None, ref_images=None
):
    """Generate image using requests (fallback when subprocess curl unavailable)"""

    if verbose:
        print(f"Using requests for generation...")
        print(f"  Model: {model}")

    import os as _os
    for _k in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"]:
        _os.environ.pop(_k, None)

    import requests as _req

    # Build parts: reference images (base64) + text prompt
    parts = []
    if ref_images:
        for img_path in ref_images:
            with open(img_path, "rb") as f:
                img_data = f.read()
            ext = Path(img_path).suffix.lower()
            mime = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
            b64 = base64.b64encode(img_data).decode()
            parts.append({"inlineData": {"mimeType": mime, "data": b64}})
    parts.append({"text": prompt})
    payload = {"contents": [{"role": "user", "parts": parts}]}

    # Determine URL
    if base_url:
        url = f"{base_url}/{model}:generateContent"
        headers = {"Content-Type": "application/json"}
        if not api_key.startswith("AIza"):
            headers["Authorization"] = f"Bearer {api_key}"
        else:
            url = f"{url}?key={api_key}"
    else:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}

    try:
        resp = _req.post(url, headers=headers, json=payload, timeout=180, proxies={"http": None, "https": None})
        resp.raise_for_status()
        response = resp.json()

        if "error" in response:
            print(f"API error: {response['error']}")
            return False

        # Extract image data
        candidates = response.get("candidates", [])
        if not candidates:
            print("No candidates in response")
            return False

        parts_out = candidates[0].get("content", {}).get("parts", [])
        for part in parts_out:
            if "inlineData" in part:
                mime_type = part["inlineData"].get("mimeType", "image/png")
                data = part["inlineData"].get("data", "")
                image_data = base64.b64decode(data)

                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)

                with open(output_path, "wb") as f:
                    f.write(image_data)

                print(f"Image saved: {output_path}")
                if verbose:
                    print(f"  Size: {len(image_data) / 1024:.2f} KB")
                return True

        print("No image data found in response")
        return False

    except _req.exceptions.Timeout:
        print("Request timed out")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def generate_image(
    api_key,
    prompt,
    model="gemini-2.0-flash-exp",
    aspect_ratio="16:9",
    output_path="output.png",
    verbose=False,
):
    """Generate image using Google Genai SDK (legacy, for text models)"""

    if verbose:
        print(f"Generating image...")
        print(f"  Model: {model}")
        print(f"  Prompt: {prompt[:80]}...")
        print(f"  Aspect ratio: {aspect_ratio}")

    try:
        # Initialize client
        client = genai.Client(api_key=api_key)

        # Generate content
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )

        # Check response
        if response and response.text:
            print(f"Model response (text): {response.text[:200]}...")
            print(f"\nNote: Model '{model}' returned text instead of image.")
            print("For image generation, use --gemini-image or --imagen flags.")

            # Try to save text response as info
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            info_path = output_path.with_suffix(".txt")
            info_path.write_text(response.text, encoding="utf-8")
            print(f"Text response saved to: {info_path}")
            return False

        # Try to get image data from response
        if hasattr(response, "candidates") and response.candidates:
            for candidate in response.candidates:
                if hasattr(candidate, "content") and candidate.content:
                    for part in candidate.content.parts:
                        if hasattr(part, "inline_data") and part.inline_data:
                            image_data = part.inline_data.data

                            # Ensure output directory exists
                            output_path = Path(output_path)
                            output_path.parent.mkdir(parents=True, exist_ok=True)

                            # Decode if base64
                            if isinstance(image_data, str):
                                image_data = base64.b64decode(image_data)

                            # Save image
                            with open(output_path, "wb") as f:
                                f.write(image_data)

                            print(f"Image saved: {output_path}")
                            if verbose:
                                print(f"  Size: {len(image_data) / 1024:.2f} KB")
                            return True

        print("No image data found in response")
        return False

    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def generate_with_imagen(
    api_key,
    prompt,
    model="imagen-4.0-generate-001",
    aspect_ratio="16:9",
    output_path="output.png",
    verbose=False,
):
    """Generate image using Imagen model"""

    if verbose:
        print(f"Generating with Imagen...")
        print(f"  Model: {model}")
        print(f"  Prompt: {prompt[:80]}...")
        print(f"  Aspect ratio: {aspect_ratio}")

    try:
        client = genai.Client(api_key=api_key)

        # Use Imagen for image generation
        response = client.models.generate_images(
            model=model,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio=aspect_ratio,
            ),
        )

        if response and response.generated_images:
            # Ensure output directory exists
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Save first image
            image = response.generated_images[0]
            image.image.save(str(output_path))

            print(f"Image saved: {output_path}")
            return True

        print("No images generated")
        return False

    except Exception as e:
        print(f"Error with Imagen: {str(e)}")
        return False


def batch_generate(
    api_key,
    prompts_file,
    model,
    aspect_ratio,
    output_dir,
    use_imagen=False,
    verbose=False,
):
    """Generate multiple images from prompts file"""

    prompts = Path(prompts_file).read_text(encoding="utf-8").strip().split("\n")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    for i, prompt in enumerate(prompts, 1):
        if prompt.strip():
            output_path = output_dir / f"image_{i:02d}.png"
            if verbose:
                print(f"\n[{i}/{len(prompts)}]")

            if use_imagen:
                success = generate_with_imagen(
                    api_key,
                    prompt.strip(),
                    model,
                    aspect_ratio,
                    str(output_path),
                    verbose,
                )
            else:
                success = generate_image(
                    api_key,
                    prompt.strip(),
                    model,
                    aspect_ratio,
                    str(output_path),
                    verbose,
                )

            if success:
                success_count += 1

    print(f"\nGenerated {success_count}/{len(prompts)} images")
    return success_count


def main():
    parser = argparse.ArgumentParser(
        description="Image Generator for OpenAI, Gemini, and OpenAI-compatible APIs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate with an OpenAI-compatible Images API
  python3 nanobanana_client.py --openai-compatible-image --prompt "A cute cat" --output cat.png

  # Generate with official OpenAI Images API
  python3 nanobanana_client.py --openai-image --prompt "A cute cat" --output cat.png

  # Generate with official Gemini Image API
  python3 nanobanana_client.py --gemini-image --prompt "A cute cat" --output cat.png

  # Human portrait cover (universal template):
  # Replace {MAIN_TITLE}, {SUBTITLE}, {TOPIC_TAGS} before use
  python3 nanobanana_client.py \\
    --prompt "WeChat article cover: right side has a [AGE]-year-old [ETHNICITY] professional, [GENDER], wearing [STYLE], slightly turned, warm orange glow on silhouette, gesturing toward left. Left area reserved for title: main title '[MAIN_TITLE]' in large bold Chinese font, subtitle '[SUBTITLE]' below. Background: subtle data/task visualization elements (curves, nodes, tags) in cool cyan. Color palette: warm orange + cream gradient, navy blue, amber accent. Style: realistic photography + light concept compositing, professional tech media feel, 16:9 horizontal. Bottom-right: small watermark space. Negative: no cyberpunk neon, no cartoon, no oversaturation." \\
    --openai-compatible-image --ref ./photo.jpg --output cover.png

  # Batch generate
  python3 nanobanana_client.py --prompts-file prompts.txt --batch --openai-compatible-image --output images/

  # Batch generate with multiple prompts (comma-separated)
  python3 nanobanana_client.py --prompts "AI conference, token economics, neural networks" --batch --openai-compatible-image --output images/
""",
    )

    parser.add_argument("--api-key", help="API key (or use config/.env)")
    parser.add_argument("--prompt", help="Single image prompt")
    parser.add_argument("--prompts", help="Multiple prompts (comma-separated)")
    parser.add_argument(
        "--prompts-file", help="File with multiple prompts (one per line)"
    )
    parser.add_argument(
        "--model",
        default="gemini-2.0-flash-exp",
        help="Model to use (default: gemini-2.0-flash-exp)",
    )
    parser.add_argument(
        "--imagen",
        action="store_true",
        help="Use Imagen 4 model for image generation (requires billing)",
    )
    parser.add_argument(
        "--imagen-model",
        default="imagen-4.0-generate-001",
        choices=[
            "imagen-4.0-generate-001",
            "imagen-4.0-fast-generate-001",
            "imagen-4.0-ultra-generate-001",
        ],
        help="Imagen model variant (default: imagen-4.0-generate-001)",
    )
    parser.add_argument(
        "--gemini-image",
        action="store_true",
        help="Use Gemini image generation model (NanoBanana 2: gemini-3.1-flash-image-preview)",
    )
    parser.add_argument(
        "--gemini-image-model",
        default="gemini-3.1-flash-image-preview",
        choices=[
            "gemini-2.0-flash-exp-image-generation",
            "gemini-2.5-flash-image-preview",
            "gemini-2.5-flash-image",
            "gemini-3-pro-image-preview",
            "gemini-3.1-flash-image-preview",
        ],
        help="Gemini image model (default: gemini-3.1-flash-image-preview)",
    )
    parser.add_argument(
        "--aspect-ratio",
        default="16:9",
        choices=["1:1", "16:9", "4:3", "3:4", "9:16"],
        help="Image aspect ratio",
    )
    parser.add_argument("--output", default="output.png", help="Output file path")
    parser.add_argument(
        "--batch", action="store_true", help="Batch mode from prompts file"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument(
        "--env",
        action="store_true",
        help="Load API key from environment (default if no --api-key)",
    )
    parser.add_argument(
        "--use-curl",
        action="store_true",
        help="Use curl instead of Python SDK (more reliable)",
    )
    parser.add_argument(
        "--ref", "-r", nargs="+", default=None,
        help="Reference image paths for img2img (optional, pass your own photo)"
    )
    parser.add_argument(
        "--openai-image",
        action="store_true",
        help="Use official OpenAI Images API",
    )
    parser.add_argument(
        "--openai-compatible-image",
        action="store_true",
        help="Use OpenAI-compatible Images API",
    )
    parser.add_argument(
        "--image-model",
        default="gpt-image-2",
        help="Images API model (default: gpt-image-2)",
    )
    parser.add_argument(
        "--image-size",
        default="1024x1024",
        help="Image size for Images API (default: 1024x1024)",
    )
    parser.add_argument(
        "--image-quality",
        default="high",
        choices=["low", "medium", "high", "auto"],
        help="Image quality for Images API (default: high)",
    )
    parser.add_argument(
        "--image-format",
        default="png",
        choices=["png", "jpeg", "webp"],
        help="Output format for Images API (default: png)",
    )
    parser.add_argument(
        "--mask",
        default=None,
        help="Mask image path for inpainting edits (optional)",
    )

    args = parser.parse_args()

    # Apply default reference image if not provided
    if args.ref is None:
        args.ref = None

    # Built-in portrait cover prompt (used when --prompt is not provided)
    PORTRAIT_COVER_PROMPT = (
        "WeChat article cover: right side has a 28-year-old East Asian professional, male, "
        "wearing minimalist dark hoodie, slightly turned, warm orange glow on silhouette, "
        "gesturing toward left. Left area reserved for title: main title '[MAIN_TITLE]' "
        "in large bold Chinese font, subtitle '[SUBTITLE]' below. Background: subtle "
        "data/task visualization elements (curves, nodes, tags) in cool cyan. "
        "Color palette: warm orange + cream gradient (Anthropic brand), navy blue, "
        "amber accent. Style: realistic photography + light concept compositing, "
        "professional tech media feel, 16:9 horizontal. Bottom-right: small watermark space. "
        "Negative: no cyberpunk neon, no cartoon, no oversaturation."
    )

    # Apply default portrait cover prompt if not provided
    if not args.prompt:
        args.prompt = PORTRAIT_COVER_PROMPT

    # Load API key
    api_key = args.api_key
    base_url = None
    config = load_config()
    openai_compatible_config = config.get("openai_compatible", {})
    use_openai_compatible = args.openai_compatible_image or bool(openai_compatible_config.get("api_key"))
    use_openai_official = args.openai_image or (not use_openai_compatible and bool(config.get("openai_api_key")))
    if use_openai_compatible:
        if args.image_size == "1024x1024" and openai_compatible_config.get("default_size"):
            args.image_size = openai_compatible_config["default_size"]
        if args.image_quality == "high" and openai_compatible_config.get("default_quality"):
            args.image_quality = openai_compatible_config["default_quality"]

    if not api_key:
        if not validate_config(config, verbose=args.verbose):
            sys.exit(1)
        if use_openai_compatible:
            api_key = openai_compatible_config.get("api_key")
            base_url = openai_compatible_config.get("base_url")
        elif use_openai_official:
            api_key = config.get("openai_api_key")
            base_url = config.get("openai_base_url", "https://api.openai.com")
        else:
            api_key = config.get("google_ai_api_key")
        if args.verbose:
            print("Loaded API key from config")

    if not api_key:
        print("Error: No API key provided")
        print("Use --api-key or configure GOOGLE_AI_API_KEY, OPENAI_API_KEY, or OPENAI_COMPATIBLE_API_KEY in config/.env")
        sys.exit(1)

    # Execute
    if args.batch and (args.prompts_file or args.prompts):
        output_dir = args.output if args.output != "output.png" else "output/images"
        imagen_model = args.imagen_model if args.imagen else args.model

        # Create prompts list
        prompts = []
        if args.prompts_file:
            prompts = (
                Path(args.prompts_file).read_text(encoding="utf-8").strip().split("\n")
            )
        elif args.prompts:
            prompts = [p.strip() for p in args.prompts.split(",") if p.strip()]

        # Generate images for each prompt
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        success_count = 0
        for i, prompt in enumerate(prompts, 1):
            if prompt.strip():
                output_path = output_dir / f"image_{i:02d}.png"
                if args.verbose:
                    print(f"\n[{i}/{len(prompts)}] {prompt[:60]}...")

                if args.imagen:
                    success = generate_with_imagen(
                        api_key,
                        prompt.strip(),
                        imagen_model,
                        args.aspect_ratio,
                        str(output_path),
                        args.verbose,
                    )
                elif use_openai_compatible or use_openai_official:
                    success = generate_with_openai_images(
                        api_key,
                        prompt.strip(),
                        args.image_model,
                        str(output_path),
                        args.verbose,
                        base_url or "https://api.openai.com",
                        args.image_size,
                        args.image_quality,
                        ref_images=args.ref,
                        mask_path=args.mask,
                    )
                elif args.gemini_image:
                    success = generate_with_gemini_image(
                        api_key,
                        prompt.strip(),
                        args.gemini_image_model,
                        str(output_path),
                        args.verbose,
                        args.use_curl,
                        base_url,
                        args.ref,
                    )
                else:
                    success = generate_image(
                        api_key,
                        prompt.strip(),
                        imagen_model,
                        args.aspect_ratio,
                        str(output_path),
                        args.verbose,
                    )

                if success:
                    success_count += 1

        print(f"\nGenerated {success_count}/{len(prompts)} images")
    elif args.prompt:
        if args.imagen:
            generate_with_imagen(
                api_key,
                args.prompt,
                args.imagen_model,
                args.aspect_ratio,
                args.output,
                verbose=args.verbose,
            )
        elif use_openai_compatible or use_openai_official:
            generate_with_openai_images(
                api_key,
                args.prompt,
                args.image_model,
                args.output,
                verbose=args.verbose,
                base_url=base_url or "https://api.openai.com",
                size=args.image_size,
                quality=args.image_quality,
                output_format=args.image_format,
                ref_images=args.ref,
                mask_path=args.mask,
            )
        elif args.gemini_image:
            generate_with_gemini_image(
                api_key,
                args.prompt,
                args.gemini_image_model,
                args.output,
                verbose=args.verbose,
                use_curl=args.use_curl,
                base_url=base_url,
                ref_images=args.ref,
            )
        else:
            generate_image(
                api_key,
                args.prompt,
                args.model,
                args.aspect_ratio,
                args.output,
                verbose=args.verbose,
            )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
