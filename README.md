# qBittorrent File Checker

This script checks a specified directory for files that are not part of any active torrents in qBittorrent and optionally deletes or moves them to the recycle bin.

## Features
- Connects to qBittorrent to retrieve torrent information.
- Checks a specified directory for files not part of any torrent.
- Supports dry run to display which files would be deleted.
- Option to delete files permanently or move them to the recycle bin.
- Uses concurrent processing for efficient handling of large numbers of files.

## Requirements
- Python 3
- qbittorrent-api
- send2trash (optional for recycle bin functionality)

## Installation
1. Clone this repository or download the script.
2. Install required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the script from the command line, providing the necessary arguments:
```bash
python qbittorrent_file_checker.py --folder_path "path/to/directory"
```

### Arguments  
```bash
--folder_path: Path to the folder containing files to check.
--dry_run: Perform a dry run without deleting files.
--recycle: Move files to recycle bin instead of permanent deletion.
--host: qBittorrent host (default: localhost).
--port: qBittorrent port (default: 8080).
--username: qBittorrent username (default: admin).
--password: qBittorrent password (default: admin).
```

## Contributing

Contributions, issues, and feature requests are welcome!
