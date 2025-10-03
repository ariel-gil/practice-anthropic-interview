class File: 
    def __init__(self, name: str, size: str = "", uploaded_at: int = 0, ttl: int = None): 
        self.name = name 
        self.size = size
        self.uploaded_at = uploaded_at
        self.ttl = ttl 

    def is_alive(self, curr_time: int):
        if self.ttl is None:
            return True 
        return self.uploaded_at + self.ttl > curr_time


class FileHostingService: 
    def __init__(self): 
        # dictionary of file_name -> list of versions
        self.files = {}  

    def FILE_UPLOAD(self, file_name: str, size: str) -> None:
        if file_name in self.files:
            raise RuntimeError("file exists") 
        else: 
            self.files[file_name] = [File(file_name, size, 0, None)]

    def FILE_GET(self, file_name: str): 
        if file_name not in self.files:
            return None
        else: 
            return self.files[file_name][-1].size

    def FILE_COPY(self, source, dest): 
        if source not in self.files:
            raise RuntimeError("sourcefile doesnt exist")
        else: 
            size = self.files[source][-1].size
            if dest not in self.files:
                self.files[dest] = []
            self.files[dest].append(File(dest, size, 0, None))

    def FILE_SEARCH(self, prefix: str):
        result = []
        for name, versions in self.files.items(): 
            latest = versions[-1]
            if name.startswith(prefix): 
                result.append((name, latest.size))
        sorted_list = sorted(result, key=lambda x: (-x[1], x[0]))
        return sorted_list[:10]

    def FILE_UPLOAD_AT(self, name: str, timestamp: int, size: str, ttl: int = None): 
        if name not in self.files: 
            self.files[name] = [] 
        if self.files[name] and self.files[name][-1].is_alive(timestamp): 
            raise RuntimeError("file exists") 
        else: 
            self.files[name].append(File(name, size, timestamp, ttl))

    def FILE_GET_AT(self, name, timestamp):
        if name in self.files:
            for item in reversed(self.files[name]):
                if item.is_alive(timestamp):
                    return item.size
        return None

    def FILE_COPY_AT(self, source: str, dest: str, timestamp: int): 
        if source not in self.files: 
            raise RuntimeError("source doesnt exist")

        latest_src = None
        for f in reversed(self.files[source]):
            if f.is_alive(timestamp): 
                latest_src = f
                break
        if latest_src is None: 
            raise RuntimeError("source is expired") 

        if latest_src.ttl is None: 
            ttl_new = None 
        else: 
            ttl_new = latest_src.ttl - (timestamp - latest_src.uploaded_at)

        if dest not in self.files: 
            self.files[dest] = [] 
        self.files[dest].append(File(dest, latest_src.size, timestamp, ttl_new)) 

    def FILE_SEARCH_AT(self, prefix: str, timestamp: int): 
        result = [] 
        for name, versions in self.files.items(): 
            for file in reversed(versions):
                if file.is_alive(timestamp): 
                    if name.startswith(prefix): 
                        result.append((name, file.size)) 
                    break  # only need most recent alive version
        sorted_list = sorted(result, key=lambda x: (-x[1], x[0])) 
        return sorted_list[:10]

    def ROLLBACK(self, timestamp: int):
        for name in list(self.files.keys()):
            versions = self.files[name]
            kept = []
            for f in versions:
                if f.uploaded_at <= timestamp:
                    kept.append(f)
            self.files[name] = kept
            if not kept:
                del self.files[name]


svc = FileHostingService()

# Level 1
svc.FILE_UPLOAD("a.txt", "100")
svc.FILE_UPLOAD("b.txt", "200")
print(svc.FILE_GET("a.txt"))         # 100
svc.FILE_COPY("a.txt", "c.txt")
print(svc.FILE_GET("c.txt"))         # 100
print(svc.FILE_SEARCH("a"))          # [('a.txt', '100')]

# Level 2
svc.FILE_UPLOAD("bigfile", "999")
svc.FILE_UPLOAD("alpha", "150")
print(svc.FILE_SEARCH("a"))          # [('alpha', '150'), ('a.txt', '100')]

# Level 3
svc.FILE_UPLOAD_AT("temp", 10, "300", ttl=5)
print(svc.FILE_GET_AT("temp", 12))   # 300
print(svc.FILE_GET_AT("temp", 20))   # None (expired)

svc.FILE_COPY_AT("alpha", "alpha_copy", 15)
print(svc.FILE_GET_AT("alpha_copy", 16))   # 150

# Level 4
svc.FILE_UPLOAD_AT("rollback_me", 50, "777")
print(svc.FILE_GET_AT("rollback_me", 51))  # 777
svc.ROLLBACK(40)
print(svc.FILE_GET_AT("rollback_me", 41))  # None (rolled back)