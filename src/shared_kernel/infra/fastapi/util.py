def make_response(resp: any):
    """Make response to send response."""

    return {
        "meta": {
            "code": 200,
            "message": "ok"
        },
        "data": resp
    }
