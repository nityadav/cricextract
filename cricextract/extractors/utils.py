def sanitize_name(name: str):
    unwanted_strs = ["(c)", "\u2020"]
    for s in unwanted_strs:
        name.replace(s, "")
    return name

def get_player_id_from_href(href):
    pass
