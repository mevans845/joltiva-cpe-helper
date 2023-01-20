import os
import os.path
import get_envrion
import time
import shutil
# import subprocess
from subprocess import Popen, PIPE, STDOUT
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

max_tries = 3


# TODO: Add a function to verify the backup directory exists
def verify_backup_dir(folder_path):
    backup_name = time.strftime("%Y%m%d%H%M")
    print('Verifying backup directory')
    if not os.path.isdir(f'{folder_path}'):
        print('Creating backup directory')
        os.makedirs(f'{folder_path}{backup_name}')
    else:
        # TODO decide if we want to create a new backup directory or not and just overwrite the old one
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


def retry(process, max_tries=3):
    for i in range(max_tries):
        try:
            time.sleep(100)
            verify_process_not_running(process)
            break
        except Exception as e:
            print(f"Unsuccessful after 3 attempts {e}")
            continue


def verify_process_not_running(process_name=get_envrion.get_env("PROCESS_NAME"), has_retried=False):
    """

    :param has_retried:
    :param process_name:
    :return:
    """
    environ = str(get_envrion.get_env("PROCESS_NAME"))
    try:
        program_path = "C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe"
        process_name = str(process_name)

        p = Popen([f"{program_path}", "-Command",
                   '&{Get-ScheduledTask -TaskPath \\* | where taskname -eq "WizNonProdAlerts" | select state;}'],
                  shell=True, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        output = output.decode("utf-8")
        print(output)
        clean_output = output.split()
        rc = p.returncode
        print(f"output: {clean_output[2]}, err: {err}, return_code: {rc}")
        status = clean_output[2]
        if status == "Ready":
            return True
        else:
            print(f"The Process is not in a good state and is currently: {status}")
            return False
            # TODO: Change retry logic here
    except Exception as e:
        print(f"Something went wrong: {e}")


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
            backup_name = time.strftime("%Y%m%d%H%M")
            # TODO:
            # print('Verifying backup directory')
            print(f"backup folder name: {backup_dir}{backup_name}")
            if not os.path.isdir(f'{backup_dir}{backup_name}'):
                print('Creating backup directory')
                os.makedirs(f'{backup_dir}{backup_name}')
            print(f"backing up existing files")
            try:
                # TODO: and Windows support
                shutil.copy(f"{dir_to_move}{file}", f"{backup_dir}{backup_name}\{file}")
                print(f"copied the source {dir_to_move}{file} to {backup_dir}{backup_name}\{file}")
            except FileNotFoundError:
                print(f"File not found: {dir_to_move}{file} is this a possible first deployment?")
            print("Moving files to destination")
            is_not_running = verify_process_not_running(get_envrion.get_env("PROCESS_NAME"))
            if is_not_running:
                shutil.copy(f"{root_path}{file}", dir_to_move)
            else:
                print("Process running retrying")
                retry(get_envrion.get_env("PROCESS_NAME"), 3)
        except Exception as e:
            print(f"Failed to move {file} or it already has been moved. {e}")
            print("Or the CSPM application is running")


def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")


if __name__ == "__main__":
    patterns = ["*.py", "*.txt", "*.md", "*.json", "*.bat", "*.sh", "*.yml", "*.yaml", "*.ps1", "*.psm1", "*.psd1"]

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

    path = get_envrion.get_env("DIRECTORY")  # "./staging/non-prod/"  # current directory
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
