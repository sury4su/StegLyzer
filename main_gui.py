import customtkinter as ctk
from stego_manager import embed_message, extract_message
import os
import mimetypes
from PIL import Image, ExifTags, ImageFile
import cv2
import datetime
from tkinter import filedialog
import tkinter as tk
import math

Image.MAX_IMAGE_PIXELS = None  
ImageFile.LOAD_TRUNCATED_IMAGES = True

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ModernSteganographyApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🔒 Steganography Analyzer - Modern UI")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)
        self.root.configure(fg_color="#0D1117")
        self.file_path = tk.StringVar()
        self.operation = tk.StringVar(value="embed")
        self.create_main_interface()
        self.animate_floating_elements()
        
    def create_main_interface(self):
        """Create the main responsive interface"""
        
        self.main_scrollable = ctk.CTkScrollableFrame(
            self.root,
            corner_radius=0,
            fg_color="#0D1117",
            scrollbar_button_color="#333333",
            scrollbar_button_hover_color="#555555"
        )
        self.main_scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.main_scrollable.grid_columnconfigure(0, weight=2)  # Left panel gets more space
        self.main_scrollable.grid_columnconfigure(1, weight=1)  # Right panel
        self.main_scrollable.grid_rowconfigure(1, weight=1)     # Main content row
        
        # Title section (full width)
        self.create_title_section()
        
        # Left panel (Controls and Animation)
        self.create_left_panel()
        
        # Right panel (Metadata)
        self.create_right_panel()
        
    def create_title_section(self):
        """Create the responsive title section"""
        title_frame = ctk.CTkFrame(
            self.main_scrollable,
            corner_radius=20,
            height=100,
            fg_color="#1a3232",
            border_width=2,
            border_color="#00FFFF"
        )
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 20))
        title_frame.grid_propagate(False)
        
        # Configure internal grid
        title_frame.grid_columnconfigure(0, weight=1)
        title_frame.grid_rowconfigure(0, weight=1)
        title_frame.grid_rowconfigure(1, weight=1)
        
        # Main title
        self.title_label = ctk.CTkLabel(
            title_frame,
            text="🔒 StegLyzer",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color="#00FFFF"
        )
        self.title_label.grid(row=0, column=0, sticky="ew", pady=(10, 0))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Modern Responsive UI • Hide & Extract Messages • Multi-Format Support",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color="#CCCCCC"
        )
        subtitle_label.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
    def create_left_panel(self):
        """Create the responsive left panel"""
        self.left_panel = ctk.CTkFrame(
            self.main_scrollable,
            corner_radius=20,
            fg_color="#1a2332",
            border_width=2,
            border_color="#1E90FF"
        )
        self.left_panel.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=(0, 10))
        
        # Configure internal grid for responsiveness
        self.left_panel.grid_columnconfigure(0, weight=1)
        self.left_panel.grid_rowconfigure(0, weight=0)  # Animation section
        self.left_panel.grid_rowconfigure(1, weight=0)  # File section
        self.left_panel.grid_rowconfigure(2, weight=0)  # Operation section
        self.left_panel.grid_rowconfigure(3, weight=1)  # Message section (expandable)
        self.left_panel.grid_rowconfigure(4, weight=0)  # Button section
        
        # Animation section
        self.create_animation_section()
        
        # File selection section
        self.create_file_section()
        
        # Operation selection section
        self.create_operation_section()
        
        # Message section
        self.create_message_section()
        
        # Action buttons section
        self.create_action_buttons()
        
    def create_animation_section(self):
        """Create responsive animation section"""
        animation_frame = ctk.CTkFrame(
            self.left_panel,
            corner_radius=15,
            height=200,
            fg_color="#0a0a0a"
        )
        animation_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        animation_frame.grid_propagate(False)
        animation_frame.grid_columnconfigure(0, weight=1)
        animation_frame.grid_rowconfigure(0, weight=1)
        
        # Canvas for animation
        self.canvas = tk.Canvas(
            animation_frame,
            bg='#0D1117',
            highlightthickness=0,
            height=180
        )
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Animation setup
        self.setup_animation()
        
    def setup_animation(self):
        """Setup animated elements"""
        self.animation_items = []
        self.animation_angle = 0
        
        # Create animated circles
        colors = ['#00FFFF', '#1E90FF', '#8A2BE2', '#FF1493', '#00FF7F']
        
        def update_canvas_size(event=None):
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            center_x, center_y = canvas_width // 2, canvas_height // 2
            
            # Clear existing items
            self.canvas.delete("all")
            self.animation_items.clear()
            
            # Create new circles based on canvas size
            if canvas_width > 50 and canvas_height > 50:
                for i, color in enumerate(colors):
                    radius = min(canvas_width, canvas_height) // 8 + i * 10
                    if radius < min(canvas_width, canvas_height) // 2 - 20:
                        circle = self.canvas.create_oval(
                            center_x - radius, center_y - radius,
                            center_x + radius, center_y + radius,
                            outline=color, width=2, fill='', tags="circle"
                        )
                        self.animation_items.append(circle)
                
                # Central glow
                self.center_circle = self.canvas.create_oval(
                    center_x - 15, center_y - 15,
                    center_x + 15, center_y + 15,
                    fill='#FFD700', outline='#FFA500', width=2
                )
        
        self.canvas.bind('<Configure>', update_canvas_size)
        
    def create_file_section(self):
        """Create responsive file selection section"""
        file_frame = ctk.CTkFrame(self.left_panel, corner_radius=15, fg_color="#1a1a1a")
        file_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        file_frame.grid_columnconfigure(1, weight=1)  # Entry field expands
        
        # Title
        ctk.CTkLabel(
            file_frame,
            text="📁 SELECT FILE",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=3, pady=(15, 10))
        
        # File path entry
        self.file_entry = ctk.CTkEntry(
            file_frame,
            textvariable=self.file_path,
            placeholder_text="Choose file to analyze...",
            height=40,
            corner_radius=20,
            font=ctk.CTkFont(size=12)
        )
        self.file_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 15))
        
        # Browse button
        browse_btn = ctk.CTkButton(
            file_frame,
            text="Browse",
            width=100,
            height=40,
            corner_radius=20,
            fg_color="#1E90FF",
            hover_color="#0080FF",
            command=self.browse_file
        )
        browse_btn.grid(row=1, column=2, sticky="e", padx=(10, 15), pady=(0, 15))
        
    def create_operation_section(self):
        """Create responsive operation section"""
        operation_frame = ctk.CTkFrame(self.left_panel, corner_radius=15, fg_color="#1a1a1a")
        operation_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 15))
        operation_frame.grid_columnconfigure(0, weight=1)
        operation_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        ctk.CTkLabel(
            operation_frame,
            text="⚙️ OPERATION",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=(15, 10))
        
        # Radio buttons in a responsive layout
        embed_radio = ctk.CTkRadioButton(
            operation_frame,
            text="🔒 Embed Message",
            variable=self.operation,
            value="embed",
            font=ctk.CTkFont(size=14),
            command=self.toggle_operation
        )
        embed_radio.grid(row=1, column=0, sticky="w", padx=15, pady=5)
        
        extract_radio = ctk.CTkRadioButton(
            operation_frame,
            text="🔓 Extract Message",
            variable=self.operation,
            value="extract",
            font=ctk.CTkFont(size=14),
            command=self.toggle_operation
        )
        extract_radio.grid(row=1, column=1, sticky="w", padx=15, pady=(5, 15))
        
    def create_message_section(self):
        """Create responsive message section"""
        message_frame = ctk.CTkFrame(self.left_panel, corner_radius=15, fg_color="#1a1a1a")
        message_frame.grid(row=3, column=0, sticky="nsew", padx=15, pady=(0, 15))
        message_frame.grid_columnconfigure(0, weight=1)
        message_frame.grid_rowconfigure(1, weight=1)  # Text area expands
        
        # Title
        self.message_label = ctk.CTkLabel(
            message_frame,
            text="💬 SECRET MESSAGE",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.message_label.grid(row=0, column=0, pady=(15, 10))
        
        # Message text area
        self.message_text = ctk.CTkTextbox(
            message_frame,
            corner_radius=15,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word"
        )
        self.message_text.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
    def create_action_buttons(self):
        """Create responsive action buttons"""
        button_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        button_frame.grid(row=4, column=0, sticky="ew", padx=15, pady=(0, 15))
        button_frame.grid_columnconfigure(0, weight=3)  # Execute button gets more space
        button_frame.grid_columnconfigure(1, weight=1)  # Clear button
        
        # Execute button
        execute_btn = ctk.CTkButton(
            button_frame,
            text="🚀 EXECUTE",
            height=45,
            corner_radius=22,
            fg_color="#FF6B6B",
            hover_color="#FF5252",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.execute_operation
        )
        execute_btn.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        # Clear button
        clear_btn = ctk.CTkButton(
            button_frame,
            text="🧹 CLEAR",
            height=45,
            corner_radius=22,
            fg_color="#6C7B7F",
            hover_color="#5A6B7F",
            command=self.clear_fields
        )
        clear_btn.grid(row=0, column=1, sticky="ew")
        
    def create_right_panel(self):
        """Create responsive metadata panel"""
        self.right_panel = ctk.CTkFrame(
            self.main_scrollable,
            corner_radius=20,
            fg_color="#2a1a32",
            border_width=2,
            border_color="#8A2BE2"
        )
        self.right_panel.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(0, 10))
        
        # Configure internal grid
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)  # Metadata content expands
        
        # Header
        header_frame = ctk.CTkFrame(
            self.right_panel,
            corner_radius=15,
            height=70,
            fg_color="#1a1a1a"
        )
        header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_rowconfigure(0, weight=1)
        
        ctk.CTkLabel(
            header_frame,
            text="📊 FILE METADATA",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#BB86FC"
        ).grid(row=0, column=0)
        
        # Metadata content (scrollable)
        metadata_frame = ctk.CTkFrame(
            self.right_panel,
            corner_radius=15,
            fg_color="#0a0a0a"
        )
        metadata_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        metadata_frame.grid_columnconfigure(0, weight=1)
        metadata_frame.grid_rowconfigure(0, weight=1)
        
        # Scrollable metadata text
        self.metadata_text = ctk.CTkTextbox(
            metadata_frame,
            corner_radius=10,
            font=ctk.CTkFont(family="Consolas", size=11),
            wrap="word"
        )
        self.metadata_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # File statistics section
        self.create_stats_section()
        
    def create_stats_section(self):
        """Create file statistics section"""
        stats_frame = ctk.CTkFrame(
            self.right_panel,
            corner_radius=15,
            height=120,
            fg_color="#1a1a1a"
        )
        stats_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 15))
        stats_frame.grid_propagate(False)
        stats_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Stats title
        ctk.CTkLabel(
            stats_frame,
            text="📈 QUICK STATS",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#00FF7F"
        ).grid(row=0, column=0, columnspan=2, pady=(10, 5))
        
        # Stats labels
        self.size_label = ctk.CTkLabel(
            stats_frame,
            text="Size: --",
            font=ctk.CTkFont(size=12),
            text_color="#CCCCCC"
        )
        self.size_label.grid(row=1, column=0, sticky="w", padx=10)
        
        self.type_label = ctk.CTkLabel(
            stats_frame,
            text="Type: --",
            font=ctk.CTkFont(size=12),
            text_color="#CCCCCC"
        )
        self.type_label.grid(row=1, column=1, sticky="w", padx=10)
        
        self.dimensions_label = ctk.CTkLabel(
            stats_frame,
            text="Dimensions: --",
            font=ctk.CTkFont(size=12),
            text_color="#CCCCCC"
        )
        self.dimensions_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 10))
        
    def animate_floating_elements(self):
        """Animate the floating elements responsively"""
        try:
            if hasattr(self, 'canvas') and self.canvas.winfo_exists():
                self.animation_angle += 2
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                
                if canvas_width > 1 and canvas_height > 1:
                    center_x, center_y = canvas_width // 2, canvas_height // 2
                    
                    for i, item in enumerate(self.animation_items):
                        if self.canvas.coords(item):
                            # Create floating effect
                            offset_angle = self.animation_angle + (i * 72)
                            offset_x = math.sin(math.radians(offset_angle)) * 1.5
                            offset_y = math.cos(math.radians(offset_angle)) * 1.5
                            
                            # Small floating movement
                            self.canvas.move(item, offset_x * 0.1, offset_y * 0.1)
                    
                    # Pulse the center circle
                    if hasattr(self, 'center_circle') and self.canvas.coords(self.center_circle):
                        pulse = 2 + math.sin(math.radians(self.animation_angle * 2)) * 0.5
                        
        except Exception:
            pass  # Continue animation even if elements are destroyed
            
        # Schedule next frame
        self.root.after(50, self.animate_floating_elements)
        
    def toggle_operation(self):
        """Toggle between embed and extract modes"""
        if self.operation.get() == "extract":
            self.message_label.configure(text="📤 EXTRACTED MESSAGE")
            self.message_text.delete("1.0", "end")
            self.message_text.insert("1.0", "Extracted message will appear here...")
        else:
            self.message_label.configure(text="💬 SECRET MESSAGE")
            self.message_text.delete("1.0", "end")
            
    def browse_file(self):
        """Open file dialog with proper file types"""
        filetypes = [
            ("All supported files", 
             "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp "
             "*.wav *.flac *.m4a *.ogg *.aiff *.au *.opus *.aac *.mp3 "
             "*.mp4 *.mkv *.mov *.avi *.webm *.flv *.wmv "
             "*.zip *.rar *.7z"),
        
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp"),
            ("Audio files", "*.wav *.flac *.m4a *.ogg *.aiff *.au *.opus *.aac *.mp3"),
            ("Video files", "*.mp4 *.mkv *.mov *.avi *.webm *.flv *.wmv"),
            ("Archive files", "*.zip *.7z *.rar"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select File - Steganography Analyzer",
            filetypes=filetypes
        )
        
        if filename:
            self.file_path.set(filename)
            self.extract_metadata(filename)
            
    def extract_metadata(self, file_path):
        """Extract and display file metadata with statistics"""
        self.metadata_text.delete("1.0", "end")
        
        if not os.path.exists(file_path):
            self.metadata_text.insert("end", "❌ File not found.\n")
            self.update_stats("--", "--", "--")
            return
            
        try:
            # Basic file info
            file_size_bytes = os.path.getsize(file_path)
            file_size_kb = file_size_bytes / 1024
            file_size_mb = file_size_kb / 1024
            
            # Format file size
            if file_size_mb >= 1:
                size_str = f"{file_size_mb:.2f} MB"
            else:
                size_str = f"{file_size_kb:.2f} KB"
                
            mime_type, _ = mimetypes.guess_type(file_path)
            file_name = os.path.basename(file_path)
            
            metadata = f"""📁 FILE INFORMATION
{'='*40}
Name: {file_name}
Path: {file_path}
Size: {size_str} ({file_size_bytes:,} bytes)
Type: {mime_type or 'Unknown'}
Modified: {datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')}

"""
            
            dimensions_str = "--"
            
            # Image metadata
            if mime_type and mime_type.startswith("image"):
                try:
                    img = Image.open(file_path)
                    dimensions_str = f"{img.width} × {img.height}"
                    
                    metadata += f"""🖼️ IMAGE DETAILS
{'='*40}
Format: {img.format}
Dimensions: {dimensions_str}
Mode: {img.mode}
Has Alpha: {'Yes' if 'A' in img.mode else 'No'}
Aspect Ratio: {img.width/img.height:.2f}:1

"""
                    
                    # EXIF data
                    exif_data = img.getexif()
                    if exif_data:
                        metadata += "📷 EXIF DATA\n" + "="*40 + "\n"
                        for tag, value in list(exif_data.items())[:10]:  # Limit to first 10
                            tag_name = ExifTags.TAGS.get(tag, f"Tag_{tag}")
                            metadata += f"{tag_name}: {value}\n"
                        if len(exif_data) > 10:
                            metadata += f"... and {len(exif_data) - 10} more EXIF entries\n"
                    else:
                        metadata += "📷 No EXIF data found.\n"
                        
                except Exception as e:
                    metadata += f"❌ Error reading image: {e}\n"
                    
            # Video metadata
            elif mime_type and mime_type.startswith("video"):
                try:
                    cap = cv2.VideoCapture(file_path)
                    if cap.isOpened():
                        fps = cap.get(cv2.CAP_PROP_FPS)
                        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        duration = frame_count / fps if fps > 0 else 0
                        dimensions_str = f"{width} × {height}"
                        
                        metadata += f"""🎥 VIDEO DETAILS
{'='*40}
Resolution: {dimensions_str}
Frame Rate: {fps:.2f} FPS
Total Frames: {frame_count:,}
Duration: {str(datetime.timedelta(seconds=int(duration)))}
Bitrate: {(file_size_bytes * 8) / (duration * 1000) if duration > 0 else 0:.0f} kbps
"""
                    cap.release()
                except Exception as e:
                    metadata += f"❌ Error reading video: {e}\n"
                    
            # Update quick stats
            self.update_stats(size_str, mime_type or "Unknown", dimensions_str)
            
            self.metadata_text.insert("1.0", metadata)
            
        except Exception as e:
            self.metadata_text.insert("1.0", f"❌ Error extracting metadata: {e}")
            self.update_stats("Error", "Error", "Error")
            
    def update_stats(self, size, file_type, dimensions):
        """Update the quick stats section"""
        self.size_label.configure(text=f"Size: {size}")
        self.type_label.configure(text=f"Type: {file_type}")
        self.dimensions_label.configure(text=f"Dimensions: {dimensions}")
        
    def clear_fields(self):
        """Clear all input fields"""
        self.file_path.set("")
        self.message_text.delete("1.0", "end")
        self.metadata_text.delete("1.0", "end")
        self.update_stats("--", "--", "--")
        
    def show_modern_popup(self, title, message, success=True):
        """Show modern responsive popup"""
        popup = ctk.CTkToplevel(self.root)
        popup.title(title)
        popup.geometry("450x250")
        popup.resizable(True, True)
        popup.minsize(350, 200)
        
        # Center the popup
        popup.transient(self.root)
        popup.grab_set()
        
        # Configure popup grid
        popup.grid_columnconfigure(0, weight=1)
        popup.grid_rowconfigure(0, weight=1)
        
        # Style the popup
        color = "#4CAF50" if success else "#FF5252"
        
        main_frame = ctk.CTkFrame(
            popup,
            corner_radius=20,
            fg_color="#1a1a1a",
            border_width=2,
            border_color=color
        )
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure((0, 1, 2), weight=1)
        
        # Icon and title
        icon = "✅" if success else "❌"
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"{icon} {title}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=color
        )
        title_label.grid(row=0, column=0, pady=20)
        
        # Message
        msg_label = ctk.CTkLabel(
            main_frame,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=400
        )
        msg_label.grid(row=1, column=0, padx=20)
        
        # OK button
        ok_btn = ctk.CTkButton(
            main_frame,
            text="OK",
            width=120,
            height=40,
            corner_radius=20,
            fg_color=color,
            command=popup.destroy
        )
        ok_btn.grid(row=2, column=0, pady=20)
        
    def execute_operation(self):
        """Execute the selected operation with proper error handling"""
        file_path = self.file_path.get()
        
        if not file_path:
            self.show_modern_popup("Error", "Please select a file first!", success=False)
            return
            
        try:
            if self.operation.get() == "embed":
                message = self.message_text.get("1.0", "end").strip()
                if not message:
                    self.show_modern_popup("Error", "Please enter a message to embed!", success=False)
                    return
                    
                # Save dialog
                file_ext = os.path.splitext(file_path)[1].lower()
                initial_filename = os.path.splitext(os.path.basename(file_path))[0] + "_stego" + file_ext
                
                if file_ext in [".png", ".jpg", ".jpeg", ".bmp"]:
                    filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")]
                elif file_ext in [".mp4", ".mkv", ".mov", ".avi", ".webm", ".flv", ".wmv"]:
                    filetypes = [("Video files", "*.mp4 *.mkv *.mov *.avi *.webm *.flv *.wmv"), ("All files", "*.*")]
                else:
                    filetypes = [("All files", "*.*")]
                    
                output_path = filedialog.asksaveasfilename(
                    title="Save Stego File As",
                    defaultextension=file_ext,
                    initialfile=initial_filename,
                    filetypes=filetypes
                )
                
                if output_path:
                    success, result = embed_message(file_path, output_path, message)
                    if success:
                        media_type = "video" if file_ext in [".mp4", ".mkv", ".mov", ".avi", ".webm", ".flv", ".wmv"] else "image"
                        self.show_modern_popup("Success!", f"Message successfully hidden in the {media_type}!\n\nSaved to: {os.path.basename(output_path)}")
                    else:
                        self.show_modern_popup("Failed", f"Operation failed: {result}", success=False)
                        
            elif self.operation.get() == "extract":
                success, message = extract_message(file_path)
                if success:
                    self.message_text.delete("1.0", "end")
                    self.message_text.insert("1.0", message)
                    
                    file_ext = os.path.splitext(file_path)[1].lower()
                    media_type = "video" if file_ext in [".mp4", ".mkv", ".mov", ".avi", ".webm", ".flv", ".wmv"] else "image"
                    char_count = len(message)
                    self.show_modern_popup("Success!", f"Message successfully extracted from the {media_type}!\n\nExtracted {char_count} characters.")
                else:
                    self.show_modern_popup("Failed", f"Extraction failed: {message}", success=False)
                    
        except Exception as e:
            self.show_modern_popup("Error", f"An unexpected error occurred:\n{str(e)}", success=False)
            
    def run(self):
        """Start the application"""
        # Bind window resize event for responsiveness
        self.root.bind('<Configure>', self.on_window_resize)
        self.root.mainloop()
        
    def on_window_resize(self, event=None):
        """Handle window resize events"""
        if event and event.widget == self.root:
            # Update canvas animation if needed
            if hasattr(self, 'canvas'):
                self.root.after_idle(self.setup_animation)

if __name__ == "__main__":
    app = ModernSteganographyApp()
    app.run()
