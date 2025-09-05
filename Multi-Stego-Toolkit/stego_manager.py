# stego_manager.py

import os
from stego_image import is_supported_image, embed_text_in_image, extract_text_from_image
from stego_audio import is_supported_audio, embed_text_in_audio, extract_text_from_audio
from stego_archive import is_supported_archive, embed_text_in_archive, extract_text_from_archive
from stego_video import is_supported_video, embed_text_in_video, extract_text_from_video

def get_file_type(file_path):
    if is_supported_image(file_path):
        return 'image'
    elif is_supported_audio(file_path):
        return 'audio'
    elif is_supported_video(file_path):
        return 'video'
    elif is_supported_archive(file_path):
        return 'archive'
    else:
        return None

def embed_message(input_path, output_path, message):
    file_type = get_file_type(input_path)
    
    if file_type == 'image':
        return embed_text_in_image(input_path, output_path, message)
    elif file_type == 'audio':
        return embed_text_in_audio(input_path, output_path, message)
    elif file_type == 'video':
        return embed_text_in_video(input_path, output_path, message)
    elif file_type == 'archive':
        return embed_text_in_archive(input_path, output_path, message)
    else:
        return False, "❌ Unsupported file type for embedding."

def extract_message(input_path):
    file_type = get_file_type(input_path)
    
    if file_type == 'image':
        return extract_text_from_image(input_path)
    elif file_type == 'audio':
        return extract_text_from_audio(input_path)
    elif file_type == 'video':
        return extract_text_from_video(input_path)
    elif file_type == 'archive':
        return extract_text_from_archive(input_path)
    else:
        return False, "❌ Unsupported file type for extraction."
