from datetime import datetime
import time


class ChronoTimer():
    """
    Class to manage a chronometer execution
    """
    DATETIME_FMT = '%Y-%m-%d %H:%M:%S'
    TIME_FMT = '%H:%M:%S'

    def __init__(self):
        self.name = ''
        self.dt_start = None
        self.dt_end = None
        self.ts_start = []
        self.ts_end = []

        self._ts_current = 0
        self._last_ts_start = None
        self._stopped = False

    def __eq__(self, other):
        self_val = self._get_compare_val(self)
        other_val = self._get_compare_val(other)

        return self_val == other_val

    def start(self):
        if not self.dt_start:
            self.dt_start = datetime.now()

        ts_start = time.perf_counter()

        self.ts_start.append(ts_start)
        self._update_current_ts(ts_start=ts_start)

    def stop(self):
        self.dt_end = datetime.now()
        self._stopped = True
        if len(self.ts_end) < len(self.ts_start):
            ts_end = time.perf_counter()
            self.ts_end.append(ts_end)
            self._update_current_ts(ts_end=ts_end)

    def pause(self):
        if len(self.ts_end) == len(self.ts_start):
            raise ValueError('Timer already paused or stopped')

        ts_end = time.perf_counter()
        self.ts_end.append(ts_end)
        self._update_current_ts(ts_end=ts_end)

    def get_current_crono(self):
        if self._last_ts_start:
            return self._ts_current + time.perf_counter() - self._last_ts_start

        return self._ts_current

    def get_str_dt_start(self):
        if not self.dt_start:
            return ''

        return datetime.strftime(self.dt_start, ChronoTimer.DATETIME_FMT)

    def get_str_dt_end(self):
        if not self.dt_end:
            return ''

        return datetime.strftime(self.dt_end, ChronoTimer.DATETIME_FMT)

    def get_str_current_crono(self):
        return time.strftime(ChronoTimer.TIME_FMT, time.gmtime(self.get_current_crono()))

    @property
    def is_stopped(self):
        return self._stopped

    @property
    def is_paused(self):
        return len(self.ts_end) == len(self.ts_start)

    def _update_current_ts(self, ts_end=None, ts_start=None):

        if ts_start and not self._last_ts_start:
            self._last_ts_start = ts_start
        elif ts_end:
            self._ts_current += ts_end - self._last_ts_start
            self._last_ts_start = None
        else:
            raise ValueError('Start time incoherece when updating crono')

    def _refresh_current_ts(self):
        self._ts_current = 0
        index = 0
        for index, (ts_end, ts_start) in zip(self.ts_end, self.ts_start):
            self._ts_current += ts_end + ts_start

        if len(self.ts_end) < index + 1:
            self._ts_current += self.ts_end[index+1] - time.perf_counter()

    def _get_compare_val(self, instance: 'ChronoTimer'):
        val = ''
        if instance._dt_start:
            val += instance.get_str_dt_start

        if instance._dt_end:
            val += ' {}'.format(instance.get_str_dt_end)

        if instance.name:
            val += ' {}'.format(instance.name)

        return val