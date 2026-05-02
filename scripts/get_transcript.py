import sys
import subprocess
import urllib.request
import re
import os

def install_dependencies():
    try:
        import youtube_transcript_api
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "youtube-transcript-api", "--quiet"])

def get_video_metadata(video_id):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        # Extract title
        title_match = re.search(r'<title>(.*?)</title>', html)
        title = title_match.group(1).replace(" - YouTube", "") if title_match else "Unknown Title"
        
        # Try to extract channel name
        channel_match = re.search(r'"author":"(.*?)"', html)
        channel = channel_match.group(1) if channel_match else "Unknown Channel"
        
        return {"title": title, "channel": channel}
    except Exception:
        return {"title": "Unknown Title", "channel": "Unknown Channel"}

def format_time(seconds):
    mins, secs = divmod(int(seconds), 60)
    hours, mins = divmod(mins, 60)
    if hours > 0:
        return f"{hours:02d}:{mins:02d}:{secs:02d}"
    return f"{mins:02d}:{secs:02d}"

def get_transcript(video_id, target_lang='en'):
    from youtube_transcript_api import YouTubeTranscriptApi
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        
        transcript_obj = None
        try:
            transcript_obj = transcript_list.find_transcript([target_lang])
        except Exception:
            for t in transcript_list:
                if t.is_translatable:
                    try:
                        transcript_obj = t.translate(target_lang)
                        break
                    except Exception:
                        pass
            if not transcript_obj:
                transcript_obj = list(transcript_list)[0]

        transcript_data = transcript_obj.fetch()
        formatted_lines = []
        for snippet in transcript_data:
            start_time = format_time(snippet.start)
            formatted_lines.append(f"[{start_time}] {snippet.text}")
            
        return "\n".join(formatted_lines)
    except Exception as e:
        return f"Transcript Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py get_transcript.py <VIDEO_ID_OR_URL> [LANG_CODE]")
        sys.exit(1)
    
    install_dependencies()
    
    video_input = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else 'en'
    
    # Robust Regex for YouTube Video ID extraction
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})(?:\?|&|/|$)', video_input)
    if match:
        video_id = match.group(1)
    else:
        # Fallback if the user just passed the raw 11-character ID
        video_id = video_input.strip()
        if len(video_id) != 11:
            print("Error: Could not extract a valid 11-character YouTube Video ID.")
            sys.exit(1)
        
    metadata = get_video_metadata(video_id)
    transcript_text = get_transcript(video_id, lang)
    
    # Check if a valid transcript was found before saving
    is_error = transcript_text.startswith("Transcript Error:")
    file_path = "None (Error fetching transcript)"
    
    if not is_error:
        # Backup full transcript to a file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        transcripts_dir = os.path.join(os.path.dirname(script_dir), "transcripts")
        if not os.path.exists(transcripts_dir):
            os.makedirs(transcripts_dir)
            
        # Cache cleanup: Delete files older than 7 days
        current_time = time.time()
        for filename in os.listdir(transcripts_dir):
            cache_file = os.path.join(transcripts_dir, filename)
            if os.path.isfile(cache_file):
                if (current_time - os.path.getmtime(cache_file)) > (7 * 86400):
                    try:
                        os.remove(cache_file)
                    except Exception:
                        pass
        
        file_path = os.path.join(transcripts_dir, f"{video_id}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"TITLE: {metadata['title']}\n")
            f.write(f"CHANNEL: {metadata['channel']}\n")
            f.write(f"LANGUAGE: {lang.upper()}\n")
            f.write("-" * 20 + "\n")
            f.write(transcript_text)
    
    # Output to console (Clean and complete)
    print(f"TITLE: {metadata['title']}")
    print(f"CHANNEL: {metadata['channel']}")
    print(f"LANGUAGE: {lang.upper()}")
    if not is_error:
        print(f"FILE_BACKUP: {file_path}")
    print("\n--- TRANSCRIPT START ---")
    print(transcript_text)
    print("--- TRANSCRIPT END ---")
