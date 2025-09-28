

#File class def - 

    #name 
    # size 


# files = {} ? 

# UPLOAD(self, name, size):
    # check if exists
    # if does: 
    # raise RuntimeError 

    # if doesnt: 
    # add File(name, size) to files{}

# GET(self, name):
    # check if doesnt exist: 
        # return None

    # if in files:
        # return files[name].size

# COPY(self, source, dest):
    # if source doesnt exist: 
        # runtime error 
    # if source exists:
        #src= files[source]
        # files[dest] = File(src.name, src.size)
    # if dest exists: 
        # overwrite it (no code)

## Level 2 

# SEARCH(self, prefix):
# pfx = []
# get a list of prefix xisting files - 
    # loop inside files - for name, file in files.items():
        # if name.startswith(prefix):
           # pfx.append(name, file.size)  #in this case, name is a File object 
# sort them by size desc and name asc 
    # srt = sorted(pfx, key = lamda x: (-x[1], x[0]))
# return 10
    # return srt[:10]

# level 3
#File class def v2 - 

    #name 
    # uploaded_at
    # size 
    # ttl

    # is_alive(self, timestamp)
        # if files[name].uploaded_at+ttl > timestamp
        #   return True
        # elif ttl = None: 
            # return True
        # else:     
        #   return False 

# UPLOAD_AT(self, name, timestamp, size, ttl= None):
    # check if exists in files and files[name].is_alive(timestamp): 
    # raise RuntimeError 

    # else: 
    # add File(name, timestamp, size, ttl) to files{}

# GET_AT(self, name, timestamp):
    #check if exists in files and files[name].is_alive(timestamp):
    #  return files[name].size
    #else: 
    #   return None

# COPY_AT(self, source, dest, timestamp)
#   check if source exists in files and files[source].is_alive(timestamp):
    #src = files[source] 
    # if src.ttl is None: 
        # ttl_new = None
    # else: 
    #   ttl_new = (src.uploaded_at + src.ttl) - timestamp
#   # files[dest] = Files(dest, timestamp, src.size, ttl_new)

    #else: 
        #raise RuntimeError("src doesnt exist")


# SEARCH_AT(self, prefix, timestamp):
# pfx = []
# get a list of prefix xisting files - 
    # loop inside files - for name, file in files.items():
        # if file.is_alive(timestamp): 
            # if name.startswith(prefix):
            # pfx.append(name, file.size)  #in this case, name is a File object 
# sort them by size desc and name asc 
    # srt = sorted(pfx, key = lamda x: (-x[1], x[0]))
# return 10
    # return srt[:10]


# level 4
# 1. latest_alive
# 2. update file to be a list of vrsions 
# 3. fix issues with other functions, to make sure they use the latest alive version 
# 4. create rollback code which iterates and rolls back the files - 
    # deletes files that are too new 
    # reverts versions of other files, incl deleted ones (?)


# notes - 
 # if file doesnt exist, need to make an empty lsit 
 # if file does exist, need to append to list 

 # file alive - add helper function latest_alive 

#File class def v3 - 

    #name 
    # uploaded_at
    # size 
    # ttl

    # is_alive(self, timestamp)
        # if files[name].uploaded_at+ttl > timestamp
        #   return True
        # elif ttl = None: 
            # return True
        # else:     
        #   return False 


# File service: 
    # latest_alive(self, name, timestamp):
        # if name not in files: 
            #return None 
        # for ver in reversed(files[name]):
            # if ver.is_alive(timestamp):
        #       return ver  
        # return None 


    # UPLOAD_AT(self, name, timestamp, size, ttl= None):
        # if self.latest_alive(name, timestamp) is not None: 
            # raise RuntimeError 
        # if name not in files
            # files[name] = [] # create the list 
        # no alive file
        # files[name].append(File(name, timestamp, size, ttl))
        

    # GET_AT(self, name, timestamp):
        # check if file of this name exists and is alive 
        # latest = self.latest_alive(name, timestamp)
        # if latest is not None:
            # return latest.size  # return its size   
        # else:
            # return none 

    # COPY_AT(self, source, dest, timestamp)
        #src_latest = self.latest_alive(source, timestamp)
    #   if src_latest is not None:  # check if source exists and has a live version
        # if src_latest.ttl is None: 
            # ttl_new = None
        # else: 
        #   ttl_new = (src_latest.uploaded_at + src_latest.ttl) - timestamp
        
        # create dest list if doesnt exist
    #   if dest not in files:
            # files[dest] = []
    #   # self.files[dest].append(File(dest, timestamp, src_latest.size, ttl_new))
    #   else: 
            #raise RuntimeError("src doesnt exist")


    # SEARCH_AT(self, prefix, timestamp):
    # add the latest_alive
    # pfx = []
    # get a list of prefix string files - 
        #  for name, file in files.items():
            # latest = latest_alive(name, timestamp)
            # if latest is not None: # alive 
                # if name.startswith(prefix):
                # pfx.append(name, latest.size)  #in this case, latest is a File object 
    # sort them by size desc and name asc 
        # srt = sorted(pfx, key = lamda x: (-x[1], x[0]))
    # return 10
        # return srt[:10]

    # ROLLBACK(timestamp)
        # for name, file in files.items() # iterat
            # for ver in files[name]
                # kept = []
                # if ver.uploaded_at < timestamp:
                #   kept.append(ver)
            # files[name] = kept
            # if kept is empty: 
            #   delete files[name]
            

        
