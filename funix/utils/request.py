from urllib.parse import urlparse, parse_qs

def is_iframe(request):
    # if has query "iframe"
    if request.GET.get("iframe") == "1":
        return True

    # if has query "next" 
    next = request.GET.get("next")

    if next:
        parsed_url = urlparse(next)
        query_params = parse_qs(parsed_url.query)
        if "iframe" in query_params and query_params["iframe"][0] == "1":
            return True

    return False