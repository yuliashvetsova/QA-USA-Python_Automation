import data

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from data import (
    URBAN_ROUTES_URL,
    ADDRESS_FROM,
    ADDRESS_TO,
    PHONE_NUMBER,
    CARD_NUMBER,
    CARD_CODE,
    MESSAGE_FOR_DRIVER,
    number_of_ice_creams,
)
from helpers import is_url_reachable, retrieve_phone_code
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # Performance logs
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

        options = Options()
        options.add_argument("--start-maximized")

        for key, value in capabilities.items():
            options.set_capability(key, value)

        if not is_url_reachable(URBAN_ROUTES_URL):
            # Fail early rather than staying on a non-working window
            raise RuntimeError(f"URL {URBAN_ROUTES_URL} is not reachable")

        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)
        cls.page = UrbanRoutesPage(cls.driver)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    # Helpers go here

    @property
    def page(self) -> UrbanRoutesPage:
        return self.__class__.page

    def _start_order_with_supportive(self):
        self.page.open_base_page(URBAN_ROUTES_URL)
        self.page.set_address_from(ADDRESS_FROM)
        self.page.set_address_to(ADDRESS_TO)
        self.page.click_call_taxi()
        self.page.select_supportive_tariff_if_needed()

    # All of the tests go here

    # Setting address testing
    def test_setting_address(self):
        self.page.open_base_page(URBAN_ROUTES_URL)

        self.page.set_address_from(ADDRESS_FROM)
        self.page.set_address_to(ADDRESS_TO)

        assert self.page.get_address_from() == ADDRESS_FROM
        assert self.page.get_address_to() == ADDRESS_TO

    # Selecting supportive plan testing
    def test_selecting_supportive_plan(self):
        self._start_order_with_supportive()
        selected_text = self.page.get_selected_tariff_name()
        assert "Supportive" in selected_text

    # Inputting the phone number testing
    def test_filling_phone_number(self):
        self._start_order_with_supportive()
        self.page.click_phone_number_button()
        self.page.fill_phone_number(PHONE_NUMBER)

        code = retrieve_phone_code(self.__class__.driver)

        self.page.fill_phone_confirmation_code(code)

        # Trimming spaces to avoid UI misunderstanding
        assert self.page.get_saved_phone() == data.PHONE_NUMBER
        self.__class__.driver.page_source.replace(" ", "")

    # Adding a credit card testing
    def test_adding_credit_card(self):
        self._start_order_with_supportive()

        self.page.open_payment_method()
        self.page.click_add_card()
        self.page.fill_card_details(CARD_NUMBER, CARD_CODE)
        self.page.click_link_card()

        assert self.page.get_payment_method_text() == "Card"

    # Writing a comment testing
    def test_writing_comment_for_the_driver(self):
        self._start_order_with_supportive()

        self.page.set_driver_comment(MESSAGE_FOR_DRIVER)
        assert self.page.get_driver_comment() == MESSAGE_FOR_DRIVER

    # Blanket and handkerchiefs order testing
    def test_ordering_blanket_and_handkerchiefs(self):
        self._start_order_with_supportive()

        self.page.select_blanket_and_handkerchiefs()
        assert self.page.is_blanket_selected() is True

    # Two ice creams order testing
    def test_ordering_two_ice_creams(self):
        self._start_order_with_supportive()

        self.page.add_ice_creams(number_of_ice_creams)
        assert self.page.get_ice_cream_count() == number_of_ice_creams

    # Ordering supportive taxi testing
    def test_order_taxi_supportive_car_search_modal(self):
        self._start_order_with_supportive()

        # Writing a comment before ordering
        self.page.set_driver_comment(MESSAGE_FOR_DRIVER)

        self.page.click_order_button()
        assert self.page.is_car_search_modal_visible()