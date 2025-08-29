def markdown_to_blocks(markdown):
    """Input: raw markdown, Output: list of 'block' strings"""
    blocks: list[str] = markdown.split("\n\n")
    final = []
    for block in blocks:
        temp = block.strip()
        if temp:
            final.append(temp)

    return final
