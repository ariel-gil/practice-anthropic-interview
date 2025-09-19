from collections import defaultdict
import typing as tp

class TimeTrackingSystemImpl:
    """
    Implements a time-tracking and payroll system for employees.
    """

    def __init__(self):
        """
        Initializes the data structures for the system.
        - workers_: Stores current info (position, compensation) for each worker.
        - work_time_: A log of all clock-in ('ENTER') and clock-out ('EXIT') events.
        - pending_promotion_: Stores promotions that are scheduled but not yet active.
        - history_: A log of each worker's position and compensation changes over time.
        """
        self.workers_: tp.Dict[str, tp.Tuple[str, int]] = {}
        self.work_time_: tp.DefaultDict[str, tp.List[tp.Tuple[str, int]]] = defaultdict(list)
        self.pending_promotion_: tp.Dict[str, tp.Tuple[str, int, int]] = {}
        self.history_: tp.DefaultDict[str, tp.List[tp.Tuple[int, str, int]]] = defaultdict(list)

    def add_worker(self, worker_id: str, position: str, compensation: int) -> bool:
        """
        Adds a new worker to the system.
        """
        if worker_id in self.workers_:
            return False

        self.workers_[worker_id] = (position, int(compensation))
        # Every worker's history starts at timestamp 0
        self.history_[worker_id].append((0, position, int(compensation)))
        return True

    def register(self, timestamp: int, worker_id: str) -> str:
        """
        Registers a work event (clock-in/out) and activates any pending promotions.
        """
        if worker_id not in self.workers_:
            return "invalid_request"

        is_purely_promo_activation = False
        # Promotions are activated by the first register event at or after their effective time.
        if worker_id in self.pending_promotion_:
            promo_info = self.pending_promotion_[worker_id]
            effective_timestamp = promo_info[2]
            if timestamp >= effective_timestamp:
                new_position, new_compensation = promo_info[0], promo_info[1]
                self.workers_[worker_id] = (new_position, new_compensation)
                
                # FIX 1: The history should record the change at its effective time, not the registration time.
                self.history_[worker_id].append((effective_timestamp, new_position, new_compensation))
                del self.pending_promotion_[worker_id]

                # FIX 2: If registration happens at the exact effective timestamp, it's for activation only.
                if timestamp == effective_timestamp:
                    is_purely_promo_activation = True
        
        if is_purely_promo_activation:
            return "registered"

        # Alternate between 'ENTER' and 'EXIT' events.
        if not self.work_time_[worker_id] or self.work_time_[worker_id][-1][0] == "EXIT":
            self.work_time_[worker_id].append(("ENTER", timestamp))
        else:
            self.work_time_[worker_id].append(("EXIT", timestamp))

        return "registered"

    def _get_intervals(self, worker_id: str) -> tp.List[tp.Tuple[int, int]]:
        """
        Helper method to convert the event log into a list of completed work intervals.
        """
        intervals = []
        events = self.work_time_[worker_id]
        for i in range(0, len(events) - 1, 2):
            start_event, end_event = events[i], events[i+1]
            intervals.append((start_event[1], end_event[1]))
        return intervals

    def get(self, worker_id: str) -> str:
        """
        Calculates the total time worked across all completed sessions for a worker.
        """
        if worker_id not in self.workers_:
            return ""

        intervals = self._get_intervals(worker_id)
        if not intervals:
            return "" # Return empty string if no completed sessions

        total_time = sum(end - start for start, end in intervals)
        return str(total_time)

    def top_n_workers(self, n: int, position: str) -> str:
        """
        Ranks workers in a given position by the time worked in their current role.
        """
        candidates = [
            w_id for w_id, info in self.workers_.items() if info[0] == position
        ]

        def get_time_in_current_position(worker_id: str) -> int:
            work_intervals = self._get_intervals(worker_id)
            # The start of the current position is the timestamp of the last history entry.
            start_of_current_pos = self.history_[worker_id][-1][0]

            total_time = 0
            for start, end in work_intervals:
                # Only consider work intervals that occur after the current position started.
                if end > start_of_current_pos:
                    # Calculate the duration of the work that falls within the current position's timeframe.
                    overlap_start = max(start, start_of_current_pos)
                    total_time += end - overlap_start
            return total_time

        ranking = {
            worker_id: get_time_in_current_position(worker_id) for worker_id in candidates
        }

        # Sort by time (descending), then by worker_id (alphabetical ascending) for tie-breaking.
        sorted_ranking = sorted(ranking.items(), key=lambda item: (-item[1], item[0]))[:n]

        return ", ".join([f"{name}({time})" for name, time in sorted_ranking])

    def promote(self, worker_id: str, new_position: str, new_compensation: int, effective_timestamp: int) -> str:
        """
        Schedules a future promotion for a worker.
        """
        if worker_id not in self.workers_ or worker_id in self.pending_promotion_:
            return "invalid_request"

        self.pending_promotion_[worker_id] = (new_position, new_compensation, effective_timestamp)
        return "success"

    def calc_salary(self, worker_id: str, start_timestamp: int, end_timestamp: int) -> str:
        """
        Calculates a worker's salary over a specific period, accounting for promotions.
        """
        if worker_id not in self.workers_:
            return ""

        work_intervals = self._get_intervals(worker_id)
        if not work_intervals:
            return "0"

        total_compensation = 0

        for work_start, work_end in work_intervals:
            # Find the intersection of the work interval and the requested salary period.
            overlap_start = max(work_start, start_timestamp)
            overlap_end = min(work_end, end_timestamp)

            if overlap_start >= overlap_end:
                continue  # This work session is outside the requested salary period.

            # For this overlapping work period, find the correct compensation rate(s).
            for i in range(len(self.history_[worker_id])):
                hist_ts, _, hist_comp = self.history_[worker_id][i]
                
                # Determine the time range for which this historical compensation rate was valid.
                next_hist_ts = float('inf')
                if i + 1 < len(self.history_[worker_id]):
                    next_hist_ts = self.history_[worker_id][i+1][0]

                # Find the final intersection of the work overlap and the history period.
                final_start = max(overlap_start, hist_ts)
                final_end = min(overlap_end, next_hist_ts)

                if final_start < final_end:
                    duration = final_end - final_start
                    total_compensation += duration * hist_comp
        
        return str(total_compensation)
