from adwe.services.repository_clone import build_clone_url


def test_build_clone_url_without_token():
    url = "https://github.com/pallets/flask"

    assert build_clone_url(url) == url
