def day_6(file_obj):
    data_stream = None
    with file_obj as f:
        data_stream = f.read().strip()
    stream_size = len(data_stream)
    MARKER_SIZE = 4

    for i in range(stream_size-MARKER_SIZE):
        last_4: str = data_stream[i:i+MARKER_SIZE]
        unique_chars = set(last_4)
        # we found 4 unique
        if len(unique_chars) == MARKER_SIZE:
            return i+MARKER_SIZE
    return -1