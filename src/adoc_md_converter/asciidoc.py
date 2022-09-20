
def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


class Adoc:
    def __init__(self, path_to_adocs, filename):
        self.path_to_adocs = path_to_adocs
        self.filename = filename
        self.path_to_file = self.path_to_adocs + self.filename
        self.adoc = self.load_adoc()

    def __repr__(self):
        return self.adoc

    def __str__(self):
        return self.adoc

    def load_adoc(self):
        with open(self.path_to_file) as f:
            content = f.readlines()

        whole_adoc = ""

        for line in content:
            if line.startswith("include::"):
                include_filename = remove_prefix(line, "include::").rstrip("[]\n")
                include_line = self.load_includes(include_filename)
                whole_adoc += include_line
                continue
            whole_adoc += line

        return whole_adoc

    def load_includes(self, include_filename):
        include_adoc = Adoc(self.path_to_adocs, include_filename)
        return str(include_adoc)

