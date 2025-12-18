from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        # instructor note: don't store WebDriverWait in __init__; build it when needed

    def _wait(self, timeout: int = 10) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout)

    # Locators

    FROM_FIELD = (By.ID, "from")
    TO_FIELD = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.XPATH, "//button[contains(., 'Call a taxi')]")

    # Tariffs / Prices bottom
    SUPPORTIVE_TARIFF_CARD = (
        By.XPATH,
        "//div[contains(@class,'tcard')][.//div[contains(text(),'Supportive')]]"
    )
    ACTIVE_TARIFF_CARD = (By.CSS_SELECTOR, ".tcard.active")

    # Phone / login bottom
    PHONE_BUTTON = (By.CLASS_NAME, "np-text")
    PHONE_FIELD = (By.ID, "phone")
    PHONE_NEXT_BUTTON = (By.XPATH, "//button[contains(., 'Next')]")
    PHONE_CONFIRMATION_FIELD = (By.ID, "code")

    # Payment method bottom
    PAYMENT_METHOD_BUTTON = (By.CLASS_NAME, "pp-value-text")
    ADD_CARD_BUTTON = (By.CLASS_NAME, "pp-plus")
    CARD_NUMBER_FIELD = (By.ID, "number")
    CARD_CODE_FIELD = (By.CSS_SELECTOR, "#code.card-input")
    CARD_LINK_BUTTON = (By.XPATH, "//button[contains(., 'Link')]")
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
    ICE_CREAM_COUNTER = (By.CLASS_NAME, "counter-value")

    # Order / car search bottom
    ORDER_BUTTON = (By.XPATH, "//button[@class='smart-button']")
    CAR_SEARCH_MODAL = (By.CLASS_NAME, "order-body")

    def open_base_page(self, url: str) -> None:
        self.driver.get(url)

    # This replaces the “_start_order_with_supportive” helper that was in main.py
    def start_order_with_supportive(self, url: str, address_from: str, address_to: str) -> None:
        self.open_base_page(url)
        self.set_address_from(address_from)
        self.set_address_to(address_to)
        self.click_call_taxi()
        self.select_supportive_tariff_if_needed()

    # Address implementation

    def set_address_from(self, address: str) -> None:
        el = self._wait().until(EC.element_to_be_clickable(self.FROM_FIELD))
        el.clear()
        el.send_keys(address)

    def set_address_to(self, address: str) -> None:
        el = self._wait().until(EC.element_to_be_clickable(self.TO_FIELD))
        el.clear()
        el.send_keys(address)

    def get_address_from(self) -> str:
        return self.driver.find_element(*self.FROM_FIELD).get_attribute("value")

    def get_address_to(self) -> str:
        return self.driver.find_element(*self.TO_FIELD).get_attribute("value")

    def click_call_taxi(self) -> None:
        self._wait().until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)).click()

    # Tariffs / Prices for supportive

    def select_supportive_tariff_if_needed(self) -> None:
        card = self._wait().until(EC.presence_of_element_located(self.SUPPORTIVE_TARIFF_CARD))
        classes = card.get_attribute("class") or ""
        if "active" not in classes:
            card.click()

    def get_selected_tariff_name(self) -> str:
        active_card = self._wait().until(EC.presence_of_element_located(self.ACTIVE_TARIFF_CARD))
        return active_card.text

    # Confirming the phone number

    def click_phone_number_button(self) -> None:
        self._wait().until(EC.element_to_be_clickable(self.PHONE_BUTTON)).click()

    def get_saved_phone(self) -> str:
        return self._wait().until(EC.visibility_of_element_located(self.PHONE_BUTTON)).text

    def fill_phone_number(self, phone_number: str) -> None:
        phone = self._wait().until(EC.element_to_be_clickable(self.PHONE_FIELD))
        phone.clear()
        phone.send_keys(phone_number)
        self.driver.find_element(*self.PHONE_NEXT_BUTTON).click()

    def fill_phone_confirmation_code(self, code: str) -> None:
        code_field = self._wait().until(EC.element_to_be_clickable(self.PHONE_CONFIRMATION_FIELD))
        code_field.clear()
        code_field.send_keys(code)
        code_field.submit()

    # Payment method

    def open_payment_method(self) -> None:
        self._wait().until(EC.element_to_be_clickable(self.PAYMENT_METHOD_BUTTON)).click()

    def click_add_card(self) -> None:
        self._wait().until(EC.element_to_be_clickable(self.ADD_CARD_BUTTON)).click()

    def fill_card_details(self, card_number: str, card_code: str) -> None:
        num = self._wait().until(EC.element_to_be_clickable(self.CARD_NUMBER_FIELD))
        num.clear()
        num.send_keys(card_number)

        code = self._wait().until(EC.element_to_be_clickable(self.CARD_CODE_FIELD))
        code.clear()
        code.send_keys(card_code)

        num.click()

    def click_link_card(self) -> None:
        self._wait().until(EC.element_to_be_clickable(self.CARD_LINK_BUTTON)).click()

    def get_payment_method_text(self) -> str:
        return self._wait().until(EC.visibility_of_element_located(self.PAYMENT_METHOD_BUTTON)).text

    # Comment writing

    def set_driver_comment(self, text: str) -> None:
        field = self._wait().until(EC.element_to_be_clickable(self.MESSAGE_FOR_DRIVER_FIELD))
        field.clear()
        field.send_keys(text)

    def get_driver_comment(self) -> str:
        return self.driver.find_element(*self.MESSAGE_FOR_DRIVER_FIELD).get_attribute("value")

    # Blanket and handkerchiefs

    def select_blanket_and_handkerchiefs(self) -> None:
        toggle = self._wait().until(EC.presence_of_element_located(self.BLANKET_TOGGLE_INPUT))
        button = self._wait().until(EC.presence_of_element_located(self.BLANKET_TOGGLE_BUTTON))
        if not toggle.get_property("checked"):
            button.click()

    def is_blanket_selected(self) -> bool:
        toggle = self.driver.find_element(*self.BLANKET_TOGGLE_INPUT)
        return bool(toggle.get_property("checked"))

    # Ice Cream plus/minus

    def add_ice_creams(self, count: int) -> None:
        plus = self._wait().until(EC.element_to_be_clickable(self.ICE_CREAM_PLUS_BUTTON))
        for _ in range(count):
            plus.click()

    def get_ice_cream_count(self) -> int:
        return int(self.driver.find_element(*self.ICE_CREAM_COUNTER).text)

    # Order and car search

    def click_order_button(self) -> None:
        self._wait().until(EC.element_to_be_clickable(self.ORDER_BUTTON)).click()

    def is_car_search_modal_visible(self) -> bool:
        try:
            self._wait().until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL))
            return True
        except Exception:
            return False
