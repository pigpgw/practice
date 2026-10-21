"""문제 10. 디버깅: 파일 핸들 누수 (난이도 중상)


## 핵심

**파일을 반드시 닫는 것**입니다. `with` 없이 두면 핸들이 새요.

이 문제도 **고치는 문제**다. 실제 시험에서 나온 적 있는 유형이라서,
버그 있는 코드를 읽고 원인을 찾아 고치는 연습을 한다.

장비 로그가 여러 파일로 나뉘어 있는 상황을 만들고, 목록에 있는 로그를 하나씩 읽어
라인 수를 합산하는 프로그램을 만들었다. 한 번 돌릴 때는 결과가 맞아 보이는데,
같은 프로그램이 반복해서 돌리면 자꾸 에러가 난다.

확인할 것.

1. 프로그램을 끝까지 돌린 뒤 **열려 있는 파일이 남아 있나?**
2. 파일이 없는 경우는 어떻게 처리하고 있나?

확인하는 방법 (macOS/Linux). 같은 프로세스 안에서 실행 전후를 비교해야 한다.

```python
import os, importlib.util

spec = importlib.util.spec_from_file_location("p17", "problem10.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

print("solve() 전 fd:", len(os.listdir("/dev/fd")))
module.solve()
print("solve() 후 fd:", len(os.listdir("/dev/fd")))
```

고친 뒤에는 두 숫자가 같아야 한다.

지금 이 코드를 그대로 돌리면 출력은 맞아 보이지만, **열려 있는 파일이 남는다.**
`/dev/fd` 개수를 실행 전후로 비교하면 숫자가 늘어난다. (늘어나는 수는 환경마다 다르다)

```text
solve() 전 fd: 4
solve() 후 fd: 7
```

핵심은 **두 숫자가 같아야 한다** 는 거다.

요구 사항은 아래와 같다.

1. `input10_list.txt`에 있는 파일 이름을 읽는다. `#` 주석과 빈 줄은 무시한다.
2. `input10_logs` 폴더에 있는 로그 파일을 읽어 라인 수를 합산한다.
3. 파일이 없으면 오류로 세고 다음 파일로 넘어간다.
4. **모든 파일은 처리가 끝나면 반드시 닫혀 있어야 한다.** 프로그램이 끝났을 때
   열린 파일 핸들이 남아 있지 않게 고치라.
5. `input10_list.txt`를 읽을 때도 같은 규칙을 지켜야 한다.

## 풀이 순서 (⏱ 15분)

1. fd 개수 비교로 누수 확인 — 3분
2. `open()` → `with open()` — 5분
3. 핸들 담아두던 목록 제거 — 4분
4. diff — 3분

> 버그 2개만 찾으면 끝입니다.

## 출력

`output10.txt`에 쓴다.

```text
Files=3
Lines=12
Missing=1
```

## 예시

> 이 예시는 앞부분만 옮긴 것이다. `input10_list.txt` 파일이 더 길어서 출력도 그만큼 더 나온다.

입력 (`input10_list.txt`):

```text
# 읽어야 할 로그 파일 목록 (input10_logs 폴더 기준입니다)
aoi_01.log
aoi_02.log
aoi_03.log
missing_99.log
```

출력 (`output10.txt`):

```text
Files=3
Lines=12
Missing=1
```

## 실행

    python3 problem10.py

입력: input10_list.txt
입력: input10_logs/*.log
출력: output10.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

LIST_PATH = HERE / "input10_list.txt"
LOG_DIR = HERE / "input10_logs"
OUTPUT_PATH = HERE / "output10.txt"

OPEN_HANDLES = []


def read_log(path: Path) -> list[str]:
    """로그 파일을 읽어 라인 목록으로 돌려줍니다."""
    handle = open(path, "r", encoding="utf-8")
    OPEN_HANDLES.append(handle)
    lines = handle.read().splitlines()
    return lines


def read_names(path: Path) -> list[str]:
    """읽어야 할 로그 파일 이름 목록을 읽습니다."""
    names = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        text = raw.strip()
        if not text or text.startswith("#"):
            continue
        names.append(text)
    return names


def solve() -> int:
    """문제 10. 디버깅: 파일 핸들 누수 (난이도 중상)"""
    names = read_names(LIST_PATH)

    files = 0
    total_lines = 0
    missing = 0

    for name in names:
        path = LOG_DIR / name
        try:
            lines = read_log(path)
        except FileNotFoundError:
            missing += 1
            continue
        files += 1
        total_lines += len(lines)

    OUTPUT_PATH.write_text(
        f"Files={files}\nLines={total_lines}\nMissing={missing}\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
