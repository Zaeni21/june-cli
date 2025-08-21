import asyncio
from playwright.async_api import async_playwright
import json

EMAIL = "email_lo@example.com"  # ganti dengan email lo

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        print(">> Buka halaman login June...")
        await page.goto("https://askjune.ai/app/")

        # Klik tombol login
        await page.click("text=Login")
        await page.fill("input[type='email']", EMAIL)
        await page.click("button[type='submit']")

        print(">> Kode OTP sudah dikirim ke:", EMAIL)
        otp = input(">> Masukkan kode OTP dari email: ")

        # Isi OTP ke field input
        await page.fill("input[type='text']", otp)
        await page.click("button[type='submit']")

        # Tunggu redirect setelah login sukses
        await page.wait_for_timeout(5000)

        # Save cookies biar bisa auto login next time
        cookies = await context.cookies()
        with open("cookies.json", "w") as f:
            json.dump(cookies, f)

        print(">> Login berhasil! Cookies disimpan ke cookies.json")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

