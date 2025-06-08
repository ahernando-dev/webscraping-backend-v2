from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright
import httpx
import asyncio

app = FastAPI()

PPLX_API_KEY = "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"

async def query_perplexity(prompt: str):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PPLX_API_KEY}",
        "Content-Type": "application/json"
    }
    json = {
        "model": "mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=json)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error al consultar Perplexity: {str(e)}"

@app.get("/")
async def root():
    return {"message": "API online"}

@app.get("/scrape")
async def scrape(url: str = Query(..., description="URL del producto")):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            await page.wait_for_load_state("networkidle")
            content = await page.content()
            await browser.close()
            return {"status": "ok", "content": content}
    except Exception as e:
        # Fallback a Perplexity
        prompt = "Extrae el nombre, precio, marca y descripción del producto desde este HTML:\n" + str(e)
        fallback = await query_perplexity(prompt)
        return JSONResponse(content={"status": "fallback", "detail": fallback})