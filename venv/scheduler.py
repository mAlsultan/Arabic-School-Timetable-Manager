# scheduler.py
DAYS = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس"]

def generate_timetable(subject_periods):
    total_periods = sum(subject_periods.values())
    periods_per_day = len(DAYS)
    rows = total_periods // periods_per_day
    if total_periods % periods_per_day != 0:
        rows += 1

    timetable = [["" for _ in DAYS] for _ in range(rows)]

    subject_list = []
    for subj, count in subject_periods.items():
        subject_list.extend([subj] * count)

    idx = 0
    for r in range(rows):
        for c in range(len(DAYS)):
            if idx < len(subject_list):
                timetable[r][c] = subject_list[idx]
                idx += 1
            else:
                timetable[r][c] = ""

    return timetable

