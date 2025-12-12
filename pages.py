from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Locators will go here

    FROM_FIELD = (By.ID, "from")
    TO_FIELD = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.XPATH,
                        "//button[contains(., 'Call a taxi')]")

    # Tariffs / Prices bottom
    SUPPORTIVE_TARIFF_CARD = (
        By.XPATH,
        "//div[contains(@class,'tcard')][.//div[contains(text(),'Supportive')]]"
    )
    ACTIVE_TARIFF_CARD = (By.CSS_SELECTOR, ".tcard.active")

    # Phone / login bottom
    PHONE_BUTTON = (By.CLASS_NAME, "np-text")
    PHONE_FIELD = (By.ID, "phone")
    PHONE_NEXT_BUTTON = (By.XPATH,
                         "//button[contains(., 'Next')]")
    PHONE_CONFIRMATION_FIELD = (By.ID, "code")

    # Payment method bottom
    PAYMENT_METHOD_BUTTON = (By.CLASS_NAME, "pp-value-text")
    ADD_CARD_BUTTON = (By.CLASS_NAME, "pp-plus")
    CARD_NUMBER_FIELD = (By.ID, "number")
    CARD_CODE_FIELD = (By.CSS_SELECTOR, "#code.card-input")
    CARD_LINK_BUTTON = (By.XPATH,
                        "//button[contains(., 'Link')]")
    PAYMENT_METHOD_VALUE = (
        By.XPATH,
        "//div[contains(@class,'payment-picker')]//span"
    )

    # Comment bottom
    MESSAGE_FOR_DRIVER_FIELD = (By.ID, "comment")

    # Blanket & handkerchiefs plus/minuses
    BLANKET_TOGGLE_INPUT = (By.CLASS_NAME, "switch-input")
    BLANKET_TOGGLE_BUTTON = (By.CLASS_NAME, "switch")

    # Ice cream bottom
    ICE_CREAM_PLUS_BUTTON = (
        By.XPATH,
        "//div[text()='Ice cream']/following-sibling::div//div[text() = '+']"
    )
    ICE_CREAM_COUNTER = (
        By.XPATH,
        "//div[text()='Ice cream']/following-sibling::div"
        "//div[contains(@class,'counter')]"
    )

    # Order / car search bottom
    ORDER_BUTTON = (By.XPATH, "//button[@class='smart-button']")
    CAR_SEARCH_MODAL = (
        By.XPATH,
        "//div[contains(@class, 'modal') or contains(@class,'order-modal')]"
        "[.//div[contains(., 'Car search')]]"
    )

    def open_base_page(self, url: str) -> None:
        self.driver.get(url)

    # Address implementation

    def set_address_from(self, address: str) -> None:
        el = self.wait.until(EC.element_to_be_clickable(self.FROM_FIELD))
        el.clear()
        el.send_keys(address)

    def set_address_to(self, address: str) -> None:
        el = self.wait.until(EC.element_to_be_clickable(self.TO_FIELD))
        el.clear()
        el.send_keys(address)

    def get_address_from(self) -> str:
        return self.driver.find_element(*self.FROM_FIELD).get_attribute("value")

    def get_address_to(self) -> str:
        return self.driver.find_element(*self.TO_FIELD).get_attribute("value")

    def click_call_taxi(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)).click()

    # Tariffs / Prices for supportive

    def select_supportive_tariff_if_needed(self) -> None:
        card = self.wait.until(
            EC.presence_of_element_located(self.SUPPORTIVE_TARIFF_CARD)
        )
        classes = card.get_attribute("class") or ""

        if "active" not in classes:
            card.click()

    def get_selected_tariff_name(self) -> str:
        active_card = self.wait.until(
            EC.presence_of_element_located(self.ACTIVE_TARIFF_CARD)
        )
        return active_card.text

    # Confirming the phone number

    def click_phone_number_button(self) -> None:
        self.wait.until(
            EC.element_to_be_clickable(self.PHONE_BUTTON)
        ).click()

    def get_saved_phone(self) -> str:
        return self.wait.until(
            EC.visibility_of_element_located(self.PHONE_BUTTON)
        ).text

    def fill_phone_number(self, phone_number: str) -> None:
        phone = self.wait.until(
            EC.element_to_be_clickable(self.PHONE_FIELD)
        )
        phone.clear()
        phone.send_keys(phone_number)
        self.driver.find_element(*self.PHONE_NEXT_BUTTON).click()

    def fill_phone_confirmation_code(self, code: str) -> None:
        code_field = self.wait.until(
            EC.element_to_be_clickable(self.PHONE_CONFIRMATION_FIELD)
        )
        code_field.clear()
        code_field.send_keys(code)
        code_field.submit()

    # Payment method will go here

    def open_payment_method(self) -> None:
        self.wait.until(
            EC.element_to_be_clickable(self.PAYMENT_METHOD_BUTTON)
        ).click()

    def click_add_card(self) -> None:
        self.wait.until(
            EC.element_to_be_clickable(self.ADD_CARD_BUTTON)
        ).click()

    def fill_card_details(self, card_number: str, card_code: str) -> None:
        num = self.wait.until(
            EC.element_to_be_clickable(self.CARD_NUMBER_FIELD)
        )
        num.clear()
        num.send_keys(card_number)

        code = self.wait.until(
            EC.element_to_be_clickable(self.CARD_CODE_FIELD)
        )
        code.clear()
        code.send_keys(card_code)

        num.click()

    def click_link_card(self) -> None:
        self.wait.until(
            EC.element_to_be_clickable(self.CARD_LINK_BUTTON)
        ).click()

    def get_payment_method_text(self) -> str:
        return self.wait.until(
            EC.visibility_of_element_located(self.PAYMENT_METHOD_BUTTON)
        ).text

    # Comment writing will go here

    def set_driver_comment(self, text: str) -> None:
        field = self.wait.until(
            EC.element_to_be_clickable(self.MESSAGE_FOR_DRIVER_FIELD)
        )
        field.clear()
        field.send_keys(text)

    def get_driver_comment(self) -> str:
        return self.driver.find_element(
            *self.MESSAGE_FOR_DRIVER_FIELD
        ).get_attribute("value")

    # Blanket and handkerchiefs will go here

    def select_blanket_and_handkerchiefs(self) -> None:
        toggle = self.wait.until(
            EC.presence_of_element_located(self.BLANKET_TOGGLE_INPUT)
        )
        button = self.wait.until(
            EC.presence_of_element_located(self.BLANKET_TOGGLE_BUTTON)
        )
        if not toggle.get_property("checked"):
            button.click()

    def is_blanket_selected(self) -> bool:
        toggle = self.driver.find_element(*self.BLANKET_TOGGLE_INPUT)
        return bool(toggle.get_property("checked"))

    # Ice Cream plus/minus will go here

    def add_ice_creams(self, count: int) -> None:
        plus = self.wait.until(
            EC.element_to_be_clickable(self.ICE_CREAM_PLUS_BUTTON)
        )
        for _ in range(count):
            plus.click()

    def get_ice_cream_count(self) -> int:
        text = self.wait.until(
            EC.visibility_of_element_located(self.ICE_CREAM_COUNTER)
        ).text
        try:
            return int(text.strip())
        except ValueError:
            return 0

    # Order and car search will go here

    def click_order_button(self) -> None:
        self.wait.until(
            EC.element_to_be_clickable(self.ORDER_BUTTON)
        ).click()

    def is_car_search_modal_visible(self) -> bool:
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.CAR_SEARCH_MODAL)
            )
            return True
        except Exception:
            return False
