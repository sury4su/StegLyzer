# stego_archive.py

import os

SUPPORTED_ARCHIVES = [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".iso", ".dmg"]

# Unique marker so we know where our message starts
MARKER = b"<<SECRET_MSG_START>>"

def is_supported_archive(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    return ext in SUPPORTED_ARCHIVES

def embed_text_in_archive(input_path, output_path, secret_text):
    if not is_supported_archive(input_path):
        return False, "❌ Unsupported archive type."

    try:
        with open(input_path, "rb") as original_file:
            data = original_file.read()

        with open(output_path, "wb") as stego_file:
            stego_file.write(data)
            stego_file.write(MARKER + secret_text.encode("utf-8"))

        return True, f"✅ Message embedded in archive: {output_path}"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def extract_text_from_archive(stego_path):
    try:
        with open(stego_path, "rb") as f:
            data = f.read()

        index = data.find(MARKER)
        if index == -1:
            return False, "⚠️ No hidden message found."

        secret_data = data[index + len(MARKER):]
        return True, secret_data.decode("utf-8", errors="replace")
    except Exception as e:
        return False, f"❌ Error: {str(e)}"
