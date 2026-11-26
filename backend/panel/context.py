def panel_nav(request):
    if not request.path.startswith("/panel/"):
        return {}
    from .registry import menu

    return {"panel_menu": menu()}
