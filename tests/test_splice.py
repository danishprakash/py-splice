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
    file_in_content = file_in.read()

    nbytes = splice(file_in.fileno(), file_out.fileno(), 0, len(file_in_content))
    file_out_content = file_out.read()

    assert nbytes == len(file_in_content)
    assert nbytes == len(file_out_content)
    assert len(file_out_content) == len(file_in_content)
    assert hash(file_out_content) == hash(file_in_content)


def test_small_file(create_files):
    (file_in, file_out) = create_files

    # create small file
    file_in = tempfile.TemporaryFile()
    file_in.write(b'foo bar')
    file_in.seek(0)
    file_in_content = file_in.read()

    nbytes = splice(file_in.fileno(), file_out.fileno(), 0, len(file_in_content))
    file_out_content = file_out.read()

    assert nbytes == len(file_in_content)
    assert nbytes == len(file_out_content)
    assert len(file_out_content) == len(file_in_content)
    assert hash(file_in_content) == hash(file_out_content)


def test_small_file_with_offset_overflow(create_files):
    (file_in, file_out) = create_files

    # create small file
    file_in = tempfile.TemporaryFile()
    file_in.write(b'foo bar')
    file_in.seek(0)
    file_in_content = file_in.read()
    offset = 4096

    with pytest.raises(OverflowError):
        splice(file_in.fileno(), file_out.fileno(), offset, len(file_in_content))


def test_empty_file(create_files):
    (file_in, file_out) = create_files

    # empty file
    file_in = tempfile.TemporaryFile()
    file_in.write(b'')
    file_in.seek(0)
    file_in_content = file_in.read()

    assert len(file_in_content) == 0
    nbytes = splice(file_in.fileno(), file_out.fileno(), 0, len(file_in_content))
    file_out_content = file_out.read()

    assert nbytes == 0
    assert nbytes == len(file_in_content)
    assert nbytes == len(file_out_content)
    assert len(file_out_content) == len(file_in_content)
    assert hash(file_in_content) == hash(file_out_content)


def test_large_file(create_files):
    (file_in, file_out) = create_files

    # create a large file
    file_in = tempfile.SpooledTemporaryFile()
    file_in.write(SAMPLE_DATA * 1)  # * 1024 when automating tests (~1GB)
    file_in.seek(0)
    file_in_content = file_in.read()

    nbytes = splice(file_in.fileno(), file_out.fileno(), 0, len(file_in_content))
    file_out_content = file_out.read()

    assert nbytes == len(file_in_content)
    assert nbytes == len(file_out_content)
    assert len(file_out_content) == len(file_in_content)
    assert hash(file_in_content) == hash(file_out_content)


def test_copy_from_certain_offset(create_files):
    (file_in, file_out) = create_files
    file_in_content = file_in.read()

    offset = 1024

    nbytes = splice(file_in.fileno(), file_out.fileno(), offset, len(file_in_content))
    file_out_content = file_out.read()

    assert nbytes == len(file_in_content[offset:])
    assert nbytes == len(file_out_content)
    assert len(file_in_content[offset:]) == len(file_out_content)
    assert hash(file_in_content[offset:]) == hash(file_out_content)


def test_arguments_not_denoting_file_descriptors(create_files):
    (file_in, file_out) = create_files

    with pytest.raises(TypeError):
        splice('test', file_out.fileno(), 0, 0)


def test_copy_certain_nbytes(create_files):
    (file_in, file_out) = create_files
    file_in_content = file_in.read()

    bytes_to_copy = 2048

    nbytes = splice(file_in.fileno(), file_out.fileno(), 0, bytes_to_copy)
    file_out_content = file_out.read()

    assert nbytes == bytes_to_copy
    assert nbytes == len(file_out_content)
    assert bytes_to_copy == len(file_out_content)
    assert len(file_in_content[:bytes_to_copy]) == len(file_out_content)
    assert hash(file_in_content[:bytes_to_copy]) == hash(file_out_content)


def test_offset_overflow(create_files):
    (file_in, file_out) = create_files
    file_in_content = file_in.read()

    offset = len(file_in_content) + 1

    with pytest.raises(OverflowError):
        splice(file_in.fileno(), file_out.fileno(), offset, len(file_in_content))


def test_len_overflow(create_files):
    (file_in, file_out) = create_files
    file_in_content = file_in.read()

    with pytest.raises(OverflowError):
        splice(file_in.fileno(), file_out.fileno(), 0, len(file_in_content)+1)


def test_incomplete_arguments(create_files):
    (file_in, file_out) = create_files

    with pytest.raises(TypeError):
        splice(file_in.fileno(), file_out.fileno(), 0)


def test_invalid_file_descriptor(create_files):
    (file_in, file_out) = create_files
    file_in_content = file_in.read()

    with pytest.raises(ValueError):
        splice(999, file_out.fileno(), 0, len(file_in_content))
