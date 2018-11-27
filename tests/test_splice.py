import pytest
import tempfile

from splice import splice


TESTFILE = "$testfile"
BIGFILE_SIZE = (1024*1024*1024)  # 1GB
SAMPLE_DATA = (b"12345abcde" * 1024 * 1024)  # 10MB


@pytest.fixture()
def create_files():
    # create files for tests (setUp)
    file_in = tempfile.TemporaryFile()
    file_out = tempfile.TemporaryFile()

    yield (file_in, file_out)

    # close file after a test is complete (teardown)
    file_out.close()
    file_in.close()


def test_simple_file(create_files):
    (file_in, file_out) = create_files
    file_in.write(SAMPLE_DATA)
    file_in.seek(0)
    file_in_contents = file_in.read()
    nbytes = splice(file_in.fileno(), file_out.fileno(), 0, len(file_in_contents))
    assert nbytes == len(file_in_contents)


def test_empty_file(create_files):
    (file_in, file_out) = create_files
    empty_file_in = tempfile.TemporaryFile()
    empty_file_in.write(b'')
    empty_file_in.seek(0)
    nbytes = splice(empty_file_in.fileno(), file_out.fileno(), 0, len(empty_file_in.read()))
    assert nbytes == 0
    empty_file_in.close()


def test_large_file(create_files):
    (file_in, file_out) = create_files
    file_in = tempfile.SpooledTemporaryFile()
    file_in.write(SAMPLE_DATA * 128)
    file_in.seek(0)
    file_in_contents = file_in.read()
    print("len: " + str(len(file_in_contents)))
    nbytes = splice(file_in.fileno(), file_out.fileno(), 0, len(file_in_contents))
    assert nbytes == len(file_in_contents)


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
