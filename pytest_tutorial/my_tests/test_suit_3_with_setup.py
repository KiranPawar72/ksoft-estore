import pytest

pytestmark = pytest.mark.be

@pytest.fixture(scope='module')
def my_setup():
    print("")
    print(">>>> MY SETUP <<<<")

    return {'name':'Kiran', 'id':14}

@pytest.mark.smoke
@pytest.mark.ll
def test_login_page_valid_user(my_setup):
    print("")
    print("Login with valid user")
    print("Function: aaaa")
    #import pdb; pdb.set_trace()
    print("Name : {}".format(my_setup.get('name')))


@pytest.mark.regression
def test_login_page_wrong_password(my_setup):
    print("Login with wrong password")
    print("Function: bbbb")
    assert 1==2, "One is not Two"