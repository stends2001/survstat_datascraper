from pathlib import Path
import os
import yaml

def get_downloads_folder():
    """
    Get the user's default downloads folder dynamically across different operating systems.
    This is the folder in which the downloads are found.
    """
    home = Path.home()
    
    possible_downloads = [
        home / "Downloads",
        home / "Download", 
        home / "downloads",
        home / "Desktop"  # Fallback
    ]
    
    for downloads_path in possible_downloads:
        if downloads_path.exists():
            return downloads_path
    
    # If none found, create Downloads folder in home directory
    downloads_path = home / "Downloads"
    downloads_path.mkdir(exist_ok=True)

    return downloads_path

project_root = Path(__file__).parent.parent.parent  # Go up from src/ to project root
config_path = project_root / "config.yaml"

if config_path.exists():
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
else:
    config = {}

def get_path(key, default):
    """Get a path, making it absolute relative to project root if it's relative."""
    config_value = config.get(key, default)
    path = Path(os.path.expanduser(config_value))
    
    # If it's a relative path, make it absolute relative to project root
    if not path.is_absolute():
        path = project_root / path
    
    return path

directories_dict = {
    'project_root': project_root,
    'dir_downloads': get_path('downloads_dir', str(Path.home() / 'Downloads')),
    'dir_data': get_path('data_dir', project_root / 'data'),
    'dir_data_raw': get_path('raw_data_dir', project_root / 'data' / 'raw'),
    'dir_data_preprocessed': get_path('preprocessed_data_dir', project_root / 'data' / 'preprocessed'),
    'dir_data_harmonization': get_path('harmonization_dir', project_root / 'data' / 'harmonization'),
}