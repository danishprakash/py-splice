import splice


TESTFILE = "$testfile"
BIGFILE_SIZE = 2500000000  # > 2GB
TEN_MB_DATA = ("12345abcde" * 1024 * 1024)  # 10MB


def _has_large_file_support():
    # taken from Python's Lib/test/test_largefile.py
    with open(TESTFILE, 'wb', buffering=0) as f:
        try:
            f.seek(BIGFILE_SIZE)
            f.write(('x'))
            f.flush()
        except (IOError, OverflowError):
            return False
        else:
            return True


def test_simple_file():
    pass


def test_large_file():
    if _has_large_file_support():
        # TODO: check here
        pass
    pass


def test_empty_file():
    pass


def test_whole_file():
    pass


def test_no_file():
    pass


def test_invalid_file_descriptor():
    pass


def test_nonexistent_file_descriptor():
    pass


def test_copy_from_offset():
    pass


def test_arguments_not_denoting_file_descriptors():
    pass


def test_copy_certain_nbytes():
    pass


def test_copy_with_zero_offset():
    pass


def test_offset_overflow():
    pass


def test_small_file():
    pass
