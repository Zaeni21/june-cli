import json
from datetime import datetime
from playwright.sync_api import sync_playwright

def ask_june(prompt, context):
    page = context.new_page()
    page.goto("https://askjune.ai/app/")
    page.fill("textarea", prompt)
    page.click("button:has-text('Send')")

    # tunggu jawaban muncul
    page.wait_for_selector(".response")  # ⚠️ pastikan sesuai selector di June
    answer = page.inner_text(".response")
    page.close()
    return answer

if __name__ == "__main__":
    # load daftar pertanyaan dari file
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

                # 🔥 save ke log
                with open("answers.log", "a", encoding="utf-8") as log:
                    log.write(f"[{datetime.now()}] Q: {prompt}\n[A]: {answer}\n\n")

            except Exception as e:
                print("⚠️ Error:", e)

            # geser ke pertanyaan berikutnya
            idx = (idx + 1) % len(questions)
