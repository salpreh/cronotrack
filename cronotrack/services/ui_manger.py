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

        try:
            while True:
                self._render_stopped_chronos()
                self._render_current_chronos()
                self._ui_worker.show_help_bar()
                self._handle_keystrokes(screen)
        except KeyboardInterrupt:
            pass

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

    def _handle_keystrokes(self, screen: curses.initscr()):
        try:
            key = screen.getkey()
            self._ui_worker.write_keystroke(key+' ')
            
            if key == 'q':
                self._handle_quit()
            elif key == 'p':
                self._handle_pause()
            elif key == 'n':
                self._handle_new_chrono()

        except curses.error:
            pass

    def _handle_pause(self):
        if len(self.chrono_list) == 0:
            return

        last_chrono = self.chrono_list[-1]
        if last_chrono.is_stopped:
            return

        if last_chrono.is_paused:
            last_chrono.start()
        else:
            last_chrono.pause()

    def _handle_stop(self):
        if len(self.chrono_list) == 0:
            return

        last_chrono = self.chrono_list[-1]
        if last_chrono.is_stopped:
            return

        # Add name to previous crono
        name_input = self._ui_worker.show_text_input(placeholder="Name: ")
        last_chrono.name = name_input

        last_chrono.stop()

    def _handle_new_chrono(self):
        self._handle_stop()

        new_chrono = ChronoTimer()
        new_chrono.start()
        self.chrono_list.append(new_chrono)

    def _handle_quit(self):
        self._handle_stop()
        raise KeyboardInterrupt('Stopped')

    def _init(self, screen: curses.initscr()):
        if not self._is_init:
            curses.curs_set(0)
            curses.noecho()
            screen.nodelay(1)

            self._ui_worker = UIWorker(screen)
            self._is_init = True