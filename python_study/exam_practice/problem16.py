"""문제 16. 고객 로그 파싱·상관 이슈 묶기·우선순위 지정 (난이도 상)


## 핵심

**순서 무관한 `키=값` 파싱 + CSV 인용 + 연속 판정**입니다. 세 가지가 얹혀 있습니다.

고객이 보낸 이슈 로그에는 메시지 안에 `;`나 `=`가 들어있는 경우도 있고, 필드 순서도 제각각이다.
FAE가 실제로 제일 많이 처리하는 업무가 이 로그를 읽고 "무엇부터 볼지"를 정하는 일이다.

`input16.txt`의 각 줄은 `Time=...;Site=...;Code=...;Severity=...;Message=...` 형식이다.
필드 순서는 바뀔 수 있고 Message 안에 `;` 또는 `=`가 들어갈 수 있다.
`Message`는 마지막 `;Message=` 이후 전체를 값으로 처리한다.
`#`로 시작하는 줄은 주석이라 건너뛴다.

1. 필수 키 누락, 중복 키, 알 수 없는 Severity(HIGH/MEDIUM/LOW만 유효), 형식 오류 행은
   `output16.csv`에 넣지 않고 오류 수에 포함한다. 오류가 있어도 다른 행은 계속 처리한다.
   오류는 stderr에 `ERROR line N: 이유` 형식으로 출력하고, 화면의 `Errors=n`에 집계한다.
2. Code가 E로 시작하면 HARDWARE, S로 시작하면 SOFTWARE, 그 외는 REVIEW로 분류한다.
   대소문자를 구분한다(소문자 `e`로 시작하면 REVIEW다).
3. Action 은 기본값이 이렇다. HIGH=`ESCALATE`, MEDIUM=`CHECK`, LOW=`MONITOR`.
4. 여기에 **HIGH 반복** 예외가 하나 있다.
   같은 Site 이고 같은 분류(Owner)인 HIGH 레코드가 **연속으로** 나오면,
   두 번째부터는 Action 을 `ESCALATE_REPEAT` 로 바꾼다.
   - Site 이 다르거나, Owner 가 다르면 연속이 끊긴다.
   - HIGH 가 아닌 레코드가 하나라도 끼면 역시 연속이 끊긴다.
   - 오류로 제외된 행은 애초에 출력에 없으니 연속 판정에도 들어가지 않는다.

   예) `Site=2 HARDWARE HIGH` → `ESCALATE`,
       바로 다음 `Site=2 HARDWARE HIGH` → `ESCALATE_REPEAT`,
       그 다음 `Site=2 SOFTWARE MEDIUM` → `CHECK` (Owner 가 달라서 연속 끊김)
5. 출력 헤더는 `Time,Site,Code,Owner,Action,Message`다.
   쉼표가 든 Message도 CSV 형식이 깨지지 않게 쓴다.
   `Message`에 쉼표가 들어가면 `"`로 감싸고, 안에 `"`가 있으면 `""`로 두 번 쓴다.
6. `Site`는 정수로 처리한다.
7. 마지막에 정상 처리 수와 오류 수를 **화면(표준 출력)**에 쓴다.
   `output16.csv`에는 정상 처리한 행만 쓴다.
8. 입력 파일을 열 수 없으면 종료 코드 1이다.

## 풀이 순서 (⏱ 40분)

1. `;Message=` 기준으로 파싱 — 10분
2. 키=값 딕셔너리로 변환 — 10분
3. CSV 인용 처리 — 8분
4. 연속 HIGH 판정 — 8분
5. 출력 — 4분

> 실전 6번 고배점이지만 시간이 부족하면 3번 뒤로 미루세요.

## 출력

`output16.csv`에 쓴다.

화면 출력:

```text
Valid=4
Errors=3
```

## 예시

입력 (`input16.txt`):

```text
# Time;Site;Code;Severity;Message
Time=10:05;Site=2;Code=E101;Severity=HIGH;Message=contact open;pin=3
Time=10:06;Site=2;Code=E102;Severity=HIGH;Message=voltage unstable
Time=10:07;Site=2;Code=S201;Severity=MEDIUM;Message=program timeout
Time=10:10;Site=1;Code=X999;Severity=LOW;Message=unknown=alarm
Time=10:20;Site=2;Code=E103;Severity=URGENT;Message=bad severity
Time=10:25;Code=E104;Severity=HIGH;Message=missing site
Time=10:30;Site=2;Site=3;Code=E105;Severity=LOW;Message=dup key
```

출력 (`output16.csv`):

```text
Time,Site,Code,Owner,Action,Message
10:05,2,E101,HARDWARE,ESCALATE,"contact open;pin=3"
10:06,2,E102,HARDWARE,ESCALATE_REPEAT,voltage unstable
10:07,2,S201,SOFTWARE,CHECK,program timeout
10:10,1,X999,REVIEW,MONITOR,unknown=alarm
```

화면 출력:

```text
Valid=4
Errors=3
```

`10:06`이 `10:05`랑 Site·Owner가 같고 HIGH라서 `ESCALATE_REPEAT`이다.
`10:07`은 Owner가 SOFTWARE로 달라서 연속이 끊기고 `CHECK`가 된다.
마지막 세 줄은 Severity가 틀렸거나, Site 키가 없고, Site 키가 중복된 오류 행이다.

## 실행

    python3 problem16.py

입력: input16.txt
출력: output16.csv
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

INPUT_PATH = HERE / "input16.txt"
OUTPUT_PATH = HERE / "output16.csv"


def solve() -> int:
    """문제 16. 고객 로그 파싱·상관 이슈 묶기·우선순위 지정 (난이도 상)"""
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
