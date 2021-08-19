# SINGLE REPONSIBILITY PRINCIPAL
# https://en.wikipedia.org/wiki/Single-responsibility_principle
# Every class should have only one responsibility


# MISTAKE
# ----------------------------------------------------------------------------
# Journal đang có 2 reponsibility
#   1. append/remove entries
#   2. save/load entries
# 1 class chỉ nên chịu trách nhiệm về một nhiệm vụ cụ thể
class Journal:
    def __init__(self):
        self.entries = []
        self.count = 0

    def append(self, text):
        self.entries.append(f"{self.count}: {text}")
        self.count += 1

    def remove(self, pos):
        del self.entries[pos]

    def __str__(self):
        return "\n".join(self.entries)

    # break SRP
    def save(self, filename):
        with open(filename, "w") as f:
            f.write(str(self))
            f.close()

    def load(self, filename):
        with open(filename, 'r') as f:
            return f.read()

    def load_from_web(self, uri):
        import requests
        response = requests.get(uri)
        return response.text


j = Journal()
j.append("I cried today.")
j.append("I ate a bug.")
print(f"Journal entries:\n{j}\n")


# SOLUTION
# ----------------------------------------------------------------------------
class Journal:
    def __init__(self):
        self.entries = []
        self.count = 0

    def append(self, text):
        self.entries.append(f"{self.count}: {text}")
        self.count += 1

    def remove(self, pos):
        del self.entries[pos]


class FileManager:
    @staticmethod
    def save(journal, filename):
        with open(filename, "w") as f:
            f.write(str(journal))
            f.close()

    @staticmethod
    def load(filename):
        with open(filename, 'r') as f:
            print(f.read())


p = FileManager()
file = r"journal.txt"
p.save(j, file)
p.load(file)
