# TO BE UPDATED
- Pathmanagement
- DataProcessor

# SurvStat Loader

A Python tool for automated data collection and processing from the [SurvStat@RKI](https://survstat.rki.de/) platform, Germany's interactive infectious disease surveillance system.

## Overview

This project automates the download and processing of disease surveillance data from the Robert Koch Institute (RKI). Using Selenium, it downloads data for specified diseases and years, organized by week and German administrative districts (Kreise). The data is then processed and harmonized using regional identification codes.

For a walkthrough of the pipleine in this rep, have a look at *Extracting_survstat_data.ipynb*, in src.

## Features

- **Automated Data Collection**: Downloads disease data from SurvStat@RKI for multiple diseases and years
- **Data Processing**: Merges yearly files into standardized datasets
- **Geographic Harmonization**: Translates district names to official regional codes (Kreiskennziffern)
- **Flexible Configuration**: Easy configuration through YAML files
- **DataProcessingOrchestrator**: A (large and generic) class for chaining data processing steps

## Installation

1. Clone the repository:
```bash
git clone https://github.com/stends2001/survstat_data.git
cd survstat_loader
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the project by editing `config.yaml` if needed.

## Usage

### Quick Start

Run the main script to download and process current year data:

```bash
python src/update_survstatdata.py
```

### Manual Usage

```python
from src.survstat_collecting.survstat_scraper import scrape_survstat_data
from src.survstat_collecting.casedata_processing import preprocess_survstat_data

# Update current datafiles for the current year
scrape_survstat_data(
    disease_names={'campylobacter': 'Campylobacter'},
    years='2025',
    output_directory=directories_dict['dir_data_raw'], 
    downloads_directory=directories_dict['dir_downloads']
)

# Process the downloaded data
preprocess_survstat_data(
    diseases=['Campylobacter'],
    years='2025',
    raw_data_dir=directories_dict['dir_data_raw'], 
    processed_data_dir=directories_dict['dir_data_preprocessed'],
    how='update'
)
```

## Demo with Sample Data

To see the tool in action with sample data:

1. **Generate sample data** (if you have real data):
```bash
python src/create_github_sample.py
```

2. **View the demo notebook**:
   - Open `src/Demo_measles_visualization.ipynb` to see a visualization of national measles data
   - The sample data contains real national measles data aggregated from the SurvStat system

3. **Sample data structure**:
   - `data/sample/measles_national.csv`: National weekly measles cases
   - Contains: `timestamp`, `cases` columns
   - Safe to share on GitHub (national-level data only)

## Project Structure

```
survstat_loader/
├── src/
│   ├── dataprocessor/          # Data processing modules
│   ├── survstat_collecting/    # Web scraping and data collection
│   ├── utils/                  # Utility functions
│   ├── update_survstatdata.py  # Main execution script
│   ├── preview_epicurve.py     # Show weekly casenumbers of downloaded data
│   ├── create_github_sample.py # Create sample data for GitHub
│   └── Demo_measles_visualization.ipynb # Demo notebook
├── data/                       # Data storage (not in git)
│   ├── raw/                    # Raw downloaded files
│   ├── preprocessed/           # Processed datasets
│   ├── harmonization/          # Geographic mapping files
│   └── sample/                 # Sample data for GitHub (committed)
├── config.yaml                 # Configuration file
└── requirements.txt            # Python dependencies
```

## Data Privacy

- **Real data**: Stored in `data/` directories and excluded from Git
- **Sample data**: Only national-level aggregated data is shared
- **Regional data**: Contains district-level information and is kept private
- **Full datasets**: Multiple diseases and years are excluded from repository

## Configuration

Edit `config.yaml` to customize:
- Data directory paths
- Download locations
- Processing options

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.