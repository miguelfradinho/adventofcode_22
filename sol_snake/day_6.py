def find_marker_after(stream : str, n_chars : int):
    stream_size = len(stream)
    for i in range(stream_size-n_chars):
        last_n: str = stream[i:i + n_chars]
        unique_chars = set(last_n)
        # we found n unique
        if len(unique_chars) == n_chars:
            return i + n_chars

def day_6(file_obj):
    data_stream = None
    with file_obj as f:
        data_stream = f.read().strip()
    stream_size = len(data_stream)
    MARKER_SIZE = 4
    MESSAGE_SIZE = 14

    return find_marker_after(data_stream, MARKER_SIZE),  find_marker_after(data_stream, MESSAGE_SIZE)