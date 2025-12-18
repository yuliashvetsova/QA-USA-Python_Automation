import data
import helpers

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
        # do not modify - we need additional logging enabled in order to retrieve phone confirmation code
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)

        # Check the URL hasn't timed out
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Check the server is on and still running")

    # Setting address testing
    def test_setting_address(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_address_from(ADDRESS_FROM)
        routes_page.set_address_to(ADDRESS_TO)

        assert routes_page.get_address_from() == ADDRESS_FROM
        assert routes_page.get_address_to() == ADDRESS_TO

    # Selecting supportive plan testing
    def test_selecting_supportive_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.start_order_with_supportive(URBAN_ROUTES_URL, ADDRESS_FROM, ADDRESS_TO)
        selected_text = routes_page.get_selected_tariff_name()
        assert "Supportive" in selected_text

    # Inputting the phone number testing
    def test_filling_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.start_order_with_supportive(URBAN_ROUTES_URL, ADDRESS_FROM, ADDRESS_TO)
        routes_page.click_phone_number_button()
        routes_page.fill_phone_number(PHONE_NUMBER)

        code = retrieve_phone_code(self.__class__.driver)
        routes_page.fill_phone_confirmation_code(code)

        assert routes_page.get_saved_phone() == data.PHONE_NUMBER

    # Adding a credit card testing
    def test_adding_credit_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.start_order_with_supportive(URBAN_ROUTES_URL, ADDRESS_FROM, ADDRESS_TO)

        routes_page.open_payment_method()
        routes_page.click_add_card()
        routes_page.fill_card_details(CARD_NUMBER, CARD_CODE)
        routes_page.click_link_card()

        assert routes_page.get_payment_method_text() == "Card"

    # Writing a comment testing
    def test_writing_comment_for_the_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.start_order_with_supportive(URBAN_ROUTES_URL, ADDRESS_FROM, ADDRESS_TO)

        routes_page.set_driver_comment(MESSAGE_FOR_DRIVER)
        assert routes_page.get_driver_comment() == MESSAGE_FOR_DRIVER

    # Blanket and handkerchiefs order testing
    def test_ordering_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.start_order_with_supportive(URBAN_ROUTES_URL, ADDRESS_FROM, ADDRESS_TO)

        routes_page.select_blanket_and_handkerchiefs()
        assert routes_page.is_blanket_selected() is True

    # Two ice creams order testing
    def test_ordering_two_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.start_order_with_supportive(URBAN_ROUTES_URL, ADDRESS_FROM, ADDRESS_TO)

        routes_page.add_ice_creams(number_of_ice_creams)
        assert routes_page.get_ice_cream_count() == number_of_ice_creams

    # Ordering supportive taxi testing
    def test_order_taxi_supportive_car_search_modal(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.start_order_with_supportive(URBAN_ROUTES_URL, ADDRESS_FROM, ADDRESS_TO)

        routes_page.set_driver_comment(MESSAGE_FOR_DRIVER)
        routes_page.click_order_button()
        assert routes_page.is_car_search_modal_visible() is True

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
