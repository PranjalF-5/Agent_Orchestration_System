import io
import contextlib
import time

code_snippet = """
page.goto("https://en.wikipedia.org/wiki/Artificial_intelligence")
print(page.title())
"""

try:
    from playwright.sync_api import sync_playwright
    output = io.StringIO()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        local_vars = {"page": page, "browser": browser, "time": time}
        
        with contextlib.redirect_stdout(output):
            exec(code_snippet, {}, local_vars)
            
        time.sleep(2)
        browser.close()
        
    print("SUCCESS:", output.getvalue())
except Exception as e:
    import traceback
    traceback.print_exc()
    print("ERROR:", str(e))
