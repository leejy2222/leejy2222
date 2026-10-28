from dataclasses import dataclass

DAY_NAMES = {"MON": "월", "TUE": "화", "WED": "수", "THU": "목", "FRI": "금"}


def to_minutes(text):
    """"10:30" 같은 시각을 0시부터 지난 분(630)으로 바꾼다."""
    hour, minute = text.split(":")
    return int(hour) * 60 + int(minute)


def to_text(minutes):
    """630 같은 분을 "10:30" 문자열로 바꾼다."""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


@dataclass
class Slot:
    """수업 시간 한 칸 (요일, 시작, 끝). 시간은 분 단위로 저장한다."""
    day: str
    start: int
    end: int

    def __str__(self):
        return f"{DAY_NAMES[self.day]} {to_text(self.start)}~{to_text(self.end)}"


@dataclass
class Course:
    """강의 하나. 일주일에 여러 번 있는 수업은 slots에 모두 들어간다."""
    code: str
    name: str
    credits: int
    required: bool
    slots: list


def make_course(code, name, credits, required, *times):
    """times는 ("MON", "10:30", "12:00") 형태의 튜플들."""
    slots = [Slot(day, to_minutes(start), to_minutes(end)) for day, start, end in times]
    return Course(code, name, credits, required, slots)


# ---------------- 충돌 판단 ----------------

def overlaps(a, b):
    """같은 요일이고 시간이 겹치면 True. (12:00에 끝나고 12:00에 시작하면 안 겹침)"""
    return a.day == b.day and a.start < b.end and b.start < a.end


def conflicts(c1, c2):
    """두 강의의 수업 시간 중 하나라도 겹치면 True."""
    for s1 in c1.slots:
        for s2 in c2.slots:
            if overlaps(s1, s2):
                return True
    return False


# ---------------- 조합 찾기 (백트래킹) ----------------

def find_timetables(required, optional, max_credits, limit=200):
    """필수 과목은 모두 넣고, 선택 과목 중 충돌 없이 넣을 수 있는 조합을 모두 찾는다.

    선택 과목마다 '넣는다 / 안 넣는다' 두 갈래로 탐색하고,
    충돌하거나 최대 학점을 넘는 갈래는 더 내려가지 않는다(가지치기).
    """
    results = []

    def backtrack(i, chosen, credits):
        if len(results) >= limit:
            return
        if i == len(optional):
            results.append(list(chosen))
            return

        course = optional[i]

        # 1) 이 강의를 넣는 경우: 학점이 남고 이미 고른 강의와 안 겹칠 때만
        if credits + course.credits <= max_credits and \
                not any(conflicts(course, c) for c in chosen):
            chosen.append(course)
            backtrack(i + 1, chosen, credits + course.credits)
            chosen.pop()

        # 2) 이 강의를 넣지 않는 경우
        backtrack(i + 1, chosen, credits)

    backtrack(0, list(required), sum(c.credits for c in required))
    return results


# ---------------- 예시 데이터로 실행 ----------------

SAMPLE_COURSES = [
    make_course("CSE2010", "자료구조", 3, True, ("MON", "10:30", "12:00"), ("WED", "10:30", "12:00")),
    make_course("MTH2005", "이산수학", 3, True, ("MON", "09:00", "10:30"), ("WED", "09:00", "10:30")),
    make_course("CSE2030", "오픈소스소프트웨어", 3, False, ("TUE", "13:00", "14:30"), ("THU", "13:00", "14:30")),
    make_course("CSE2040", "컴퓨터구조", 3, False, ("TUE", "13:30", "15:00"), ("THU", "13:30", "15:00")),
    make_course("CSE2050", "데이터베이스", 3, False, ("TUE", "10:30", "12:00"), ("THU", "10:30", "12:00")),
    make_course("GEN1010", "대학영어", 2, False, ("FRI", "09:00", "11:00")),
]


def main():
    max_credits = 12
    required = [c for c in SAMPLE_COURSES if c.required]
    optional = [c for c in SAMPLE_COURSES if not c.required]

    print("=== 강의 목록 ===")
    for c in SAMPLE_COURSES:
        kind = "필수" if c.required else "선택"
        times = ", ".join(str(s) for s in c.slots)
        print(f"[{kind}] {c.name} ({c.credits}학점) - {times}")

    print("\n=== 시간이 겹치는 강의 ===")
    for i in range(len(SAMPLE_COURSES)):
        for j in range(i + 1, len(SAMPLE_COURSES)):
            a, b = SAMPLE_COURSES[i], SAMPLE_COURSES[j]
            if conflicts(a, b):
                print(f"{a.name} <-> {b.name}")

    results = find_timetables(required, optional, max_credits)
    results.sort(key=lambda combo: sum(c.credits for c in combo), reverse=True)

    print(f"\n=== 가능한 시간표 {len(results)}개 (최대 {max_credits}학점) ===")
    for n, combo in enumerate(results, start=1):
        total = sum(c.credits for c in combo)
        names = ", ".join(c.name for c in combo)
        print(f"{n}. [{total}학점] {names}")


if __name__ == "__main__":
    main()
