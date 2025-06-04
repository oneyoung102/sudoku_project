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
MAX_STAGE = 4

LOG_IN = 'l'
SIGN_IN = 's'

PASSWORD = 0
STAGE = 1
MAX_SCORE = 2

NAME_LEN_MIN = 3
NAME_LEN_MAX = 10

PW_LEN_MIN = 5
PW_LEN_MAX = 15

TURORIAL_SHOW_COUNT = 3

SCATTER_POSSIBILITY = 40
CLUSTER_POSSIBILITY = 70

TOP_NUMBER = 3
######################################################################################################

def get_users_information_dict() :
    FILE = open("sudoku_users_information.csv",'r')
    users_information_dict = {}
    for s in FILE.readlines() :
        name, pw, stage, max_score = s.strip().split(',')
        users_information_dict[name] = [pw,int(stage),float(max_score)]
    FILE.close()
    return users_information_dict

def transfer_to_csv(name,pw,stage,max_score) :
    return name+','+pw+','+str(stage)+','+str(max_score)+'\n'

def update_sudoku_users_information(users_information_dict) :
    FILE = open("sudoku_users_information.csv",'w')
    for name, (pw, stage, max_score) in users_information_dict.items() :
        FILE.write(transfer_to_csv(name,pw,stage,max_score))
    FILE.close()

def append_user_information(name, pw, stage, max_score) :
    FILE = open("sudoku_users_information.csv",'a')
    FILE.write(transfer_to_csv(name,pw,stage,max_score))
    FILE.close()

######################################################################################################
def get_user_name(user_input,users_information_dict) :
    if user_input == LOG_IN :
        while(True) :
            name = input("user name : ")
            if name in  users_information_dict :
                print()
                return name
            else :
                print("<사용자 정보가 없습니다!>")
    elif user_input == SIGN_IN:
        available_character = {chr(i) for i in range(ord('a'), ord('z')+1)} | {chr(i) for i in range(ord('0'), ord('9')+1)}
        
        print(f"<사용자 이름은 최소 {NAME_LEN_MIN}글자 최대 {NAME_LEN_MAX}글자까지 가능, 알파벳, 숫자만 사용 가능>")
        while(True) :
            name = input("user name : ")
            if len(name) < NAME_LEN_MIN :
                print(f"<{NAME_LEN_MIN}글자보다 짧습니다!>")
            elif len(name) > NAME_LEN_MAX :
                print(f"<{NAME_LEN_MAX}글자보다 깁니다!>")
            elif len(available_character & set(name)) != len(set(name)) :
                print("<허용되지 않는 문자가 포함되어 있습니다!>")
            elif name in users_information_dict :
                print("<사용 중인 이름입니다.>")
            else :
                print("<사용가능한 이름입니다.>\n")
                return name
            
def get_user_pw(user_input,name,users_information_dict) :
    if user_input == LOG_IN :
        while(True) :
            pw = input("user password : ")
            if pw == users_information_dict[name][PASSWORD] :
                print("<성공적으로 로그인이 완료되었습니다.>\n")
                return pw
            else :
                print("<올바르지 않은 비밀번호입니다!>")
    elif user_input == SIGN_IN:
        available_character = {chr(i) for i in range(ord('a'), ord('z')+1)} | {chr(i) for i in range(ord('0'), ord('9')+1)}
        
        print(f"<비밀번호는 최소 {PW_LEN_MIN}글자 최대 {PW_LEN_MAX}글자까지 가능, 이름과 다른 비밀번호>\n<알파벳, 숫자만 가능, 최소 알파벳 한 개 포함, 최소 숫자 한 개 포함>")
        while(True) :
            pw = input("user password : ")
            if len(pw) < PW_LEN_MIN :
                print(f"<{PW_LEN_MIN}글자보다 짧습니다!>")
            elif len(pw) > PW_LEN_MAX :
                print(f"<{PW_LEN_MAX}글자보다 깁니다!>")
            elif len(available_character & set(pw)) != len(set(pw)) :
                print("<허용되지 않는 문자가 포함되어 있습니다!>")
            elif len(numbers & set(pw)) == 0 :
                print("<숫자가 없습니다!>")
            elif len(alphabet & set(pw)) == 0 :
                print("<알파벳이 없습니다!>")
            elif pw == name :
                print("<비밀번호와 이름이 같습니다.>")
            else :
                print("<성공적으로 회원가입이 완료되었습니다.>\n")
                return pw
            
def get_user_information() :
    print(f"<로그인 : {LOG_IN}, 회원가입 : {SIGN_IN}>")
    while(True) :
        user_input = input("입력 : ")
        if user_input == LOG_IN :
            print("\n< 로그인 >\n")
            break
        elif user_input == SIGN_IN:
            print("\n< 화원가입 >\n")
            break
        else :
            print("<입력형식에 맞지 않습니다!>")
            
    users_information_dict = get_users_information_dict()
    
    name = get_user_name(user_input,users_information_dict)
    pw = get_user_pw(user_input,name,users_information_dict)
    
    if user_input == LOG_IN :
        return name,users_information_dict[name][STAGE],users_information_dict[name][MAX_SCORE],users_information_dict
    elif user_input == SIGN_IN:
        append_user_information(name, pw, 0, 0)
        users_information_dict[name] = [pw,0,0]
        return name,0,0,users_information_dict

######################################################################################################
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
    if BOARD_LENGTH < 10 :
        numbers = [i for i in range(1,BOARD_LENGTH+1)] #가능한 숫자를 담은 리스트 생성
    else : #9보다 크면 알파벳으로 설정
        numbers = [chr(i) for i in range(ord('a'), ord('a')+BOARD_LENGTH)]
        
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
            if i != numbers[i] :
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

def scatter_punch(BOARD_LENGTH,PUNCH_COUNT,board) :
    board_to_coords = [(i, j) for i in range(BOARD_LENGTH) for j in range(BOARD_LENGTH)] #board의 모든 좌표를 list로 전환
    shuffle(board_to_coords)#섞기
    return board_to_coords[:PUNCH_COUNT]#섞인 상태에서 PUNCH_COUNT만큼 가져오기, 즉, 구멍 위치 가져오기
    
def cluster_punch(BOARD_LENGTH,PUNCH_COUNT,board) :
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

def diagonal_punch(BOARD_LENGTH,PUNCH_COUNT,board) :
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
    punch_coord_list = []
    
    MODE_POSSIBILITY = randint(0,99)
    if MODE_POSSIBILITY < SCATTER_POSSIBILITY : #scatter mode
        punch_coord_list = scatter_punch(BOARD_LENGTH,PUNCH_COUNT,board)
    elif MODE_POSSIBILITY < CLUSTER_POSSIBILITY : #cluster mode
        punch_coord_list = cluster_punch(BOARD_LENGTH,PUNCH_COUNT,board)
    else : #diagonal mode
        punch_coord_list = diagonal_punch(BOARD_LENGTH,PUNCH_COUNT,board)
                
    
    punched_board = [row[:] for row in board] #깊은 복사
    for coord in punch_coord_list :
        punched_board[coord[0]][coord[1]] = '_' #빈칸 뚫기
    return punched_board, punch_coord_list


######################################################################################################

def print_board(BLOCK_R,BLOCK_C,board,current_punch_count) :
    TITLE = f"{BLOCK_R}x{BLOCK_C} SUDOKU"
    BOARD_LENGTH = BLOCK_R*BLOCK_C
    TITLE_LENGTH = (BOARD_LENGTH*2+BLOCK_R-2-len(TITLE))
    
    buffer = TITLE + '-'*TITLE_LENGTH + '\n'
    
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
    buffer += '-'*BLANK_SHOW_LENGHTH + BLANK_SHOW + "\n\n"
    print(buffer)

######################################################################################################
    
def test_input_by_board(user_r,user_c,user_v,try_count,hint_count,punch_coord_list,board,punched_board) :
    if user_v == "hint" :
        user_r, user_c = punch_coord_list[randint(0,len(punch_coord_list)-1)]#빈칸 리스트에서 무작위 빈칸 좌표 반환
        punched_board[user_r][user_c] = board[user_r][user_c]
        punch_coord_list.remove((user_r,user_c)) #시간 복잡도가 크지만 set으로 하든 list로 하든 전체 시간 복잡도는 큰 차이 없음
        return try_count+1,hint_count+1,f"<({user_c+1},{user_r+1}) 위치의 값을 공개합니다.>"
    elif punched_board[user_r][user_c] != '_' :
        return -1,-1,"<빈칸이 아닙니다!>"
    elif board[user_r][user_c] == user_v :
        punched_board[user_r][user_c] = board[user_r][user_c]
        punch_coord_list.remove((user_r,user_c))
        return try_count+1,hint_count,"<올바른 입력값입니다!>"
    else :
        return try_count+1,hint_count,"<잘못된 입력값입니다!>"
    
def test_input_by_condition(user_input,try_count,hint_count,punch_coord_list,BOARD_LENGTH,board,punched_board) :
    if user_input == "hint" : #힌트 사용 시 
        return test_input_by_board(0,0,"hint",try_count,hint_count,punch_coord_list,board,punched_board)
    if user_input.count(',') != 1 :#콤마가 없으면
        return -1,-1,"<입력형식에 맞지 않습니다!>"
    user_c, r_amp_v = user_input.split(',')#첫 번째 값 추출
    if(not user_c.isdigit() or not (1 <= int(user_c) <= BOARD_LENGTH)) :#첫 번째 값이 범위에 맞지 않으면
        return -1,-1,"<가로가 범위를 초과하였습니다!>"
    if r_amp_v.count('=') != 1 :#괄호가 없으면
        return -1,-1,"<입력형식에 맞지 않습니다!>"
    user_r, user_v = r_amp_v.split('=')#두,세 번째 값 추출
    if(not user_r.isdigit() or not (1 <= int(user_r) <= BOARD_LENGTH)) :#두 번째 값이 범위에 맞지 않으면
        return -1,-1,"<세로가 범위를 초과하였습니다!>"
    if(BOARD_LENGTH < 10) :
        if(user_v.isdigit() and 1 <= int(user_v) <= BOARD_LENGTH) :#세 번째값이 범위 맞으면
            return test_input_by_board(int(user_r)-1,int(user_c)-1,int(user_v),try_count,hint_count,punch_coord_list,board,punched_board)
    else :#최대 숫자가 10이상일 경우 알파뱃으로 입력받기
        if(ord('a') <= ord(user_v) < ord('a') + BOARD_LENGTH) : #세 번째값이 범위 맞으면 
            return test_input_by_board(int(user_r)-1,int(user_c)-1,user_v,try_count,hint_count,punch_coord_list,board,punched_board) #입력받은 알파벳으로 숫자로 치환
    return -1,-1,"<입력값이 범위를 초과하였습니다!>"

def get_user_input(try_count,hint_count,punch_coord_list,BOARD_LENGTH,board,punched_board) :
    if(try_count < TURORIAL_SHOW_COUNT) :
        print("<\"가로,세로=입력값\" 형태로 입력하세요.>")
        if(BOARD_LENGTH < 10) :
            print(f"<가로 : 1 ~ {BOARD_LENGTH}, 세로 : 1 ~ {BOARD_LENGTH}, 입력값 : 1 ~ {BOARD_LENGTH}>") 
        else :
            print(f"<가로 : 1 ~ {BOARD_LENGTH}, 세로 : 1 ~ {BOARD_LENGTH}, 입력값 : a ~ {chr(BOARD_LENGTH+ord('a')-1)}>")
        print("<\"hint\"를 입력하면 빈칸 중 하나를 공개하지만 점수가 감점됩니다.>")
    while(True) :
        user_input = input("입력 : ")
        t,h,text = test_input_by_condition(user_input,try_count,hint_count,punch_coord_list,BOARD_LENGTH,board,punched_board)
        print(text)
        if t != -1 and h != -1 :
            print()
            return t,h 
        
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

def print_update_records(name,stage,score,try_count,hint_count,PUNCH_COUNT,TAKEN_TIME_TEXT,users_information_dict) :
    def get_next_stage(score) : #유저의 점수에 따라 다음 stage로 넘어갈 수 있는지 없는지 판단
        POINT = score/(stage+1)
        if(POINT < 25 and stage > MIN_STAGE) : #stage 가중치를 제거한 점수가 하위 25% 이내라면
            return stage-1
        elif(POINT >= 75 and stage < MAX_STAGE) :#stage 가중치를 제거한 점수가 상위 25% 이내라면
            return stage+1
        return stage #어느 것도 아니라면
    RECORD = f" 소요시간 : {TAKEN_TIME_TEXT} | 시도횟수 : {try_count}/{PUNCH_COUNT} | 힌트 사용 횟수 : {hint_count} "
    print('-'*len(RECORD))
    print(f" {name}님의 기록 ")
    if score > users_information_dict[name][MAX_SCORE] :
        print(f" 점수 : {score}점 | 최고 기록 경신!")
        users_information_dict[name][MAX_SCORE] = score #최고 기록 업데이트
        update_sudoku_users_information(users_information_dict)
    else :
        print(f" 점수 : {score}점 | 최고 점수 : {users_information_dict[name][MAX_SCORE]}")
    print(f"{RECORD}")
    print('-'*len(RECORD))
    users_information_dict[name][STAGE] = get_next_stage(score)
    update_sudoku_users_information(users_information_dict)

    
def print_standing(name, users_information_dict) :
    def print_rank(r,ls) :
        NAME_SPACE_LENGTH = NAME_LEN_MAX-len(ls[0])
        print(f"{r}등 \t| {ls[0]}"+' '*NAME_SPACE_LENGTH+f" | {ls[1][MAX_SCORE]}점")
    
    STANDING = sorted(users_information_dict.items(),key = lambda l : l[1][MAX_SCORE],reverse = True)
    
    rank = 1
    prev_score = 0 #동점자 처리를 위한 전 사람 점수 저장
    sub_rank = 1 #동점자 처리를 위한 전 사람 등수 저장
    current_user_appear = False
    for ls in STANDING :
        if rank <= TOP_NUMBER : #상위 TOP_NUMBER명만 출력
            if prev_score != ls[1][MAX_SCORE] :
                prev_score = ls[1][MAX_SCORE]
                print_rank(rank,ls)
                sub_rank = rank
            else : #동점자 처리
                print_rank(subrank,ls)
            if ls[0] == name : #현재 사용자가 등장한다면
                current_user_appear = True
        elif not current_user_appear: #상위 3명 안에 현재 사용자가 없다면 나올 때까지 반복
            if prev_score != ls[1][MAX_SCORE] :
                prev_score = ls[1][MAX_SCORE]
                if ls[0] == name :
                    print_rank(rank,ls)
                    break
                sub_rank = rank
            elif ls[0] == name :
                print_rank(subrank,ls)
                break
        else :
            break
        rank += 1
######################################################################################################
    
def set_game() :
    name, stage, max_score, users_information_dict = get_user_information() #유저의 저장된 정보가 있으면 가져오고 없으면 생성 
    #name, pw, max_score,stage = "semi","sesomi1",0,4 #----------------------------------------테스트용, 테스트 시에 윗 줄들을 주석처리, 이 줄을 주석처리 해제하고 사용하시오
    BLOCK_R,BLOCK_C = get_board_size(stage)
    board = get_random_board(BLOCK_R,BLOCK_C)#stage에 따른 무작위 보드 생성
    shuffle_board(BLOCK_R,BLOCK_C,board)#보드 섞기
    
    PUNCH_COUNT = get_punch_count(BLOCK_R,BLOCK_C,stage)#stage에 따른 보드 구멍 개수 반환
    punched_board, punch_coord_list = get_punched_board(BLOCK_R*BLOCK_C,PUNCH_COUNT,board)#보드에 구멍 뚫기, 힌트를 위한 구멍 좌표 set 반환
    
    return name, stage, BLOCK_R, BLOCK_C, board, PUNCH_COUNT, punched_board, punch_coord_list, users_information_dict

def start_game(stage, BLOCK_R, BLOCK_C, board, PUNCH_COUNT, punched_board, punch_coord_list) :
    try_count = 0#시도 횟수
    hint_count = 0#힌트 사용 횟수 
    START_TIME = perf_counter()#시간 제기 시작
    while(len(punch_coord_list) != 0) : #빈칸이 존재할 경우
        print_board(BLOCK_R,BLOCK_C,punched_board,len(punch_coord_list))#보드 출력
        try_count, hint_count = get_user_input(try_count,hint_count,punch_coord_list,BLOCK_R*BLOCK_C,board,punched_board)#사용자 입력에 따라 올바른 값인지 판단하고 변경된 try_count, hint_count 반환
        
    TAKEN_TIME = perf_counter()-START_TIME#시간 제기 종료, 소요 시간 반환
    print_board(BLOCK_R,BLOCK_C,punched_board,0)#마지막으로 완성된 보드 출력
    
    return try_count, hint_count, TAKEN_TIME


def finish_game(name,stage,try_count,hint_count,PUNCH_COUNT,BOARD_LENGTH,TAKEN_TIME,users_information_dict) :
    #점수 산출
    score = get_score(stage,try_count,hint_count,PUNCH_COUNT,BOARD_LENGTH,TAKEN_TIME)
    #소요 시간을 h,m,s 문자열로 전환
    TAKEN_TIME_TEXT = time_to_string(TAKEN_TIME)
    #결과 출력
    print_update_records(name,stage,score,try_count,hint_count,PUNCH_COUNT,TAKEN_TIME_TEXT,users_information_dict) 
    #순위표 출력
    print_standing(name,users_information_dict)

######################################################################################################

name, stage, BLOCK_R, BLOCK_C, board, PUNCH_COUNT, punched_board, punch_coord_list, users_information_dict = set_game()#게임 준비
try_count, hint_count, TAKEN_TIME = start_game(stage, BLOCK_R, BLOCK_C, board, PUNCH_COUNT, punched_board, punch_coord_list)#게임 시작
finish_game(name,stage,try_count,hint_count,PUNCH_COUNT,BLOCK_R*BLOCK_C,TAKEN_TIME,users_information_dict)#게임 종료
