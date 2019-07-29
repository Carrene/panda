from panda.validators import DOMAIN_PATTERN as pattern


def test_organization_domain_pattern():
    assert pattern.match('example.com')
    assert pattern.match('example.com.org')
    assert pattern.match('example.co')
    assert pattern.match('example.co.org.com')

    assert not pattern.match('http://www.example.com')
    assert not pattern.match('https://www.example.com')
    assert not pattern.match('http://example.com')
    assert not pattern.match('https://example.com')
    assert not pattern.match('www.example.co')
    assert not pattern.match('www.example.co.org')
    assert not pattern.match('www.example.com')
    assert not pattern.match('www')
    assert not pattern.match('www.example')
    assert not pattern.match('http://.')
    assert not pattern.match('https://.com')
    assert not pattern.match('example.com/a')
    assert not pattern.match('example/abc')
    assert not pattern.match('')

