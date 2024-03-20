def markdown_to_blocks(markdown):
    return list(
            map(
                lambda line: line.strip("\n"),
                filter(
                    lambda line: len(line) != 0,
                    markdown.split("\n\n")
                    )
                )
            )