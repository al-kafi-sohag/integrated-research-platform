import requests
from bs4 import BeautifulSoup
import time

class ScholarScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_full_article_details(self, url):
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            
            possible_abstract_tags = [
                soup.find("div", class_="abstract"),
                soup.find("section", class_="abstract"),
                soup.find("div", id="abstract"),
                soup.find("section", id="abstract"),
                soup.find("abstract"),
                soup.find("div", class_="paper-abstract"),
            ]
            
            for tag in possible_abstract_tags:
                if tag and tag.text.strip():
                    return tag.text.strip()
            
            return None
        except Exception as e:
            return None

    def scrape_articles(self, query, num_pages, progress_callback=None):
        articles = []
        page = 0
        expected_total = num_pages * 10
        results_processed = 0
        
        while page < num_pages:
            try:
                if progress_callback:
                    progress_callback(results_processed / expected_total, 
                                    f"Scraping page {page + 1} of {num_pages}")

                url = f"https://scholar.google.com/scholar?start={page*10}&q={query}&hl=en&as_sdt=0,5"
                response = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(response.text, "html.parser")
                results = soup.find_all("div", class_="gs_ri")

                if page == 0:
                    results_per_page = len(results)
                    expected_total = results_per_page * num_pages
                    if expected_total == 0:
                        if progress_callback:
                            progress_callback(-1, "No results found for the query")
                        return articles

                for result in results:
                    title_elem = result.find("h3", class_="gs_rt")
                    title = title_elem.text if title_elem else "No title available"
                    title = title.replace("[PDF] ", "").replace("[HTML] ", "")
                    
                    authors_elem = result.find("div", class_="gs_a")
                    authors = authors_elem.text if authors_elem else "No authors available"
                    
                    results_processed += 1
                    if progress_callback:
                        progress = min(results_processed / expected_total, 0.99)
                        progress_callback(progress, 
                                       f"Processing result {results_processed} of ~{expected_total} (Page {page + 1})")
                    
                    main_link = ""
                    pdf_link = ""
                    
                    title_links = title_elem.find_all("a") if title_elem else []
                    for link in title_links:
                        href = link.get("href", "")
                        if href.lower().endswith('.pdf'):
                            pdf_link = href
                        elif not main_link:
                            main_link = href

                    if not pdf_link:
                        side_links = result.find_parent("div", class_="gs_r").find_all("div", class_="gs_or_ggsm")
                        for side_link in side_links:
                            link = side_link.find("a")
                            if link:
                                href = link.get("href", "")
                                if href.lower().endswith('.pdf') or '[pdf]' in link.text.lower():
                                    pdf_link = href
                                    break

                    if not pdf_link:
                        all_links = result.find_all("a")
                        for link in all_links:
                            href = link.get("href", "")
                            if href.lower().endswith('.pdf'):
                                pdf_link = href
                                break

                    citation_elem = result.find("div", class_="gs_fl").find_all("a")
                    citations = "0"
                    for cite in citation_elem:
                        if "Cited by" in cite.text:
                            citations = cite.text.replace("Cited by", "").strip()
                            break

                    description_elem = result.find("div", class_="gs_rs")
                    description = description_elem.text if description_elem else "No description available"
                    
                    full_details = None
                    if main_link:
                        full_details = self.get_full_article_details(main_link)
                    
                    articles.append({
                        "Title": title,
                        "Authors": authors,
                        "Main Link": main_link,
                        "Citations": citations,
                        "Short Description": description,
                    })

                page += 1
                time.sleep(2)
                
            except Exception as e:
                if progress_callback:
                    progress_callback(-1, f"Error on page {page}: {str(e)}")
                page += 1
                continue

        if progress_callback:
            progress_callback(1, "Scraping complete!")
        return articles
