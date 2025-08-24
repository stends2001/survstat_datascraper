from utils.dirs import directories_dict
from dataprocessor import DataProcessingOrchestrator
from utils.libs import plt, mdates
import os


def preview_epicurve(disease_name: str):
    """
    Preview the epicurve of a given disease.

    Parameters:
    ----------
    disease_name: str 
        The name of the disease.
    """
    # Get the directory path and check if it exists
    data_dir = os.path.join(directories_dict['dir_data_preprocessed'], disease_name)
    data_file = os.path.join(data_dir, f'{disease_name}.csv')
    
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Data file not found: {data_file}")
    
    regional_data = (DataProcessingOrchestrator(name=disease_name)
                 .import_data(filename=f'{disease_name}.csv', directory=data_dir)
                 .change_dtype({'timestamp': 'datetime64[ns]',
                                'year': 'str'})
                 )

    # Group by year to get total cases per year
    cases_per_year = regional_data.copy().groupby(groupby_columns=['year'], aggregations={'cases': 'sum'}).reset_index()  # type: ignore
    
    # Filter years that have cases > 0
    years_with_cases = cases_per_year.filter(conditions=[('cases', 0, ">")])
    
    # Get unique years as a list (convert numpy array to list)
    unique_years = years_with_cases.df['year'].unique().tolist()  # type: ignore

    # Create national data by grouping by timestamp
    national_data = (regional_data.copy()
                    .filter([('year', unique_years, 'in')])
                    .groupby(groupby_columns=['timestamp'], aggregations={'cases': 'sum'})  # type: ignore
                    .reset_index()
                    .df
                    )

    fig, ax = plt.subplots(figsize = (12,4))
    ax.plot(national_data['timestamp'], national_data['cases'])
    ax.grid()
    ax.set_title(f'Weekly reported cases of {disease_name} in Germany \nBetween {national_data["timestamp"].min().strftime("%Y-%m-%d")} and {national_data["timestamp"].max().strftime("%Y-%m-%d")}')
    ax.set_ylabel('Weekly cases')

    if len(national_data) < 5 * 52:
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    else:
        ax.xaxis.set_major_locator(mdates.YearLocator(2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    plt.show()

if __name__ == "__main__":
    preview_epicurve(disease_name = 'tick_borne_encephalitis')