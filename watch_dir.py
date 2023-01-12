import os
import os.path
from os import path
import get_envrion
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import shutil


def move_files(files, directory_to_move):
    print('Moving files')
    verify_backup_dir(directory_to_move)
    if verify_backup_dir(directory_to_move):
        create_backup(files)
        compress_files()
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

        os.system(f'cp -r {file} ./non-prod/{file}')


def compress_files():
    print('Compressing files')
    os.system('tar -czvf non-prod.tar.gz non-prod')


def on_created(event):
    print(os.path.basename(event.src_path))
    print(f"SOMETHING WAS CREATED, {event.src_path} has been created!")


def on_deleted(event):
    print(f"ITEMS WHERE DELETED {event.src_path}!")


def on_modified(event):
    print(os.path.basename(event.src_path))
    # root_path = os.path.dirname(event.src_path)
    root_path = get_envrion.get_env('DIRECTORY')
    modified_files = [os.path.basename(event.src_path)]
    print(f"HEY, {event.src_path} has been MODIFIED")
    print(root_path)
    dir_to_move = get_envrion.get_env('DIRECTORY_TO_MOVE')
    backup_dir = get_envrion.get_env('BACKUP')
    for file in modified_files:
        print(f"Moving {file}")
        try:
            # create_backup(modified_files)
            # TODO: Testing shortcut
            shutil.copy(f"{dir_to_move}/{file}", f"{backup_dir}/{file}")
            shutil.copy(f"{root_path}{file}", dir_to_move)
        except Exception as e:
            print(f"Failed to move {file} or it already has been moved. {e}")


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

    path = "./staging/non-prod/"  # current directory
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
