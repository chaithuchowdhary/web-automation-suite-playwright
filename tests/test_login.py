from testdata.credentials import EMAIL, PASSWORD


def test_valid_login(login_page):
    login_page.open()
    login_page.login(EMAIL, PASSWORD)
    assert login_page.is_logged_in()


def test_wrong_password_shows_error(login_page):
    login_page.open()
    login_page.login(EMAIL, "definitely-the-wrong-password")
    login_page.expect_login_error()


def test_logout(login_page):
    login_page.open()
    login_page.login(EMAIL, PASSWORD)
    assert login_page.is_logged_in()

    login_page.logout()
    assert "/login" in login_page.page.url
