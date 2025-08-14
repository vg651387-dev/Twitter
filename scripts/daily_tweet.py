#!/usr/bin/env python3
import argparse
import datetime
import hashlib
import os
import random
import sys
from typing import List, Optional, Tuple

# Pillow is optional for dry-run or no-image modes
try:
    from PIL import Image, ImageDraw, ImageFont  # type: ignore
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False


def read_tips_from_file(file_path: str) -> List[str]:
    if not os.path.exists(file_path):
        return []
    tips: List[str] = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            tip = line.strip()
            if tip and not tip.startswith("#"):
                tips.append(tip)
    return tips


def get_default_tips() -> List[str]:
    return [
        "Write clear, descriptive variable and function names. Readers > cleverness.",
        "Prefer small, focused functions. One responsibility per function.",
        "Fail fast: validate inputs early and return on error conditions.",
        "Write tests for edge cases first. They define behavior.",
        "Avoid premature optimization. Make it work, then make it fast.",
        "Use version control branches for each change; keep commits atomic.",
        "Document non-obvious decisions in code comments or ADRs.",
        "Log context, not noise. Include identifiers that help debugging.",
        "Handle errors explicitly. Never swallow exceptions silently.",
        "Prefer composition over inheritance to reduce coupling.",
        "Keep dependencies up to date; pin versions for reproducibility.",
        "Automate formatting and linting to keep diffs clean.",
        "Make data structures immutable unless mutation is required.",
        "Name booleans with positive intent (isEnabled, hasAccess).",
        "Review diffs before pushing; consider readability and design.",
        "Prefer pure functions; minimize shared state.",
        "Use feature flags to roll out risky changes safely.",
        "Add metrics around hot paths; measure before optimizing.",
        "Design APIs for ergonomics and clear failure modes.",
        "Write idempotent jobs so retries are safe.",
        "Paginate APIs; never assume small datasets.",
        "Cache wisely: define TTLs and invalidation strategies.",
        "Validate user input on both client and server.",
        "Avoid magic numbers; extract constants with names.",
        "Prefer UTC for timestamps and store ISO 8601 strings.",
        "Separate config from code; use environment variables.",
        "Keep functions under ~20-30 lines for readability.",
        "Write meaningful commit messages: what and why.",
        "Use guards to reduce nesting and improve clarity.",
        "Prefer explicit over implicit; be obvious in code.",
        "Add type hints where they add clarity and safety.",
        "Binary search your bugs: bisect changes to find regressions.",
        "Use code reviews to learn and teach, not just to approve.",
        "Write integration tests for critical flows end-to-end.",
        "Avoid global mutable state; pass context explicitly.",
        "Structure modules by domain, not by technical layers only.",
        "Monitor error budgets and prioritize reliability work.",
        "Prefer dependency injection over hard-coded singletons.",
        "Make CLI tools idempotent and scriptable (exit codes, flags).",
        "Document APIs with examples; tests can serve as docs.",
    ]


def deterministic_index(total: int, date: Optional[datetime.date] = None) -> int:
    if total <= 0:
        return 0
    if date is None:
        date = datetime.date.today()
    # Use ISO date string to compute a stable hash per day
    date_str = date.isoformat().encode("utf-8")
    digest = hashlib.sha256(date_str).digest()
    value = int.from_bytes(digest[:8], byteorder="big", signed=False)
    return value % total


def wrap_text(text: str, draw: "ImageDraw.ImageDraw", font: "ImageFont.ImageFont", max_width: int) -> List[str]:
    words = text.split()
    lines: List[str] = []
    current: List[str] = []
    for word in words:
        trial = (" ".join(current + [word])).strip()
        bbox = draw.textbbox((0, 0), trial, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width or not current:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def pick_colors(seed: int) -> tuple:
    random.seed(seed)
    # Pastel-like colors
    base_hues = [200, 220, 260, 300, 180, 160, 210]
    hue = random.choice(base_hues)
    def hsl_to_rgb(h, s, l):
        import colorsys
        return tuple(int(c * 255) for c in colorsys.hls_to_rgb(h / 360.0, l, s))
    c1 = hsl_to_rgb(hue, 0.45, 0.60)
    c2 = hsl_to_rgb((hue + 40) % 360, 0.45, 0.40)
    return c1, c2


def generate_image_with_text(text: str, output_path: str, seed: int) -> Optional[str]:
    if not PIL_AVAILABLE:
        print("Pillow not available; skipping image generation.")
        return None

    width, height = 1200, 675  # 16:9, good for social sharing
    img = Image.new("RGB", (width, height), color=(24, 26, 27))
    draw = ImageDraw.Draw(img)

    # Gradient background
    color_top, color_bottom = pick_colors(seed)
    for y in range(height):
        ratio = y / (height - 1)
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Load fonts with fallback
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/SFNS.ttf",
    ]
    title_font = None
    body_font = None
    for path in font_paths:
        if os.path.exists(path):
            try:
                title_font = ImageFont.truetype(path, 56)
                body_font = ImageFont.truetype(path, 36)
                break
            except Exception:
                continue
    if title_font is None:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    # Draw header "Code Tip"
    header = "Code Tip"
    bbox = draw.textbbox((0, 0), header, font=title_font)
    header_w = bbox[2] - bbox[0]
    header_h = bbox[3] - bbox[1]
    header_x = 60
    header_y = 60
    draw.rounded_rectangle((header_x - 24, header_y - 16, header_x + header_w + 24, header_y + header_h + 16), radius=16, fill=(0, 0, 0))
    draw.text((header_x, header_y), header, font=title_font, fill=(255, 255, 255))

    # Draw the tip, wrapped
    max_text_width = width - 120
    lines = wrap_text(text, draw, body_font, max_text_width)

    y = header_y + header_h + 48
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=body_font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text(((width - w) // 2, y), line, font=body_font, fill=(255, 255, 255))
        y += h + 12

    # Footer
    footer = "#coding  #programming  #devtips"
    footer_font = body_font
    bbox = draw.textbbox((0, 0), footer, font=footer_font)
    fw = bbox[2] - bbox[0]
    fh = bbox[3] - bbox[1]
    draw.text(((width - fw) // 2, height - fh - 40), footer, font=footer_font, fill=(230, 230, 230))

    img.save(output_path, format="JPEG", quality=92)
    return output_path


def build_tweet_text(tip: str) -> str:
    hashtags = "\n\n#coding #programming #devtips"
    max_len = 280
    allowed_tip_len = max_len - len(hashtags)
    if len(tip) > allowed_tip_len:
        tip = tip[: max(0, allowed_tip_len - 1)].rstrip() + "…"
    return f"{tip}{hashtags}"


def post_to_twitter(status_text: str, media_path: Optional[str]) -> None:
    api_key = os.environ.get("TWITTER_API_KEY")
    api_secret = os.environ.get("TWITTER_API_SECRET")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    access_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

    missing = [name for name, val in [
        ("TWITTER_API_KEY", api_key),
        ("TWITTER_API_SECRET", api_secret),
        ("TWITTER_ACCESS_TOKEN", access_token),
        ("TWITTER_ACCESS_TOKEN_SECRET", access_secret),
    ] if not val]

    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    import tweepy  # imported here to allow dry-run without dependency

    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
    api = tweepy.API(auth)

    media_ids = None
    if media_path:
        upload = api.media_upload(media_path)
        media_ids = [upload.media_id]

    api.update_status(status=status_text, media_ids=media_ids)


# --- New helpers for Google Images and News ---

def fetch_image_from_google(query: str, output_path: str) -> Optional[str]:
    """Fetch an image via Google Custom Search JSON API and save to output_path.
    Requires env vars GOOGLE_API_KEY and GOOGLE_CSE_ID.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    cse_id = os.environ.get("GOOGLE_CSE_ID")
    if not api_key or not cse_id:
        print("Google API not configured; skipping Google image fetch.")
        return None

    import requests

    params = {
        "key": api_key,
        "cx": cse_id,
        "q": query,
        "searchType": "image",
        "safe": "active",
        "num": 10,
    }
    rights = os.environ.get("GOOGLE_IMAGE_RIGHTS_FILTER")
    if rights:
        params["rights"] = rights

    try:
        resp = requests.get("https://www.googleapis.com/customsearch/v1", params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items") or []
        # Prefer larger images with jpeg/png formats
        candidates: List[str] = []
        for item in items:
            link = item.get("link")
            if not link:
                continue
            if any(link.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
                candidates.append(link)
        if not candidates and items:
            candidates = [i.get("link") for i in items if i.get("link")]
        if not candidates:
            print("No image results from Google.")
            return None

        image_url = candidates[0]
        r = requests.get(image_url, timeout=20)
        r.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(r.content)
        return output_path
    except Exception as e:
        print(f"Failed to fetch Google image: {e}")
        return None


def fetch_top_news(topic: str) -> Optional[Tuple[str, str]]:
    """Fetch top news headline and link for a topic using Google News RSS (no API key required)."""
    import requests
    import xml.etree.ElementTree as ET
    import urllib.parse as urlparse

    rss_url = f"https://news.google.com/rss/search?q={urlparse.quote(topic)}&hl=en-US&gl=US&ceid=US:en"
    try:
        resp = requests.get(rss_url, timeout=15)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        # Find first item
        channel = root.find("channel")
        if channel is None:
            return None
        item = channel.find("item")
        if item is None:
            return None
        title_el = item.find("title")
        link_el = item.find("link")
        if title_el is None or link_el is None:
            return None
        title = title_el.text or ""
        link = link_el.text or ""
        # Google News links often redirect; prefer as-is
        return (title.strip(), link.strip())
    except Exception as e:
        print(f"Failed to fetch news: {e}")
        return None


def build_news_tweet(title: str, url: str, topic: str) -> str:
    """Compose a tweet containing a news headline and link within 280 chars."""
    base_hashtags = f"\n\n#news #{topic.lower().replace(' ', '')}"
    max_len = 280
    # Reserve 25 chars for t.co shortened link + newline
    reserved = len(base_hashtags) + 25 + 1
    allowed_title_len = max_len - reserved
    text = title
    if len(text) > allowed_title_len:
        text = text[: max(0, allowed_title_len - 1)].rstrip() + "…"
    return f"{text}\n{url}{base_hashtags}"


def derive_image_query(preferred_query: Optional[str], news_title: Optional[str], topic: Optional[str], tip: Optional[str]) -> str:
    for candidate in [preferred_query, news_title, topic, tip]:
        if candidate and candidate.strip():
            # Use up to first 8 words to keep query concise
            words = candidate.strip().split()
            return " ".join(words[:8])
    return "technology"


# New: programmatic entry point for serverless usage
# Returns a dict with keys: ok (bool), dry_run (bool), tweet_text (str), media_path (Optional[str]), error (Optional[str])
def run_daily_tweet(
    dry_run: bool = False,
    no_image: bool = False,
    tips_file: Optional[str] = None,
    image_source: str = "generated",
    image_query: str = "",
    news_topic: str = "",
) -> dict:
    if tips_file is None:
        tips_file = os.path.join(os.path.dirname(__file__), "..", "content", "coding_tips.txt")

    # Select content: news or coding tip
    tweet_text: str
    news_title: Optional[str] = None
    news_url: Optional[str] = None

    if news_topic.strip():
        news = fetch_top_news(news_topic.strip())
        if news:
            news_title, news_url = news
            tweet_text = build_news_tweet(news_title, news_url, news_topic.strip())
        else:
            # Fallback to coding tip
            tips = read_tips_from_file(os.path.abspath(tips_file))
            if not tips:
                tips = get_default_tips()
            idx = deterministic_index(len(tips))
            tip = tips[idx]
            tweet_text = build_tweet_text(tip)
    else:
        tips = read_tips_from_file(os.path.abspath(tips_file))
        if not tips:
            tips = get_default_tips()
        idx = deterministic_index(len(tips))
        tip = tips[idx]
        tweet_text = build_tweet_text(tip)

    # Determine media
    media_path: Optional[str] = None
    if not no_image and image_source != "none":
        tmp_dir = os.environ.get("RUNNER_TEMP") or "/tmp"
        desired_output = os.path.join(tmp_dir, "daily_tweet.jpg")

        if image_source == "google":
            candidate_tip: Optional[str] = None
            if not news_topic.strip():
                # Derive from tip text when not posting news
                tips = read_tips_from_file(os.path.abspath(tips_file))
                if not tips:
                    tips = get_default_tips()
                idx = deterministic_index(len(tips))
                candidate_tip = tips[idx]
            query = derive_image_query(image_query, news_title, news_topic.strip() or None, candidate_tip)
            fetched = fetch_image_from_google(query, desired_output)
            if fetched:
                media_path = fetched
            else:
                if news_topic.strip():
                    seed = deterministic_index(1000)
                    media_path = generate_image_with_text(news_title or news_topic.strip(), desired_output, seed)
                else:
                    tips = read_tips_from_file(os.path.abspath(tips_file))
                    if not tips:
                        tips = get_default_tips()
                    idx = deterministic_index(len(tips))
                    tip = tips[idx]
                    media_path = generate_image_with_text(tip, desired_output, idx)
        else:
            # generated image
            if news_topic.strip():
                seed = deterministic_index(1000)
                media_path = generate_image_with_text(news_title or news_topic.strip(), desired_output, seed)
            else:
                tips = read_tips_from_file(os.path.abspath(tips_file))
                if not tips:
                    tips = get_default_tips()
                idx = deterministic_index(len(tips))
                tip = tips[idx]
                media_path = generate_image_with_text(tip, desired_output, idx)

    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "tweet_text": tweet_text,
            "media_path": media_path,
        }

    try:
        post_to_twitter(tweet_text, media_path)
    except Exception as e:
        return {
            "ok": False,
            "dry_run": False,
            "tweet_text": tweet_text,
            "media_path": media_path,
            "error": str(e),
        }

    return {
        "ok": True,
        "dry_run": False,
        "tweet_text": tweet_text,
        "media_path": media_path,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Post a daily coding tip with image to Twitter.")
    parser.add_argument("--dry-run", action="store_true", help="Generate content and print without posting.")
    parser.add_argument("--no-image", action="store_true", help="Do not generate or attach an image.")
    parser.add_argument("--tips-file", default=os.path.join(os.path.dirname(__file__), "..", "content", "coding_tips.txt"), help="Path to a newline-delimited tips file.")
    # New options
    parser.add_argument("--image-source", choices=["generated", "google", "none"], default="generated", help="Select image source: generated (default), google, or none.")
    parser.add_argument("--image-query", default="", help="Query for fetching image when using --image-source google.")
    parser.add_argument("--news-topic", default="", help="If set, post news for this topic instead of a coding tip.")
    args = parser.parse_args()

    # Select content: news or coding tip
    tweet_text: str

    news_title: Optional[str] = None
    news_url: Optional[str] = None

    if args.news_topic.strip():
        news = fetch_top_news(args.news_topic.strip())
        if news:
            news_title, news_url = news
            tweet_text = build_news_tweet(news_title, news_url, args.news_topic.strip())
        else:
            print("News fetch failed; falling back to coding tip.")
            tips = read_tips_from_file(os.path.abspath(args.tips_file))
            if not tips:
                tips = get_default_tips()
            idx = deterministic_index(len(tips))
            tip = tips[idx]
            tweet_text = build_tweet_text(tip)
    else:
        tips = read_tips_from_file(os.path.abspath(args.tips_file))
        if not tips:
            tips = get_default_tips()
        idx = deterministic_index(len(tips))
        tip = tips[idx]
        tweet_text = build_tweet_text(tip)

    # Determine media
    media_path = None
    if not args.no_image and args.image_source != "none":
        tmp_dir = os.environ.get("RUNNER_TEMP") or "/tmp"
        desired_output = os.path.join(tmp_dir, "daily_tweet.jpg")

        if args.image_source == "google":
            # Derive query from provided query, news, or tip
            candidate_tip = None
            if not args.news_topic.strip():
                # When not posting news, derive from tip text if available
                # Re-read tips to obtain the same selected tip for query context
                tips = read_tips_from_file(os.path.abspath(args.tips_file))
                if not tips:
                    tips = get_default_tips()
                idx = deterministic_index(len(tips))
                candidate_tip = tips[idx]
            query = derive_image_query(args.image_query, news_title, args.news_topic.strip() or None, candidate_tip)
            fetched = fetch_image_from_google(query, desired_output)
            if fetched:
                media_path = fetched
                print(f"Attached Google image for query: '{query}'.")
            else:
                print("Falling back to generated image.")
                if args.news_topic.strip():
                    seed = deterministic_index(1000)
                    media_path = generate_image_with_text(news_title or args.news_topic.strip(), desired_output, seed)
                else:
                    tips = read_tips_from_file(os.path.abspath(args.tips_file))
                    if not tips:
                        tips = get_default_tips()
                    idx = deterministic_index(len(tips))
                    tip = tips[idx]
                    media_path = generate_image_with_text(tip, desired_output, idx)
        else:
            # generated image
            if args.news_topic.strip():
                seed = deterministic_index(1000)
                media_path = generate_image_with_text(news_title or args.news_topic.strip(), desired_output, seed)
            else:
                tips = read_tips_from_file(os.path.abspath(args.tips_file))
                if not tips:
                    tips = get_default_tips()
                idx = deterministic_index(len(tips))
                tip = tips[idx]
                media_path = generate_image_with_text(tip, desired_output, idx)

    if args.dry_run:
        print("[DRY RUN] Would post tweet:\n")
        print(tweet_text)
        if media_path:
            print(f"\n[DRY RUN] Image generated at: {media_path}")
        else:
            print("\n[DRY RUN] No image attached.")
        return

    try:
        post_to_twitter(tweet_text, media_path)
    except Exception as e:
        print(f"Failed to post tweet: {e}", file=sys.stderr)
        sys.exit(1)

    print("Tweet posted successfully.")


if __name__ == "__main__":
    main()