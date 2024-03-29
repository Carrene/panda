from panda.validators import USER_EMAIL_PATTERN as pattern


def test_user_email_pattern():
    assert pattern.match('user@example.com')
    assert pattern.match('5@example.com')
    assert pattern.match('u@example.com')
    assert pattern.match('user@5.com')
    assert pattern.match('user@e.com')
    assert pattern.match('user@example.org')
    assert pattern.match('user@example.co')
    assert pattern.match('1@1.com')
    assert pattern.match('e@e.com')

    assert not pattern.match('userexample.com')
    assert not pattern.match('user@examplecom')
    assert not pattern.match('user$example.com')
    assert not pattern.match('user#example.com')
    assert not pattern.match('user^example.com')
    assert not pattern.match('user1example.com')
    assert not pattern.match('user@.com')
    assert not pattern.match('example.com')
    assert not pattern.match('example')
    assert not pattern.match('@')
    assert not pattern.match('e')
    assert not pattern.match('.')

