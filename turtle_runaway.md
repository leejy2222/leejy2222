![header](https://capsule
render.vercel.app/api?type=waving&color=auto&height=200&section=header&text=Turtle%20Runaway!&fontSize=32)

## :turtle: 게임 소개

게임 개요 : 파란 거북이(**Runner**)는 무작위로 도망다니고, 빨간 거북이(**Chaser**)는 사용자가 방향키로 조종해서 Runner를 잡는 게임
게임 목표 : 제한 시간 **60초** 동안 최대한 많이 잡아 점수를 올리기

### 게임 실행

```bash
python turtle_runaway.py
```

> - Mac / Linux에서는 `python3 turtle_runaway.py`로 실행해요.
> - Linux에서 `No module named tkinter` 오류가 나면 `sudo apt install python3-tk`로 설치해요.
> - Spyder에서는 F5로 바로 실행되지 않으므로 IPython 콘솔에 `!python turtle_runaway.py`를 입력해요.

### 조작법

키 | 동작
:---: | ---
`↑` | 앞으로 이동 (`step_move` 만큼)
`↓` | 뒤로 이동 (`step_move` 만큼)
`←` | 왼쪽으로 회전 (`step_turn` 만큼)
`→` | 오른쪽으로 회전 (`step_turn` 만큼)

---

## 📦 기존 기능

기능 | 관련 코드 | 설명
--- | --- | ---
게임 세팅 | `RunawayGame.__init__()` | Runner는 파란색, Chaser는 빨간색 거북이로 만들고, 상태 문구를 출력할 숨겨진 `drawer` turtle 생성
잡힘 판정 | `is_catched()`, `catch_radius` | 두 거북이 거리가 `catch_radius`(기본 50)보다 가까우면 잡힌 것으로 판정 (제곱값으로 비교해 계산 절약)
게임 루프 | `start()`, `step()` | 100ms마다 `step()`을 반복 호출해 두 거북이를 움직이고, 잡힘 여부를 화면에 출력
거북이 움직임 | `ManualMover`, `RandomMover` | Chaser는 방향키로 직접 조종, Runner는 전진·좌회전·우회전 중 하나를 무작위로 선택
화면 구성 | `__main__` | 700×700 tkinter 캔버스에 `TurtleScreen`을 올리고 게임 실행

---

## ✨ 추가된 기능 (jy 추가 / 수정)

기능 | 관련 코드 | 설명
--- | --- | ---
제한 시간 | `import time`, `time_limit`, `start_time`, `remain` | 게임 시작 시각을 기록하고 60초에서 경과 시간을 빼 남은 시간 계산
점수 & 재배치 | `score`, `_reset_pos()` | 잡을 때마다 점수 +1, 두 거북이를 처음 위치로 다시 떨어뜨려 게임 계속 진행
상태 표시 (수정) | `drawer.write(...)` | 잡힘 여부 + **거리 / 기준 거리 / 남은 시간 / 점수**를 한 줄로 표시
게임 종료 | `if remain <= 0:` | 시간이 다 되면 `Game over! Final Score: N` 출력 후 게임 정지

### 화면 출력 예시

```
Is catched? False / Distance: 213.4 (need < 50) / Remain: 42.7 / score: 3
```

```
Game over! Final Score: 7
```
