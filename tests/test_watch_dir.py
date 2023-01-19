from unittest import TestCase

import watch_dir


class TestWatchDir(TestCase):
    def test_move_files(self):
        self.fail()

    def test_verify_backup_dir(self):
        self.fail()

    def test_create_backup(self):
        self.fail()

    def test_compress_files(self):
        self.fail()

    def test_on_created(self):
        self.fail()

    def test_on_deleted(self):
        self.fail()

    def test_on_modified(self):
        self.fail()

    def test_on_moved(self):
        self.fail()

    def test_verify_process_not_running(self):

        result = watch_dir.verify_process_not_running()
        print("I'm printing the result")
        print(result)
        self.fail()
