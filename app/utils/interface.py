from fastapi import Request
def https_url_for(request: Request, name: str, path: str) -> str:

    http_url = str(request.url_for(name, path=path))
    
    if "localhost" in http_url or "127.0.0.1" in http_url:
        return http_url
    
    # Replace 'http' with 'https'
    return http_url.replace("http", "https", 1)