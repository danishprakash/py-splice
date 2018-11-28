import pytest
import tempfile

from splice import splice

SAMPLE_DATA = (b"12345abcde" * 1024 * 1024)  # ~10MB


@pytest.fixture()
def create_files():
    # create files for tests (setUp)
    file_in = tempfile.TemporaryFile()
    file_out = tempfile.TemporaryFile()
    file_in.write(SAMPLE_DATA)
    file_in.seek(0)

    yield (file_in, file_out)

    # close files after a test is complete (teardown)
    file_out.close()
    file_in.close()


def test_simple_file(create_files):
    (file_in, file_out) = create_files
    file_in_contents = file_in.read()

    nbytes = splice(file_in.fileno(), file_out.fileno(), 0, len(file_in_contents))
    assert nbytes == len(file_in_contents)


def test_small_file(create_files):
    (file_in, file_out) = create_files
    file_in = tempfile.TemporaryFile()
    file_in.write(b'foo bar')
    file_in.seek(0)
    file_in_contents = file_in.read()

    nbytes = splice(file_in.fileno(), file_out.fileno(), 0, len(file_in_contents))
    assert nbytes == len(file_in_contents)


def test_small_file_with_offset_overflow(create_files):
    (file_in, file_out) = create_files
    file_in = tempfile.TemporaryFile()
    file_in.write(b'foo bar')
    file_in.seek(0)
    file_in_contents = file_in.read()
    offset = 4096

    with pytest.raises(OverflowError):
        nbytes = splice(file_in.fileno(), file_out.fileno(), offset, len(file_in_contents))


def test_empty_file(create_files):
    (file_in, file_out) = create_files

    # empty file 
    file_in = tempfile.TemporaryFile()
    file_in.write(b'')
    file_in.seek(0)
    file_in_contents = file_in.read()

    assert len(file_in_contents) == 0
    nbytes = splice(file_in.fileno(), file_out.fileno(), 0, len(file_in_contents))
    assert nbytes == 0


def test_large_file(create_files):
    (file_in, file_out) = create_files

    # create a large file
    file_in = tempfile.SpooledTemporaryFile()
    file_in.write(SAMPLE_DATA * 1)  # set to * 1024 when automating tests (~1GB)
    file_in.seek(0)
    file_in_contents = file_in.read()

    nbytes = splice(file_in.fileno(), file_out.fileno(), 0, len(file_in_contents))
    assert nbytes == len(file_in_contents)


def test_copy_from_certain_offset(create_files):
    (file_in, file_out) = create_files
    file_in_contents = file_in.read()

    offset = 1024

    nbytes = splice(file_in.fileno(), file_out.fileno(), offset, len(file_in_contents))
    assert nbytes == len(file_in_contents[offset:])


def test_arguments_not_denoting_file_descriptors(create_files):
    (file_in, file_out) = create_files

    with pytest.raises(TypeError):
        nbytes = splice('test', file_out.fileno(), 0, 0)


def test_copy_certain_nbytes(create_files):
    (file_in, file_out) = create_files
    file_in_contents = file_in.read()

    bytes_to_copy = 2048

    nbytes = splice(file_in.fileno(), file_out.fileno(), 0, bytes_to_copy)
    assert nbytes == bytes_to_copy


def test_offset_overflow(create_files):
    (file_in, file_out) = create_files
    file_in_contents = file_in.read()

    offset = len(file_in_contents) + 1

    with pytest.raises(OverflowError):
        nbytes = splice(file_in.fileno(), file_out.fileno(), offset, len(file_in_contents))


def test_len_overflow(create_files):
    (file_in, file_out) = create_files
    file_in_contents = file_in.read()

    with pytest.raises(OverflowError):
        nbytes = splice(file_in.fileno(), file_out.fileno(), 0, len(file_in_contents)+1)


def test_incomplete_arguments(create_files):
    (file_in, file_out) = create_files

    with pytest.raises(TypeError):
        nbytes = splice(file_in.fileno(), file_out.fileno(), 0)


def test_invalid_file_descriptor(create_files):
    (file_in, file_out) = create_files
    file_in_contents = file_in.read()

    with pytest.raises(ValueError):
        nbytes = splice(999, file_out.fileno(), 0, len(file_in_contents))
