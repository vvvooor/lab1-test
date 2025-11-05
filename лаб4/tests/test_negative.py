from pages.order_page import OrderPage
from pathlib import Path

def test_negative(driver):
    page = OrderPage(driver)
    form_path = Path(__file__).parent / "resources" / "test_form.html"
    page.visit(form_path.resolve().as_uri())


    page.fill_form(["", "2", "3", "4", "5"], delay_per_field=1.5)
    page.submit_form()

    assert "Пожалуйста, заполните все обязательные поля." in page.get_error_message()
