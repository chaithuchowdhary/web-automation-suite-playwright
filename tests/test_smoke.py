def test_home_page_loads(page):
    page.goto("/")
    assert "Automation Exercise" in page.title()
