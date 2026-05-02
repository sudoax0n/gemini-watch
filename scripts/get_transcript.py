import sys
import subprocess
import urllib.request
import re
import os

def install_dependencies():
    try:
        import youtube_transcript_api
    except ImportError:
        print("Installing dependencies...", file=sys.stderr)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "youtube-transcript-api", "--quiet"])

def get_video_metadata(video_id):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        # Extract title
        title_match = re.search(r'<title>(.*?)</title>', html)
        title = title_match.group(1).replace(" - YouTube", "") if title_match else "Unknown Title"
        
        # Try to extract channel name from basic metadata
        channel_match = re.search(r'"author":"(.*?)"', html)
        channel = channel_match.group(1) if channel_match else "Unknown Channel"
        
        return {"title": title, "channel": channel}
    except Exception as e:
        return {"title": f"Could not fetch metadata: {str(e)}", "channel": "Unknown"}

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
            # 1. Try target language first (e.g., 'en')
            transcript_obj = transcript_list.find_transcript([target_lang])
        except:
            # 2. Fallback to translation if not available natively
            for t in transcript_list:
                if t.is_translatable:
                    try:
                        transcript_obj = t.translate(target_lang)
                        break
                    except:
                        pass
            # 3. Absolute fallback: Just grab whatever the default is
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
    
    video_id = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else 'en'
    
    # Handle full URLs
    if "v=" in video_id:
        video_id = video_id.split("v=")[1].split("&")[0]
    elif "youtu.be/" in video_id:
        video_id = video_id.split("youtu.be/")[1].split("?")[0]
    
    video_id = video_id.strip()
        
    metadata = get_video_metadata(video_id)
    transcript_text = get_transcript(video_id, lang)
    
    # Save full transcript to a file to prevent truncation issues
    script_dir = os.path.dirname(os.path.abspath(__file__))
    transcripts_dir = os.path.join(os.path.dirname(script_dir), "transcripts")
    if not os.path.exists(transcripts_dir):
        os.makedirs(transcripts_dir)
    
    file_path = os.path.join(transcripts_dir, f"{video_id}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"TITLE: {metadata['title']}\n")
        f.write(f"CHANNEL: {metadata['channel']}\n")
        f.write(f"LANGUAGE: {lang.upper()}\n")
        f.write("-" * 20 + "\n")
        f.write(transcript_text)
    
    print(f"--- VIDEO METADATA ---")
    print(f"Title: {metadata['title']}")
    print(f"Channel: {metadata['channel']}")
    print(f"Language: {lang.upper()}")
    print(f"FULL_FILE_PATH: {file_path}")
    print(f"--- TRANSCRIPT (SNIPPET) ---")
    # Only print first 50 lines to console to avoid truncation warnings
    lines = transcript_text.split("\n")
    print("\n".join(lines[:50]))
    if len(lines) > 50:
        print(f"\n... [{len(lines) - 50} lines omitted].")
        print(f"CRITICAL: Use 'read_file' on the FULL_FILE_PATH above to see the entire transcript.")
