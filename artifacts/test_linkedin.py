# Ajoute en haut du fichier
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Dans la boucle d'extraction, ajoute :
for i, card in enumerate(job_cards[:limit]):
    try:
        logger.debug(f"=== Carte #{i+1} ===")
        logger.debug(f"HTML: {card.inner_html()[:300]}...")  # Voir la structure
        
        # Essayer TOUS les sélecteurs possibles pour le titre
        title_selectors = [
            ".job-card-list__title",
            "a.job-card-list__title", 
            "[data-job-id] .job-card-list__title",
            ".artdeco-entity-lockup__title",
            "span.job-card-container__title",
        ]
        title = None
        for sel in title_selectors:
            el = card.query_selector(sel)
            if el:
                title = el.inner_text().strip()
                logger.debug(f"✅ Titre trouvé avec: {sel}")
                break
        
        if not title:
            logger.warning(f"❌ Aucun sélecteur n'a trouvé le titre")
            # Sauvegarder le HTML pour analyse manuelle
            with open(f"artifacts/card_{i}_debug.html", "w", encoding="utf-8") as f:
                f.write(card.inner_html())
            continue
            
        # ... reste du code
# Remplace la boucle d'extraction par cette version debug :
for i, card in enumerate(job_cards[:limit]):
    try:
        print(f"\n🔎 Carte #{i+1}:")
        print(f"   HTML partiel: {card.inner_html()[:200]}...")  # Voir la structure
        
        # Essayer plusieurs sélecteurs possibles pour le titre
        title_selectors = [
            ".job-card-list__title",
            ".job-card-container__title", 
            "a.job-card-list__title",
            "[data-job-id] .job-card-list__title",
            ".artdeco-entity-lockup__title"
        ]
        title = None
        for sel in title_selectors:
            el = card.query_selector(sel)
            if el:
                title = el.inner_text().strip()
                print(f"   ✅ Titre trouvé avec: {sel}")
                break
        
        # Même chose pour l'entreprise
        company_selectors = [
            ".artdeco-entity-lockup__subtitle",
            ".job-card-container__company-name",
            ".job-card-container__primary-description"
        ]
        company = None
        for sel in company_selectors:
            el = card.query_selector(sel)
            if el:
                company = el.inner_text().strip()
                print(f"   ✅ Entreprise trouvée avec: {sel}")
                break
        
        if title and company:
            job = {
                "title": title,
                "company": company,
                "link": card.get_attribute("href") or card.query_selector("a")?.get_attribute("href"),
                "status": "scraped"
            }
            jobs.append(job)
            print(f"   📦 OFFRE: {job['title']} @ {job['company']}")
        else:
            print(f"   ❌ Pas trouvé: title={title is not None}, company={company is not None}")
            
    except Exception as e:
        print(f"   ⚠️  Erreur: {e}")
        import traceback
        traceback.print_exc()