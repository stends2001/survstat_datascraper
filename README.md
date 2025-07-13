# SurvStat Loader

A Python tool for automated data collection and processing from the [SurvStat@RKI](https://survstat.rki.de/) platform, Germany's interactive infectious disease surveillance system.

## Overview

This project automates the download and processing of disease surveillance data from the Robert Koch Institute (RKI). Using Selenium, it downloads data for specified diseases and years, organized by week and German administrative districts (Kreise). The data is then processed and harmonized using regional identification codes.

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

## Project Structure

```
survstat_loader/
├── src/
│   ├── dataprocessor/          # Data processing modules
│   ├── survstat_collecting/    # Web scraping and data collection
│   ├── utils/                  # Utility functions
│   └── update_survstatdata.py  # Main execution script
│   └── preview_epicurve.py     # show weekly casenumbers of downloaded data
├── data/                       # Data storage (not in git)
│   ├── raw/                    # Raw downloaded files
│   ├── preprocessed/           # Processed datasets
│   └── harmonization/          # Geographic mapping files
├── config.yaml                 # Configuration file
└── requirements.txt            # Python dependencies
```

## Configuration

Edit `config.yaml` to customize:
- Data directory paths
- Download locations
- Processing options

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.