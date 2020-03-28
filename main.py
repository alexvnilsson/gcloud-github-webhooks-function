def github_webhook():
    """Github webhook trigger."""

    data = request.get_json()

    print(data)