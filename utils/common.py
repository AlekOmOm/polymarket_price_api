import urllib.parse

def slugify(text: str) -> str:
    """
    accept either a slug or a full polymarket URL
    and return the slug string.
    """
    if text.startswith(("http://", "https://")):
        return urllib.parse.urlparse(text).path.rstrip("/").split("/")[-1]
    return text.strip("/")
