import sys
import variable as v_
from PyQt5.QtTest import *
sys.path.append('C:/my_games/' + str(v_.game_folder) + '/' + str(v_.data_folder) + '/mymodule')

def go_test(cla):
    print('hi test! schedule', cla)


def myQuest_play_check(cla, data):
    try:
        import os.path
        from datetime import datetime
        from datetime import date, timedelta

        refresh_ = False

        # 닉네임 받아와서 전역변수 설정하기
        nowDay_ = datetime.today().strftime("%Y%m%d")
        nowDay = int(nowDay_)
        nowTime = int(datetime.today().strftime("%H"))
        yesterday_ = date.today() - timedelta(1)
        yesterday = int(yesterday_.strftime('%Y%m%d'))

        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        file_path = dir_path + "\\mysettings\\myschedule\\schedule.txt"
        file_path2 = dir_path + "\\mysettings\\refresh_time\\quest.txt"
        file_path3 = dir_path + "\\mysettings\\myschedule\\schedule2.txt"
        file_path13 = dir_path + "\\mysettings\\refresh_time\\refresh_time.txt"

        isRefresh = False
        while isRefresh is False:
            if os.path.isfile(file_path13) == True:
                with open(file_path13, "r", encoding='utf-8-sig') as file:
                    isRefresh = True
                    refresh_time = file.read()
                    print("refresh_time", refresh_time)
            else:
                with open(file_path13, "w", encoding='utf-8-sig') as file:
                    file.write(str(6))


        if nowTime >= int(refresh_time):
            nowDay = str(nowDay)
            print("1 : 퀘스트 갱신된 상황이라 체크 후 진행", nowDay)
        else:
            nowDay = yesterday
            nowDay = str(nowDay)
            print("날짜가 다르다")
            print("2 : 퀘스트 갱신되기 전이라 그냥 진행", nowDay)

        #스케쥴 초기화 관련
        if os.path.isfile(file_path2) == True:
            print("nowDay : ", nowDay)
            # 파일 읽기
            with open(file_path2, "r", encoding='utf-8-sig') as file:
                lines2 = file.read().splitlines()
                day_ = lines2[0].split(":")
            if day_[0] == nowDay:
                print("nowDay ing good")
            else:

                if datetime.today().weekday() == 0:

                    with open(file_path2, "w", encoding='utf-8-sig') as file:
                        file.write(str(nowDay) + ":" + str(refresh_time) + "\n")
                        # 월요일 갱신
                        print("월요일 갱신")
                        reset_schedule_ = ""
                        with open(file_path, "r", encoding='utf-8-sig') as file:
                            lines = file.read().splitlines()
                            lines = ' '.join(lines).split()

                            isSchedule_ = False
                            while isSchedule_ is False:
                                if lines == [] or lines == "":
                                    print("스케쥴이 비었다 : myQuest_play_check")
                                    with open(file_path3, "r", encoding='utf-8-sig') as file:
                                        schedule_ready = file.read()
                                    with open(file_path, "w", encoding='utf-8-sig') as file:
                                        file.write(schedule_ready)
                                    with open(file_path, "r", encoding='utf-8-sig') as file:
                                        lines = file.read().splitlines()
                                else:
                                    isSchedule_ = True

                            for i in range(len(lines)):
                                complete_ = lines[i].split(":")
                                for j in range(len(complete_)):
                                    if j < 3:
                                        reset_schedule_ += complete_[j] + ":"
                                    if j == 3:
                                        reset_schedule_ += '대기중:'
                                    if 3 < j < 7:
                                        reset_schedule_ += complete_[j] + ":"
                                    if j == 7:
                                        reset_schedule_ += "대기중\n"
                            print('reset_schedule_', reset_schedule_)
                            with open(file_path, "w", encoding='utf-8-sig') as file:
                                file.write(reset_schedule_)
                            # with open(file_path3, "w", encoding='utf-8-sig') as file:
                            #     file.write(reset_schedule_)
                else:
                    with open(file_path2, "w", encoding='utf-8-sig') as file:
                        file.write(str(nowDay) + ":" + str(refresh_time) + "\n")
                        # 월요일을 제외한 갱신
                        print("월요일을 제외한 갱신")
                        reset_schedule_ = ""
                        with open(file_path, "r", encoding='utf-8-sig') as file:
                            lines = file.read().splitlines()
                            lines = ' '.join(lines).split()

                            isSchedule_ = False
                            while isSchedule_ is False:
                                if lines == [] or lines == "":
                                    print("스케쥴이 비었다 : myQuest_play_check")
                                    with open(file_path3, "r", encoding='utf-8-sig') as file:
                                        schedule_ready = file.read()
                                    with open(file_path, "w", encoding='utf-8-sig') as file:
                                        file.write(schedule_ready)
                                    with open(file_path, "r", encoding='utf-8-sig') as file:
                                        lines = file.read().splitlines()
                                else:
                                    isSchedule_ = True

                            for i in range(len(lines)):
                                complete_ = lines[i].split(":")
                                for j in range(len(complete_)):
                                    if j < 3:
                                        reset_schedule_ += complete_[j] + ":"
                                    if j == 3:

                                        reset_schedule_ += '대기중:'
                                    if 3 < j < 7:
                                        reset_schedule_ += complete_[j] + ":"
                                    if j == 7:

                                        reset_schedule_ += '대기중\n'

                            print('reset_schedule_', reset_schedule_)
                            with open(file_path, "w", encoding='utf-8-sig') as file:
                                file.write(reset_schedule_)
                            # with open(file_path3, "w", encoding='utf-8-sig') as file:
                            #     file.write(reset_schedule_)
                refresh_ = True
                # 초기화 할때 변경해야할 전역 변수
                v_.dead_count = 0
                v_.daily_mission_ready = True


        else:
            with open(file_path2, "w", encoding='utf-8-sig') as file:
                file.write(str(nowDay) + ":" + str(refresh_time) + "\n")
                myQuest_play_check(cla, data)

        #스케쥴 관련
        cla_schedule = ""
        if os.path.isfile(file_path) == True:
            print("3_", nowDay)
            # 파일 읽기
            with open(file_path, "r", encoding='utf-8-sig') as file:
                lines = file.read().splitlines()
                isSchedule_ = False
                while isSchedule_ is False:
                    if lines == [] or lines == "":
                        print("스케쥴이 비었다 : myQuest_grow_check")
                        with open(file_path3, "r", encoding='utf-8-sig') as file:
                            schedule_ready = file.read()
                        with open(file_path, "w", encoding='utf-8-sig') as file:
                            file.write(schedule_ready)
                        with open(file_path, "r", encoding='utf-8-sig') as file:
                            lines = file.read().splitlines()
                    else:
                        isSchedule_ = True

                for i in range(len(lines)):
                    complete_ = lines[i].split(":")
                    for j in range(len(complete_)):
                        if cla == 'one' or cla == "three" or cla == "five":
                            if j < 3:
                                cla_schedule += complete_[j] + ":"
                            if j == 3:
                                cla_schedule += complete_[3] + "\n"
                        if cla == 'two' or cla == "four" or cla == "six":
                            if 3 < j < 7:
                                cla_schedule += complete_[j] + ":"
                            if j == 7:
                                cla_schedule += complete_[7] + "\n"
            #시작 스케쥴 파악하기

            forBreak = False
            schedule_ = cla_schedule.split("\n")
            schedule_ = ' '.join(schedule_).split()
            print("schedule_", schedule_)
            for i in range(len(schedule_)):
                schedule_2 = schedule_[i].split(":")
                for j in range(len(schedule_2)):
                    if schedule_2[3] != "완료":
                        forBreak = True
                        print("대기중인 첫번째", i)
                        start_ = i
                        break
                if forBreak == True:
                    break
            print("start!", start_)
            start = schedule_[start_].split(":")
            start = ' '.join(start).split()
            print("start[1]!", start[1])

            dunjeon_spl_re = "none"
            if '_' in start[2]:
                dunjeon_spl_ = start[2].split("_")
                print("dunjeon_spl_[0]", dunjeon_spl_[0])
                print("dunjeon_spl_[1]", dunjeon_spl_[1])
                dunjeon_spl_re = dunjeon_spl_[0]





###################################################################################################

        else:
            print('파일 없당')
            if os.path.isdir(dir_path) == True:
                print('디렉토리 존재함')
                with open(file_path3, "r", encoding='utf-8-sig') as file:
                    shcedule = file.read().splitlines()
                with open(file_path, "w", encoding='utf-8-sig') as file:
                    file.write(shcedule)
                    myQuest_play_check(cla, data)
            else:
                print('디렉토리 존재하지 않음')
                os.makedirs(dir_path)
                with open(file_path3, "r", encoding='utf-8-sig') as file:
                    shcedule = file.read().splitlines()
                with open(file_path, "w", encoding='utf-8-sig') as file:
                    file.write(shcedule)
                    myQuest_play_check(cla, data)

        return start, start_, refresh_
    except Exception as e:
        print(e)
        return 0


def myQuest_play_add(cla, data):
    try:
        import os.path
        from datetime import datetime
        from datetime import date, timedelta
        from function_game import click_pos_2

        newCharacter = True
        add = True
        # cla는 몇번째 클라우드인지...
        print(cla)
        print(data)
        clear_mission = data
        if cla == 'one':
            clalal_ = 'One'
        if cla == 'two':
            clalal_ = 'Two'
        if cla == "three":
            clalal_ = 'Three'
        if cla == "four":
            clalal_ = 'Four'
        if cla == "five":
            clalal_ = 'Five'
        if cla == "six":
            clalal_ = 'Six'

        nowDay_ = datetime.today().strftime("%Y%m%d")
        nowDay = int(nowDay_)
        nowTime = int(datetime.today().strftime("%H"))
        yesterday_ = date.today() - timedelta(1)
        yesterday = int(yesterday_.strftime('%Y%m%d'))



        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        file_path = dir_path + "\\mysettings\\myschedule\\schedule.txt"
        file_path2 = dir_path + "\\mysettings\\refresh_time\\quest.txt"
        file_path3 = dir_path + "\\mysettings\\myschedule\\schedule2.txt"
        file_path13 = dir_path + "\\mysettings\\refresh_time\\refresh_time.txt"

        isRefresh = False
        while isRefresh is False:
            if os.path.isfile(file_path13) == True:
                with open(file_path13, "r", encoding='utf-8-sig') as file:
                    isRefresh = True
                    refresh_time = file.read()
                    print("refresh_time", refresh_time)
            else:
                with open(file_path13, "w", encoding='utf-8-sig') as file:
                    file.write(str(6))

        if nowTime >= int(refresh_time):
            nowDay = str(nowDay)
            print("1", nowDay)
        else:
            nowDay = yesterday
            nowDay = str(nowDay)
            print("2", nowDay)

        if os.path.isdir(dir_path) == True:
            print('디렉토리 존재')
        else:
            os.makedirs(dir_path)

        if os.path.isfile(file_path2) == True:
            # 파일 읽기
            with open(file_path2, "r", encoding='utf-8-sig') as file:
                lines2 = file.read().splitlines()
            day_ = lines2[0].split(":")
            print("lines", lines2)
            print("day_", day_)
            print("day_[0]", day_[0])
        else:
            print('없다')

            isNowday = False
            while isNowday is False:
                if os.path.isfile(file_path2) == True:
                    with open(file_path2, "r", encoding='utf-8-sig') as file:
                        isNowday = True
                        lines2 = file.read().splitlines()
                        day_ = lines2[0].split(":")
                        print("day_", day_)
                else:
                    with open(file_path2, "w", encoding='utf-8-sig') as file:
                        file.write(str(nowDay) + ":" + str(refresh_time) + "\n")

            # with open(file_path2, "w", encoding='utf-8-sig') as file:
            #     file.write(str(nowDay) + ":" + str(refresh_time) + "\n")
            # with open(file_path2, "r", encoding='utf-8-sig') as file:
            #     lines2 = file.read().splitlines()
            #     day_ = lines2[0].split(":")




        if day_[0] == nowDay:
            print("nowDay ing good")
            # 스케쥴 관련

            cla_schedule1 = ""
            cla_schedule2 = ""
            if os.path.isfile(file_path) == True:
                print("3_", nowDay)
                # 파일 읽기
                with open(file_path, "r", encoding='utf-8-sig') as file:
                    lines = file.read().splitlines()
                    lines = ' '.join(lines).split()

                    isSchedule_ = False
                    while isSchedule_ is False:
                        if lines == [] or lines == "":
                            print("스케쥴이 비었다 : myQuest_grow_check")
                            with open(file_path3, "r", encoding='utf-8-sig') as file:
                                schedule_ready = file.read()
                            with open(file_path, "w", encoding='utf-8-sig') as file:
                                file.write(schedule_ready)
                            with open(file_path, "r", encoding='utf-8-sig') as file:
                                lines = file.read().splitlines()
                        else:
                            isSchedule_ = True

                    for i in range(len(lines)):
                        complete_ = lines[i].split(":")
                        for j in range(len(complete_)):
                            if j < 3:
                                cla_schedule1 += complete_[j] + ":"
                            if j == 3:
                                cla_schedule1 += complete_[3] + "\n"
                            if 3 < j < 7:
                                cla_schedule2 += complete_[j] + ":"
                            if j == 7:
                                cla_schedule2 += complete_[7] + "\n"
                #여기서 현재 부분 체크...
                cla_schedule1_ = cla_schedule1.split("\n")
                cla_schedule2_ = cla_schedule2.split("\n")
                print('lines', lines)
                print('lines[0]', lines[0])
                print('cla_schedule1', cla_schedule1)
                print('cla_schedule2', cla_schedule2)
                print('cla_schedule1_[0]', cla_schedule1_[0])
                print('cla_schedule2_[0]', cla_schedule2_[0])
                if cla == 'one' or cla == "three" or cla == "five":
                    cla_schedule = cla_schedule1
                if cla == 'two' or cla == "four" or cla == "six":
                    cla_schedule = cla_schedule2
                # 시작 스케쥴 파악하기
                forBreak = False
                schedule_ = cla_schedule.split("\n")
                print("schedule_", schedule_)
                for i in range(len(schedule_)):
                    schedule_2 = schedule_[i].split(":")
                    for j in range(len(schedule_2)):
                        if schedule_2[3] != "완료":
                            forBreak = True
                            print("대기중인 첫번째", i)
                            start_ = i
                            break
                    if forBreak == True:
                        break
                print("start!", start_)
                start = schedule_[start_].split(":")
                start = ' '.join(start).split()
                print("start[start_]!", start[1])
            # ############################################################################################################
            print('start', start)
            print('clear_mission', clear_mission)
            print('start', start[2])
            print('start[1]', start[1])
            print('clalal_', clalal_)
            print('start[0]', start[0])

            # dunjeon_spl_re = "none"
            # if '_' in start[2]:
            #     dunjeon_spl_ = start[2].split("_")
            #     print("dunjeon_spl_[0]", dunjeon_spl_[0])
            #     print("dunjeon_spl_[1]", dunjeon_spl_[1])
            #     dunjeon_spl_re = dunjeon_spl_[0]
            # else:
            #     dunjeon_spl_re = start[2]


            if data == start[2] and clalal_ == start[0]:
            # if clalal_ == start[0]:

                if cla == 'one' or cla == "three" or cla == 'five':
                    v_.one_cla_ing = 'check'
                    start_re = start[0] + ":" + start[1] + ":" + start[2] + ":" + '완료' + ":" + cla_schedule2_[start_]
                if cla == 'two' or cla == "four" or cla == 'six':
                    v_.two_cla_ing = 'check'
                    start_re = cla_schedule1_[start_] + ":" + start[0] + ":" + start[1] + ":" + start[2] + ":" + '완료'

                print("start_re", start_re)

                print('lines111', lines)
                del lines[start_]
                lines.insert(start_, start_re)
                print('lines222', lines)

                last_result = ""
                for i in range(len(lines)):
                    last_result += lines[i] + "\n"
                print('lines333', last_result)

                with open(file_path, "w", encoding='utf-8-sig') as file:
                    file.write(last_result)

            else:
                print("아직 미션 진행중")
        else:


            if datetime.today().weekday() == 0:

                with open(file_path2, "w", encoding='utf-8-sig') as file:
                    file.write(str(nowDay) + ":" + str(refresh_time) + "\n")
                    # 월요일 갱신
                    print("월요일 갱신")
                    reset_schedule_ = ""
                    with open(file_path, "r", encoding='utf-8-sig') as file:
                        lines = file.read().splitlines()
                        lines = ' '.join(lines).split()

                        isSchedule_ = False
                        while isSchedule_ is False:
                            if lines == [] or lines == "":
                                print("스케쥴이 비었다 : myQuest_play_check")
                                with open(file_path3, "r", encoding='utf-8-sig') as file:
                                    schedule_ready = file.read()
                                with open(file_path, "w", encoding='utf-8-sig') as file:
                                    file.write(schedule_ready)
                                with open(file_path, "r", encoding='utf-8-sig') as file:
                                    lines = file.read().splitlines()
                            else:
                                isSchedule_ = True

                        for i in range(len(lines)):
                            complete_ = lines[i].split(":")
                            for j in range(len(complete_)):
                                if j < 3:
                                    reset_schedule_ += complete_[j] + ":"
                                if j == 3:
                                    reset_schedule_ += '대기중:'
                                if 3 < j < 7:
                                    reset_schedule_ += complete_[j] + ":"
                                if j == 7:
                                    reset_schedule_ += '대기중\n'
                        print('reset_schedule_', reset_schedule_)
                        with open(file_path, "w", encoding='utf-8-sig') as file:
                            file.write(reset_schedule_)
                        # with open(file_path3, "w", encoding='utf-8-sig') as file:
                        #     file.write(reset_schedule_)
            else:
                with open(file_path2, "w", encoding='utf-8-sig') as file:
                    file.write(str(nowDay) + ":" + str(refresh_time) + "\n")
                    # 월요일을 제외한 갱신
                    print("월요일을 제외한 갱신")
                    reset_schedule_ = ""
                    with open(file_path, "r", encoding='utf-8-sig') as file:
                        lines = file.read().splitlines()
                        lines = ' '.join(lines).split()

                        isSchedule_ = False
                        while isSchedule_ is False:
                            if lines == [] or lines == "":
                                print("스케쥴이 비었다 : myQuest_play_check")
                                with open(file_path3, "r", encoding='utf-8-sig') as file:
                                    schedule_ready = file.read()
                                with open(file_path, "w", encoding='utf-8-sig') as file:
                                    file.write(schedule_ready)
                                with open(file_path, "r", encoding='utf-8-sig') as file:
                                    lines = file.read().splitlines()
                            else:
                                isSchedule_ = True

                        for i in range(len(lines)):
                            complete_ = lines[i].split(":")
                            for j in range(len(complete_)):
                                if j < 3:
                                    reset_schedule_ += complete_[j] + ":"
                                if j == 3:
                                    reset_schedule_ += '대기중:'
                                if 3 < j < 7:
                                    reset_schedule_ += complete_[j] + ":"
                                if j == 7:

                                    reset_schedule_ += '대기중\n'

                        print('reset_schedule_', reset_schedule_)
                        with open(file_path, "w", encoding='utf-8-sig') as file:
                            file.write(reset_schedule_)
                        # with open(file_path3, "w", encoding='utf-8-sig') as file:
                        #     file.write(reset_schedule_)

            myQuest_play_add(cla, data)


            # 초기화 할때 변경해야할 전역 변수
            v_.dead_count = 0
            v_.daily_mission_ready = True


        add_result = 'check'
        return add_result

    except Exception as e:
        print(e)
        return 0



