"""Parameterized Selenium smoke/E2E tests for the four deployed app experiences.
Install: pip install -r requirements.txt && pytest -q
Uses Chrome/Chromedriver via Selenium Manager; headless safe.
"""
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE = os.getenv("APP_BASE_URL", "http://localhost:8080")
APPS = [("sp-event-horizon", "#events"), ("sp-attribution-atlas", "#bars"),
        ("sp-pixel-foundry", "#processed"), ("sp-graph-forge", "#map")]

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    instance = webdriver.Chrome(options=options)
    yield instance
    instance.quit()

@pytest.mark.parametrize("project,selector", APPS)
def test_app_renders(driver, project, selector):
    driver.get(f"{BASE}/{project}/")
    node = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
    assert node.is_displayed()
    assert not driver.find_elements(By.CSS_SELECTOR, "#fatal-error")

def test_attribution_method_updates(driver):
    driver.get(f"{BASE}/sp-attribution-atlas/")
    select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#method")))
    from selenium.webdriver.support.ui import Select
    before = driver.find_element(By.CSS_SELECTOR, "#bars").text
    Select(select).select_by_value("last")
    after = driver.find_element(By.CSS_SELECTOR, "#bars").text
    assert before != after
