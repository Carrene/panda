from panda.validators import ORGANIZATION_TITLE_PATTERN as pattern


def test_organization_title_pattern():
    assert pattern.match('name')
    assert pattern.match('name-name')
    assert pattern.match('123')
    assert pattern.match('name123')
    assert pattern.match('name-123')
    assert pattern.match('123name')
    assert pattern.match('name-name-name')

    assert not pattern.match('')
    assert not pattern.match('-name')
    assert not pattern.match('name-')
    assert not pattern.match('-name-')
    assert not pattern.match('name!')
    assert not pattern.match('name@')
    assert not pattern.match('name#')
    assert not pattern.match('name$')
    assert not pattern.match('name%')
    assert not pattern.match('name^')
    assert not pattern.match('name_name')
    assert not pattern.match('name:')
    assert not pattern.match('name]')
    assert not pattern.match('&')

