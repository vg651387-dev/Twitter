# Twitter

## Documentation
- See `docs/README.md` for the documentation index
- Generate reference docs (when code is present): `bash scripts/generate-docs.sh`

## Status
This repository currently has no source files. Documentation scaffolding has been added under `docs/` to support future development.

## Daily Twitter Automation
A GitHub Actions workflow posts a daily coding tip with an image to Twitter.

### Configure Secrets
Create the following repository secrets with credentials from your Twitter/X developer app (OAuth 1.0a):
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`

Optional for Google Images (Custom Search API):
- `GOOGLE_API_KEY`
- `GOOGLE_CSE_ID`

Optional rights filter for images (set as an environment variable, not a secret if preferred):
- `GOOGLE_IMAGE_RIGHTS_FILTER` (e.g., `cc_publicdomain|cc_attribute`)

### Schedule
The workflow runs daily at 14:00 UTC. You can adjust the `cron` in `.github/workflows/daily_tweet.yml` and also trigger manually via “Run workflow”.

### Local Dry Run
You can preview the tweet text (and optionally the generated image) without posting:

```bash
python scripts/daily_tweet.py --dry-run --no-image
```

Remove `--no-image` to also generate an image locally (requires Pillow).

### Google Images and News Tweets
The script supports fetching images from Google and posting news-based tweets.

- Use Google Images for the picture (falls back to generated if keys are missing):
```bash
python scripts/daily_tweet.py --dry-run --image-source google
```

- Post a news tweet for a topic, with a Google image based on the headline/topic:
```bash
python scripts/daily_tweet.py --dry-run --news-topic "technology" --image-source google
```

- Provide an explicit image query (optional):
```bash
python scripts/daily_tweet.py --dry-run --image-source google --image-query "python programming"
```

- Real post with news + Google image (requires all Twitter secrets, and optional Google keys):
```bash
TWITTER_API_KEY=... \
TWITTER_API_SECRET=... \
TWITTER_ACCESS_TOKEN=... \
TWITTER_ACCESS_TOKEN_SECRET=... \
GOOGLE_API_KEY=... \
GOOGLE_CSE_ID=... \
python scripts/daily_tweet.py --news-topic "technology" --image-source google
```

- Tip content file: `content/coding_tips.txt` (optional; defaults are built in).

### CI Behavior
The GitHub workflow will:
- Post a daily coding tip using `--image-source google` if Google keys are configured (otherwise it generates an image).
- Post a daily technology news tweet using `--news-topic "technology" --image-source google`.
