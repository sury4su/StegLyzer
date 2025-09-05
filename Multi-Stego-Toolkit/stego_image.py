# stego_image.py

from stegano import lsb
from PIL import Image, ImageFile
import os

# Allow very large images without warnings
Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Supported formats (JPGs will be converted)
SUPPORTED_IMAGE_TYPES = [".png", ".bmp", ".jpg", ".jpeg"]

def is_supported_image(file_path: str) -> bool:
    """Check if the file extension is a supported image type."""
    ext = os.path.splitext(file_path)[-1].lower()
    return ext in SUPPORTED_IMAGE_TYPES

def convert_jpg_to_png(input_path: str) -> str:
    """Convert JPG/JPEG to PNG to ensure LSB stego works reliably."""
    output_path = os.path.splitext(input_path)[0] + "_converted.png"
    try:
        img = Image.open(input_path)
        img = img.convert("RGB")  # Remove alpha if present
        img.save(output_path, "PNG", optimize=False)
        return output_path
    except Exception as e:
        raise ValueError(f"❌ JPG conversion failed: {str(e)}")

def embed_text_in_image(cover_image_path: str, output_image_path: str, secret_text: str):
    """Embed secret text into an image using LSB steganography."""
    if not is_supported_image(cover_image_path):
        raise ValueError("Only PNG, BMP, JPG, and JPEG images are supported.")

    # Convert JPG/JPEG before embedding
    ext = os.path.splitext(cover_image_path)[-1].lower()
    if ext in [".jpg", ".jpeg"]:
        cover_image_path = convert_jpg_to_png(cover_image_path)

    try:
        # Hide the message
        secret_image = lsb.hide(cover_image_path, secret_text)

        # Save safely for large PNGs
        secret_image.save(output_image_path, format="PNG", optimize=False)

        return True, f"✅ Message embedded successfully in: {output_image_path}"
    except Exception as e:
        return False, f"❌ Failed to embed message: {str(e)}"

def extract_text_from_image(stego_image_path: str):
    """Extract hidden text from an image using LSB steganography."""
    if not is_supported_image(stego_image_path):
        raise ValueError("Only PNG, BMP, JPG, and JPEG images are supported.")

    # Convert JPG/JPEG before extraction
    ext = os.path.splitext(stego_image_path)[-1].lower()
    if ext in [".jpg", ".jpeg"]:
        stego_image_path = convert_jpg_to_png(stego_image_path)

    try:
        message = lsb.reveal(stego_image_path)
        if message:
            return True, message
        else:
            return False, "⚠️ No hidden message found."
    except Exception as e:
        return False, f"❌ Error extracting message: {str(e)}"
