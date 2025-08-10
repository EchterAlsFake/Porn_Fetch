import os
import json

from typing import List
from tempfile import NamedTemporaryFile


def load_state(path) -> dict:
    """
    Load the JSON state from disk, returning a dict with key "models" mapping each model URL to its state.
    Each model state contains:
      - downloaded: list of URLs already fetched
      - pending: list of URLs to download
    """
    if not os.path.exists(path):
        return {"models": {}}
    with open(path, 'r') as f:
        try:
            state = json.load(f)
        except json.JSONDecodeError:
            state = {"models": {}}
    # ensure each model has both lists
    for m, data in state.setdefault("models", {}).items():
        data.setdefault("downloaded", [])
        data.setdefault("pending", [])
    return state


def save_state(state: dict, path):
    """
    Atomically write the state back to disk.
    """
    dirn = os.path.dirname(os.path.abspath(path)) or '.'
    with NamedTemporaryFile('w', delete=False, dir=dirn) as tmp:
        json.dump(state, tmp, indent=2)
        tmp_path = tmp.name
    os.replace(tmp_path, path)


def get_all_saved_models(path: str, state: dict = None) -> List[str]:
    """
    Return a list of all model URLs currently tracked in the database.
    """
    state = state or load_state(path)
    list_of_models = []
    for model in state.get("models", {}).items():
        list_of_models.append(model)

    return list_of_models

def add_model_url(model_url: str, path: str, state: dict = None) -> bool:
    """
    Add a new model URL to the state, initializing its downloaded and pending lists if absent.
    """
    state = state or load_state(path)
    models = state.setdefault("models", {})
    if model_url in models:
        print(f"Model URL already present: {model_url}")
        return False
    models[model_url] = {"downloaded": [], "pending": []}
    save_state(state, path=path)
    print(f"Added model URL: {model_url}")
    return True


def remove_model_url(model_url: str, path: str, state: dict = None) -> bool:
    """
    Remove a model URL and its history from the state.
    """
    state = state or load_state(path)
    models = state.get("models", {})
    if model_url not in models:
        print(f"Model URL not found: {model_url}")
        return False
    del models[model_url]
    save_state(state, path=path)
    print(f"Removed model URL: {model_url}")
    return True


def is_video_downloaded(model_url: str, video_url: str, path: str, state: dict = None) -> bool:
    """
    Check whether a given video_url has already been downloaded for the specified model.
    """
    state = state or load_state(path)
    model_state = state.get("models", {}).get(model_url, {})
    return video_url in set(model_state.get("downloaded", []))


def record_download(model_url: str, video_url: str, path: str, state: dict = None) -> bool:
    """
    Record that a video_url was downloaded for the given model_url.
    Removes it from pending if present.
    """
    state = state or load_state(path)
    models = state.setdefault("models", {})
    model_state = models.setdefault(model_url, {"downloaded": [], "pending": []})
    downloaded = set(model_state.get("downloaded", []))
    if video_url in downloaded:
        return False
    downloaded.add(video_url)
    model_state["downloaded"] = list(downloaded)
    # remove from pending
    model_state["pending"] = [u for u in model_state.get("pending", []) if u != video_url]
    save_state(state, path=path)
    return True

def update_pending_for_all_models(fetch_generator_fn, path: str):
    """
    For each model URL in state, fetch the generator via fetch_generator_fn(model_url),
    iterate videos until a downloaded URL is hit, and add new URLs to pending.
    """
    state = load_state(path)
    for model_url, data in state.get("models", {}).items():
        print(f"Gathering URLs for model: {model_url}")
        downloaded = set(data.get("downloaded", []))
        pending = set(data.get("pending", []))
        try:
            gen = fetch_generator_fn(model_url, do_return=True)
            for video in gen:
                url = video.url
                if url in downloaded:
                    # once we hit a known video, older ones are already processed
                    break
                if url not in pending:
                    print(f"  New URL: {url}")
                    pending.add(url)
        except Exception as e:
            print(f"  Error fetching videos for {model_url}: {e}")
        # update state
        data["pending"] = list(pending)
    save_state(state, path=path)
    print("Pending lists updated.")


def show_stats(path: str, state: dict = None):
    """
    Print statistics: number of models tracked, pending and downloaded counts per model.
    """
    state = state or load_state(path)
    models = state.get("models", {})
    print(f"Total models tracked: {len(models)}")
    for url, data in models.items():
        dcount = len(data.get("downloaded", []))
        pcount = len(data.get("pending", []))
        print(f" - {url}: {dcount} downloaded, {pcount} pending")


def show_help():
    """
    Display help text describing the feature.
    """
    help_text = """
Automatic Model Downloader:
This feature tracks videos per model with download capabilities.

Options:
1) Show this help text.
2) Add model URLs to tracking.
3) Fetch and save pending video URLs (without downloading).
4) Delete model URLs.
5) Show statistics (downloaded vs pending).
6) Exit

99) Start downloading all videos that are marked as pending in the database (use option 3 before doing this :) 

State file (`download_state.json`) stores for each model:
  - downloaded: list of URLs already downloaded
  - pending: list of URLs to download next
  
"""
    print(help_text)

