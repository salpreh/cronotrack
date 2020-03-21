from typing import List
from curses import wrapper, error

from cronotrack.services.ui_manger import UIManager
from cronotrack.services.chrono_timer import ChronoTimer


class App(object):
    def run(self):
        chrono_list = []
        ui_manager = UIManager(chrono_list)

        ct = ChronoTimer()
        ct.start()
        chrono_list.append(ct)

        try:
            wrapper(ui_manager.run)
        except error as e:
            print("Application finished with unexpected error: \n> > {}\n".format(str(e)))

        self._print_summary(chrono_list)

    def _print_summary(self, chrono_list: List[ChronoTimer]):
        print("\n{:^54s}".format('SUMMARY'))
        print("{}".format('-'*54))
        for chrono in chrono_list:
            l = '[{:19s}] - [{:19s}] {}'.format(chrono.get_str_dt_start(),
                                                chrono.get_str_dt_end(),
                                                chrono.get_str_current_crono())
            if chrono.name:
                l += ' | {}'.format(chrono.name)

            print(l)

        print()
