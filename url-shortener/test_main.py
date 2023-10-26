from urlshort import create_app


def test_shorten(client):
    response = client.get('/')
    assert b'Shorten' in response.data
    assert b'Your URL' in response.data
    assert b'Code' in response.data
    assert b'Shorten My URL!' in response.data
