import curses, curses.textpad
from collections import namedtuple

from .chrono_timer import ChronoTimer


class UIWorker():
    """
    Class to interact with terminal UI using curses library
    """
    _COLOR_BG_CYAN = 1
    _COLOR_BG_GREEN = 2
    _COLOR_BG_YELLOW = 3
    _COLOR_BG_RED = 4
    _COLOR_BG_WHITE = 5

    def __init__(self, screen: curses.initscr()):
        self._screen = screen
        self._cursor_pos = Position(0, 0)
        self._init_colors()

    @staticmethod
    def get_init_instance():
        ui_worker = UIWorker(None)
        curses.wrapper(ui_worker._init_screen)

        return ui_worker

    def write_chrono_line(self, chrono_timer: ChronoTimer, end_line=False):
        # self._screen.move(self._cursor_pos.y, self._cursor_pos.x)
        pos_x = self._cursor_pos.x
        pos_y = self._cursor_pos.y

        eol = '\n' if end_line else ''
        chrono_style = self._get_crono_style(chrono_timer)

        output = ' [{}] '.format(chrono_timer.get_str_dt_start())
        pos_x, _ = self._write_line(pos_y, pos_x, output, curses.A_BOLD)

        output = '{}'.format(chrono_timer.get_str_current_crono())
        pos_x, _ = self._write_line(pos_y, pos_x, output, chrono_style)

        if chrono_timer.name:
            output = ' - {}'.format(chrono_timer.name)
            pos_x, _ = self._write_line_with_limit(pos_y, pos_x, output)

        self._write_line(pos_y, pos_x, eol)
        self._screen.refresh()

        if end_line:
            self._cursor_pos.y += 1

    def show_help_bar(self, pos_y=-1, pos_x=3):
        if pos_y == -1:
            max_y, max_x = self._screen.getmaxyx()
            pos_y = max_y - 1

        help_str = '|q: quit, p: pause/resume, n: new_chron'
        output = '{}{}'.format(help_str, ' '*(max_x - len(help_str) - pos_x - 1))
        self._screen.addstr(pos_y, pos_x, output, curses.color_pair(self._COLOR_BG_WHITE))

        self._screen.refresh()

    def write_keystroke(self, key: str, pos_y=-1, pos_x=0):
        if pos_y == -1:
            pos_y, _ = self._screen.getmaxyx()

        self._screen.addstr(pos_y-1, pos_x, ':{}'.format(key))
        self._screen.refresh()

    def _write_line(self, pos_y: int, pos_x: int, output: str, style=curses.A_NORMAL) -> (int, int):
        self._screen.addstr(pos_y, pos_x, output, style)

        new_x = pos_x + len(output)
        new_y = pos_y + 1 if output.endswith('\n') else pos_y

        return (new_x, new_y)

    def _write_line_with_limit(self, pos_y: int, pos_x: int, output: str, limit=-1, style=curses.A_NORMAL) -> (int, int):
        """
        Write a string until a limit is reached. If limit is -1 (default) the limit woluld be the current line
        """
        if limit == -1:
            _, max_x = self._screen.getmaxyx()
            limit = max_x - pos_x - 1

        self._screen.addnstr(pos_y, pos_x, output, limit, style)

        new_x = pos_x + min(len(output), limit)
        new_y = pos_y + 1 if output.endswith('\n') else pos_y

        return (new_x, new_y)

    def show_text_input(self, pos_y=-1, pos_x=1, add_frame=True, placeholder="") -> str:
        max_y, max_x = self._screen.getmaxyx()
        if pos_y == -1:
            pos_y = max_y - 3

        if add_frame:
            curses.textpad.rectangle(self._screen,
                                     pos_y - 1, 0,
                                     pos_y + 1, max_x - 1)

        self._screen.addstr(pos_y, pos_x, placeholder)

        txt_win = curses.newwin(1, max_x - len(placeholder),
                                pos_y, pos_x + len(placeholder))

        txt_box = curses.textpad.Textbox(txt_win)
        curses.curs_set(1)
        self._screen.refresh()

        txt_input = txt_box.edit()
        self._clear_lines([pos_y -1, pos_y, pos_y + 1])
        curses.curs_set(0)

        return txt_input

    def _clear_lines(self, lines_indices):
        for line_index in lines_indices:
            self._screen.move(line_index, 0)
            self._screen.clrtoeol()

    def _init_colors(self):
        curses.start_color()
        curses.init_pair(self._COLOR_BG_CYAN, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(self._COLOR_BG_GREEN, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(self._COLOR_BG_YELLOW, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(self._COLOR_BG_RED, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(self._COLOR_BG_WHITE, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def _init_screen(self, screen):
        self._screen = screen

    def _get_crono_style(self, chrono_timer: ChronoTimer):
        style = curses.color_pair(self._COLOR_BG_CYAN)
        if chrono_timer.is_stopped:
            style = curses.color_pair(self._COLOR_BG_GREEN)
        elif chrono_timer.is_paused:
            style = curses.color_pair(self._COLOR_BG_RED) | curses.A_BLINK

        return style


class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y