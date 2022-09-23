MAX_NUMBER_OF_NESTING = 10


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


class AdocMdConverter:
    def __init__(self, adoc):
        self.adoc = adoc
        self.markdown = ""
        self.number_in_line = {}
        self.clear_numbered_list()
        self.ordered_list_line = False

    def clear_numbered_list(self):
        self.number_in_line = {i: 0 for i in range(MAX_NUMBER_OF_NESTING)}

    def convert(self):
        for line in self.adoc.adoc.split('\n'):
            if line.startswith("="):
                # block
                if line.count("=") > 4:
                    print("BLOCK")  # TODO

                # document header
                elif line.count("=") == 1:
                    print("DOCUMENT HEADER")  # TODO

                # heading
                else:
                    self.parse_headings(line)

            elif line.startswith("****") and len(line) < 5:  # side block todo
                pass

            elif line.startswith("----"):  # listing block todo
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
            if line.startswith((i+1)*character + " "):
                self.markdown += i*4 * " " + character + remove_prefix(line, (i+1)*character) + "\n"

    def parse_ordered_list(self, line: str, character: str):
        for i in range(MAX_NUMBER_OF_NESTING):
            if line.startswith((i+1)*character + " "):
                self.markdown += i*4 * " " + str(self.number_in_line[i]+1) + "." + remove_prefix(line, (i+1)*character) + "\n"
                self.number_in_line[i] += 1

    def parse_links(self, line):
        # todo link with label and relative links
        pass

    def parse_cross_reference(self):
        pass

    def parse_image(self, line):
        pass

    def parse_block_quote(self, line):
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
