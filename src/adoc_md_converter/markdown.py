import os


class Markdown:
    def __init__(self, output_dir, name):
        self.output_dir = output_dir
        self.name = name
        self.markdown = ""
        self.create_dir_if_not_exists()

    def __repr__(self):
        return self.markdown

    def __str__(self):
        return self.markdown

    def create_dir_if_not_exists(self):
        if not os.path.isdir(self.output_dir):
            print("CREATING DIR")
            os.mkdir(self.output_dir)
        else:
            print("not creating")
