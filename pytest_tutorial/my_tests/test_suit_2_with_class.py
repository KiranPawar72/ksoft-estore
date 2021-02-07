import pytest

pytestmark = [pytest.mark.fe, pytest.mark.slow]

@pytest.fixture(scope='module')
def my_setup():
    print("")
    print(">>>> MY SETUP <<<<")

    return {'name':'Kiran', 'id':14}

@pytest.mark.smoke
@pytest.mark.abc
class TestCheckout(object):

    def test_checkout_with_guest(self, my_setup):
        print("Checkout with guest")
        print("Function: 1111")

    def test_checkout_with_existing_user(self, my_setup):
        print("Checkout with existing user")
        print("Function: 2222")