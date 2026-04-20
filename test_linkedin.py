from playwright.sync_api import sync_playwright
import json
from pathlib import Path

def scrape_linkedin(keyword="python developer", location="france", limit=3):
    print(f"🚀 Démarrage du scraper LinkedIn pour '{keyword}' à '{location}'...")
    
    session_file = Path("artifacts/linkedin_session.json")
    session_file.parent.mkdir(parents=True, exist_ok=True)
    
    with sync_playwright() as p:
        # 1. Lancer le navigateur visible
        browser = p.chromium.launch(headless=False)
        
        # 2. Charger la session ou se connecter
        if session_file.exists():
            context = browser.new_context(storage_state=session_file)
            print("✅ Session chargée depuis artifacts/linkedin_session.json")
        else:
            print("🔐 Première utilisation : connecte-toi manuellement.")
            context = browser.new_context()
            page = context.new_page()
            page.goto("https://www.linkedin.com/login")
            input("⏳ Appuie sur ENTRÉE une fois connecté...")
            context.storage_state(path=session_file)
            print("✅ Session sauvegardée.")
            
        # 3. Navigation vers la recherche
        page = context.new_page()
        url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}"
        print(f"🔍 URL: {url}")
        page.goto(url)
        page.pause() 
        page.wait_for_timeout(3000)  # Laisse LinkedIn charger les résultats
        
        # 4. Extraction
        jobs = []
        cards = page.query_selector_all(".job-card-list__title")
        print(f"📦 {len(cards)} cartes détectées. Extraction des {limit} premières...")
        
        for i, card in enumerate(cards[:limit]):
            try:
                title_el = card.query_selector(".job-card-container__title h3")
                company_el = card.query_selector(".job-card-container__company-name")
                
                if title_el and company_el:
                    job = {
                        "title": title_el.inner_text().strip(),
                        "company": company_el.inner_text().strip(),
                        "link": card.get_attribute("href"),
                        "status": "scraped"
                    }
                    jobs.append(job)
                    print(f"  {i+1}. {job['title']} @ {job['company']}")
            except Exception as e:
                print(f"  ⚠️  Erreur offre {i}: {e}")
                
        browser.close()
        
    # 5. Sauvegarde
    output = Path("artifacts/linkedin_jobs.json")
    with open(output, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)
    print(f"💾 {len(jobs)} offres sauvegardées dans {output}")
    return jobs

if __name__ == "__main__":
    scrape_linkedin(keyword="python", location="france", limit=3)