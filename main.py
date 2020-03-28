from flask import Request, abort, jsonify

def github_webhook(request: Request):
    """Github webhook trigger."""

    data = request.get_json()

    print(data)