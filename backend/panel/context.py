def panel_nav(request):
    if not request.path.startswith("/panel/") or not request.user.is_authenticated or not request.user.is_staff:
        return {}
    from .registry import menu, user_scope

    return {"panel_menu": menu(request.user), "panel_scope": user_scope(request.user)}
