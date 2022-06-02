import headlines_win
import headline_block
import curses


class HeadlineBlockList:
    def __init__(self, data: list[dict]):
        self.headlines = [headline_block.HeadlineBlock(**article) for article in data]
        # Set initial block positions. RTB is the block capacity of the headlines window.
        visible_blocks_range = min(headlines_win.HeadlinesWin.get_block_cap(), len(self.headlines))
        for i in range(visible_blocks_range):
            self.headlines[i].update_lines(
                -i - 1
            )  # HeadlineBlock block_pos inits to -1

    def get_visible_block_idxs(self):
        """Return a list of the indices of all HeadlineBlock objects in visible range"""
        return [
            bi
            for bi in range(len(self.headlines))
            if self.headlines[bi].block_pos in range(headlines_win.HeadlinesWin.get_block_cap())
        ]

    def scroll_blocks(self, incr):
        visible_blocks_idxs = self.get_visible_block_idxs()
        new_range_start = visible_blocks_idxs[0] + incr
        new_range_end = new_range_start + headlines_win.HeadlinesWin.get_block_cap()
        # Reset the zeroth index if incr is 1
        # Reset the last index if incr is -1
        reset_idx = (incr - 1) and -1
        self.headlines[visible_blocks_idxs[reset_idx]].reset_lines()
        for i in range(new_range_start, new_range_end):
            self.headlines[i].update_lines(incr)

    def print_blocks(self, win: curses.window):
        for i in self.get_visible_block_idxs():
            self.headlines[i].print_block(win)

    def get_selected_idx(self) -> int:
        return next(
            (i for i in range(len(self.headlines)) if self.headlines[i].selected), -1
        )

    def get_selected(self) -> headline_block.HeadlineBlock:
        return next(
            (block for block in self.headlines if block.selected), self.headlines[0]
        )

    def toggle_block_selected_status_and_update(self, idx, win: curses.window):
        self.headlines[idx].toggle_selected_status_and_update(win)

    def toggle_selected_block(self, idx):
        self.headlines[idx].toggle_selected_status()

    def scroll_selected_headline(self, incr, win: curses.window):
        selected = self.get_selected()
        selected.scroll_line_horiz(0, incr)
        selected.print_line(0, win)

    def scroll_selected_summary(self, incr, win: curses.window):
        selected = self.get_selected()
        selected.scroll_line_horiz(1, incr)
        selected.print_line(1, win)

    def get_len(self):
        return len(self.headlines)

    def shift_selection_and_update(self, old_idx, new_idx, win: curses.window):
        self.headlines[old_idx].toggle_selected_status_and_update(win)
        self.headlines[old_idx].print_block(win)
        self.headlines[new_idx].toggle_selected_status_and_update(win)