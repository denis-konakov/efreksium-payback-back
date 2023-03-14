from pydantic import AnyHttpUrl
from urllib.parse import urlsplit, urlencode, parse_qs

args_type = dict[str, str]
def url_add_arguments(url: AnyHttpUrl | str, args: args_type) -> str:
    url = str(url)
    parsed_url = urlsplit(url)
    query = parse_qs(parsed_url.query)
    rq: dict[str, str] = {}
    for i in query.keys():
        rq[i] = ','.join(query[i])
    for i in args.keys():
        rq[i] = args[i]
    return parsed_url._replace(query=urlencode(rq)).geturl()
