import os
import os.path
from os import path
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


def move_files(files, directory_to_move):
    print('Moving files')
    verify_backup_dir(directory_to_move)
    pass


def verify_backup_dir(folder_path):
    backup_name = time.strftime("%Y%m%d")
    print('Verifying backup directory')
    if not os.path.isdir(f'{folder_path}'):
        print('Creating backup directory')
        os.makedirs(f'{folder_path}/{backup_name}')
    else:
        print('Directory already exists')


def create_backup(changed_files=None):
    if changed_files is None:
        changed_files = []
    print('Creating backup')

    for file in changed_files:

        os.system('cp -r ./staging/non-prod ./non-prod/')


def compress_files():
    print('Compressing files')
    os.system('tar -czvf non-prod.tar.gz non-prod')


def on_created(event):
    print(os.path.basename(event.src_path))
    print(f"hey, {event.src_path} has been created!")


def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")


def on_modified(event):
    print(os.path.basename(event.src_path))
    print(f"hey buddy, {event.src_path} has been modified")


def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")


if __name__ == "__main__":
    patterns = ["*.py", "*.txt", "*.md", "*.json", "*.bat", "*.sh"]

    # TODO: add .gitignore and .env to patterns
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    directory_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    directory_event_handler.on_created = on_created
    directory_event_handler.on_deleted = on_deleted
    directory_event_handler.on_modified = on_modified
    directory_event_handler.on_moved = on_moved
    # directory_event_handler.on_copy = on_moved

    path = "./staging/non-prod"  # current directory
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(directory_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
