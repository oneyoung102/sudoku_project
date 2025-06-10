from random import randint
from random import shuffle
from time import perf_counter
from math import sqrt

BLOCK_SIZE_TUPLE = (((2,2),(2,3),(3,2),(2,4),(4,2)),#stage에 따른 보드 크기 튜플
                    ((2,4),(4,2),(3,3),(2,5),(5,2)),
                    ((3,3),(2,5),(5,2),(3,4),(4,3),(3,5),(5,3)),
                    ((3,5),(5,3),(3,6),(6,3),(4,4),(4,5),(5,4)),
                    ((3,7),(7,3),(4,6),(6,4),(5,5))) #BLOCK_R*BLOCK_C < 27

PUNCH_COUNT_TUPLE = ((6, 8, 8, 14, 14),#stage에 따른 빈칸 개수 튜플
                    (17, 17, 24, 28, 28),
                    (31, 36, 36, 42, 42, 58, 58),
                    (65, 65, 70, 70, 78, 110, 110),
                    (130, 130, 145, 145, 190)) #BLOCK_R*BLOCK_C < 27

MIN_STAGE = 0
MAX_STAGE = len(BLOCK_SIZE_TUPLE)-1

PASSWORD = 0
STAGE = 1
MAX_SCORE = 2

NAME_LEN_MAX_GLOBAL = 10

USER_INFORMATION_FILE_NAME = "sudoku_users_information.csv"

HORIZONTAL_BAR = "-"
VALID= 1
INVALID = 0
REPEAT = -1
######################################################################################################

def get_users_information_dict() :
    FILE = open(USER_INFORMATION_FILE_NAME,'r')
    users_information_dict = {}
    for s in FILE.readlines() :
        name, pw, stage, max_score = s.strip().split(',')
        users_information_dict[name] = [pw,int(stage),float(max_score)]
    FILE.close()
    return users_information_dict

def convert_to_csv(name,pw,stage,max_score) :
    return name+','+pw+','+str(stage)+','+str(max_score)+'\n'

def update_sudoku_users_information(users_information_dict) :
    FILE = open(USER_INFORMATION_FILE_NAME,'w')
    for name, (pw, stage, max_score) in users_information_dict.items() :
        FILE.write(convert_to_csv(name,pw,stage,max_score))
    FILE.close()

def append_user_information(name, pw, stage, max_score) :
    FILE = open(USER_INFORMATION_FILE_NAME,'a')
    FILE.write(convert_to_csv(name,pw,stage,max_score))
    FILE.close()

######################################################################################################
def test_name_in_login(name,users_information_dict) :    
    if name in users_information_dict :
        print()
        return True
    print("<There is no user information available!>")
    return False

def test_pw_in_login(pw,correct_pw) :
    if pw == correct_pw :
        print("<You have successfully logged in.>\n")
        return True
    print("<The password is incorrect!>")
    return False


def test_name_in_signin(name,users_information_dict,v,NAME_LEN_MIN,NAME_LEN_MAX) :
    if len(name) < NAME_LEN_MIN :
        print(f"<It is shorter than {NAME_LEN_MIN} characters!>")
        return False
    if len(name) > NAME_LEN_MAX :
        print(f"<It is longer than {NAME_LEN_MAX} characters!>")
        return False
    
    NAME_SET = set(name)
    if len(AVAILABLE_CHARACTER_SET & NAME_SET) != len(NAME_SET) :
        print("<It contains invalid characters!>")
        return False
    if name in users_information_dict :
        print("<This username is already in use!>")
        return False
    print("<This username is available.>\n")
    return True


def test_pw_in_signin(pw,name,LETTER_SET,NUMBER_SET,AVAILABLE_CHARACTER_SET,PW_LEN_MIN,PW_LEN_MAX) :
    if len(pw) < PW_LEN_MIN :
        print(f"<It is shorter than {PW_LEN_MIN} characters!>")
        return False
    if len(pw) > PW_LEN_MAX :
        print(f"<It is longer than {PW_LEN_MAX} characters!>")
        return False
    
    PW_SET = set(pw)
    if len(AVAILABLE_CHARACTER_SET & PW_SET) != len(PW_SET) :
        print("<It contains invalid characters!>")
        return False
    if len(LETTER_SET & PW_SET) == 0 :
        print("<It contains only numbers!>")
        return False
    if len(NUMBER_SET & PW_SET) == 0 :
        print("<It contains only letters!>")
        return False
    if pw == name :
        print("<The password is the same as the username!>")
        return False
    print("<You have successfully signed up.>\n")
    return True

            
def get_user_information() :
    LOG_IN = 'l'
    SIGN_IN = 's'
    print(f"<Log in : {LOG_IN}, Sign in : {SIGN_IN}>\n")
    while(True) :
        user_input = input("Enter : ")
        if user_input != LOG_IN and user_input != SIGN_IN :
            print("<The input format is invalid!>")
            continue
        users_information_dict = get_users_information_dict()
        if user_input == LOG_IN :
            print("\n< Log in >\n")
            while(True) :
                name = input("user name : ")
                if test_name_in_login(name,users_information_dict) :
                    break
            while(True) :
                pw = input("user password : ")
                if test_pw_in_login(pw,users_information_dict[name][PASSWORD]) :
                    break
            return name,users_information_dict[name][STAGE],users_information_dict[name][MAX_SCORE],users_information_dict
        else :
            NAME_LEN_MIN = 3
            NAME_LEN_MAX = NAME_LEN_MAX_GLOBAL
            PW_LEN_MIN = 5
            PW_LEN_MAX = 15
            LETTER_SET = {chr(i) for i in range(ord('a'), ord('z')+1)}
            NUMBER_SET = {chr(i) for i in range(ord('0'), ord('9')+1)}
            AVAILABLE_CHARACTER_SET = LETTER_SET.union(NUMBER_SET)
            print("\n< Sign in >\n")
            print(f"<The username must be between {NAME_LEN_MIN} and {NAME_LEN_MAX} characters long>\n<It can only contain letters and numbers.>")
            while(True) :
                name = input("user name : ")
                if test_name_in_signin(name,users_information_dict,AVAILABLE_CHARACTER_SET,NAME_LEN_MIN,NAME_LEN_MAX) :
                    break
            print(f"<The password must be between {PW_LEN_MIN} and {PW_LEN_MAX} characters long>\n<It can only contain letters and numbers.>\n<It must include at least one letter and at least one number.>\n<It must be different from the username>")
            while(True) :
                pw = input("user password : ")
                if test_pw_in_signin(pw,name,LETTER_SET,NUMBER_SET,AVAILABLE_CHARACTER_SET,PW_LEN_MIN,PW_LEN_MAX) :
                    break
            append_user_information(name, pw, 0, 0)
            users_information_dict[name] = [pw,0,0]
            return name,0,0,users_information_dict
        

######################################################################################################
def get_start_ascii_in_board(BOARD_LENGTH) :
    if BOARD_LENGTH < 10 :
        return ord('1')
    #9보다 크면 알파벳으로 설정
    return ord('a')

def get_board_size(stage) :
    BLOCK_R, BLOCK_C = BLOCK_SIZE_TUPLE[stage][randint(0,len(BLOCK_SIZE_TUPLE[stage])-1)] #stage에 따른 랜덤 보드 크기 얻기
    return BLOCK_R, BLOCK_C

def get_random_board(BLOCK_R, BLOCK_C) :
    BOARD_LENGTH = BLOCK_R*BLOCK_C
    def get_row_pushed_left_by_block(row) :#블럭 단위로 왼쪽으로 민 보드 행 반환 
        return row[BLOCK_C:] + row[0:BLOCK_C]
    def get_row_pushed_left_by_element(row) :#원소 단위로 왼쪽으로 민 블럭 행 반환
        new_numbers = []
        for i in range(0,BOARD_LENGTH,BLOCK_C) : #다음 블럭의 첫 행 설정
            new_numbers += row[i:i+BLOCK_C][1:]+row[i:i+BLOCK_C][:1] #원소 단위로 왼쪽으로 민 블럭 행 push_back
        return new_numbers
    
    board = []
    START_ASCII = get_start_ascii_in_board(BOARD_LENGTH)
    numbers = [chr(i) for i in range(START_ASCII, START_ASCII+BOARD_LENGTH)] #리스트 생성
        
    shuffle(numbers) #무작위 섞기
    
    for _ in range(BLOCK_C) : #행에 대해 반복
        new_numbers = numbers[:]
        for _ in range(BLOCK_R) :#블록의 행에 대해 반복
            board.append(new_numbers) #섞인 행 push_back
            new_numbers = get_row_pushed_left_by_block(new_numbers) #블럭 단위로 왼쪽으로 민 보드 행
        numbers = get_row_pushed_left_by_element(numbers)#원소 단위로 왼쪽으로 민 보드 행
    return board

def shuffle_board(BLOCK_R,BLOCK_C,board) :
    def row_block_shuffle(ROW_NUM) : #블록 행 섞기 
        ROW_BLOCK = board[ROW_NUM:ROW_NUM+BLOCK_R]
        numbers = [i for i in range(BLOCK_R)] #블록의 행의 순서를 담은 숫자 생성 
        shuffle(numbers) #무작위 섞기
        for i in range(BLOCK_R) : #섞인 숫서를 board에 적용
            if i != numbers[i] :
                board[ROW_NUM+i] = ROW_BLOCK[numbers[i]]
    for i in range(0,BLOCK_C*BLOCK_R,BLOCK_R) :
        row_block_shuffle(i)
        
    def col_block_shuffle(COL_NUM) :#블록 열 섞기 
        COL_BLOCK = [[board[i][COL_NUM+j] for j in range(BLOCK_C)] for i in range(BLOCK_C*BLOCK_R)]
        numbers = [i for i in range(BLOCK_C)] #블록의 열의 순서를 담은 숫자 생성 
        shuffle(numbers) #무작위 섞기
        for i in range(BLOCK_C) :#섞인 숫서를 board에 적용
            if i == numbers[i] :
                for j in range(BLOCK_C*BLOCK_R) :
                    board[j][COL_NUM+i] = COL_BLOCK[j][numbers[i]]
    for i in range(0,BLOCK_C*BLOCK_R,BLOCK_C) :
        col_block_shuffle(i)

######################################################################################################

def get_punch_count(BLOCK_R,BLOCK_C,stage) :
    for i in range(len(BLOCK_SIZE_TUPLE[stage])) :
        if BLOCK_SIZE_TUPLE[stage][i] == (BLOCK_R,BLOCK_C) :
            GAP = int(sqrt(PUNCH_COUNT_TUPLE[stage][i]/PUNCH_COUNT_TUPLE[MIN_STAGE][0]))
            return randint(PUNCH_COUNT_TUPLE[stage][i]-GAP,PUNCH_COUNT_TUPLE[stage][i]+GAP)

def scatter_punch(BOARD_LENGTH,PUNCH_COUNT) :
    board_to_coords = [(i, j) for i in range(BOARD_LENGTH) for j in range(BOARD_LENGTH)] #board의 모든 좌표를 list로 전환
    shuffle(board_to_coords)#섞기
    return board_to_coords[:PUNCH_COUNT]#섞인 상태에서 PUNCH_COUNT만큼 가져오기, 즉, 구멍 위치 가져오기
    
def cluster_punch(BOARD_LENGTH,PUNCH_COUNT) :
    punch_coord_list = []
    
    DIRECTION = ((1,0),(-1,0),(0,1),(0,-1))
    CLUSTER_R,CLUSTER_C = randint(0,BOARD_LENGTH-1),randint(0,BOARD_LENGTH-1)
    visited = [[False for j in range(BOARD_LENGTH)] for i in range(BOARD_LENGTH)]
    visited[CLUSTER_R][CLUSTER_C] = True
    queue = [(CLUSTER_R,CLUSTER_C)] #queue를 배우지 않았으므로 list로 대체
    rest = PUNCH_COUNT
    while len(queue) != 0 :#BFS
        if rest > 0 :
            for d in DIRECTION :
                r,c = queue[0][0]+d[0], queue[0][1]+d[1]
                if 0 <= r < BOARD_LENGTH and 0 <= c < BOARD_LENGTH and (not visited[r][c]) :
                    queue.append((r,c))
                    visited[r][c] = True
            rest -= 1
            punch_coord_list.append((queue[0][0],queue[0][1]))
        queue.remove(queue[0])
        
    return punch_coord_list

def diagonal_punch(BOARD_LENGTH,PUNCH_COUNT) :
    punch_coord_list = []
    
    left_punch_count = randint(PUNCH_COUNT//3,2*PUNCH_COUNT//3)# PUNCH_COUNT는 전체 칸의 1/3보다 작으므로 좌우 대각선 배치에서 곂칠 일 없음
    right_punch_count = PUNCH_COUNT-left_punch_count
    for i in range(0,BOARD_LENGTH,2) :#왼쪽 위 대각선 배치
        r,c = 0,i
        while c >= 0 and r < BOARD_LENGTH and left_punch_count > 0 :
            punch_coord_list.append((r,c))
            r,c = r+1,c-1
            left_punch_count -= 1
    for i in range(BOARD_LENGTH-1,-1,-2) : #오른쪽 아래 대각선 배치
        r,c = BOARD_LENGTH-1,i
        while c < BOARD_LENGTH and r >= 0 and right_punch_count > 0 :
            punch_coord_list.append((r,c))
            r,c = r-1,c+1
            right_punch_count -= 1
            
    return punch_coord_list

def get_punched_board(BOARD_LENGTH,PUNCH_COUNT,board) :
    SCATTER_POSSIBILITY = 40
    CLUSTER_POSSIBILITY = 70
    punch_coord_list = []
    
    MODE_POSSIBILITY = randint(0,99)
    if MODE_POSSIBILITY < SCATTER_POSSIBILITY : #scatter mode
        punch_coord_list = scatter_punch(BOARD_LENGTH,PUNCH_COUNT)
    elif MODE_POSSIBILITY < CLUSTER_POSSIBILITY : #cluster mode
        punch_coord_list = cluster_punch(BOARD_LENGTH,PUNCH_COUNT)
    else : #diagonal mode
        punch_coord_list = diagonal_punch(BOARD_LENGTH,PUNCH_COUNT)
                
    punched_board = [row[:] for row in board] #깊은 복사
    for coord in punch_coord_list :
        punched_board[coord[0]][coord[1]] = '_' #빈칸 뚫기
    return punched_board, punch_coord_list


######################################################################################################

def print_board(BLOCK_R,BLOCK_C,board,current_punch_count) :
    TITLE = f"{BLOCK_R}x{BLOCK_C} SUDOKU"
    BOARD_LENGTH = BLOCK_R*BLOCK_C
    TITLE_LENGTH = (BOARD_LENGTH*2+BLOCK_R-2-len(TITLE))
    
    buffer = TITLE + HORIZONTAL_BAR*TITLE_LENGTH + "\n\n"
    
    for i in range(BOARD_LENGTH) :
        for j in range(BOARD_LENGTH) :
            buffer += str(board[i][j]) + ' '
            if((j+1)%BLOCK_C == 0) : #행에서블럭 단위로 띄어놓기 
                buffer += ' '
        buffer += '\n'
        if((i+1)%BLOCK_R == 0) :#열에서블럭 단위로 띄어놓기 
            buffer += '\n'
                
    BLANK_SHOW = f"Blank : {current_punch_count}"
    BLANK_SHOW_LENGHTH = (BOARD_LENGTH*2+BLOCK_R-2-len(BLANK_SHOW))
    buffer += HORIZONTAL_BAR*BLANK_SHOW_LENGHTH + BLANK_SHOW + "\n\n"
    print(buffer)

######################################################################################################
def show_random_hint_coord(punch_coord_list,punched_board,board) :    
    r, c = punch_coord_list[randint(0,len(punch_coord_list)-1)]#빈칸 리스트에서 무작위 빈칸 좌표 반환
    print(f"<Revealing the value at position ({c+1}, {r+1}).>")
    punched_board[r][c] = board[r][c]
    punch_coord_list.remove((r,c)) #시간 복잡도가 크지만 set으로 하든 list로 하든 전체 시간 복잡도는 큰 차이 없음

def show_correct_punch(user_r,user_c,punch_coord_list,punched_board,board) : 
    punched_board[user_r][user_c] = board[user_r][user_c]
    punch_coord_list.remove((user_r,user_c))

    
def test_input_by_condition(user_input,BOARD_LENGTH) :
    if user_input == "hint" : #힌트 사용 시 
        return REPEAT,REPEAT,"hint"
    if user_input.count(',') != 1 :#콤마가 없으면
        print("<The input format is incorrect!>")
        return REPEAT,REPEAT,REPEAT
    user_c, r_amp_v = user_input.split(',')#첫 번째 값 추출
    if(not user_c.isdigit() or not (1 <= int(user_c) <= BOARD_LENGTH)) :#첫 번째 값이 범위에 맞지 않으면
        print("<The column is out of range!>")
        return REPEAT,REPEAT,REPEAT
    if r_amp_v.count('=') != 1 :#괄호가 없으면
        print("<The input format is incorrect!>")
        return REPEAT,REPEAT,REPEAT
    user_r, user_v = r_amp_v.split('=')#두,세 번째 값 추출
    if(not user_r.isdigit() or not (1 <= int(user_r) <= BOARD_LENGTH)) :#두 번째 값이 범위에 맞지 않으면
        print("<The row is out of range!>")
        return REPEAT,REPEAT,REPEAT
    
    START_ASCII = get_start_ascii_in_board(BOARD_LENGTH)
    if START_ASCII > ord(user_v) or ord(user_v) >= START_ASCII+ BOARD_LENGTH :#세 번째값이 범위 맞으면
        print("<The input value is out of range!>")
        return REPEAT,REPEAT,REPEAT
    return int(user_r)-1,int(user_c)-1,user_v


def test_input_by_board(user_r,user_c,user_v,punched_board,board) :
    if punched_board[user_r][user_c] != '_' :
        print("<This is not an empty space!>")
        return REPEAT
    if board[user_r][user_c] == user_v :
        print("<This is a valid input!>\n")
        return VALID
    print("<This is an invalid input!>")
    return INVALID
    

def get_user_input(try_count,hint_count,punch_coord_list,punched_board,BOARD_LENGTH,board) :
    TURORIAL_SHOW_COUNT = 3
    if(try_count < TURORIAL_SHOW_COUNT) :
        print("<Please enter in the format: “Column,Row=Value”.>")
        START_ASCII = get_start_ascii_in_board(BOARD_LENGTH)
        print(f"<Column: 1 to {BOARD_LENGTH}, Row: 1 to {BOARD_LENGTH}, Value: {chr(START_ASCII)} to {chr(BOARD_LENGTH + START_ASCII - 1)}>\n<Typing “hint” will reveal one of the empty cells, but your score will be reduced.>")
    while(True) :
        user_input = input("Enter : ")
        user_r, user_c, user_v = test_input_by_condition(user_input,BOARD_LENGTH)
        if user_v == REPEAT :
            continue
        if user_v == "hint" :
            show_random_hint_coord(punch_coord_list,punched_board,board)
            return try_count+1,hint_count+1
        TEST_VALUE = test_input_by_board(user_r,user_c,user_v,punched_board,board)
        if TEST_VALUE == VALID :
            show_correct_punch(user_r,user_c,punch_coord_list,punched_board,board)
            return try_count+1,hint_count
        if TEST_VALUE == INVALID :
            try_count += 1
        
######################################################################################################
        
def get_score(stage,try_count,hint_count,PUNCH_COUNT,BOARD_LENGTH,taken_time) :
    THIKING_TIME = 1.5
    NOTICING_TIME = 0.35 #문자 하나 인식 시간 약 0.35초
    TYPING_TIME = 1 #평균타수가 300이라 가정했을 떄 r,c=v 를 입력하는데 걸리는 시간은 1초
    CRITERIA_TIME = PUNCH_COUNT*((3*BOARD_LENGTH-2)*NOTICING_TIME + THIKING_TIME + TYPING_TIME)
    
    score = 100*(PUNCH_COUNT/try_count)*(stage+1)*(CRITERIA_TIME/TAKEN_TIME) #시간, 시도 횟수를 고려한 점수 생성
    if score > 100*(stage+1) :#점수가 일정 범위 초과 시 조정 
        score = 100*(stage+1)
    score = round(score-(stage+1)*(100/PUNCH_COUNT)*hint_count,2) #힌트 사용에 따른 점수 차감, 셋째 자리에서 반올림
    if score < 0 :#점수가 일정 범위 초과 시 조정 
        score = 0
    return score
        
######################################################################################################
def time_to_string(taken_time) :
    taken_time_text = ""
    taken_time = int(taken_time)
    if(taken_time >= 3600) :
        taken_time_text += str(taken_time//3600)+'h'
        taken_time %= 3600
    if(taken_time >= 60) :
        taken_time_text += str(taken_time//60)+'m'
        taken_time %= 60
    if(taken_time > 0) :
        taken_time_text += str(taken_time)+'s'
    return taken_time_text

######################################################################################################

def print_records(max_score,stage,score,try_count,hint_count,PUNCH_COUNT,TAKEN_TIME_TEXT) :
    buffer_list = [HORIZONTAL_BAR]
    buffer_list.append(f" Record of {name}")
    if score > max_score :
        buffer_list.append(f" Score: {score} points | New High Score!")
    else :
        buffer_list.append(f" Score: {score} points | Highest Score: {max_score}")
    buffer_list.append(f" Time Taken: {TAKEN_TIME_TEXT} | Attempts: {try_count}/{PUNCH_COUNT} | Hints Used: {hint_count}")
    return buffer_list

def update_records(score,max_score,stage) :
    def get_next_stage() : #유저의 점수에 따라 다음 stage로 넘어갈 수 있는지 없는지 판단
        POINT = score/(stage+1)
        if(POINT < 25 and stage > MIN_STAGE) : #stage 가중치를 제거한 점수가 하위 25% 이내라면
            return stage-1
        if(POINT >= 75 and stage < MAX_STAGE) :#stage 가중치를 제거한 점수가 상위 25% 이내라면
            return stage+1
        return stage #어느 것도 아니라면
    
    if score > max_score :
        max_score = score #최고 기록 업데이트
    return get_next_stage(),max_score
    
def print_standing(name,users_information_dict) :
    TOP_NUMBER = 5
    buffer_list = [HORIZONTAL_BAR]
    def print_rank(r,ls) :
        NAME_LEN_MAX = NAME_LEN_MAX_GLOBAL
        NAME_SPACE_LENGTH = NAME_LEN_MAX-len(ls[0])
        suffix = "th"
        rank_number = str(r)
        if rank_number[-1] == '1' :
            suffix = "st"
        elif rank_number[-1] == '2' :
            suffix = "nd"
        elif rank_number[-1] == '3' :
            suffix = "rd"
        RANK_SPACE_LENGTH = 8-len(rank_number+suffix)
        buffer_list.append(f"{rank_number+suffix}{' ' * RANK_SPACE_LENGTH} | {ls[0]}{' ' * NAME_SPACE_LENGTH} | {ls[1][MAX_SCORE]} points")
    
    STANDING = sorted(users_information_dict.items(),key = lambda l : l[1][MAX_SCORE],reverse = True)
    
    prev_high_score,prev_score = 0,0 #동점자 처리를 위한 전 사람 점수 저장
    current_user_appear = False
    rank = 0
    while rank < len(STANDING) :
        if current_user_appear and rank >= TOP_NUMBER :
            break
        if not current_user_appear :
            prev_high_score = prev_score
        prev_score = STANDING[rank][1][MAX_SCORE]
        subrank = rank
        while subrank < len(STANDING) :
            if prev_score != STANDING[subrank][1][MAX_SCORE] :
                rank = subrank-1
                break
            if name == STANDING[subrank][0] :
                current_user_appear = True 
            if rank < TOP_NUMBER : #상위 TOP_NUMBER등만 출력
                print_rank(rank+1,STANDING[subrank])
            elif name == STANDING[subrank][0] : # 상위 출력 밖에서 사용자가 등장한다면
                buffer_list.append("...")
                print_rank(rank+1,STANDING[subrank])
                break
            subrank += 1
        rank += 1
        
    if prev_high_score != 0 :
        buffer_list.append(HORIZONTAL_BAR)
        LEFT_POINT = round(prev_high_score-users_information_dict[name][MAX_SCORE],2)
        buffer_list.append(f" {LEFT_POINT} points left to reach the next rank.")
    return buffer_list
######################################################################################################

def game_interface() :
    print("SUDOKU GAME PLAY\n")
    name, stage, max_score, users_information_dict = get_user_information() #유저의 저장된 정보가 있으면 가져오고 없으면 생성 
    return name, stage, max_score, users_information_dict

def set_game(stage) :
    BLOCK_R,BLOCK_C = get_board_size(stage)
    board = get_random_board(BLOCK_R,BLOCK_C)#stage에 따른 무작위 보드 생성
    shuffle_board(BLOCK_R,BLOCK_C,board)#보드 섞기
    
    PUNCH_COUNT = get_punch_count(BLOCK_R,BLOCK_C,stage)#stage에 따른 보드 구멍 개수 반환
    punched_board, punch_coord_list = get_punched_board(BLOCK_R*BLOCK_C,PUNCH_COUNT,board)#보드에 구멍 뚫기, 힌트를 위한 구멍 좌표 set 반환
    
    return BLOCK_R, BLOCK_C, board, PUNCH_COUNT, punched_board, punch_coord_list, users_information_dict

def start_game(stage, BLOCK_R, BLOCK_C, board, PUNCH_COUNT, punched_board, punch_coord_list) :
    try_count = 0#시도 횟수
    hint_count = 0#힌트 사용 횟수 
    START_TIME = perf_counter()#시간 제기 시작
    while(len(punch_coord_list) != 0) : #빈칸이 존재할 경우
        print_board(BLOCK_R,BLOCK_C,punched_board,len(punch_coord_list))#보드 출력
        try_count, hint_count = get_user_input(try_count,hint_count,punch_coord_list,punched_board,BLOCK_R*BLOCK_C,board)#사용자 입력에 따라 올바른 값인지 판단하고 변경된 try_count, hint_count 반환
        
    TAKEN_TIME = perf_counter()-START_TIME#시간 제기 종료, 소요 시간 반환
    print_board(BLOCK_R,BLOCK_C,punched_board,0)#마지막으로 완성된 보드 출력
    
    return try_count, hint_count, TAKEN_TIME


def finish_game(name,stage,max_score,try_count,hint_count,PUNCH_COUNT,BOARD_LENGTH,TAKEN_TIME,users_information_dict) :
    #점수 산출
    score = get_score(stage,try_count,hint_count,PUNCH_COUNT,BOARD_LENGTH,TAKEN_TIME)
    #소요 시간을 h,m,s 문자열로 전환
    TAKEN_TIME_TEXT = time_to_string(TAKEN_TIME)
    #결과 출력
    buffer_list = print_records(users_information_dict[name][MAX_SCORE],stage,score,try_count,hint_count,PUNCH_COUNT,TAKEN_TIME_TEXT)
    users_information_dict[name][STAGE], users_information_dict[name][MAX_SCORE] = update_records(score,max_score,stage)
    update_sudoku_users_information(users_information_dict)
    #순위표 출력
    buffer_list.extend(print_standing(name,users_information_dict))
    #전체출력 
    buffer = ""
    max_length_of_string = 0
    for b in buffer_list :
        if b != HORIZONTAL_BAR and max_length_of_string < len(b) :
            max_length_of_string = len(b)
    for b in buffer_list :
        if b == HORIZONTAL_BAR :
            buffer += HORIZONTAL_BAR*max_length_of_string
        else :
            buffer += b
        buffer += '\n'
    print(buffer)
        
######################################################################################################
name, stage, max_score, users_information_dict = game_interface()#게임 인터페이스
BLOCK_R, BLOCK_C, board, PUNCH_COUNT, punched_board, punch_coord_list, users_information_dict = set_game(stage)#게임 준비
try_count, hint_count, TAKEN_TIME = start_game(stage, BLOCK_R, BLOCK_C, board, PUNCH_COUNT, punched_board, punch_coord_list)#게임 시작
finish_game(name,stage,max_score,try_count,hint_count,PUNCH_COUNT,BLOCK_R*BLOCK_C,TAKEN_TIME,users_information_dict)#게임 종료
