import pytest
import tempfile

from splice import splice
from splice import SPLICE_F_MORE, SPLICE_F_MOVE, SPLICE_F_GIFT, SPLICE_F_NONBLOCK

SAMPLE_DATA = (b'12345abcde' * 1024 * 1024)  # ~10MB


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
    content_in = file_in.read()

    bytes_copied = splice(file_in.fileno(), file_out.fileno())
    content_out = file_out.read()

    assert bytes_copied == len(content_in)
    assert bytes_copied == len(content_out)
    assert len(content_out) == len(content_in)
    assert hash(content_out) == hash(content_in)


def test_simple_file_with_all_optional_args(create_files):
    (file_in, file_out) = create_files
    content_in = file_in.read()

    bytes_copied = splice(file_in.fileno(), file_out.fileno(),
                          offset=0, nbytes=len(content_in),
                          flags=SPLICE_F_MORE)

    content_out = file_out.read()

    assert bytes_copied == len(content_in)
    assert bytes_copied == len(content_out)
    assert len(content_out) == len(content_in)
    assert hash(content_out) == hash(content_in)


def test_simple_file_with_all_flags(create_files):
    (file_in, file_out) = create_files
    content_in = file_in.read()

    bytes_copied = splice(file_in.fileno(), file_out.fileno(),
                          flags=SPLICE_F_MORE | SPLICE_F_MOVE
                          | SPLICE_F_NONBLOCK | SPLICE_F_GIFT)

    content_out = file_out.read()

    assert bytes_copied == len(content_in)
    assert bytes_copied == len(content_out)
    assert len(content_out) == len(content_in)
    assert hash(content_out) == hash(content_in)


def test_small_file(create_files):
    (file_in, file_out) = create_files

    # create small file
    file_in = tempfile.TemporaryFile()
    file_in.write(b'foo bar')
    file_in.seek(0)
    content_in = file_in.read()

    bytes_copied = splice(file_in.fileno(), file_out.fileno())
    content_out = file_out.read()

    assert bytes_copied == len(content_in)
    assert bytes_copied == len(content_out)
    assert len(content_out) == len(content_in)
    assert hash(content_in) == hash(content_out)


def test_small_file_with_flag(create_files):
    (file_in, file_out) = create_files

    # create small file
    file_in = tempfile.TemporaryFile()
    file_in.write(b'foo bar')
    file_in.seek(0)
    content_in = file_in.read()

    bytes_copied = splice(file_in.fileno(), file_out.fileno(),
                          flags=SPLICE_F_MORE)

    content_out = file_out.read()

    assert bytes_copied == len(content_in)
    assert bytes_copied == len(content_out)
    assert len(content_out) == len(content_in)
    assert hash(content_in) == hash(content_out)


def test_small_file_with_offset_overflow(create_files):
    (file_in, file_out) = create_files

    # create small file
    file_in = tempfile.TemporaryFile()
    file_in.write(b'foo bar')
    file_in.seek(0)
    offset = 4096

    with pytest.raises(OverflowError):
        splice(file_in.fileno(), file_out.fileno(), offset=offset)


def test_empty_file(create_files):
    (file_in, file_out) = create_files

    # empty file
    file_in = tempfile.TemporaryFile()
    file_in.write(b'')
    file_in.seek(0)
    content_in = file_in.read()

    bytes_copied = splice(file_in.fileno(), file_out.fileno())
    content_out = file_out.read()

    assert bytes_copied == 0
    assert len(content_in) == 0
    assert bytes_copied == len(content_in)
    assert bytes_copied == len(content_out)
    assert len(content_in) == len(content_out)
    assert hash(content_in) == hash(content_out)


def test_large_file(create_files):
    (file_in, file_out) = create_files

    # create a large file
    file_in = tempfile.SpooledTemporaryFile()
    file_in.write(SAMPLE_DATA * 1)  # * 1024 when automating tests (~1GB)
    file_in.seek(0)
    content_in = file_in.read()

    bytes_copied = splice(file_in.fileno(), file_out.fileno(),
                          nbytes=len(content_in))

    content_out = file_out.read()

    assert bytes_copied == len(content_in)
    assert bytes_copied == len(content_out)
    assert len(content_in) == len(content_out)
    assert hash(content_in) == hash(content_out)


def test_copy_from_certain_offset(create_files):
    (file_in, file_out) = create_files
    content_in = file_in.read()

    offset = 1024
    bytes_copied = splice(file_in.fileno(), file_out.fileno(),
                          offset=offset)

    content_out = file_out.read()

    assert bytes_copied == len(content_out)
    assert bytes_copied == len(content_in[offset:])
    assert len(content_in[offset:]) == len(content_out)
    assert hash(content_in[offset:]) == hash(content_out)


def test_copy_certain_bytes_copied(create_files):
    (file_in, file_out) = create_files
    content_in = file_in.read()

    bytes_to_copy = 2048
    bytes_copied = splice(file_in.fileno(), file_out.fileno(),
                          nbytes=bytes_to_copy)

    content_out = file_out.read()

    assert bytes_copied == bytes_to_copy
    assert bytes_copied == len(content_out)
    assert bytes_to_copy == len(content_out)
    assert len(content_in[:bytes_to_copy]) == len(content_out)
    assert hash(content_in[:bytes_to_copy]) == hash(content_out)


def test_offset_overflow(create_files):
    (file_in, file_out) = create_files
    content_in = file_in.read()

    offset = len(content_in) + 1

    with pytest.raises(OverflowError):
        splice(file_in.fileno(), file_out.fileno(), offset=offset)


def test_len_overflow(create_files):
    (file_in, file_out) = create_files
    content_in = file_in.read()

    with pytest.raises(OverflowError):
        splice(file_in.fileno(), file_out.fileno(),
               nbytes=len(content_in)+1)


def test_invalid_argument_types(create_files):
    (file_in, file_out) = create_files

    with pytest.raises(TypeError):
        splice('test', file_out.fileno(), 0, 0)

    with pytest.raises(TypeError):
        splice(file_in.fileno(), 'test', 0, 0)


def test_incomplete_arguments(create_files):
    (file_in, file_out) = create_files

    with pytest.raises(TypeError):
        splice(file_out.fileno(), offset=0)

    with pytest.raises(TypeError):
        splice(file_in.fileno(), offset=0)


def test_invalid_file_descriptors(create_files):
    (file_in, file_out) = create_files
    content_in = file_in.read()

    with pytest.raises(ValueError):
        splice(999, file_out.fileno(), 0, len(content_in))

    with pytest.raises(ValueError):
        splice(file_in.fileno(), 999, 0, len(content_in))
