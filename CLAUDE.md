# AI Workshop Site

Static GitHub Pages site collecting the "Effective AI for Educators" workshop:
embedded videos, slide-derived notes, transcripts, and per-video summaries.

## Layout

* `build.py` -- generator; produces `www/` from `slides/` + `content/`
* `slides/` -- source slide decks (`<base>.md`) and `slides/pdfs/<base>.pdf`
* `content/summaries/<num>.md` -- per-session summary (optional)
* `content/transcripts/<num>.md` -- per-session transcript (optional)
* `content/topics/<num>.md` -- index-page "topics covered" list (optional)
* `www/` -- generated output. Do NOT hand-edit; it is wiped on every build.

Edit `slides/` or `content/`, then re-run the build. Never edit `www/` directly.

## Sessions

| num | video id      | base                    |
|-----|---------------|-------------------------|
| 1   | gOUW4jmGJVY   | 1_command_line_agents   |
| 2   | 5i7lhEwNf_Q   | 2_authoring_materials   |
| 3   | ThDrQYSa1hs   | 3_building_assessments  |
| 4   | sy7_FeHPPRo   | 4_running_the_course    |
| 5   | qnng0s1sNaU   | 5_qa_and_handson        |

## Building

Requires the `markdown` Python package. Run with the shared scripts venv:

```bash
uv run --project ../templates/csci-366-template/meta/scripts python build.py
```

Or any environment with `markdown` installed (`pip install markdown`).

## Updating Transcripts

The videos are recorded livestreams. YouTube disables captions until it finishes
processing, so the first build shipped placeholders. When captions appear:

1. Fetch the timestamped transcript for each video id:

```python
from youtube_transcript_api import YouTubeTranscriptApi
api = YouTubeTranscriptApi()
for seg in api.fetch("gOUW4jmGJVY"):   # seg.text, seg.start (seconds), seg.duration
    ...
```

   * If `fetch` raises `TranscriptsDisabled`, captions are still not ready -- stop
     and leave the placeholder. Do not invent a transcript.
   * `yt-dlp --list-subs <url>` is a fallback check for caption availability.

2. Write the transcript to `content/transcripts/<num>.md` as plain markdown.
   Keep periodic timestamp markers so readers can find a spot, e.g.
   `**[12:30]** ...text...`.

3. Write a summary to `content/summaries/<num>.md`. Link key moments to the
   video at the right second using `https://youtu.be/<id>?t=SECONDS`
   (integer seconds, taken from `seg.start`). Example:

   ```markdown
   * [Setting up CLAUDE.md](https://youtu.be/gOUW4jmGJVY?t=420)
   ```

   These summaries matter because the speaker sometimes goes off-topic; the
   summary plus timestamp links let viewers jump to the relevant parts.

4. Optionally write `content/topics/<num>.md` as a markdown bullet list of the
   topics covered; it replaces the index-page placeholder.

5. Re-run the build and confirm the placeholders are gone:

```bash
uv run --project ../templates/csci-366-template/meta/scripts python build.py
grep -rl "coming soon\|will be added\|will be posted" www/   # should be empty when complete
```

## Conventions

* Keep prose terse, ASCII only, no em-dashes.
* Do not fabricate transcript text, timestamps, or topics. If the source is not
  available, leave the placeholder in place.
