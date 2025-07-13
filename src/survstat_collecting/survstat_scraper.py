import os
import zipfile
import shutil
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from typing import Optional, Union, List, Dict
from tqdm import tqdm

def remove_downloads_folder(downloads_path: Path):
    """
    Removes possibly existing survstat.zip folder in Downloads.
    Thereby ensuring that a new survstat.zip will not be called survstat.zip (1) and further.
    """

    for file in downloads_path.iterdir():
        if file.is_file() and file.name.lower().startswith("survstat") and file.suffix == ".zip":
            try:
                file.unlink()
            except:
                pass
    
def scraper(disease: str,
            year: str,
            downloads_path: Path) -> Path:
    
    """
    Scrapes survstat data for a given disease and year.
    """

    # Initializing a Chrome tab
    chrome_options = webdriver.ChromeOptions()

    # Your existing preferences
    prefs = {
        "download.default_directory": str(downloads_path.absolute()),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Add these lines to suppress logs
    chrome_options.add_argument("--log-level=3")  # Only errors, no info or warnings
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    # Open website
    driver.get("https://survstat.rki.de/Content/Query/Create.aspx")
    time.sleep(2)
    
    # Add new filter dropdown - FIRST ADD BUTTON
    add_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@title='Add']")))
    add_button.click()
    time.sleep(1)

    # Press the newly added dropdown box - find fresh each time
    clicked = False
    for attempt in range(3):
        try:
            select_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Select an option')]")
            for element in select_elements:
                try:
                    if element.is_displayed():
                        element.click()
                        clicked = True
                        break
                except:
                    continue
            if clicked:
                break
            time.sleep(1)
        except:
            time.sleep(1)
            continue
    
    if not clicked:
        raise Exception("Could not click 'Select an option' dropdown")
    
    time.sleep(1)

    # Add as selection feature disease to be specified
    disease_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Disease/ Pathogen')]")))
    disease_button.click()        
    
    # Press box to select disease
    chosen_container = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//select[@title='Reporting category by disease name']/following-sibling::div[contains(@class, 'chosen-container')]")))
    chosen_container.click()            

    # Select actual disease
    disease_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,  f"//li[contains(text(), '{disease}')]")))
    disease_option.click()       

    # Add another filter dropdown - FIND ADD BUTTON FRESH WITH RETRY
    add_button_clicked = False
    for attempt in range(3):
        try:
            add_button_second = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@title='Add']")))
            add_button_second.click()
            add_button_clicked = True
            break
        except:
            time.sleep(1)
            continue
    
    if not add_button_clicked:
        raise Exception("Could not click second Add button")
    
    time.sleep(1)
    
    # Press the newly added dropdown box - find fresh each time
    clicked = False
    for attempt in range(3):
        try:
            select_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Select an option')]")
            for element in select_elements:
                try:
                    if element.is_displayed():
                        element.click()
                        clicked = True
                        break
                except:
                    continue
            if clicked:
                break
            time.sleep(1)
        except:
            time.sleep(1)
            continue
    
    if not clicked:
        raise Exception("Could not click second 'Select an option' dropdown")
    
    time.sleep(1)

    # Add as selection feature year to be specified
    year_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Year of notification')]")))
    year_option.click()

    # Clicking the year box
    year_chosen_container = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Year of notification']/../..//div[contains(@class, 'chosen-container')]")))
    year_chosen_container.click()        

    # Selecting the actual year
    year_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//li[text()='{year}']")))
    year_option.click()        

    # Selecting weeknumber as rowvalue
    js_script_rows = """
    var rowsSelect = document.getElementById('ContentPlaceHolderMain_ContentPlaceHolderAltGridFull_DropDownListRowHierarchy');
    rowsSelect.value = '[ReportingDate].[Week]';
    rowsSelect.dispatchEvent(new Event('change'));
    
    if (typeof $ !== 'undefined' && $(rowsSelect).data('chosen')) {
        $(rowsSelect).trigger('chosen:updated');
    }
    """
    driver.execute_script(js_script_rows)
    time.sleep(1)
    
    # Selecting spatial unit as columns
    js_script_columns = """
    var columnsSelect = document.getElementById('ContentPlaceHolderMain_ContentPlaceHolderAltGridFull_DropDownListColHierarchy');
    columnsSelect.value = '[DeutschlandNodes].[Kreise71Web]';
    columnsSelect.dispatchEvent(new Event('change'));
    
    if (typeof $ !== 'undefined' && $(columnsSelect).data('chosen')) {
        $(columnsSelect).trigger('chosen:updated');
    }
    """
    driver.execute_script(js_script_columns)
    time.sleep(1)

    # More specifically, selecting County (Kreise) as columnvalue
    js_script_county = """
    var colSelect = document.getElementById('ContentPlaceHolderMain_ContentPlaceHolderAltGridFull_DropDownListCol');
    colSelect.value = '[DeutschlandNodes].[Kreise71Web].[CountyKey71]';
    colSelect.dispatchEvent(new Event('change'));
    
    if (typeof $ !== 'undefined' && $(colSelect).data('chosen')) {
        $(colSelect).trigger('chosen:updated');
    }
    """
    driver.execute_script(js_script_county)
    time.sleep(1)
    
    # Add zero values (so that there's no missing observations, i.e. empty rows/columns)
    zero_values_checkbox = driver.find_element(By.ID, "ContentPlaceHolderMain_ContentPlaceHolderAltGridFull_CheckBoxNonEmpty")
    if not zero_values_checkbox.is_selected():
        zero_values_checkbox.click()
        time.sleep(1)
    
    # Waiting for the query result to appear
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "ContentPlaceHolderMain_ContentPlaceHolderAltGridFull_LabelQueryResultInfo")))

    # Wait for download button and click it        
    download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ContentPlaceHolderMain_ContentPlaceHolderAltGridFull_ButtonDownload")))
    
    # download data
    download_button.click()
    max_wait_time = 30
    wait_interval = 2
    elapsed_time = 0
        
    latest_zip = None
    while elapsed_time < max_wait_time:
        time.sleep(wait_interval)
        elapsed_time += wait_interval

        survstat_zips = [f for f in downloads_path.iterdir() 
                        if f.is_file() and f.name.lower().startswith("survstat") and f.suffix == ".zip"]
        
        if survstat_zips:
            latest_zip = max(survstat_zips, key=lambda x: x.stat().st_mtime)
            break

    if latest_zip:
        return latest_zip
    
    else:
        raise FileNotFoundError("No survstat ZIP file found after download")

def extract_zip(downloads_path: Path,
             latest_zip: Path,
             disease_name_alias: str,
             output_directory: Path,
             year: str):
    """
    Extracts data from the .zip file into the new output_directory.
    """

    temp_extract_path = downloads_path / "temp_extract"
    temp_extract_path.mkdir(exist_ok=True)
    
    with zipfile.ZipFile(latest_zip, 'r') as zip_ref:
        zip_ref.extractall(temp_extract_path)
    
    # Find Data.csv and copy it with the new name
    data_csv_path = temp_extract_path / "Data.csv"
    if data_csv_path.exists():
        # Create disease-specific directory
        disease_folder_name = disease_name_alias.lower().replace(' ', '_')
        disease_directory = os.path.join(output_directory, disease_folder_name)
        os.makedirs(disease_directory, exist_ok=True)
        
        # Create filename and full path
        output_filename = f"{disease_name_alias.lower().replace(' ', '_')}_{year}.csv"
        output_path = os.path.join(disease_directory, output_filename)
        
        # Simply copy the file as-is
        shutil.copy2(data_csv_path, output_path)
        
        # Clean up - remove the downloaded ZIP and temp folder
        latest_zip.unlink()
        shutil.rmtree(temp_extract_path)
    
    else:
        raise FileNotFoundError("Data.csv not found in downloaded ZIP file")

def scrape_survstat_data(disease_names: Union[Dict, List, str], 
                         years:  Union[str, List[str], range, int], 
                         downloads_directory: Union[str, Path],
                         output_directory: Union[str, Path],
                         ):
    """
    Scrapes data from SurvStat for a specific disease and year.
    The result is a .csv-file in the specified folder within which
    a new folder is initiated of the disease. By default:
    'data / raw / {disease_name_alias}'

    Parameters:
    ----------
    disease_names: Union[str, Dict[str,str], List[str]]
        Name of the disease such that the function can find it on Survstat. For example: 'Keuchhusten'.
        You can put in a dictionary, [disease_name_rki : disease_name_alias], or a list of the disease-name_rki,
        where disease_name_rki corresponds to the naming convention by the RKI, and the disease_name_alias is the name
        for local use. If not specified, the function will use the disease_name_rki. Else, the data will be stored 
        using the naming of disease_name_alias.
    year: Union[str, int, List] 
        Year(s) to scrape data for
    downloads_directory: Union[str, Path]
        download-directory where .zip folders are introduced to the system.
    output_directory: Union[str, Path]
        Directory to save the data
        
    Examples:
    --------
    >>> scrape_survstat_data(disease_names=diseases_dict, 
    >>>                      years=current_year, 
    >>>                      output_directory=directories_dict['dir_data_raw'], 
    >>>                      downloads_directory=directories_dict['dir_downloads'])

    See also:
    ---------
    remove_downloads_folder
    scraper
    extract_zip
    """
    # input validation
    if isinstance(years, int):
        years = str(years)

    if isinstance(years, str):
        years = [years]

    if isinstance(years, range):
        years = [str(yy) for yy in years]

    if isinstance(disease_names, str):
        disease_names = {disease_names:disease_names}

    if isinstance(disease_names, List):
        disease_names = {dd:dd for dd in disease_names}

    # Handle downloads_path
    if isinstance(downloads_directory, str):
        downloads_directory = Path(downloads_directory)

    if isinstance(output_directory, str):
        output_directory = Path(output_directory)        

    # Clearing up all survstat zip folders in the downloads folder
    remove_downloads_folder(downloads_directory)    

    # use tqdm if there are multiple diseases
    bug_iter = tqdm(disease_names.items(), desc="Diseases") if len(disease_names) > 1 else disease_names.items()

    for bug_name_rki, bug_name_alias in bug_iter:
        # use tqdm if there are multiple years
        year_iter = tqdm(years, desc=f"Years for {bug_name_alias}") if len(years) > 1 else years
        for yy in year_iter:
            # Downloading the data
            zip = scraper(bug_name_rki, yy, downloads_directory)

            extract_zip(downloads_directory, zip, bug_name_alias, output_directory, yy)

    print('✅ all data has been scraped')