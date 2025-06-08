from fastapi import FastAPI, Query
from playwright.sync_api import sync_playwright
import os
import subprocess

app = FastAPI()

# Instala navegadores de Playwright si no están ya instalados
def ensure_playwright_browsers_installed():
    try:
        subprocess.run(["playwright", "install"], check=True)
    except Exception as e:
        print(f"Error installing playwright browsers: {e}")

ensure_playwright_browsers_installed()

@app.get("/track-product")
def track_product(url: str = Query(..., description="URL del producto a analizar")):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            html = page.content()
            browser.close()
        return {
            "message": "Página cargada correctamente",
            "html_length": len(html)
        }
    except Exception as e:
        return {
            "message": "Error al cargar la página",
            "error": str(e)
        }