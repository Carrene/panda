from panda.validators import URL_PATTERN as pattern


def test_organization_url_pattern():
    assert pattern.match('www.example.com')
    assert pattern.match('http://www.example.com')
    assert pattern.match('https://www.example.com')
    assert pattern.match('http://example.com')
    assert pattern.match('https://example.com')
    assert pattern.match('www.example.co')
    assert pattern.match('www.example.co.org')

    assert not pattern.match('www')
    assert not pattern.match('www.example')
    assert not pattern.match('example.com')
    assert not pattern.match('http://.')
    assert not pattern.match('https://.com')
    assert not pattern.match('www.example.com/a')
    assert not pattern.match('http://www.example.com/a')
    assert not pattern.match('')

