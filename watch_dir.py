import os
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


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
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    directory_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    directory_event_handler.on_created = on_created
    directory_event_handler.on_deleted = on_deleted
    directory_event_handler.on_modified = on_modified
    directory_event_handler.on_moved = on_moved
    # directory_event_handler.on_copy = on_moved

    path = "./tmp"  # current directory
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
