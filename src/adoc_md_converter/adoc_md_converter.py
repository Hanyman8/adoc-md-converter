from asciidoc import Adoc
from markdown import Markdown
from converter import AdocMdConverter


def main():
    adoc = Adoc("./data/", "short.adoc")
    # md = Markdown("output_dir", "name.md")
    adoc_md_converter = AdocMdConverter(adoc)
    adoc_md_converter.convert()
    print(adoc_md_converter.markdown)


if __name__ == "__main__":
    main()
