from fastapi import FastAPI, Query
from playwright.async_api import async_playwright

app = FastAPI()

@app.get("/track-product")
async def track_product(url: str = Query(..., description="URL del producto")):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        html = await page.content()
        await browser.close()

    return {
        "html_length": len(html),
        "message": "Página cargada correctamente"
    }