from utils.logger import read_log, log_script_run
from utils.dirs import directories_dict
from survstat_collecting.survstat_scraper import scrape_survstat_data
from survstat_collecting.casedata_processing import preprocess_survstat_data
from datetime import datetime
import sys

def main():
    """
    Main function that orchestrates the SurvStat data collection and processing workflow.
    
    Workflow:
    1. Read disease configuration from log file
    2. Scrape current year data from SurvStat@RKI
    3. Process and merge the downloaded data
    4. Log the script execution
    
    The diseases for which data is downloaded and processed are extracted from log.txt.
    You can adjust the diseases by modifying the log.txt file or changing the variables here.
    
    Raises:
        ValueError: If no diseases are found in the log file
        Exception: If scraping or processing fails
    """
    try:
        current_year = datetime.now().year
        diseases_dict = read_log()

        diseases_dict = {'Dengue' : 'dengue'}

        if len(diseases_dict) == 0:
            raise ValueError('No diseases found! Check the log.txt file.')

        all_years = range(2001, current_year + 1)

        print(f"🔄 Starting data collection for {len(diseases_dict)} diseases...")
        
        # Step 1: Scrape data from SurvStat
        scrape_survstat_data(
            disease_names=diseases_dict, 
            years=all_years, # str(current_year), 
            output_directory=directories_dict['dir_data_raw'], 
            downloads_directory=directories_dict['dir_downloads']
        )

        print(f"🔄 Processing downloaded data...")
        
        # Step 2: Process and merge data
        preprocess_survstat_data(
            bugs=list(diseases_dict.values()), 
            years= all_years, #str(current_year),
            raw_data_dir=directories_dict['dir_data_raw'], 
            processed_data_dir=directories_dict['dir_data_preprocessed'],
            how='reconstruct'
        )

        # Step 3: Log the execution (append new diseases to existing ones)
        log_script_run(diseases_dict, all_years, append_mode=True)
        
        print("✅ Data collection and processing completed successfully!")
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
