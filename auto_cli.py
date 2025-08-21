import json
from datetime import datetime
from playwright.sync_api import sync_playwright

def ask_june(prompt, context):
    page = context.new_page()
    page.goto("https://askjune.ai/app/")
    page.fill("textarea", prompt)
    page.click("button:has-text('Send')")

    # tunggu jawaban muncul (⚠️ sesuaikan selector-nya dengan DOM June)
    page.wait_for_selector(".response")
    answer = page.inner_text(".response")
    page.close()
    return answer

if __name__ == "__main__":
    # load daftar pertanyaan
    with open("questions.txt", "r") as f:
        questions = [q.strip() for q in f.readlines() if q.strip()]

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context()

        # load cookies hasil login.py
        with open("cookies.json") as f:
            context.add_cookies(json.load(f))

        idx = 0
        while True:
            prompt = questions[idx]
            print(f"\n[{datetime.now()}] Q: {prompt}")
            try:
                answer = ask_june(prompt, context)
                print(f"[A]: {answer}")
            except Exception as e:
                print("⚠️ Error:", e)

            # geser ke pertanyaan berikutnya
            idx = (idx + 1) % len(questions)  # kalau udah habis, balik ke awal

