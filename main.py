from data import URBAN_ROUTES_URL
from helpers import is_url_reachable


class TestUrbanRoutes:
    # Task 4: Check the Server is on
    @classmethod
    def setup_class(cls):
        if is_url_reachable(URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Check the server is on and still running")

    # Task 3: Prepare main.py
    def test_set_route(self):
        # Add in S8
        print('function is for set route')
        pass

    def test_select_plan(self):
        # Add in S8
        print('function created for select plan')
        pass

    def test_fill_phone_number(self):
        # Add in S8
        print('function created for fill phone number')
        pass

    def test_fill_card(self):
        # Add in S8
        print('function created for fill card')
        pass

    def test_comment_for_driver(self):
        # Add in S8
        print('function created for comment for driver')
        pass

    def test_order_blanket_and_handkerchiefs(self):
        # Add in S8
        print('function created for blanket & handkerchiefs')
        pass

    # Task 5: Preparing the ice cream order
    def test_order_2_ice_creams(self):
        for i in range(2):
            # Add in S8
            pass

    def test_car_search_model_appears(self):
        # Add in S8
        print('function created for car search model appears')
        pass
