# Demo Video Draft

This folder contains a half-size HyperFrames preview render of the 3-minute visual draft for the Kaggle demo video.

The official HyperFrames agent workflow is skill-based:

```bash
npx skills add heygen-com/hyperframes
```

That installs the HyperFrames authoring skills plus the CLI workflow guidance. The render/preview commands still use the official `npx hyperframes` CLI.

## Files

- `index.html` - HyperFrames preview entrypoint, rendered at `960 x 540`.
- `narration_180.m4a` - 180-second generated English narration track.
- `gemma_garden_guardian_demo_preview_with_audio.mp4` - rendered preview MP4 with narration.

## Placeholder Section

The `0:45 - 1:40` demo segment is intentionally mocked with a Streamlit-style UI and a small `placeholder demo footage` ribbon. After recording the real app demo, replace that segment with the screen recording or edit the HTML section that starts at:

```html
<section id="scene-demo-placeholder" class="clip scene" data-start="45" data-duration="55" data-track-index="1">
```

Recommended real footage for replacement:

1. Upload a tomato sample image.
2. Enter crop type: `tomato`.
3. Add short notes about yellow lower leaves and dry soil.
4. Click analyze.
5. Show the dashboard, todos, JSON, history, and weekly report.

## Render

Requirements:

- Node.js 22 or later
- FFmpeg
- HyperFrames skills installed with `npx skills add heygen-com/hyperframes`

## FFmpeg Install Options

HyperFrames only needs `ffmpeg` and `ffprobe` to be available on `PATH`.

### Option A: MacPorts

```bash
sudo port install ffmpeg
export PATH="/opt/local/bin:$PATH"
ffmpeg -version
ffprobe -version
```

### Option B: npm static binaries

This avoids Homebrew and keeps the binaries local to the project, but it needs small wrapper scripts because the npm packages expose paths from Node modules rather than normal shell commands.

```bash
npm install --save-dev ffmpeg-static ffprobe-static
```

Then create wrapper commands named `ffmpeg` and `ffprobe`, add that wrapper directory to `PATH`, and run HyperFrames from the same shell.

### Option C: standalone macOS binaries

Download standalone macOS builds of `ffmpeg` and `ffprobe`, put both binaries in a local tools directory such as `tools/ffmpeg/`, make them executable, and add that directory to `PATH`.

```bash
chmod +x tools/ffmpeg/ffmpeg tools/ffmpeg/ffprobe
export PATH="$PWD/tools/ffmpeg:$PATH"
ffmpeg -version
ffprobe -version
```

Render:

```bash
npx hyperframes lint demo_video_preview --verbose
npx hyperframes inspect demo_video_preview --samples 12
npx hyperframes render demo_video_preview --output demo_video_preview/gemma_garden_guardian_demo_preview.mp4 --quality draft --fps 15 --workers 1
```

## Notes

- The composition is visual-only. Use `docs/video_script.md` as the narration script when recording voiceover.
- The thumbnail image lives at `assets/thumbnail.png`.
- The mock demo segment can stay in the draft video until real app footage is ready.
