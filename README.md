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

### Schedule
The workflow runs daily at 14:00 UTC. You can adjust the `cron` in `.github/workflows/daily_tweet.yml` and also trigger manually via “Run workflow”.

### Local Dry Run
You can preview the tweet text (and optionally the generated image) without posting:

```bash
python scripts/daily_tweet.py --dry-run --no-image
```

Remove `--no-image` to also generate an image locally (requires Pillow).
