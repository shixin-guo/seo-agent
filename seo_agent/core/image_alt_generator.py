"""AI-powered alt text generation for images.

This module provides functionality to analyze images and generate
SEO-optimized alt text using vision models.
"""

import os
from typing import Any, Dict, Optional
from pathlib import Path

import dspy
from PIL import Image as PILImage  # type: ignore


class ImageAltTextGenerator(dspy.Signature):
    """Generate SEO-optimized alt text for images."""

    image_description = dspy.InputField(
        desc="Description of what is visible in the image"
    )
    context = dspy.InputField(desc="Additional context about the image usage")
    alt_text = dspy.OutputField(
        desc="SEO-optimized alt text that is descriptive and concise"
    )


class ImageAltGenerator:
    """AI-powered image alt text generator."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the image alt text generator.

        Args:
            config: Configuration dictionary containing API settings.
        """
        self.config = config

        openai_key = os.environ.get("OPENAI_API_KEY") or config.get("apis", {}).get(
            "openai_key"
        )

        if not openai_key:
            raise ValueError("OpenAI API key is required for image alt text generation")

        self.lm = dspy.LM(
            model="gpt-4o",
            api_key=openai_key,
            max_tokens=150,
            temperature=0.3,
        )

        dspy.configure(lm=self.lm)
        self.generator = dspy.ChainOfThought(ImageAltTextGenerator)

    def analyze_image(self, image_path: str) -> str:
        """Analyze image content and return description.

        Args:
            image_path: Path to the image file.

        Returns:
            Description of the image content.
        """
        try:
            with PILImage.open(image_path) as img:
                img_format = img.format or "Unknown"
                img_size = img.size
                img_mode = img.mode

                description = f"Image format: {img_format}, Size: {img_size[0]}x{img_size[1]}, Mode: {img_mode}"

                if hasattr(img, "info") and img.info:
                    if "description" in img.info:
                        description += f", Description: {img.info['description']}"

                return description

        except Exception as e:
            return f"Unable to analyze image: {str(e)}"

    def generate_alt_text(self, image_path: str, context: Optional[str] = None) -> str:
        """Generate SEO-optimized alt text for an image.

        Args:
            image_path: Path to the image file.
            context: Optional context about how the image will be used.

        Returns:
            Generated alt text.
        """
        if not Path(image_path).exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")

        image_description = self.analyze_image(image_path)

        if not context:
            context = "General website content"

        try:
            result = self.generator(
                image_description=image_description, context=context
            )

            alt_text = result.alt_text.strip()

            if len(alt_text) > 125:
                alt_text = alt_text[:122] + "..."

            return str(alt_text)

        except Exception:
            return f"Professional image for {context.lower()}"

    def validate_image(self, image_path: str) -> Dict[str, Any]:
        """Validate image file and return metadata.

        Args:
            image_path: Path to the image file.

        Returns:
            Dictionary containing validation results and metadata.
        """
        try:
            with PILImage.open(image_path) as img:
                file_size = Path(image_path).stat().st_size

                return {
                    "valid": True,
                    "format": img.format,
                    "size": img.size,
                    "mode": img.mode,
                    "file_size": file_size,
                    "error": None,
                }

        except Exception as e:
            return {
                "valid": False,
                "format": None,
                "size": None,
                "mode": None,
                "file_size": None,
                "error": str(e),
            }
