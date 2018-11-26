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
    file_in.write(SAMPLE_DATA)
    file_in.seek(0)
    file_in_contents = file_in.read()

    yield (file_in, file_out, file_in_contents)

    # close file after a test is complete (teardown)
    file_out.close()
    file_in.close()


def test_simple_file(create_files):
    (file_in, file_out, file_in_contents) = create_files
    nbytes = splice(file_in.fileno(), file_out.fileno(), 0, len(file_in_contents))
    assert nbytes == len(file_in_contents)

# def test_large_file():
#     if _has_large_file_support():
#         # TODO: check here
#         pass
#     pass


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
