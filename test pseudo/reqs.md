Level 1 – Basic Functions

FILE_UPLOAD(name, size)

Add new file.

Error if file already exists.

FILE_GET(name)

Return file size, or None if not found.

FILE_COPY(source, dest)

Copy source → dest.

Error if source missing.

Overwrite dest if it already exists.

Level 2 – Data Processing

FILE_SEARCH(prefix)

Find up to 10 files with names starting with prefix.

Order: size descending → then name ascending.

Level 3 – With Timestamps & TTL

FILE_UPLOAD_AT(name, timestamp, size, ttl=None)

Add file at a given time.

TTL = how long file lives (seconds).

No TTL = infinite.

FILE_GET_AT(name, timestamp)

Return size if file exists and is alive at timestamp.

FILE_COPY_AT(source, dest, timestamp)

Copy file version alive at timestamp.

Dest gets new timestamp.

TTL reduced to reflect remaining lifetime.

FILE_SEARCH_AT(prefix, timestamp)

Like Level 2, but only include files alive at timestamp.

Level 4 – Rollback

ROLLBACK(timestamp)

Restore the system to the exact state it had at that time.

Versions uploaded later are discarded.

Files with no valid versions left are removed.

TTLs work automatically (no recalculation needed).