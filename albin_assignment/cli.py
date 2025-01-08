import argparse
from albin_assignment.fetcher import PubMedFetcher  # Correct package import


def main():
    parser = argparse.ArgumentParser(
        description="Fetch research papers from PubMed and filter non-academic authors."
    )
    parser.add_argument("query", help="Search query for PubMed.")
    parser.add_argument(
        "-f", "--file", help="Specify the output filename (CSV). If not provided, print to console."
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Print debug information during execution."
    )

    args = parser.parse_args()

    if args.debug:
        print(f"Debug Mode Enabled")
        print(f"Query: {args.query}")
        if args.file:
            print(f"Output will be saved to: {args.file}")
        else:
            print("No output file specified. Results will be printed to the console.")

    try:
        # Fetch papers
        if args.debug:
            print("Fetching papers...")
        papers = PubMedFetcher.fetch_papers(args.query)
        
        # Filter results
        if args.debug:
            print("Filtering non-academic authors...")
        results = PubMedFetcher.filter_non_academic(papers)

        # Handle output
        if args.file:
            PubMedFetcher.save_to_csv(results, args.file)
            print(f"Results saved to {args.file}")
        else:
            print("Results:")
            for result in results:
                print(result)

    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
