# Sudoku_Project

> 대학교 1학년 과제를 위해 만든 스도쿠 게임입니다.   
> 제한적인 문법 사용으로 인해 코드가 지저분할 수 있습니다.

<hr/>

## 로그인, 회원가입

- #### 회원가입
  
  **조건**   
  이름 : 3글자 이상, 10글자 이하, 알파벳&숫자만 가능   
  비밀번호 : 5글자 이상, 15글자 이하, 알파벳&숫자만 가능, 최소한 숫자, 알파벳 한 개씩 포함, 이름과 달라야 함

  [**비로그인 상태 플레이**](https://github.com/oneyoung102/Sudoku_project/blob/main/README.md#비회원-플레이)

- #### 로그인

  올바른 이름과 비밀번호를 입력해야 합니다.
  
  [**로그인 상태 플레이**](https://github.com/oneyoung102/Sudoku_project/blob/main/README.md#회원-플레이)

<hr/>

## 난이도

> 총 **5단계**의 난이도가 있습니다. 난이도에 따라 보드크기와 빈칸 개수가 달라집니다.   
> 보드크기 `(m,n)`은 한 변의 길이가 `m*n`인 정사각 보드를 의미합니다.

| 단계 | 보드 크기 목록 | 빈칸 개수 목록 |
| --- | ------ | ------ |
| 1단계 | `(2,2),(2,3),(3,2),(2,4),(4,2)` | `6, 8, 8, 14, 14` |
| 2단계 | `(2,4),(4,2),(3,3),(2,5),(5,2)` | `17, 17, 24, 28, 28` |
| 3단계 | `(3,3),(2,5),(5,2),(3,4),(4,3),(3,5),(5,3)` | `31, 36, 36, 42, 42, 58, 58` |
| 4단계 | `(3,5),(5,3),(3,6),(6,3),(4,4),(4,5),(5,4)` | `65, 65, 70, 70, 78, 110, 110` |
| 5단계 | `(3,7),(7,3),(4,6),(6,4),(5,5)` | `130, 130, 145, 145, 190` |

<hr/>

## 빈칸 배치

1. 난이도별 보드 크기를 담은 튜플에서 랜덤으로 크기 설정(2x2 ~ 5x5), 보드 크기가 10 이상이면 숫자대신 알파벳으로 출력
2. 난이도별 보드 크기에 따른 빈칸 개수를 담은 튜플에서 랜덤으로 오차 범위 내에서 빈칸 개수 설정
  > **오차범위 계산식**
  > ```python
  > GAP = int(sqrt(PUNCH_COUNT_TUPLE[stage][i]/PUNCH_COUNT_TUPLE[MIN_STAGE][0]))


### 빈칸 배치 모드
  - #### scatter
    > 무작위로 배치합니다.
    <img width="94" height="128" alt="image" src="https://github.com/user-attachments/assets/3e3e542a-c230-4a23-89b1-4334da63fcf7" />
    
  - #### diagonal grid
    > 서로 마주보는 모서리부터 시작해서 대각선 격자 형태로 배치합니다.
    <img width="185" height="195" alt="image" src="https://github.com/user-attachments/assets/aa723a04-4f32-4215-bb7a-8270b8369c4f" />

  - #### vacuum
    > 블록 단위로 배치합니다.
    <img width="258" height="287" alt="image" src="https://github.com/user-attachments/assets/70cf7899-ebfc-435b-bc71-f0d0f5e0338d" />

  - #### cluster
    > 무작위 위치에서 군집 형태로 퍼져나가게 배치합니다.
    <img width="314" height="299" alt="image" src="https://github.com/user-attachments/assets/fda92e59-b179-449a-aad8-de45925559c0" />

<hr/>

### 사용자 입력
<img width="643" height="70" alt="image" src="https://github.com/user-attachments/assets/9a6db22a-3dcd-452f-8d43-b7a7c992b542" />

- #### 위치 입력
  > 사용자 편의를 위해 행과 열을 반대로 입력하도록 합니다.
  ```python
  Enter : 5,4=9
  ```
  > 숫자가 아닌 알파벳으로 표시될 경우 `=` 우측에 알파벳을 입력합니다.
  
- #### 힌트 요청
  > 남아 있는 빈칸 중 무작위 위치를 공개합니다.
  ```python
  Enter : hint
  ```
    
<hr/>

### 점수 산출

- #### 다음 난이도 진출   
> 난이도에서 특정 점수 이상에 도달하면 다음 난이도로 진출할 수 있습니다.
> 또한 난이도에서 최대로 얻을 수 있는 점수는 제한적입니다.

| 단계 | 하락 점수 | 상승 점수 | 최대 점수 |
| ---- | ---- | ---- | ---- |
| 1단계 | - | 75~ | 100 |
| 2단계 | ~50 | 150~ | 200 |
| 3단계 | ~75 | 225~ | 300 |
| 4단계 | ~100 | 300~ | 400 |
| 5단계 | ~125 | - | 500 |

- #### 점수표   
<img width="660" height="107" alt="image" src="https://github.com/user-attachments/assets/a765365a-7745-42f8-ab9d-2b1c659b8bf6" />

> 보드크기 대비, 걸린 시간이 길수록, 시도횟수가 많을수록, 힌트 사용횟수가 많을수록 점수가 떨어집니다.

> **점수 산출식**
> ```python
> THIKING_TIME = 1.5
> NOTICING_TIME = 0.35 #문자 하나 인식 시간 약 0.35초
> TYPING_TIME = 1 #평균타수가 300이라 가정했을 떄 r,c=v 를 입력하는데 걸리는 시간은 1초
> CRITERIA_TIME = PUNCH_COUNT*((3*BOARD_LENGTH-2)*NOTICING_TIME + THIKING_TIME + TYPING_TIME)
>
> score = 100*(PUNCH_COUNT/try_count)*(stage+1)*(CRITERIA_TIME/TAKEN_TIME) #시간, 시도 횟수를 고려한 점수 생성
> if score > 100*(stage+1) :#점수가 일정 범위 초과 시 조정 
>     score = 100*(stage+1)
> score = round(score-(stage+1)*(100/PUNCH_COUNT)*hint_count,2) #힌트 사용에 따른 점수 차감, 셋째 자리에서 반올림
> if score < 0 :#점수가 일정 범위 초과 시 조정 
>   score = 0
> return score

<hr/>

## 순위표

1. 본인을 포함하여 1등부터 5등까지의 점수와 이름을 공개합니다.
2. 동점자는 같은 등수로 처리합니다.
3. 본인보다 높은 등수의 사람과의 점수차를 알려줍니다.
   
<img width="357" height="210" alt="image" src="https://github.com/user-attachments/assets/89d8e06f-03b9-4c9b-bfc7-5e4bc02d2e93" />   
> aaa가 보는 순위표입니다.

<hr/>

## 플레이

> **sudoku_code.py**를 실행하여 쉘에서 사용자 입력으로 플레이합니다.

- #### 비로그인 플레이
    1. 점수는 기록되지 않으며, **1단계**만 플레이할 수 있습니다.
    2. 순위표를 볼 수 없습니다.
- #### 로그인 플레이
    1. 점수가 기록되며, 가장 최근 얻은 점수에 따라 난이도가 변동됩니다.
    2. 순위표를 볼 수 있습니다.


