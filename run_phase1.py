import time
from crawler.browser import BrowserManager
from storage.json_store import save_json

BASE_URL = "https://makaan24.com/property-type/flat-apartment/"
MAX_PAGES = 100  # safety limit

def run():
    print("🚀 Phase 1: Makaan24 – Property URL Collection (Pagination)")

    browser = BrowserManager(headless=False)
    page = browser.start()

    all_urls = set()
    page_no = 1

    while page_no <= MAX_PAGES:
        if page_no == 1:
            url = BASE_URL
        else:
            url = f"{BASE_URL}page/{page_no}/"

        print(f"\n🌐 Opening page {page_no}: {url}")
        page.goto(url, timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        # 🔥 Property cards
        cards = page.locator("a[href*='/property/']")
        count = cards.count()

        print(f"📦 Found {count} property cards on page {page_no}")

        if count == 0:
            print("🛑 No properties found — stopping pagination")
            break

        page_urls = []

        for i in range(count):
            href = cards.nth(i).get_attribute("href")
            if href:
                if href.startswith("/"):
                    href = "https://makaan24.com" + href
                all_urls.add(href)
                page_urls.append(href)

        # Live preview
        for u in page_urls[:3]:
            print("[PROPERTY]", u)

        page_no += 1
        time.sleep(1)

    output = {
        "source": "makaan24.com",
        "property_type": "flat-apartment",
        "total_properties": len(all_urls),
        "urls": sorted(list(all_urls))
    }

    save_json(output, "makaan24_flat_apartment_urls.json")

    browser.stop()
    print("\n✅ Phase 1 completed successfully")

if __name__ == "__main__":
    run()
