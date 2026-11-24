from .data import POSTS

def blog_info(request):
    return {
        "site_name": "Межпространственный блог",
        "published_count": sum(1 for post in POSTS if post["is_published"]),
    }