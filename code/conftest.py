import logging

from webdriver_manager.chrome import ChromeDriverManager

from api.client import ApiClient
from ui.fixtures import *


def pytest_addoption(parser):
    parser.addoption('--url', default='http://qa.digift.ru/')
    parser.addoption('--browser', default='chrome')
    parser.addoption('--debug_log', action='store_true')


@pytest.fixture(scope='function')
def temp_dir(request, base_temp_dir):
    test_dir = os.path.join(base_temp_dir, request._pyfuncitem.nodeid.replace("::", "_"))
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='function')
def driver(config):
    browser = config['browser']
    url = config['url']
    if browser == 'chrome':
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    else:
        raise RuntimeError(f'Unsupported browser: "{browser}"')
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    browser = request.config.getoption('--browser')

    return {'browser': browser, 'url': url}


@pytest.fixture(scope="function")
def api_client() -> ApiClient:
    api_client = ApiClient()
    return api_client


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def base_temp_dir():
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    return base_dir


@pytest.fixture(scope='function', autouse=True)
def logger(temp_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    log_file = os.path.join(temp_dir, 'test.log')
    log_level = logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()
