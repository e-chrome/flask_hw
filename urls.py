def add_urls(app, advertisement_view, spam_view):
    app.add_url_rule(
        "/advertisement/<int:advertisement_id>/",
        view_func=advertisement_view.as_view("get_advertisement"),
        methods=["GET"]
    )
    app.add_url_rule(
        "/advertisement/",
        view_func=advertisement_view.as_view("create_advertisement"),
        methods=["POST"]
    )
    app.add_url_rule(
        "/advertisement/<int:advertisement_id>/",
        view_func=advertisement_view.as_view("delete_advertisement"),
        methods=["DELETE"]
    )
    app.add_url_rule(
        "/spam/<string:task_id>",
        view_func=spam_view.as_view("get_spam_result"),
        methods=["GET"]
    )
    app.add_url_rule(
        "/spam/",
        view_func=spam_view.as_view("do_spam"),
        methods=["POST"]
    )
