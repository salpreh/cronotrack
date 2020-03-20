import curses
from typing import List

from .ui_worker import UIWorker
from .chrono_timer import ChronoTimer


class UIManager():
    def __init__(self, chrono_list=None):
        self.chrono_list: List[ChronoTimer] = chrono_list if chrono_list is not None else []

        self._ui_worker: UIWorker = None
        self._current_chr_index: int = 0
        self._last_keystroke = -1
        self._is_init = False

    def run(self, screen):
        self._init(screen)

        self._render_stopped_chronos()
        self._render_current_chronos()

    def _render_stopped_chronos(self):
        """
        Assumption: Stoped chronos always will be at the beginig of the list.
            So when no stopped chrono found the rest should be also not stopped
        """
        if len(self.chrono_list) == 0 or self._current_chr_index == len(self.chrono_list):
            return
        
        last_stopped_index = self._current_chr_index
        for i in range(self._current_chr_index, len(self.chrono_list)):
            chrono = self.chrono_list[i]
            if chrono.is_stopped:
                self._ui_worker.write_chrono_line(chrono, end_line=True)
                last_stopped_index = i + 1

        self._current_chr_index = last_stopped_index

    def _render_current_chronos(self):
        """
        Assumption: There should be at most only one chrono not stopped(currently used).
            If this chrono exists it will be at the end of the list
        """
        if len(self.chrono_list) == 0:
            return

        last_chrono = self.chrono_list[-1]
        if not last_chrono.is_stopped:
            self._ui_worker.write_chrono_line(last_chrono)

    def _init(self, screen):
        if not self._is_init:
            self._ui_worker = UIWorker(screen)
            curses.curs_set(0)