from selenium import webdriver

browser = webdriver.Firefox()
browser.get("http://localhost:8000")

# changed from book assertion as my version of Django has a different 
# title
assert "worked" in browser.title
