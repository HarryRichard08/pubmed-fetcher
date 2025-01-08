import requests
import pandas as pd
from typing import List, Dict

class PubMedFetcher:
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    EMAIL = "richard.harry623@gmail.com"

    @staticmethod
    def fetch_papers(query: str, max_results: int = 100) -> List[Dict]:
        # Fetch PubMed IDs
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "email": PubMedFetcher.EMAIL
        }
        response = requests.get(PubMedFetcher.BASE_URL, params=params)
        response.raise_for_status()
        ids = response.json().get("esearchresult", {}).get("idlist", [])

        # Fetch paper details
        details_params = {
            "db": "pubmed",
            "id": ",".join(ids),
            "retmode": "json",
            "email": PubMedFetcher.EMAIL
        }
        details_response = requests.get(PubMedFetcher.DETAILS_URL, params=details_params)
        details_response.raise_for_status()
        papers = details_response.json().get("result", {}).values()
        return [paper for paper in papers if isinstance(paper, dict)]

    @staticmethod
    def filter_non_academic(papers: List[Dict]) -> List[Dict]:
        # Identify non-academic authors based on heuristics
        results = []
        for paper in papers:
            authors = paper.get("authors", [])
            non_academic_authors = [
                author for author in authors if "pharma" in author.get("affiliation", "").lower()
            ]
            if non_academic_authors:
                results.append({
                    "PubmedID": paper.get("uid"),
                    "Title": paper.get("title"),
                    "Publication Date": paper.get("pubdate"),
                    "Non-academic Author(s)": ", ".join(
                        author.get("name") for author in non_academic_authors
                    ),
                    "Company Affiliation(s)": ", ".join(
                        author.get("affiliation") for author in non_academic_authors
                    ),
                })
        return results

    @staticmethod
    def save_to_csv(results: List[Dict], filename: str):
        df = pd.DataFrame(results)
        df.to_csv(filename, index=False)
