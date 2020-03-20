import curses
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
        self._screen.move(self._cursor_pos.y, self._cursor_pos.x)

        eol = '\n' if end_line else ''
        chrono_style = self._get_crono_style(chrono_timer)

        self._screen.addstr(' [{}] '.format(chrono_timer.get_str_dt_start()), curses.A_BOLD)
        self._screen.addstr('{}'.format(chrono_timer.get_str_current_crono()),
                            curses.color_pair(chrono_style))

        if chrono_timer.name:
            self._screen.addstr(' - {}'.format(chrono_timer.name))

        self._screen.addstr('{}'.format(eol))
        self._screen.refresh()

        if eol:
            self._cursor_pos.y += 1

    def _init_colors(self):
        curses.start_color()
        curses.init_pair(self._COLOR_BG_CYAN, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(self._COLOR_BG_GREEN, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(self._COLOR_BG_YELLOW, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(self._COLOR_BG_RED, curses.COLOR_WHITE, curses.COLOR_RED)

    def _init_screen(self, screen):
        self._screen = screen

    def _get_crono_style(self, chrono_timer: ChronoTimer):
        style = self._COLOR_BG_CYAN
        if chrono_timer.is_stopped:
            style = self._COLOR_BG_GREEN
        elif chrono_timer.is_paused:
            style = self._COLOR_BG_RED
            
        return style


class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y