import os
import qbittorrentapi
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
try:
    from send2trash import send2trash
except ImportError:
    send2trash = None

def establish_qbittorrent_connection(conn_info):
    """Establish connection to qBittorrent client."""
    try:
        qbt_client = qbittorrentapi.Client(**conn_info)
        qbt_client.auth_log_in()
        sys.stdout.write('Successfully connected to qBittorrent\n')
        return qbt_client
    except qbittorrentapi.LoginFailed as e:
        sys.stdout.write(f'Login failed: {e}\n')
        sys.exit()

def get_torrent_info_dict(qbt_client):
    """Retrieve and normalize torrent file paths and sizes from qBittorrent."""
    torrent_info_dict = {}
    all_torrents = qbt_client.torrents_info(status_filter='all')
    for torrent in all_torrents:
        for file_entry in torrent.files:
            normalized_path = os.path.normpath(os.path.join(torrent.name, file_entry.name))
            torrent_info_dict[normalized_path] = file_entry.size
    return torrent_info_dict

def get_file_names_set(torrent_info_dict):
    """Create a set of file names for quicker lookup."""
    return {os.path.basename(path) for path in torrent_info_dict}

def handle_file(file_path, args):
    """Handle each file based on script arguments, either dry run or delete/recycle."""
    if args.dry_run:
        sys.stdout.write(f'Dry run: File "{file_path}" will be deleted\n')
    else:
        sys.stdout.write(f'Deleting: File "{file_path}"\n')
        if args.recycle:
            if send2trash:
                send2trash(file_path)
            else:
                sys.stdout.write('Send to recycle bin option is not available.\n')
        else:
            os.remove(file_path)

def process_file(file_path, file_names_set, args):
    """Process an individual file."""
    file_name_only = os.path.basename(file_path)
    if file_name_only not in file_names_set:
        handle_file(file_path, args)

def process_files_concurrently(folder_path, file_names_set, args):
    """Process files in the specified folder using concurrent processing."""
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_file, os.path.join(root, file), file_names_set, args) 
                   for root, _, files in os.walk(folder_path) for file in files]

        for _ in as_completed(futures):
            pass

    sys.stdout.write('\nProcessing finished!\n')

# Main script starts here
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check and delete files and folders not part of qBittorrent torrents.")
    parser.add_argument('--folder_path', help='Path to the folder containing files to check', dest='folder_path')
    parser.add_argument('--dry_run', action='store_true', help='Dry run to just print files that will be deleted')
    parser.add_argument('--recycle', action='store_true', help='Move files to recycle bin instead of permanent deletion')
    parser.add_argument('--host', default='localhost', help='qBittorrent host')
    parser.add_argument('--port', type=int, default=8080, help='qBittorrent port')
    parser.add_argument('--username', default='admin', help='qBittorrent username')
    parser.add_argument('--password', default='admin', help='qBittorrent password')
    args = parser.parse_args()

    conn_info = {
        'host': args.host,
        'port': args.port,
        'username': args.username,
        'password': args.password
    }

    qbt_client = establish_qbittorrent_connection(conn_info)
    torrent_info_dict = get_torrent_info_dict(qbt_client)
    file_names_set = get_file_names_set(torrent_info_dict)

    folder_path = args.folder_path or os.getcwd()
    if not os.path.exists(folder_path):
        sys.stdout.write(f'Error: Invalid folder path: {folder_path}\n')
        sys.exit()

    process_files_concurrently(folder_path, file_names_set, args)
