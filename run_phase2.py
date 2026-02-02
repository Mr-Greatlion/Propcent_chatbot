import json
import time
import re
from crawler.browser import BrowserManager
from storage.json_store import save_json

# 🔁 CHANGE THIS TO YOUR ACTUAL PHASE 1 FILE
PHASE1_FILE = "output/20260125_174112_makaan24_flat_apartment_urls.json"

def clean(text):
    if text:
        return re.sub(r"\s+", " ", text.strip())
    return None

def run():
    print("🚀 Phase 2: Makaan24 – Property Detail Scraper")

    # Load URLs from Phase 1
    with open(PHASE1_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    urls = data.get("urls", [])
    print(f"📥 Loaded {len(urls)} property URLs\n")

    browser = BrowserManager(headless=False)
    page = browser.start()

    results = []

    for idx, url in enumerate(urls, start=1):
        print(f"\n🔍 [{idx}/{len(urls)}] Opening: {url}")

        try:
            page.goto(url, timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)

            page_text = page.inner_text("body")

            # 🔍 FIELD EXTRACTION (TEXT-BASED, SAFE)
            price = re.search(r"₹[\d,.\s]+(Cr|L)?", page_text)
            area = re.search(r"\d{3,5}\s*(sq\.?ft|sqft)", page_text, re.I)
            bhk = re.search(r"\d+\s*BHK", page_text, re.I)

            # DOM-based selectors
            def safe_text(selector):
                try:
                    return clean(page.locator(selector).first.inner_text())
                except:
                    return None

            location = safe_text("text=Location") or safe_text("h1")
            builder = safe_text("text=Builder") or safe_text("text=Owner")
            property_type = safe_text("text=Apartment") or safe_text("text=Flat")

            property_data = {
                "url": url,
                "price": price.group() if price else None,
                "area": area.group() if area else None,
                "bhk": bhk.group() if bhk else None,
                "location": location,
                "builder": builder,
                "property_type": property_type
            }

            print("──────── PROPERTY ────────")
            for k, v in property_data.items():
                print(f"{k.upper():14}: {v}")

            results.append(property_data)

        except Exception as e:
            print(f"⚠️ Failed to scrape {url} → {e}")
            continue

        time.sleep(1)  # polite delay

    output = {
        "source": "makaan24.com",
        "total_properties_scraped": len(results),
        "properties": results
    }

    save_json(output, "makaan24_property_details.json")

    browser.stop()
    print("\n✅ Phase 2 completed successfully")

if __name__ == "__main__":
    run()
