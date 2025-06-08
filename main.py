from fastapi import FastAPI
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "API online"}


@app.get("/scrape")
async def scrape():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com")
        title = await page.title()
        await browser.close()
        return JSONResponse(content={"title": title})