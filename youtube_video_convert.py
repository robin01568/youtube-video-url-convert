from django import template
from urllib.parse import urlparse, parse_qs

register = template.Library()

@register.filter
def youtube_embed(value):
    """
    Convert a YouTube link into an embeddable URL.
    Example:
    Input: https://youtu.be/6stlCkUDG_s?feature=shared
    Input: https://www.youtube.com/embed/6stlCkUDG_s?si=dFBDOxA7c7o8uMtH
    Input: https://www.youtube.com/watch?v=6stlCkUDG_s&list=PL4Gr5tOAPttLOY9IrWVjJlv4CtkYI5cI_

    
    Output: https://www.youtube.com/embed/6stlCkUDG_s
    """
    parsed_url = urlparse(value)
    if "youtu.be" in parsed_url.netloc:  # Shortened YouTube URL
        video_id = parsed_url.path[1:]  # Extract the path after '/'
    elif "youtube.com" in parsed_url.netloc and "/watch" in parsed_url.path:  # Full YouTube URL
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get("v", [None])[0]
    elif "youtube.com" in parsed_url.netloc:  # Extract Embed URL
        video_id = parsed_url.path[7:]
    else:
        return value  # Return as-is if not a valid YouTube link

    # Construct the embed URL
    if video_id:
        return f"https://www.youtube.com/embed/{video_id}"
    return value  # Return as-is if no video ID found


