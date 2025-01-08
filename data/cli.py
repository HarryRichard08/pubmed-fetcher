import argparse
from fetcher import PubMedFetcher


def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", help="Search query for PubMed.")
    parser.add_argument("-f", "--file", help="Output filename for results (CSV).")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")

    args = parser.parse_args()

    if args.debug:
        print(f"Query: {args.query}")
    
    try:
        papers = PubMedFetcher.fetch_papers(args.query)
        results = PubMedFetcher.filter_non_academic(papers)

        if args.file:
            PubMedFetcher.save_to_csv(results, args.file)
            print(f"Results saved to {args.file}")
        else:
            print(results)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
