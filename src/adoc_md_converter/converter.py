MAX_NUMBER_OF_NESTING = 10


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def is_blockquote(line):
    for char in ["=", "*"]:
        if line.count(char) == 4 and len(line.lstrip(char)) == 0:
            return True
    return False


class AdocMdConverter:
    def __init__(self, adoc):
        self.adoc = adoc
        self.markdown = ""
        self.number_in_line = {}
        self.clear_numbered_list()
        self.ordered_list_line = False

        self.is_code_block = False
        self.is_code_block_open = False

        self.is_blockquote = False
        self.number_of_blockquote_indent = 0
        self.set_of_used_indents = set()
        self.is_code_in_block_quote = False

    def clear_numbered_list(self):
        self.number_in_line = {i: 0 for i in range(MAX_NUMBER_OF_NESTING)}

    def convert(self):
        for line in self.adoc.adoc.split('\n'):

            if is_blockquote(line) or self.is_blockquote:  # todo more type of blocks
                self.parse_blockquote(line)

            elif line.startswith("="):
                self.parse_headings(line)

            elif line.startswith("****") and len(line) < 5:  # side block todo
                pass

            elif line.lstrip().startswith("*"):
                self.parse_list(line, "*")

            elif line.startswith("."):  # ordered list or title
                if line.startswith(".") and line[1].isalnum():  # title
                    pass
                # elif:   # inline anchor title

                else:  # ordered list
                    self.ordered_list_line = True
                    self.parse_ordered_list(line, ".")

            # code block parsing
            elif line.startswith("[source") or self.is_code_block:
                if self.parse_code_block(line):
                    continue

            elif line.startswith("----"):  # listing block todo
                pass

            else:
                self.parse_text(line)

            # clear ordered list - does not work in every situation
            if self.ordered_list_line and not line.startswith("."):
                self.clear_numbered_list()

    def parse_headings(self, line):
        newline = line.replace("=", "#")
        self.markdown += newline + "\n"

    def parse_list(self, line: str, character: str):
        for i in range(MAX_NUMBER_OF_NESTING):
            if line.startswith((i + 1) * character + " "):
                self.markdown += i * 4 * " " + character + remove_prefix(line, (i + 1) * character) + "\n"

    def parse_ordered_list(self, line: str, character: str):
        for i in range(MAX_NUMBER_OF_NESTING):
            if line.startswith((i + 1) * character + " "):
                self.markdown += i * 4 * " " + str(self.number_in_line[i] + 1) + "." + remove_prefix(line, (
                        i + 1) * character) + "\n"
                self.number_in_line[i] += 1

    def parse_links(self, line):
        # todo link with label and relative links
        pass

    def parse_cross_reference(self):
        pass

    def parse_image(self, line):  # could be in text
        pass

    def parse_blockquote(self, line):  # todo resolve comments in blockquote
        print("blockquote")
        if line.startswith("====") or line.startswith("****"):
            if line[0] not in self.set_of_used_indents:
                self.is_blockquote = True
                print(f"Adding {line[0]}")
                self.number_of_blockquote_indent += 1
                self.set_of_used_indents.add(line[0])
            else:
                print(f"Removing {line[0]}")
                self.set_of_used_indents.remove(line[0])
                self.number_of_blockquote_indent -= 1
                self.markdown += ">" * self.number_of_blockquote_indent + "\n"
        elif (line.startswith("....") or line.startswith("----")) and not self.is_code_in_block_quote:
            self.markdown += ">" * self.number_of_blockquote_indent + "\n"
            self.is_code_in_block_quote = True
        elif (line.startswith("....") or line.startswith("----")) and self.is_code_in_block_quote:
            self.is_code_in_block_quote = False
            self.markdown += ">" * self.number_of_blockquote_indent + "\n"
        elif self.is_code_in_block_quote:
            self.markdown += ">" * self.number_of_blockquote_indent + 5 * " " + line + "\n"
        else:
            self.markdown += ">" * self.number_of_blockquote_indent + " " + line + "\n"

        if self.number_of_blockquote_indent == 0:
            self.is_blockquote = False
            self.markdown += "\n"

    def parse_literal_monospace(self, line):  # todo in text
        pass

    def parse_table(self, line):
        pass

    def parse_literal_block(self, line):
        """
        In asciidoc indented by one or more spaces
        or Delimited as:
        ....
        somthing
        ....

        :param line:
        :return:
        """
        pass

    def parse_code_block(self, line):
        """
        In adoc represented as:
        [source,java]
        ----
        code
        ----

        In Md represented as:
        ```java
        code
        ```

        :param line:
        :return:
        """
        self.is_code_block = True
        if line.startswith("----") and not self.is_code_block_open:
            self.is_code_block_open = True
            return True
        elif line.startswith("----") and self.is_code_block_open:
            self.is_code_block_open = False
            self.is_code_block = False
            self.markdown += "```\n"
            return True
        if line.startswith("[source"):
            self.markdown += "```" + remove_prefix(line, "[source,", ).rstrip("]") + "\n"
        else:
            self.markdown += line + "\n"

    def parse_thematic_break(self, line):
        pass

    def parse_diagrams_kroki(self, line):
        """
        Adoc:
        [plantuml]
        ....
        Bob->Alice : hello
        Alice -> Bob : hi
        ....

        Md:
        ```plantuml
        Bob -> Alice : hello
        Alice -> Bob : hi
        ```

        :param line:
        :return:
        """
        pass

    def parse_uri_reference(self, line):
        pass

    def parse_text(self, line):
        pass
