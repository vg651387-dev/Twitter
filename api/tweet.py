import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Ensure project root is in sys.path for importing 'scripts'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.daily_tweet import run_daily_tweet


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query_params = parse_qs(urlparse(self.path).query)

        def get_bool(name: str, default: bool = False) -> bool:
            raw = (query_params.get(name, [str(default).lower()])[0] or "").strip().lower()
            return raw in ("1", "true", "yes", "on")

        dry_run = get_bool("dry_run", False)
        no_image = get_bool("no_image", False)
        image_source = (query_params.get("image_source", ["google"])[0] or "google").strip()
        image_query = (query_params.get("image_query", [""])[0] or "").strip()
        news_topic = (query_params.get("news_topic", [""])[0] or "").strip()

        tips_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "content", "coding_tips.txt"))

        result = run_daily_tweet(
            dry_run=dry_run,
            no_image=no_image,
            tips_file=tips_file,
            image_source=image_source,
            image_query=image_query,
            news_topic=news_topic,
        )

        body_bytes = json.dumps(result, ensure_ascii=False).encode("utf-8")
        status_code = 200 if result.get("ok") else 500

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body_bytes)))
        self.end_headers()
        self.wfile.write(body_bytes)