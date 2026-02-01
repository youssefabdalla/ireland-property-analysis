from src.ingest import ingest_ppr
def main():
    print("--- Starting Ireland Property Analysis Pipeline ---")
    # Iteration 1: Ingest
    ingest_ppr.download_and_extract_ppr()
    
    # Future Iterations:
    # transform_data()
    # upload_to_s3()
    print("--- Pipeline Iteration Complete ---")

if __name__ == "__main__":
    main()