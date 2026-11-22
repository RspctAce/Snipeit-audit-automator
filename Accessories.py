from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page(viewport={"width": 1600, "height": 900})
    page.goto("https://demo.snipeitapp.com")

    page.get_by_role("textbox", name="Username").fill("admin")
    page.get_by_role("textbox", name="Password").fill("password")
    page.get_by_role("button", name="Login").click()

    page.locator("a[href*='/accessories']").first.click()
    page.wait_for_selector("table tbody tr")

    headers = [th.inner_text().strip() for th in page.locator("table thead th").all()]

    low_stock_rows = page.locator("table tbody tr", has=page.locator("span.text-danger"))
    print(f"Found {low_stock_rows.count()} item(s) below minimum quantity.\n")

    while low_stock_rows.count() > 0:
        current_row = low_stock_rows.first
        cells = [td.inner_text().strip() for td in current_row.locator("td").all()]
        row_data = dict(zip(headers, cells))

        name = row_data.get("Name", "Unknown")
        model_no = row_data.get("Model No.", "N/A")
        category = row_data.get("Category", "N/A")
        location = row_data.get("Location", "N/A")
        min_qty = row_data.get("Min. QTY", "N/A")
        total_qty = row_data.get("Total", "N/A")

        print("=" * 45)
        print(f"ITEM:       {name}")
        print(f"MODEL NO.:  {model_no}")
        print(f"CATEGORY:   {category}")
        print(f"LOCATION:   {location}")
        print(f"MIN. QTY:   {min_qty}  (Current Total: {total_qty})")
        print("=" * 45)
        print("Waiting for you to adjust quantity and hit Save...\n")

        current_row.locator("button.adjust-quantity").click()

        modal = page.locator("#adjustQuantityModal")
        modal.wait_for(state="visible")
        modal.wait_for(state="hidden", timeout=0)

        page.wait_for_timeout(1000)

    print("All low-stock accessories have been processed!")
    input("Review the table in the browser, then press Enter here to close...")