from utils.logger import read_log, log_script_run
from utils.dirs import directories_dict
from survstat_collecting.survstat_scraper import scrape_survstat_data
from survstat_collecting.casedata_processing import preprocess_survstat_data
from datetime import datetime
import sys

def update_survstat_data(years=None, diseases_dict=None, append_log=True, method = ['update', 'construct']):
    """
    Main function that orchestrates the SurvStat data collection and processing workflow.
    
    Parameters:
    -----------
    years : int, list, or str, optional
        Year(s) to collect data for. Can be:
        - Single year (int): 2023
        - List of years: [2020, 2021, 2022]
        - String: "2023" or "2020,2021,2022"
        - None: uses current year
    diseases_dict : dict, optional
        Dictionary mapping disease keys to SurvStat names.
        Example: {'measles': 'Measles', 'campylobacter': 'Campylobacter'}
        If None, reads from log.txt file
    append_log : bool, optional
        Whether to append to the log file. Default True.
    
    Workflow:
    1. Read disease configuration from log file (if not provided)
    2. Scrape data from SurvStat@RKI
    3. Process and merge the downloaded data
    4. Log the script execution (if append_log=True)

    Raises:
        ValueError: If no diseases are found in the log file
        Exception: If scraping or processing fails
    """
    try:
        current_year = datetime.now().year
        
        # Handle years parameter
        if years is None:
            years = str(current_year)
        elif isinstance(years, str):
            # Already a string, keep as is
            pass
        elif isinstance(years, int):
            years = str(years)

        
        # Handle diseases parameter
        if diseases_dict is None:
            diseases_dict = read_log()
        
        if len(diseases_dict) == 0:
            raise ValueError('No diseases found! Check the log.txt file or provide diseases_dict parameter.')

        print(f"🔄 Starting data collection for {len(diseases_dict)} diseases...")
        print(f"📅 Years: {years}")
        print(f"🦠 Diseases: {list(diseases_dict.values())}")
        
        # Step 1: Scrape data from SurvStat
        scrape_survstat_data(
            disease_names=diseases_dict, 
            years=years, 
            output_directory=directories_dict['dir_data_raw'], 
            downloads_directory=directories_dict['dir_downloads']
        )

        print(f"🔄 Processing downloaded data...")
        
        # Step 2: Process and merge data
        preprocess_survstat_data(
            diseases=list(diseases_dict.values()), 
            years=years,
            raw_data_dir=directories_dict['dir_data_raw'], 
            processed_data_dir=directories_dict['dir_data_preprocessed'],
            how=method
        )

        # Step 3: Log the execution (if requested)
        if append_log:
            all_years = range(2001, current_year + 1)
            log_script_run(diseases_dict, all_years, append_mode=True)
        
        print("✅ Data collection and processing completed successfully!")
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise

def main():
    """
    Command-line entry point that uses default settings.
    """
    try:
        update_survstat_data()
    except (ValueError, Exception) as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
