class FileStorageSystemImpl:
    """
    An in-memory implementation of a simplified file storage system.
    """

    def __init__(self):
        """
        Initializes the data structures for the file system.
        - self.files: Stores file paths and their sizes.
        - self.users: Stores user IDs and their remaining storage capacity.
        - self.file_ownership: Maps each file path to its owner's user ID.
        """
        # {file_path: size}
        self.files = {}
        
        # {user_id: remaining_capacity}
        # The 'admin' user has unlimited capacity for the ADD_FILE operation.
        self.users = {"admin": float('inf')}
        
        # {file_path: user_id}
        self.file_ownership = {}

    def add_file(self, file_path: str, file_size: int) -> str:
        """
        Creates a new file owned by the 'admin' user.
        """
        # This is a simplified version of add_file_by_user for the admin.
        # We can reuse the more complex logic.
        result = self.add_file_by_user(file_path, "admin", file_size)
        
        if result == "":
            return "false"
        else:
            return "true"

    def delete_file(self, file_path: str) -> str:
        """
        Deletes a file and restores capacity to its owner.
        """
        if file_path not in self.files:
            return "false"

        size = self.files[file_path]
        owner = self.file_ownership[file_path]

        # Restore the capacity to the user who owned the file.
        if owner in self.users:
            self.users[owner] += size

        # Remove the file from records
        del self.files[file_path]
        del self.file_ownership[file_path]

        return str(size)

    def get_file_size(self, file_path: str) -> str:
        """
        Retrieves the size of a specified file.
        """
        if file_path not in self.files:
            return ""
        
        return str(self.files[file_path])

    def get_n_files_by_prefix(self, prefix: str, count: int) -> str:
        """
        Finds and ranks files matching a given prefix.
        """
        # Filter files that start with the given prefix
        candidates = {
            path: size for path, size in self.files.items() if path.startswith(prefix)
        }

        # Sort the candidates. The key is a tuple:
        # 1. -size: Sorts by size in descending order.
        # 2. path: Sorts by path lexicographically for tie-breaking.
        sorted_items = sorted(candidates.items(), key=lambda item: (-item[1], item[0]))

        # Take the top 'count' results
        top_items = sorted_items[:int(count)]

        # Format the output string
        formatted_results = [f"{path}({size})" for path, size in top_items]
        return ", ".join(formatted_results)

    def add_user(self, user_id: str, capacity: int) -> str:
        """
        Creates a new user with a specified storage capacity.
        """
        if user_id in self.users:
            return "false"
        
        self.users[user_id] = int(capacity)
        return "true"

    def add_file_by_user(self, file_path: str, user_id: str, file_size: int) -> str:
        """
        Adds a file on behalf of a specific user, deducting from their capacity.
        """
        size = int(file_size)

        # Check for failure conditions
        if user_id not in self.users:
            return ""
        if file_path in self.files:
            return ""
        if size > self.users[user_id]:
            return ""

        # If all checks pass, add the file
        self.files[file_path] = size
        self.file_ownership[file_path] = user_id
        self.users[user_id] -= size

        return str(self.users[user_id])

    def merge_users(self, target_user_id: str, source_user_id: str) -> str:
        """
        Merges the source user's files and capacity into the target user.
        """
        # Check for failure conditions
        if target_user_id not in self.users or source_user_id not in self.users:
            return ""
        if target_user_id == source_user_id:
            return ""

        # Transfer remaining capacity
        self.users[target_user_id] += self.users[source_user_id]

        # Re-assign ownership of all source user's files to the target user.
        # Iterate over a copy of the items to allow modification during the loop.
        for path, owner in list(self.file_ownership.items()):
            if owner == source_user_id:
                self.file_ownership[path] = target_user_id
        
        # Delete the source user
        del self.users[source_user_id]

        return str(self.users[target_user_id])
