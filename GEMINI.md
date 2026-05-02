# Gemini Watch Extension

This extension allows Gemini CLI to "watch" YouTube videos by extracting transcripts, timestamps, and metadata natively.

## Core Mandate
When a user provides a YouTube URL, you must:
1. Extract the Video ID.
2. Run the `get_transcript.py` script to fetch the metadata and timestamped text content.
3. Summarize or analyze the content as requested.

## Tools
### `get_youtube_transcript`
**Usage:** `py scripts/get_transcript.py <VIDEO_ID_OR_URL> [LANG_CODE]`
**Output:** Video metadata followed by a transcript snippet and a `FULL_FILE_PATH`.

## Guidelines
- **Large Transcripts:** If the video is long, the script will output a `FULL_FILE_PATH`. You **MUST** use the `read_file` tool on that path to retrieve the full content for analysis. Do not rely on the console snippet for long-form summarization.
- **Privacy:** Do not store transcripts permanently unless requested.
- **Context:** Use the extracted Title and Channel to better understand the overall context before analyzing the transcript.
- **Timestamps:** When answering specific questions or summarizing key moments, always include the `[MM:SS]` timestamps provided in the transcript to help the user navigate to those moments.
- **Language:** If the user asks for a summary of a video in a specific language, you can pass the 2-letter language code (e.g. `es`, `fr`) as an optional second argument to the script to attempt to fetch a translated transcript.

## Example
User: "Summarize this video: https://www.youtube.com/watch?v=dQw4w9WgXcQ"
Agent Strategy:
1. ID = `dQw4w9WgXcQ`
2. Run `py scripts/get_transcript.py dQw4w9WgXcQ`
3. Read the output. Note the title and channel.
4. Process the text and provide the summary, referencing key timestamps.

## Known Issues
- **Transcript Truncation:** For long videos (>20 mins), the CLI's console output may be truncated, causing the agent to miss the middle content. 

## Roadmap
- [x] **Large Transcript Handling:** Update the engine to save full transcripts to a local file and provide the path to the agent for direct reading.
- [ ] **Playlist Support:** Add the ability to fetch transcripts for all videos in a YouTube playlist.
- [ ] **Language Targeting:** Improve native support for specifying target translation languages.
