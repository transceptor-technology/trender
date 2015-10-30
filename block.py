from .block_text import BlockText
from .block_if import BlockIf
from .block_for import BlockFor
from .block_macro import BlockMacro
from .block_block import BlockBlock
from .block_paste import BlockPaste
from .block_extend import BlockExtend
from .exceptions import UnexpectedBlockError
from .exceptions import UnexpectedEOFError
from .constants import (
    LINE_IF,
    LINE_ELIF,
    LINE_FOR,
    LINE_MACRO,
    LINE_BLOCK,
    LINE_ELSE,
    LINE_TEXT,
    LINE_END,
    LINE_PASTE,
    LINE_COMMENT,
    LINE_INCLUDE,
    LINE_EXTEND,
    EOF_TEXT
)


class Block:

    def __init__(self, lines, allowed):
        self._blocks = []
        self._compile(lines, allowed)

    def render(self, namespace):
        return '\n'.join([text for text in [block.render(namespace) for block in self._blocks] if text is not None])

    def _compile(self, lines, allowed):
        self._text = []
        while lines.next is not None:
            if not allowed & lines.current_type:
                raise UnexpectedBlockError('Unexpected block at: {}, {}'.format(lines.pos, lines.current))

            if lines.current_type == LINE_COMMENT:
                continue

            if lines.current_type == LINE_IF:
                self._reset_plain()
                self._blocks.append(BlockIf(lines))
                continue

            if lines.current_type == LINE_FOR:
                self._reset_plain()
                self._blocks.append(BlockFor(lines))
                continue

            if lines.current_type == LINE_MACRO:
                self._reset_plain()
                self._blocks.append(BlockMacro(lines))
                continue

            if lines.current_type == LINE_BLOCK:
                self._reset_plain()
                self._blocks.append(BlockBlock(lines))
                continue

            if lines.current_type == LINE_PASTE:
                self._reset_plain()
                self._blocks.append(BlockPaste(lines))
                continue

            if lines.current_type == LINE_INCLUDE:
                lines.include()
                continue

            if lines.current_type == LINE_EXTEND:
                self._reset_plain()
                self._blocks.append(BlockExtend(lines))
                continue

            if lines.current_type == LINE_END or lines.current_type == LINE_ELSE or lines.current_type == LINE_ELIF:
                break

            if lines.current_type == LINE_TEXT:
                self._text.append(lines.current)
                continue

            raise RuntimeError('Damm, we should not get here. Current line:', lines.current)
        else:
            if not allowed & EOF_TEXT:
                raise UnexpectedEOFError('Unexpected end of file, missing #end')
        self._reset_plain()

    def _reset_plain(self):
        if self._text:
            self._blocks.append(BlockText('\n'.join(self._text)))
        self._text.clear()
