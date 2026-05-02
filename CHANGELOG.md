# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-05-02
### Added
- **Titanium Parser**: Robust Regex engine to flawlessly extract video IDs from any URL format (Shorts, mobile links, query parameters).
- **Smart Caching**: Automatically saves large transcripts to local `.txt` files to bypass CLI console truncation limits.
- **Auto-Cleanup**: Automatically deletes cached transcripts older than 7 days to keep your system clean.

### Fixed
- Fixed an issue where YouTube Shorts URLs would crash the script due to illegal filename characters.
- Fixed a bug where a failed fetch would generate a useless error file.
- Removed artificial console truncation and alarming warnings, opting for a clean data dump.

## [1.0.0] - 2026-04-29
### Added
- Initial release of **Gemini Watch**.
- Native transcription engine using `youtube-transcript-api`.
- Real-time **Timestamp** formatting (`[MM:SS]`) for precise navigation.
- **Metadata Extraction** (Title and Channel) for instant context.
- Auto-dependency installation logic for zero-friction setup.
- Multi-language support with automatic translation fallback.
- Comprehensive `README.md` and `LICENSE`.
- Gemini-native `GEMINI.md` instruction set.
