# stego_audio.py - Enhanced Multi-Format Audio Steganography (MP3 Removed)

import os
import wave
import contextlib
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
from mutagen.aiff import AIFF
from mutagen.wave import WAVE
from pydub import AudioSegment
import tempfile
import struct

# Supported audio formats (MP3 REMOVED)
SUPPORTED_LSB_FORMATS = [".wav", ".aiff", ".au", ".raw"]  # Uncompressed formats for LSB
SUPPORTED_METADATA_FORMATS = [".flac", ".m4a", ".mp4", ".ogg", ".aac"]  # Compressed formats for metadata (NO MP3)
SUPPORTED_CONVERTED_FORMATS = [".opus", ".amr", ".ac3", ".dts", ".tta", ".ape", ".wv"]  # Convert to WAV for processing

ALL_SUPPORTED_FORMATS = SUPPORTED_LSB_FORMATS + SUPPORTED_METADATA_FORMATS + SUPPORTED_CONVERTED_FORMATS

def is_supported_audio(file_path):
    """Check if the audio format is supported"""
    ext = os.path.splitext(file_path)[-1].lower()
    return ext in ALL_SUPPORTED_FORMATS

def get_audio_format_type(file_path):
    """Determine the audio format category"""
    ext = os.path.splitext(file_path)[-1].lower()
    
    if ext in SUPPORTED_LSB_FORMATS:
        return "lsb"
    elif ext in SUPPORTED_METADATA_FORMATS:
        return "metadata"
    elif ext in SUPPORTED_CONVERTED_FORMATS:
        return "convert"
    else:
        return "unsupported"

# -------------------------
# Main Audio Steganography Functions
# -------------------------

def embed_text_in_audio(input_path, output_path, secret_text):
    """Main function to embed text in various audio formats (NO MP3)"""
    if not is_supported_audio(input_path):
        ext = os.path.splitext(input_path)[1].lower()
        if ext == ".mp3":
            return False, "❌ MP3 format not supported due to metadata compatibility issues."
        return False, "❌ Unsupported audio format."
    
    format_type = get_audio_format_type(input_path)
    
    try:
        if format_type == "lsb":
            return embed_lsb_audio(input_path, output_path, secret_text)
        elif format_type == "metadata":
            return embed_metadata_audio(input_path, output_path, secret_text)
        elif format_type == "convert":
            return embed_convert_audio(input_path, output_path, secret_text)
        else:
            return False, "❌ Unsupported audio format."
    except Exception as e:
        return False, f"❌ Error embedding message: {str(e)}"

def extract_text_from_audio(input_path):
    """Main function to extract text from various audio formats (NO MP3)"""
    if not is_supported_audio(input_path):
        ext = os.path.splitext(input_path)[1].lower()
        if ext == ".mp3":
            return False, "❌ MP3 format not supported due to metadata compatibility issues."
        return False, "❌ Unsupported audio format."
    
    format_type = get_audio_format_type(input_path)
    
    try:
        if format_type == "lsb":
            return extract_lsb_audio(input_path)
        elif format_type == "metadata":
            return extract_metadata_audio(input_path)
        elif format_type == "convert":
            return extract_convert_audio(input_path)
        else:
            return False, "❌ Unsupported audio format."
    except Exception as e:
        return False, f"❌ Error extracting message: {str(e)}"

# -------------------------
# LSB Steganography (Uncompressed Formats)
# -------------------------

def _text_to_bits(text):
    """Convert text to binary representation"""
    return ''.join(format(ord(c), '08b') for c in text)

def _bits_to_text(bits):
    """Convert binary representation back to text"""
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(char, 2)) for char in chars if char)

def embed_lsb_audio(input_path, output_path, secret_text):
    """Embed text using LSB method for uncompressed audio"""
    ext = os.path.splitext(input_path)[1].lower()
    
    if ext == ".wav":
        return embed_text_in_wav(input_path, output_path, secret_text)
    elif ext in [".aiff", ".au", ".raw"]:
        # Convert to WAV first, then embed
        temp_wav_in = tempfile.mktemp(suffix=".wav")
        temp_wav_out = tempfile.mktemp(suffix=".wav")
        
        try:
            # Convert input to WAV
            audio = AudioSegment.from_file(input_path)
            audio.export(temp_wav_in, format="wav")
            
            # Embed in WAV
            success, result = embed_text_in_wav(temp_wav_in, temp_wav_out, secret_text)
            
            if success:
                # Convert back to original format
                stego_audio = AudioSegment.from_wav(temp_wav_out)
                stego_audio.export(output_path, format=ext[1:])  # Remove the dot
                return True, f"✅ Message embedded in {ext.upper()} file: {output_path}"
            else:
                return success, result
                
        finally:
            # Clean up temp files
            for temp_file in [temp_wav_in, temp_wav_out]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)

def extract_lsb_audio(input_path):
    """Extract text using LSB method from uncompressed audio"""
    ext = os.path.splitext(input_path)[1].lower()
    
    if ext == ".wav":
        return extract_text_from_wav(input_path)
    elif ext in [".aiff", ".au", ".raw"]:
        # Convert to WAV first, then extract
        temp_wav = tempfile.mktemp(suffix=".wav")
        
        try:
            # Convert to WAV
            audio = AudioSegment.from_file(input_path)
            audio.export(temp_wav, format="wav")
            
            # Extract from WAV
            return extract_text_from_wav(temp_wav)
            
        finally:
            if os.path.exists(temp_wav):
                os.remove(temp_wav)

def embed_text_in_wav(input_path, output_path, secret_text):
    """Enhanced WAV LSB embedding"""
    try:
        with wave.open(input_path, 'rb') as audio:
            params = audio.getparams()
            frames = bytearray(audio.readframes(audio.getnframes()))

        # Add length prefix and EOF marker
        message_length = len(secret_text)
        length_bits = format(message_length, '032b')  # 32-bit length
        text_bits = _text_to_bits(secret_text)
        bits = length_bits + text_bits + '1111111111111110'  # EOF marker

        if len(bits) > len(frames):
            return False, f"❌ Message too large. Max capacity: {len(frames)//8} characters"

        # Embed bits in LSB
        for i, bit in enumerate(bits):
            frames[i] = (frames[i] & 254) | int(bit)

        with wave.open(output_path, 'wb') as stego_audio:
            stego_audio.setparams(params)
            stego_audio.writeframes(frames)

        return True, f"✅ Message embedded in WAV: {output_path}"
        
    except Exception as e:
        return False, f"❌ WAV embedding error: {str(e)}"

def extract_text_from_wav(stego_path):
    """Enhanced WAV LSB extraction"""
    try:
        with wave.open(stego_path, 'rb') as audio:
            frames = bytearray(audio.readframes(audio.getnframes()))

        # Extract length (first 32 bits)
        length_bits = ''
        for i in range(32):
            if i < len(frames):
                length_bits += str(frames[i] & 1)

        if len(length_bits) < 32:
            return False, "⚠️ No valid message found."

        message_length = int(length_bits, 2)
        
        if message_length <= 0 or message_length > 100000:  # Sanity check
            return False, "⚠️ No valid hidden message found."

        # Extract message bits
        message_bits = ''
        for i in range(32, 32 + (message_length * 8)):
            if i < len(frames):
                message_bits += str(frames[i] & 1)

        if len(message_bits) < message_length * 8:
            return False, "⚠️ Incomplete message found."

        return True, _bits_to_text(message_bits)
        
    except Exception as e:
        return False, f"❌ WAV extraction error: {str(e)}"

# -------------------------
# Metadata Steganography (Compressed Formats - NO MP3)
# -------------------------

def embed_metadata_audio(input_path, output_path, secret_text):
    """Embed text in audio metadata for compressed formats (NO MP3)"""
    ext = os.path.splitext(input_path)[1].lower()
    
    try:
        # Copy file first
        if input_path != output_path:
            with open(input_path, 'rb') as src, open(output_path, 'wb') as dst:
                dst.write(src.read())
        
        # Embed in metadata based on format (MP3 REMOVED)
        if ext == ".flac":
            return embed_flac_metadata(output_path, secret_text)
        elif ext in [".m4a", ".mp4", ".aac"]:
            return embed_mp4_metadata(output_path, secret_text)
        elif ext == ".ogg":
            return embed_ogg_metadata(output_path, secret_text)
        else:
            return False, f"❌ Metadata embedding not supported for {ext}"
            
    except Exception as e:
        return False, f"❌ Metadata embedding error: {str(e)}"

def extract_metadata_audio(input_path):
    """Extract text from audio metadata (NO MP3)"""
    ext = os.path.splitext(input_path)[1].lower()
    
    try:
        # MP3 support removed
        if ext == ".flac":
            return extract_flac_metadata(input_path)
        elif ext in [".m4a", ".mp4", ".aac"]:
            return extract_mp4_metadata(input_path)
        elif ext == ".ogg":
            return extract_ogg_metadata(input_path)
        else:
            return False, f"❌ Metadata extraction not supported for {ext}"
            
    except Exception as e:
        return False, f"❌ Metadata extraction error: {str(e)}"

# Specific metadata handlers (MP3 functions removed)
def embed_flac_metadata(file_path, secret_text):
    """Embed in FLAC Vorbis comments"""
    try:
        audio = FLAC(file_path)
        audio["COMMENT"] = secret_text
        audio.save()
        return True, "✅ Message embedded in FLAC metadata."
    except Exception as e:
        return False, f"❌ FLAC metadata error: {str(e)}"

def extract_flac_metadata(file_path):
    """Extract from FLAC Vorbis comments"""
    try:
        audio = FLAC(file_path)
        comment = audio.get("COMMENT", [None])[0]
        return (True, comment) if comment else (False, "⚠️ No comment metadata found.")
    except Exception as e:
        return False, f"❌ FLAC metadata error: {str(e)}"

def embed_mp4_metadata(file_path, secret_text):
    """Embed in MP4/M4A/AAC metadata"""
    try:
        audio = MP4(file_path)
        audio["\xa9cmt"] = secret_text  # Comment atom
        audio.save()
        return True, "✅ Message embedded in MP4 metadata."
    except Exception as e:
        return False, f"❌ MP4 metadata error: {str(e)}"

def extract_mp4_metadata(file_path):
    """Extract from MP4/M4A/AAC metadata"""
    try:
        audio = MP4(file_path)
        comment = audio.get("\xa9cmt", [None])[0]
        return (True, comment) if comment else (False, "⚠️ No comment metadata found.")
    except Exception as e:
        return False, f"❌ MP4 metadata error: {str(e)}"

def embed_ogg_metadata(file_path, secret_text):
    """Embed in OGG Vorbis comments"""
    try:
        audio = OggVorbis(file_path)
        audio["COMMENT"] = secret_text
        audio.save()
        return True, "✅ Message embedded in OGG metadata."
    except Exception as e:
        return False, f"❌ OGG metadata error: {str(e)}"

def extract_ogg_metadata(file_path):
    """Extract from OGG Vorbis comments"""
    try:
        audio = OggVorbis(file_path)
        comment = audio.get("COMMENT", [None])[0]
        return (True, comment) if comment else (False, "⚠️ No comment metadata found.")
    except Exception as e:
        return False, f"❌ OGG metadata error: {str(e)}"

# -------------------------
# Convert-to-WAV Method (Exotic Formats)
# -------------------------

def embed_convert_audio(input_path, output_path, secret_text):
    """Convert exotic formats to WAV, embed, then convert back"""
    ext = os.path.splitext(input_path)[1].lower()
    temp_wav_in = tempfile.mktemp(suffix=".wav")
    temp_wav_out = tempfile.mktemp(suffix=".wav")
    
    try:
        # Convert input to WAV
        audio = AudioSegment.from_file(input_path)
        audio.export(temp_wav_in, format="wav")
        
        # Embed in WAV
        success, result = embed_text_in_wav(temp_wav_in, temp_wav_out, secret_text)
        
        if success:
            # Convert back to original format
            stego_audio = AudioSegment.from_wav(temp_wav_out)
            stego_audio.export(output_path, format=ext[1:])
            return True, f"✅ Message embedded in {ext.upper()} file: {output_path}"
        else:
            return success, result
            
    except Exception as e:
        return False, f"❌ Conversion embedding error: {str(e)}"
        
    finally:
        # Clean up temp files
        for temp_file in [temp_wav_in, temp_wav_out]:
            if os.path.exists(temp_file):
                os.remove(temp_file)

def extract_convert_audio(input_path):
    """Convert exotic formats to WAV and extract"""
    temp_wav = tempfile.mktemp(suffix=".wav")
    
    try:
        # Convert to WAV
        audio = AudioSegment.from_file(input_path)
        audio.export(temp_wav, format="wav")
        
        # Extract from WAV
        return extract_text_from_wav(temp_wav)
        
    except Exception as e:
        return False, f"❌ Conversion extraction error: {str(e)}"
        
    finally:
        if os.path.exists(temp_wav):
            os.remove(temp_wav)

# -------------------------
# Utility Functions
# -------------------------

def get_audio_info(file_path):
    """Get detailed audio file information (NO MP3)"""
    try:
        ext = os.path.splitext(file_path)[1].lower()
        
        # Check if MP3 and return error message
        if ext == ".mp3":
            return {"error": "MP3 format not supported due to metadata compatibility issues"}
        
        audio = AudioSegment.from_file(file_path)
        format_type = get_audio_format_type(file_path)
        
        info = {
            "format": ext[1:].upper(),
            "format_type": format_type,
            "duration": len(audio) / 1000.0,  # seconds
            "channels": audio.channels,
            "sample_rate": audio.frame_rate,
            "frame_width": audio.frame_width,
            "max_message_length": estimate_capacity(file_path)
        }
        return info
        
    except Exception as e:
        return {"error": str(e)}

def estimate_capacity(file_path):
    """Estimate message capacity for audio file (NO MP3)"""
    try:
        ext = os.path.splitext(file_path)[1].lower()
        
        # No capacity for MP3
        if ext == ".mp3":
            return 0
            
        format_type = get_audio_format_type(file_path)
        
        if format_type == "lsb":
            # For LSB, capacity depends on audio length
            audio = AudioSegment.from_file(file_path)
            total_samples = len(audio.raw_data)
            return total_samples // 8  # rough estimate
            
        elif format_type in ["metadata", "convert"]:
            # For metadata, typically limited to comment field
            return 1000  # conservative estimate
            
        return 0
        
    except Exception:
        return 0

def get_supported_formats_info():
    """Get information about supported formats"""
    return {
        "lsb_formats": SUPPORTED_LSB_FORMATS,
        "metadata_formats": SUPPORTED_METADATA_FORMATS,
        "convert_formats": SUPPORTED_CONVERTED_FORMATS,
        "all_formats": ALL_SUPPORTED_FORMATS,
        "removed_formats": [".mp3"],
        "removal_reason": "MP3 ID3 comment metadata compatibility issues"
    }
