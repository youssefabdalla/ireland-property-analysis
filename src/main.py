from src.ingest import ingest_ppr, clean_ppr
def main():
    print("--- Starting Ireland Property Analysis Pipeline ---")
    # Ingest
    ingest_ppr.download_and_extract_ppr()
    # transform_data()
    clean_ppr.clean_ppr_data(
        input_csv=ingest_ppr.RAW_DATA_DIR / "PPR-ALL.csv",
        output_csv=clean_ppr.PROCESSED_DATA_DIR / "ppr_cleaned.csv"
    )

    print("--- Pipeline Iteration Complete ---")

if __name__ == "__main__":
    main()