"""Utility helper functions."""

import base64
import io
from datetime import datetime


def image_to_base64(uploaded_file):
    """Convert uploaded file to base64 string for storage."""
    if uploaded_file is None:
        return None
    try:
        from PIL import Image
        image = Image.open(uploaded_file)
        image = image.convert('RGB')
        max_size = (500, 500)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=80)
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/jpeg;base64,{img_str}"
    except ImportError:
        # Pillow not available - store raw base64
        content = uploaded_file.read()
        img_str = base64.b64encode(content).decode('utf-8')
        return f"data:image/jpeg;base64,{img_str}"


def format_time_ago(iso_time):
    """Convert ISO timestamp to human-readable time ago string."""
    if not iso_time:
        return "Unknown"
    try:
        then = datetime.fromisoformat(iso_time)
        now = datetime.utcnow()
        diff = now - then
        seconds = diff.total_seconds()
        if seconds < 60:
            return "Just now"
        elif seconds < 3600:
            return f"{int(seconds // 60)}m ago"
        elif seconds < 86400:
            return f"{int(seconds // 3600)}h ago"
        elif seconds < 604800:
            return f"{int(seconds // 86400)}d ago"
        else:
            return then.strftime("%b %d, %Y")
    except (ValueError, TypeError):
        return "Unknown"
