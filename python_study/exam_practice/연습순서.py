"""연습 순서 뽑기 — 문제를 무작위 순서로 섞어서 보여준다.

실제 시험은 6문제가 어떤 순서로 나오는지 알 수 없다. 이 스크립트로 순서를 매번
섞어서 풀어보면 그 느낌에 익숙해진다.

사용:
    python3 연습순서.py              # 7개 전체를 무작위 순서로
    python3 연습순서.py 5           # 실전 모의처럼 5문제만
    python3 연습순서.py --제외 1 3   # 푼 문제를 빼고
    python3 연습순서.py --난이도 상       # 난이도만 골라서
    python3 연습순서.py --시드 7          # 같은 순서를 다시 보려면
"""

import argparse
import datetime
import pathlib
import random
import re

HERE = pathlib.Path(__file__).resolve().parent


def load_problems() -> list[tuple[int, str, str]]:
    """(번호, 난이도, 제목) 목록을 읽어옵니다."""
    problems = []
    for path in sorted(HERE.glob("problem*.py")):
        text = path.read_text(encoding="utf-8")
        head = text.split('"""')[1].strip().splitlines()[0]
        level = re.search(r"\(난이도 ([^)]+)\)", head)
        title = head.split(". ", 1)[1].split("(")[0].strip()
        problems.append((int(path.stem[-2:]), level.group(1) if level else "?", title))
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="연습 순서를 무작위로 섞습니다")
    parser.add_argument("개수", nargs="?", type=int, default=0, help="뽑을 문제 수 (0이면 전부)")
    parser.add_argument("--제외", nargs="*", type=int, default=[], help="뺄 문제 번호")
    parser.add_argument("--난이도", choices=["하", "중", "중상", "상"], help="이 난이도만")
    parser.add_argument("--시드", type=int, default=None, help="난수 시드 (같은 순서 재현)")
    args = parser.parse_args()

    problems = load_problems()
    if args.난이도:
        problems = [p for p in problems if p[1] == args.난이도]
    if args.제외:
        problems = [p for p in problems if p[0] not in args.제외]

    seed = args.시드 if args.시드 is not None else datetime.date.today().toordinal()
    random.seed(seed)

    picked = problems[:]
    random.shuffle(picked)
    if args.개수:
        picked = picked[: args.개수]

    print(f"연습 순서 (시드 {seed}, {len(picked)}문제)")
    print("-" * 52)
    for index, (number, level, title) in enumerate(picked, 1):
        print(f"{index:>2}. {number:02d}번 [{level}] {title}")
    print("-" * 52)
    print("2시간 타이머를 켜고 시작하세요.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
