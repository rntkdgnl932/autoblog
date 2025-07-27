# import random
# import pyautogui
# import pytesseract
# import numpy as np
# import numpy
# from PIL import Image
# import re
# import cv2

from PyQt5.QtTest import *

import time
import sys
import variable as v_

sys.path.append('C:/my_games/' + str(v_.game_folder) + '/' + str(v_.data_folder) + '/mymodule')


def go_test(cla):
    print('hi test!', cla)


def macro_out(cla):
    import os
    try:
        dir_path = "C:\\my_games\\load\\" + str(v_.game_folder)
        file_path = dir_path + "\\start.txt"
        # cla.txt
        cla_data = str(cla) + "cla"
        file_path2 = dir_path + "\\" + cla_data + ".txt"
        with open(file_path, "w", encoding='utf-8-sig') as file:
            data = 'no'
            file.write(str(data))
            time.sleep(0.2)
        with open(file_path2, "w", encoding='utf-8-sig') as file:
            data = cla
            file.write(str(data))
            time.sleep(0.2)
        os.execl(sys.executable, sys.executable, *sys.argv)



    except Exception as e:
        print(e)
        return 0

# 이미지 특정 색상 제외함
def image_processing(src, min_color, max_color):
    import cv2
    import numpy
    try:
        img_ = cv2.cvtColor(numpy.array(src), cv2.COLOR_RGB2BGR)
        exception_img = cv2.inRange(img_, min_color, max_color)
        return exception_img
    except Exception as e:
        print(e)
        return 0


def random_int():
    try:
        import random
        result = random.randint(1, 4)
        return int(result)
    except Exception as e:
        print(e)


def random_int_2():
    try:
        import random
        result = random.randint(100, 200)
        return result
    except Exception as e:
        print(e)


def random_int_3():
    try:
        import random
        result = random.randint(50, 100)
        return result
    except Exception as e:
        print(e)


def isNumber_(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def change_number_float(many_potion):
    import re
    try:

        potion_ = many_potion

        print("num ??? ", potion_)
        potion_.strip()
        if " " in potion_:
            potion_ = potion_.replace(' ', '')
            print("!!!!!! ['   '] !!!!!!!", potion_)
        # if "\n" in potion_:
        #     potion_ = potion_.replace('\n', '')
        #     print("!!!!!! [' 엔터 제거  '] !!!!!!!", potion_)
        if "고" in potion_:
            potion_ = potion_.replace('고', '2')
            print("!!!!!! [' 고 => 2 '] !!!!!!!", potion_)
        if "ㄷ" in potion_:
            potion_ = potion_.replace('ㄷ', '5')
            print("!!!!!! [' ㄷ => 5 '] !!!!!!!", potion_)
        if "요" in potion_:
            potion_ = potion_.replace('요', '8')
            print("!!!!!! [' 요 => 8 '] !!!!!!!", potion_)
        if "°" in potion_:
            potion_ = potion_.replace('°', '0')
            print("!!!!!! [   ° => 0   ] !!!!!!!", potion_)
        if ")" in potion_:
            potion_ = potion_.replace(')', '1')
            print("!!!!!! [   ) => 1   ] !!!!!!!", potion_)
        if "‘" in potion_:
            potion_ = potion_.replace('‘', '1')
            print("!!!!!! [   ‘ => 1   ] !!!!!!!", potion_)
        if "?" in potion_:
            potion_ = potion_.replace('?', '2')
            print("!!!!!! [   ? => 2  ] !!!!!!!", potion_)
        if "L" in potion_:
            potion_ = potion_.replace('L', '1')
            print("!!!!!! [   L => 1  ] !!!!!!!", potion_)
        if "|" in potion_:
            potion_ = potion_.replace('|', '1')
            print("!!!!!!![   | => 1  ]!!!!!!!!!!!", potion_)
        if "A" in potion_:
            potion_ = potion_.replace('A', '4')
            print("!!!!!!!!![  A => 4 ]!!!!!!!!!!!!!", potion_)
        if "D" in potion_:
            potion_ = potion_.replace('D', '2')
            print("!!!!!!!!![  D => 2 ]!!!!!!!!!!!!!", potion_)
        if "G" in potion_:
            potion_ = potion_.replace('G', '6')
            print("!!!!!!!!![  G => 6 ]!!!!!!!!!!!!!", potion_)
        if "B" in potion_:
            potion_ = potion_.replace('B', '8')
            print("!!!!!!!!![  B => 8  ]!!!!!!!!!!!!!", potion_)
        if "T" in potion_:
            potion_ = potion_.replace('T', '7')
            print("!!!!!!!!![  T => 7  ]!!!!!!!!!!!!!", potion_)
        if "S" in potion_:
            potion_ = potion_.replace('S', '5')
            print("!!!!!!!!![  S => 5  ]!!!!!!!!!!!!!", potion_)
        if "Q" in potion_:
            potion_ = potion_.replace('Q', '9')
            print("!!!!!!!!![  Q => 9  ]!!!!!!!!!!!!!", potion_)
        if "F" in potion_:
            potion_ = potion_.replace('F', '9')
            print("!!!!!!!!![  F => 9  ]!!!!!!!!!!!!!", potion_)
        if "R" in potion_:
            potion_ = potion_.replace('R', '8')
            print("!!!!!!!!![  R => 8  ]!!!!!!!!!!!!!", potion_)
        if "a" in potion_:
            potion_ = potion_.replace('a', '4')
            print("!!!!!!!!![  a => 4  ]!!!!!!!!!!!!!", potion_)
        if "g" in potion_:
            potion_ = potion_.replace('g', '9')
            print("!!!!!!!!![  g => 9  ]!!!!!!!!!!!!!", potion_)
        if "i" in potion_:
            potion_ = potion_.replace('i', '1')
            print("!!!!!!!!![  i => 1  ]!!!!!!!!!!!!!", potion_)
        if "l" in potion_:
            potion_ = potion_.replace('l', '1')
            print("!!!!!!!!![  l => 1  ]!!!!!!!!!!!!!", potion_)
        if "u" in potion_:
            potion_ = potion_.replace('u', '11')
            print("!!!!!!!!![  u => 11  ]!!!!!!!!!!!!!", potion_)
        if "s" in potion_:
            potion_ = potion_.replace('s', '5')
            print("!!!!!!!!![  s => 5  ]!!!!!!!!!!!!!", potion_)

        potion_ = potion_.replace(',', '').strip()
        potion_ = float(potion_)

        return potion_
    except Exception as e:
        print(e)


def change_number(many_potion):
    try:

        potion_ = many_potion

        for i in range(5):
            print("i", i)
            print("num ??? ", potion_)
            result_digit = potion_.isdigit()

            if result_digit == True:
                break
            else:
                if " " in potion_:
                    potion_ = potion_.replace(' ', '')
                    print("!!!!!! ['   '] !!!!!!!", potion_)
                if "고" in potion_:
                    potion_ = potion_.replace('고', '2')
                    print("!!!!!! [' 고 => 2 '] !!!!!!!", potion_)
                if "ㄷ" in potion_:
                    potion_ = potion_.replace('ㄷ', '5')
                    print("!!!!!! [' ㄷ => 5 '] !!!!!!!", potion_)
                if "요" in potion_:
                    potion_ = potion_.replace('요', '8')
                    print("!!!!!! [' 요 => 8 '] !!!!!!!", potion_)
                if "°" in potion_:
                    potion_ = potion_.replace('°', '0')
                    print("!!!!!! [   ° => 0   ] !!!!!!!", potion_)
                if ")" in potion_:
                    potion_ = potion_.replace(')', '1')
                    print("!!!!!! [   ) => 1   ] !!!!!!!", potion_)
                if "‘" in potion_:
                    potion_ = potion_.replace('‘', '1')
                    print("!!!!!! [   ‘ => 1   ] !!!!!!!", potion_)
                if "?" in potion_:
                    potion_ = potion_.replace('?', '2')
                    print("!!!!!! [   ? => 2  ] !!!!!!!", potion_)
                if "L" in potion_:
                    potion_ = potion_.replace('L', '1')
                    print("!!!!!! [   L => 1  ] !!!!!!!", potion_)
                if "|" in potion_:
                    potion_ = potion_.replace('|', '1')
                    print("!!!!!!![   | => 1  ]!!!!!!!!!!!", potion_)
                if "A" in potion_:
                    potion_ = potion_.replace('A', '4')
                    print("!!!!!!!!![  A => 4 ]!!!!!!!!!!!!!", potion_)
                if "D" in potion_:
                    potion_ = potion_.replace('D', '2')
                    print("!!!!!!!!![  D => 2 ]!!!!!!!!!!!!!", potion_)
                if "G" in potion_:
                    potion_ = potion_.replace('G', '6')
                    print("!!!!!!!!![  G => 6 ]!!!!!!!!!!!!!", potion_)
                if "B" in potion_:
                    potion_ = potion_.replace('B', '8')
                    print("!!!!!!!!![  B => 8  ]!!!!!!!!!!!!!", potion_)
                if "T" in potion_:
                    potion_ = potion_.replace('T', '7')
                    print("!!!!!!!!![  T => 7  ]!!!!!!!!!!!!!", potion_)
                if "S" in potion_:
                    potion_ = potion_.replace('S', '5')
                    print("!!!!!!!!![  S => 5  ]!!!!!!!!!!!!!", potion_)
                if "Q" in potion_:
                    potion_ = potion_.replace('Q', '9')
                    print("!!!!!!!!![  Q => 9  ]!!!!!!!!!!!!!", potion_)
                if "F" in potion_:
                    potion_ = potion_.replace('F', '9')
                    print("!!!!!!!!![  F => 9  ]!!!!!!!!!!!!!", potion_)
                if "R" in potion_:
                    potion_ = potion_.replace('R', '8')
                    print("!!!!!!!!![  R => 8  ]!!!!!!!!!!!!!", potion_)
                if "a" in potion_:
                    potion_ = potion_.replace('a', '4')
                    print("!!!!!!!!![  a => 4  ]!!!!!!!!!!!!!", potion_)
                if "g" in potion_:
                    potion_ = potion_.replace('g', '9')
                    print("!!!!!!!!![  g => 9  ]!!!!!!!!!!!!!", potion_)
                if "u" in potion_:
                    potion_ = potion_.replace('u', '11')
                    print("!!!!!!!!![  u => 11  ]!!!!!!!!!!!!!", potion_)
                if "s" in potion_:
                    potion_ = potion_.replace('s', '5')
                    print("!!!!!!!!![  s => 5  ]!!!!!!!!!!!!!", potion_)

        potion_ = int_put_(potion_)

        if potion_[0] == "0":
            potion_ = "1" + potion_
            print("potion_ = '1' + potion_", potion_)

        return potion_
    except Exception as e:
        print(e)


def int_put_(data):
    try:
        import re
        data_ = data.replace(',', '').strip()
        data_2 = data_.replace('.', '').strip()
        data_3 = data_2.replace(' ', '').strip()
        data_4 = data_3.replace('/', '').strip()

        # data_2 = data_.strip().replace('.', '')
        # data_3 = data_2.strip().replace(' ', '')
        # data_4 = data_3.strip().replace('/', '')
        result = re.sub(r'[^0-9]', '', data_4)
        return result
    except ValueError:
        return False


def float_put_(data):
    try:
        import re
        data_ = data.replace(',', '').strip()
        data_2 = data_.replace('.', '').strip()
        data_3 = data_2.replace(' ', '').strip()
        data_4 = data_3.replace('/', '').strip()

        # data_2 = data_.strip().replace('.', '')
        # data_3 = data_2.strip().replace(' ', '')
        # data_4 = data_3.strip().replace('/', '')
        result = re.sub(r'[^0-9]', '', data_4)
        return result
    except ValueError:
        return False


def in_number_check(data):
    import cv2
    import numpy as np
    try:

        isNumber = False
        # print("들어온 데이타?", data)
        # print("len potion", len(data))
        if len(data) > 0:
            # print("길이가 0 보다 크다", len(data))
            for i in range(len(data)):
                result_num_bool = data[i].isdigit()
                if result_num_bool == True:
                    isNumber = True
        else:
            print("데이터가 길이가 없고 비어있다")

        return isNumber
    except Exception as e:
        print(e)


def imgs_set(a, b, c, d, cla, img):
    try:
        from PIL import ImageGrab
        from functools import partial
        import pyautogui

        ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

        if cla == 'one':
            plus = 0
        if cla == 'two':
            plus = 960
        if cla == 'three':
            plus = 960 * 2
        if cla == 'four':
            plus = 960 * 3
        if cla == 'five':
            plus = 960 * 4
        if cla == 'six':
            plus = 960 * 5

        result = pyautogui.locateCenterOnScreen(img, region=(a + plus, b, c - a + 10, d - b + 10),
                                                confidence=0.7)
        return result
    except ValueError:
        return False


def imgs_set_(a, b, c, d, cla, img, data):
    try:
        from PIL import ImageGrab
        from functools import partial
        import pyautogui

        ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

        if cla == 'one':
            plus = 0
        if cla == 'two':
            plus = 960
        if cla == 'three':
            plus = 960 * 2
        if cla == 'four':
            plus = 960 * 3
        if cla == 'five':
            plus = 960 * 4
        if cla == 'six':
            plus = 960 * 5

        # pos = (a + plus, b, c - a, d - b)
        # pyautogui.screenshot("asd.png", region=pos)

        result = pyautogui.locateCenterOnScreen(img, region=(a + plus, b, c - a, d - b),
                                                confidence=data)
        return result
    except ValueError:
        return False


def imgs_set_num(a, b, c, d, cla, img, data):
    try:
        from PIL import ImageGrab
        from functools import partial
        import pyautogui

        ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

        if cla == 'one':
            plus = 0
        if cla == 'two':
            plus = 960
        if cla == 'three':
            plus = 960 * 2
        if cla == 'four':
            plus = 960 * 3
        if cla == 'five':
            plus = 960 * 4
        if cla == 'six':
            plus = 960 * 5

        # pos = (a + plus, b, c - a, d - b)
        # pyautogui.screenshot("asd.png", region=pos)

        result = pyautogui.locateCenterOnScreen(img, region=(a + plus, b, c - a, d - b),
                                                confidence=data)
        return result
    except ValueError:
        return False


def imgs_set_reg(a, b, c, d, cla, img, data):
    try:
        from PIL import ImageGrab
        from functools import partial
        import pyautogui

        ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

        if cla == 'one':
            plus = 0
        if cla == 'two':
            plus = 0
        if cla == 'three':
            plus = 0
        if cla == 'four':
            plus = 0
        if cla == 'five':
            plus = 0
        if cla == 'six':
            plus = 0

        # pos = (a + plus, b, c - a, d - b)
        # pyautogui.screenshot("asd.png", region=pos)

        result = pyautogui.locateCenterOnScreen(img, region=(a + plus, b, c - a, d - b),
                                                confidence=data)
        return result
    except ValueError:
        return False


def imgs_set_for(a, b, c, d, cla, img, data):
    try:
        from PIL import ImageGrab
        from functools import partial
        import pyautogui

        ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

        # 예시
        # full_path = "c:\\my_games\\arthdal\\data_arthdal\\imgs\\jadong\\bookmark_star.PNG"
        # img_array = np.fromfile(full_path, np.uint8)
        # img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        # imgs_ = imgs_set_for(870, 420, 950, 720, cla, img, 0.85)
        # if imgs_ is not None and imgs_ != False:
        #     print("bookmark_star", imgs_)
        #     for i in range(len(imgs_)):
        #         print("imgs_", i, imgs_[i])
        #         print("imgs_", i, imgs_[i][0])
        #         print("imgs_", i, imgs_[i][1])

        if cla == 'one':
            plus = 0
        if cla == 'two':
            plus = 960
        if cla == 'three':
            plus = 960 * 2
        if cla == 'four':
            plus = 960 * 3
        if cla == 'five':
            plus = 960 * 4
        if cla == 'six':
            plus = 960 * 5

        regs = []

        for i in pyautogui.locateAllOnScreen(img, region=(a + plus, b, c - a, d - b), confidence=data):
            print('i', i)
            last_x = i.left + int(i.width / 2)
            last_y = i.top + int(i.height / 2)
            last = [last_x, last_y]
            regs.append(last)

        return regs
    except ValueError:
        return False


def click_with_image(image_path):
    try:
        from PIL import ImageGrab
        from functools import partial
        import pyautogui

        ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

        isClick = False
        data_count = 0
        while isClick is False:
            data_count += 1
            if data_count > 7:
                isClick = True
            location = pyautogui.locateOnScreen(image_path)
            if location is not None:
                pyautogui.click(location)
                isClick = True
    except Exception as e:
        print(e)


def get_region(start_x, start_y, end_x, end_y, cla):
    coordinate = 0
    if cla == 'one':
        coordinate = 0
    if cla == 'two':
        coordinate = 960
    if cla == 'three':
        coordinate = 960 * 2
    if cla == 'four':
        coordinate = 960 * 3
    if cla == 'five':
        coordinate = 960 * 4
    if cla == 'six':
        coordinate = 960 * 5

    value = (start_x + coordinate, start_y, end_x - start_x, end_y - start_y)
    return value


def click_pos(pos):
    try:
        import pyautogui
        pyautogui.moveTo(pos[0] + random_int(), pos[1] + random_int())
        time.sleep(random_int())
        pyautogui.click()
    except Exception as e:
        print(e)


def mouse_move(x, y):
    import pydirectinput
    try:
        reg_x = x + random_int()
        reg_y = y + random_int()
        pydirectinput.moveTo(reg_x, reg_y)
        print("mouse_move", reg_x, reg_y)

    except Exception as e:
        print(e)
        return 0


def win_left_move(cla):
    try:
        import serial

        arduino_port = v_.COM_
        baudrate = v_.speed_

        print("win_left_move", cla)

        ser = serial.Serial(arduino_port, baudrate)

        moveX = 0
        moveY = 0
        moveZ = 7

        data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
        ser.write(data.encode())

        ser.close()
        QTest.qWait(10)

    except Exception as e:
        print(e)
        return 0


def win_right_move(cla):
    try:
        import serial

        arduino_port = v_.COM_
        baudrate = v_.speed_

        print("win_right_move", cla)

        ser = serial.Serial(arduino_port, baudrate)

        moveX = 0
        moveY = 0
        moveZ = 6

        data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
        ser.write(data.encode())

        ser.close()
        QTest.qWait(10)

    except Exception as e:
        print(e)
        return 0


def click_pos_2(pos_1, pos_2, cla):
    try:
        import serial
        import pyautogui

        pos_1 = int(pos_1)
        pos_2 = int(pos_2)

        coordinate = 0
        if cla == 'one':
            coordinate = 0
        if cla == 'two':
            coordinate = 960
        if cla == 'three':
            coordinate = 960 * 2
        if cla == 'four':
            coordinate = 960 * 3
        if cla == 'five':
            coordinate = 960 * 4
        if cla == 'six':
            coordinate = 960 * 5

        pyautogui.moveTo(pos_1 + coordinate, pos_2)

        if v_.now_arduino == "on":
            arduino_port = v_.COM_
            baudrate = v_.speed_

            ser = serial.Serial(arduino_port, baudrate)

            moveZ = 1
            k_reg = v_.mouse_speed
            c_reg = v_.mouse_pm

            move_ = False
            move_count = 0
            while move_ is False:
                move_count += 1
                if move_count > v_.mouse_move_count:
                    print("move_count", move_count)
                    move_ = True

                # 이동 시킬 포인트 계산
                x_reg = pos_1 + coordinate - pyautogui.position()[0]
                y_reg = pos_2 - pyautogui.position()[1]
                # if move_count > 280:
                #     print("이동 시킬 포인트 계산 y_reg", y_reg)

                if -c_reg < x_reg < c_reg:
                    moveX = x_reg
                elif x_reg > 0:
                    if x_reg == k_reg:
                        moveX = x_reg
                    else:
                        moveX = min(k_reg, x_reg)
                else:
                    if x_reg == -k_reg:
                        moveX = x_reg
                    else:
                        moveX = max(-k_reg, x_reg)

                if -c_reg < y_reg < c_reg:
                    moveY = y_reg
                elif y_reg > 0:
                    if y_reg == k_reg:
                        moveY = y_reg
                    else:
                        moveY = min(k_reg, y_reg)
                else:
                    if y_reg == -k_reg:
                        moveY = y_reg
                    else:
                        moveY = max(-k_reg, y_reg)

                # # 이동 시킬 포인트 결과값
                # print("이동 시킬 포인트 결과값 moveY", moveY)

                data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
                ser.write(data.encode())
                received_data = ser.readline().decode().strip()

                if -c_reg < moveX < c_reg and -c_reg < moveY < c_reg:
                    x_reg = pos_1 + coordinate - pyautogui.position()[0]
                    y_reg = pos_2 - pyautogui.position()[1]
                    if -c_reg < x_reg < c_reg and -c_reg < y_reg < c_reg and pyautogui.position()[1] >= 31:
                        # print("move_count", move_count)
                        # print("moveX", moveX)
                        # print("moveY", moveY)
                        # print("x_reg", x_reg)
                        # print("y_reg", y_reg)
                        move_ = True

                        # moveZ = 2
                        # data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
                        # ser.write(data.encode())

                        moveX = 0
                        moveY = 0
                        moveZ = 3
                        data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
                        ser.write(data.encode())

                        time.sleep(0.1)

                        moveX = 0
                        moveY = 0
                        moveZ = 4
                        data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
                        ser.write(data.encode())

                # else:
                #     print("아직 오차 범위 밖이다...", move_count)
                #     print("x_reg", x_reg)
                #     print("y_reg", y_reg)
            ser.close()
            QTest.qWait(10)
        else:

            # pyautogui.moveTo(pos_1 + random_int() + coordinate, pos_2 + random_int())
            # time.sleep(0.2)
            pyautogui.click(pos_1 + random_int() + coordinate, pos_2 + random_int())
        time.sleep(0.1)

    except Exception as e:
        print("error:", e)


def click_pos_reg(pos_1, pos_2, cla):
    import serial
    import pyautogui
    try:

        pos_1 = int(pos_1)
        pos_2 = int(pos_2)

        coordinate = 0
        if cla == 'one':
            coordinate = 0
        if cla == 'two':
            coordinate = 0
        if cla == 'three':
            coordinate = 0
        if cla == 'four':
            coordinate = 0
        if cla == 'five':
            coordinate = 0
        if cla == 'six':
            coordinate = 0

        pyautogui.moveTo(pos_1 + coordinate, pos_2)

        if v_.now_arduino == "on":
            arduino_port = v_.COM_
            baudrate = v_.speed_

            ser = serial.Serial(arduino_port, baudrate)

            moveZ = 1
            k_reg = v_.mouse_speed
            c_reg = v_.mouse_pm

            move_ = False
            move_count = 0
            while move_ is False:
                move_count += 1
                if move_count > v_.mouse_move_count:
                    move_ = True

                # 이동 시킬 포인트 계산
                x_reg = pos_1 + coordinate - pyautogui.position()[0]
                y_reg = pos_2 - pyautogui.position()[1]

                if -c_reg < x_reg < c_reg:
                    moveX = x_reg
                elif x_reg > 0:
                    if x_reg == k_reg:
                        moveX = x_reg
                    else:
                        moveX = min(k_reg, x_reg)
                else:
                    if x_reg == -k_reg:
                        moveX = x_reg
                    else:
                        moveX = max(-k_reg, x_reg)

                if -c_reg < y_reg < c_reg:
                    moveY = y_reg
                elif y_reg > 0:
                    if y_reg == k_reg:
                        moveY = y_reg
                    else:
                        moveY = min(k_reg, y_reg)
                else:
                    if y_reg == -k_reg:
                        moveY = y_reg
                    else:
                        moveY = max(-k_reg, y_reg)

                data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
                ser.write(data.encode())
                received_data = ser.readline().decode().strip()

                if received_data == '0' or (-c_reg < moveX < c_reg and -c_reg < moveY < c_reg):
                    x_reg = pos_1 + coordinate - pyautogui.position()[0]
                    y_reg = pos_2 - pyautogui.position()[1]
                    if -c_reg < x_reg < c_reg and -c_reg < y_reg < c_reg and pyautogui.position()[1] >= 31:
                        move_ = True

                        # moveZ = 2
                        # data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
                        # ser.write(data.encode())

                        moveX = 0
                        moveY = 0
                        moveZ = 3
                        data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
                        ser.write(data.encode())

                        time.sleep(0.1)

                        moveX = 0
                        moveY = 0
                        moveZ = 4
                        data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
                        ser.write(data.encode())

                        # drag_pos_Press()
                        # time.sleep(0.1)
                        # drag_pos_Release()

            ser.close()
            QTest.qWait(10)
        else:

            # pyautogui.moveTo(pos_1 + random_int() + coordinate, pos_2 + random_int())

            pyautogui.click(pos_1 + random_int() + coordinate, pos_2 + random_int())
        time.sleep(0.1)


    except Exception as e:
        print("error:", e)


def mouse_move_cpp(pos_1, pos_2, cla):
    try:
        import serial
        import pyautogui

        pos_1 = int(pos_1)
        pos_2 = int(pos_2)

        arduino_port = v_.COM_
        baudrate = v_.speed_

        coordinate = 0
        if cla == 'one':
            coordinate = 0
        if cla == 'two':
            coordinate = 960
        if cla == 'three':
            coordinate = 960 * 2
        if cla == 'four':
            coordinate = 960 * 3
        if cla == 'five':
            coordinate = 960 * 4
        if cla == 'six':
            coordinate = 960 * 5

        pyautogui.moveTo(pos_1 + coordinate, pos_2)

        if v_.now_arduino == "on":

            ser = serial.Serial(arduino_port, baudrate)

            moveZ = 1
            k_reg = v_.mouse_speed
            c_reg = v_.mouse_pm

            move_ = False
            move_count = 0
            while move_ is False:
                move_count += 1
                if move_count > v_.mouse_move_count:
                    move_ = True

                # 이동 시킬 포인트 계산
                x_reg = pos_1 + coordinate - pyautogui.position()[0]
                y_reg = pos_2 - pyautogui.position()[1]

                if -c_reg < x_reg < c_reg:
                    moveX = x_reg
                elif x_reg > 0:
                    if x_reg == k_reg:
                        moveX = x_reg
                    else:
                        moveX = min(k_reg, x_reg)
                else:
                    if x_reg == -k_reg:
                        moveX = x_reg
                    else:
                        moveX = max(-k_reg, x_reg)

                if -c_reg < y_reg < c_reg:
                    moveY = y_reg
                elif y_reg > 0:
                    if y_reg == k_reg:
                        moveY = y_reg
                    else:
                        moveY = min(k_reg, y_reg)
                else:
                    if y_reg == -k_reg:
                        moveY = y_reg
                    else:
                        moveY = max(-k_reg, y_reg)

                data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
                ser.write(data.encode())
                received_data = ser.readline().decode().strip()

                if -c_reg < moveX < c_reg and -c_reg < moveY < c_reg:
                    x_reg = pos_1 + coordinate - pyautogui.position()[0]
                    y_reg = pos_2 - pyautogui.position()[1]
                    if -c_reg < x_reg < c_reg and -c_reg < y_reg < c_reg and pyautogui.position()[1] >= 31:
                        move_ = True
                        data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
                        ser.write(data.encode())

            ser.close()
            QTest.qWait(10)
        else:
            pyautogui.moveTo(pos_1 + random_int() + coordinate, pos_2 + random_int(), 0.1)

    except Exception as e:
        print("error:", e)


def mouse_move_cpp_reg(pos_1, pos_2, cla):
    try:
        import serial
        import pyautogui

        pos_1 = int(pos_1)
        pos_2 = int(pos_2)

        arduino_port = v_.COM_
        baudrate = v_.speed_

        coordinate = 0

        # pyautogui.moveTo(pos_1 + coordinate, pos_2)

        if v_.now_arduino == "on":

            ser = serial.Serial(arduino_port, baudrate)

            moveZ = 1
            k_reg = v_.mouse_speed
            c_reg = v_.mouse_pm

            move_ = False
            move_count = 0
            while move_ is False:
                move_count += 1
                if move_count > v_.mouse_move_count:
                    move_ = True

                # 이동 시킬 포인트 계산
                x_reg = pos_1 + coordinate - pyautogui.position()[0]
                y_reg = pos_2 - pyautogui.position()[1]

                if -c_reg < x_reg < c_reg:
                    moveX = x_reg
                elif x_reg > 0:
                    if x_reg == k_reg:
                        moveX = x_reg
                    else:
                        moveX = min(k_reg, x_reg)
                else:
                    if x_reg == -k_reg:
                        moveX = x_reg
                    else:
                        moveX = max(-k_reg, x_reg)

                if -c_reg < y_reg < c_reg:
                    moveY = y_reg
                elif y_reg > 0:
                    if y_reg == k_reg:
                        moveY = y_reg
                    else:
                        moveY = min(k_reg, y_reg)
                else:
                    if y_reg == -k_reg:
                        moveY = y_reg
                    else:
                        moveY = max(-k_reg, y_reg)

                data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
                ser.write(data.encode())
                received_data = ser.readline().decode().strip()

                if -c_reg < moveX < c_reg and -c_reg < moveY < c_reg:
                    x_reg = pos_1 + coordinate - pyautogui.position()[0]
                    y_reg = pos_2 - pyautogui.position()[1]
                    if -c_reg < x_reg < c_reg and -c_reg < y_reg < c_reg and pyautogui.position()[1] >= 31:
                        move_ = True
                        data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
                        ser.write(data.encode())

            ser.close()
            QTest.qWait(10)
        else:
            pyautogui.moveTo(pos_1 + random_int() + coordinate, pos_2 + random_int(), 0.1)

    except Exception as e:
        print("error:", e)


def mouse_move_drag(pos_1, pos_2, cla, speed):
    try:
        import serial
        import pyautogui

        pos_1 = int(pos_1)
        pos_2 = int(pos_2)

        arduino_port = v_.COM_
        baudrate = v_.speed_

        coordinate = 0
        if cla == 'one':
            coordinate = 0
        if cla == 'two':
            coordinate = 960
        if cla == 'three':
            coordinate = 960 * 2
        if cla == 'four':
            coordinate = 960 * 3
        if cla == 'five':
            coordinate = 960 * 4
        if cla == 'six':
            coordinate = 960 * 5

        if v_.now_arduino == "on":

            ser = serial.Serial(arduino_port, baudrate)

            moveZ = 1
            k_reg = speed
            c_reg = v_.mouse_pm

            move_ = False
            move_count = 0
            while move_ is False:
                move_count += 1
                if move_count > v_.mouse_move_count:
                    move_ = True

                # 이동 시킬 포인트 계산
                x_reg = pos_1 + coordinate - pyautogui.position()[0]
                y_reg = pos_2 - pyautogui.position()[1]

                if -c_reg < x_reg < c_reg:
                    moveX = x_reg
                elif x_reg > 0:
                    if x_reg == k_reg:
                        moveX = x_reg
                    else:
                        moveX = min(k_reg, x_reg)
                else:
                    if x_reg == -k_reg:
                        moveX = x_reg
                    else:
                        moveX = max(-k_reg, x_reg)

                if -c_reg < y_reg < c_reg:
                    moveY = y_reg
                elif y_reg > 0:
                    if y_reg == k_reg:
                        moveY = y_reg
                    else:
                        moveY = min(k_reg, y_reg)
                else:
                    if y_reg == -k_reg:
                        moveY = y_reg
                    else:
                        moveY = max(-k_reg, y_reg)

                data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
                ser.write(data.encode())
                received_data = ser.readline().decode().strip()

                if -c_reg < moveX < c_reg and -c_reg < moveY < c_reg:
                    x_reg = pos_1 + coordinate - pyautogui.position()[0]
                    y_reg = pos_2 - pyautogui.position()[1]
                    if -c_reg < x_reg < c_reg and -c_reg < y_reg < c_reg and pyautogui.position()[1] >= 31:
                        move_ = True
                        data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
                        ser.write(data.encode())

            ser.close()
            QTest.qWait(10)
        else:
            pyautogui.moveTo(pos_1 + random_int() + coordinate, pos_2 + random_int(), 0.1)

    except Exception as e:
        print("error:", e)


def mouse_move_drag_reg(pos_1, pos_2, cla, speed):
    try:
        import serial
        import pyautogui

        pos_1 = int(pos_1)
        pos_2 = int(pos_2)

        arduino_port = v_.COM_
        baudrate = v_.speed_

        coordinate = 0

        if v_.now_arduino == "on":

            ser = serial.Serial(arduino_port, baudrate)

            moveZ = 1
            k_reg = speed
            c_reg = v_.mouse_pm

            move_ = False
            move_count = 0
            while move_ is False:
                move_count += 1
                if move_count > v_.mouse_move_count:
                    move_ = True

                # 이동 시킬 포인트 계산
                x_reg = pos_1 + coordinate - pyautogui.position()[0]
                y_reg = pos_2 - pyautogui.position()[1]

                if -c_reg < x_reg < c_reg:
                    moveX = x_reg
                elif x_reg > 0:
                    if x_reg == k_reg:
                        moveX = x_reg
                    else:
                        moveX = min(k_reg, x_reg)
                else:
                    if x_reg == -k_reg:
                        moveX = x_reg
                    else:
                        moveX = max(-k_reg, x_reg)

                if -c_reg < y_reg < c_reg:
                    moveY = y_reg
                elif y_reg > 0:
                    if y_reg == k_reg:
                        moveY = y_reg
                    else:
                        moveY = min(k_reg, y_reg)
                else:
                    if y_reg == -k_reg:
                        moveY = y_reg
                    else:
                        moveY = max(-k_reg, y_reg)

                data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
                ser.write(data.encode())
                received_data = ser.readline().decode().strip()

                if -c_reg < moveX < c_reg and -c_reg < moveY < c_reg:
                    x_reg = pos_1 + coordinate - pyautogui.position()[0]
                    y_reg = pos_2 - pyautogui.position()[1]
                    if -c_reg < x_reg < c_reg and -c_reg < y_reg < c_reg and pyautogui.position()[1] >= 31:
                        move_ = True
                        data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
                        ser.write(data.encode())

            ser.close()
            QTest.qWait(10)


        else:
            pyautogui.moveTo(pos_1 + random_int() + coordinate, pos_2 + random_int(), 0.1)

    except Exception as e:
        print("error:", e)


def mouse_move_adu_drag(pos_1, pos_2, cla):
    try:
        import serial
        import pyautogui

        pos_1 = int(pos_1)
        pos_2 = int(pos_2)

        arduino_port = v_.COM_
        baudrate = v_.speed_

        coordinate = 0
        if cla == 'one':
            coordinate = 0
        if cla == 'two':
            coordinate = 960
        if cla == 'three':
            coordinate = 960 * 2
        if cla == 'four':
            coordinate = 960 * 3
        if cla == 'five':
            coordinate = 960 * 4
        if cla == 'six':
            coordinate = 960 * 5

        # if v_.now_arduino == "on":
        #
        #     ser = serial.Serial(arduino_port, baudrate)
        #
        #     moveZ = 1
        #     k_reg = v_.mouse_speed
        #     c_reg = v_.mouse_pm
        #
        #     move_ = False
        #     move_count = 0
        #     while move_ is False:
        #         move_count += 1
        #         if move_count > v_.mouse_move_count:
        #             move_ = True
        #
        #
        #
        #         # 이동 시킬 포인트 계산
        #         x_reg = pos_1 + coordinate - pyautogui.position()[0]
        #         y_reg = pos_2 - pyautogui.position()[1]
        #
        #         if -c_reg < x_reg < c_reg:
        #             moveX = x_reg
        #         elif x_reg > 0:
        #             if x_reg == k_reg:
        #                 moveX = x_reg
        #             else:
        #                 moveX = min(k_reg, x_reg)
        #         else:
        #             if x_reg == -k_reg:
        #                 moveX = x_reg
        #             else:
        #                 moveX = max(-k_reg, x_reg)
        #
        #         if -c_reg < y_reg < c_reg:
        #             moveY = y_reg
        #         elif y_reg > 0:
        #             if y_reg == k_reg:
        #                 moveY = y_reg
        #             else:
        #                 moveY = min(k_reg, y_reg)
        #         else:
        #             if y_reg == -k_reg:
        #                 moveY = y_reg
        #             else:
        #                 moveY = max(-k_reg, y_reg)
        #
        #         data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
        #         ser.write(data.encode())
        #         received_data = ser.readline().decode().strip()
        #
        #         if -c_reg < moveX < c_reg and -c_reg < moveY < c_reg:
        #             x_reg = pos_1 + coordinate - pyautogui.position()[0]
        #             y_reg = pos_2 - pyautogui.position()[1]
        #             if -c_reg < x_reg < c_reg and -c_reg < y_reg < c_reg and pyautogui.position()[1] >= 31:
        #                 move_ = True
        #                 data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
        #                 ser.write(data.encode())
        #
        #
        #     ser.close()
        #     QTest.qWait(10)
        # else:
        pyautogui.moveTo(pos_1 + random_int() + coordinate, pos_2 + random_int(), 0.1)

    except Exception as e:
        print("error:", e)


def drag_pos_Press():
    try:
        import serial
        import pyautogui

        arduino_port = v_.COM_
        baudrate = v_.speed_

        ser = serial.Serial(arduino_port, baudrate)

        # 마우스 누르기
        moveX = 0
        moveY = 0
        moveZ = 3
        data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
        ser.write(data.encode())

        ser.close()
        QTest.qWait(10)

    except Exception as e:
        print("error:", e)


def drag_pos_Release():
    try:
        import serial
        import pyautogui

        arduino_port = v_.COM_
        baudrate = v_.speed_

        ser = serial.Serial(arduino_port, baudrate)
        # 마우스 떼기
        moveX = 0
        moveY = 0
        moveZ = 4
        data = f'x = {moveX}, y = {moveY}, z = {moveZ}\n'
        ser.write(data.encode())

        ser.close()
        QTest.qWait(10)

    except Exception as e:
        print("error:", e)


def drag_pos(pos_1, pos_2, pos_3, pos_4, cla):
    try:
        import pyautogui

        if cla == 'one':
            coordinate = 0
        if cla == 'two':
            coordinate = 960
        if cla == 'three':
            coordinate = 960 * 2
        if cla == 'four':
            coordinate = 960 * 3
        if cla == 'five':
            coordinate = 960 * 4
        if cla == 'six':
            coordinate = 960 * 5

        pyautogui.moveTo(pos_1 + coordinate, pos_2)

        if v_.now_arduino == "on":

            # 마우스 이동
            mouse_move_drag(pos_1, pos_2, cla, 20)

            # 0.1초
            time.sleep(0.1)
            # 마우스 누르기
            drag_pos_Press()
            # # 0.2초
            time.sleep(0.3)
            # 마우스 이동
            mouse_move_drag(pos_3, pos_4, cla, 3)
            # # 0.2초
            time.sleep(0.2)
            # 마우스 떼기
            drag_pos_Release()
            # 0.2초
            time.sleep(0.5)

        else:
            mouse_move_cpp(pos_1, pos_2, cla)
            pyautogui.dragTo(pos_3 + random_int() + coordinate, pos_4 + random_int(), 0.5, button='left')
            time.sleep(0.3)


    except Exception as e:
        print("error:", e)


def drag_pos_py(pos_1, pos_2, pos_3, pos_4, cla):
    try:
        import pyautogui

        if cla == 'one':
            coordinate = 0
        if cla == 'two':
            coordinate = 960
        if cla == 'three':
            coordinate = 960 * 2
        if cla == 'four':
            coordinate = 960 * 3
        if cla == 'five':
            coordinate = 960 * 4
        if cla == 'six':
            coordinate = 960 * 5

        mouse_move_cpp(pos_1, pos_2, cla)
        pyautogui.dragTo(pos_3 + random_int() + coordinate, pos_4 + random_int(), 0.5, button='left')
        time.sleep(0.3)


    except Exception as e:
        print("error:", e)


def drag_pos_click(pos_1, pos_2, pos_3, pos_4, cla):
    try:
        import pyautogui

        if cla == 'one':
            coordinate = 0
        if cla == 'two':
            coordinate = 960
        if cla == 'three':
            coordinate = 960 * 2
        if cla == 'four':
            coordinate = 960 * 3
        if cla == 'five':
            coordinate = 960 * 4
        if cla == 'six':
            coordinate = 960 * 5

        click_pos_2(pos_1, pos_2, cla)

        if v_.now_arduino == "on":

            # 마우스 이동
            mouse_move_drag(pos_1, pos_2, cla, 20)

            # 0.1초
            time.sleep(0.1)
            # 마우스 누르기
            drag_pos_Press()
            # # 0.2초
            time.sleep(0.2)
            # 마우스 이동
            mouse_move_drag(pos_3, pos_4, cla, 5)
            # # 0.2초
            time.sleep(0.2)
            # 마우스 떼기
            drag_pos_Release()
            # 0.2초
            time.sleep(0.5)

        else:
            mouse_move_cpp(pos_1, pos_2, cla)
            pyautogui.dragTo(pos_3 + random_int() + coordinate, pos_4 + random_int(), 0.5, button='left')
            time.sleep(0.3)


    except Exception as e:
        print("error:", e)


def drag_pos_reg(pos_1, pos_2, pos_3, pos_4, cla):
    try:
        import pyautogui

        coordinate = 0
        if cla == 'one':
            coordinate = 0
        if cla == 'two':
            coordinate = 0
        if cla == 'three':
            coordinate = 0
        if cla == 'four':
            coordinate = 0
        if cla == 'five':
            coordinate = 0
        if cla == 'six':
            coordinate = 0

        pyautogui.moveTo(pos_1 + coordinate, pos_2)

        if v_.now_arduino == "on":
            cla = "one"
            # 마우스 이동
            mouse_move_drag_reg(pos_1, pos_2, cla, 20)

            # 0.1초
            time.sleep(0.1)
            # 마우스 누르기
            drag_pos_Press()
            # 0.2초
            time.sleep(0.2)
            # 마우스 이동
            mouse_move_drag_reg(pos_3, pos_4, cla, 5)
            # 0.2초
            time.sleep(0.2)
            # 마우스 떼기
            drag_pos_Release()
            # 0.5초
            time.sleep(0.5)
        else:
            pyautogui.moveTo(pos_1 + random_int() + coordinate, pos_2 + random_int(), 0.5)
            pyautogui.dragTo(pos_3 + random_int() + coordinate, pos_4 + random_int(), 0.5)
            time.sleep(0.3)

    except Exception as e:
        print("error:", e)


def drag_pos_reg_py(pos_1, pos_2, pos_3, pos_4, cla):
    try:
        import pyautogui

        coordinate = 0
        if cla == 'one':
            coordinate = 0
        if cla == 'two':
            coordinate = 0
        if cla == 'three':
            coordinate = 0
        if cla == 'four':
            coordinate = 0
        if cla == 'five':
            coordinate = 0
        if cla == 'six':
            coordinate = 0

        pyautogui.moveTo(pos_1 + random_int() + coordinate, pos_2 + random_int(), 0.5)
        pyautogui.dragTo(pos_3 + random_int() + coordinate, pos_4 + random_int(), 0.5)
        time.sleep(0.3)

    except Exception as e:
        print("error:", e)


def drag_pos_reg_click(pos_1, pos_2, pos_3, pos_4, cla):
    try:
        import pyautogui

        coordinate = 0
        if cla == 'one':
            coordinate = 0
        if cla == 'two':
            coordinate = 0
        if cla == 'three':
            coordinate = 0
        if cla == 'four':
            coordinate = 0
        if cla == 'five':
            coordinate = 0
        if cla == 'six':
            coordinate = 0

        click_pos_reg(pos_1, pos_2, cla)

        if v_.now_arduino == "on":
            cla = "one"
            # 마우스 이동
            mouse_move_drag_reg(pos_1, pos_2, cla, 20)

            # 0.1초
            time.sleep(0.1)
            # 마우스 누르기
            drag_pos_Press()
            # 0.2초
            time.sleep(0.2)
            # 마우스 이동
            mouse_move_drag_reg(pos_3, pos_4, cla, 5)
            # 0.2초
            time.sleep(0.2)
            # 마우스 떼기
            drag_pos_Release()
            # 0.5초
            time.sleep(0.5)
        else:
            pyautogui.moveTo(pos_1 + random_int() + coordinate, pos_2 + random_int(), 0.5)
            pyautogui.dragTo(pos_3 + random_int() + coordinate, pos_4 + random_int(), 0.5)
            time.sleep(0.3)

    except Exception as e:
        print("error:", e)


# def text_check(posX1, posY1, posX2, posY2, text, method, method_pos):
#     try:
#         isClick = False
#         pos = (posX1, posY1, posX2 - posX1, posY2 - posY1)
#         while isClick is False:
#             pic = pyautogui.screenshot("asd.png", region=pos)
#             pic_ = numpy.array(pic)
#             # result = reader.readtext(pic_)
#             for txt in result:
#                 if txt is not None:
#                     print(txt[1])
#                     for text_ in text:
#                         if txt[1] == text_:
#                             print("aaa!!")
#                             method(method_pos)
#                             isClick = True
#     except Exception as e:
#         print(e)

def text_check_potion(posX1, posY1, posX2, posY2, cla):
    try:
        from PIL import ImageGrab
        from functools import partial
        import pyautogui
        import pytesseract

        ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

        potion = 0

        # result = pyautogui.locateCenterOnScreen(img, region=(a + plus, b, c - a + 10, d - b + 10),
        #                                         confidence=0.7)

        img = pyautogui.screenshot('asd.png', region=(get_region(posX1, posY1, posX2, posY2, cla)))
        white_img = image_processing(img, (148, 148, 148), (255, 255, 255))
        potion_count_ = pytesseract.image_to_string(white_img, lang=None)
        # print("text_check_potion", potion_count_)

        result_num_in = in_number_check(potion_count_)
        if result_num_in == True:
            potion = change_number(potion_count_)
            potion_bloon = potion.isdigit()
            if potion_bloon == True:
                potion = int(potion)
            else:
                print("potion => 숫자 아님")

        return potion
    except Exception as e:
        print(e)
        return 0



def text_check_get_black_white(posX1, posY1, posX2, posY2, cla):
    try:
        from PIL import ImageGrab
        from functools import partial
        import cv2
        import pytesseract
        import numpy
        import pyautogui

        ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

        coordinate = 0
        if cla == 'one':
            coordinate = 0
        if cla == 'two':
            coordinate = 960
        if cla == 'three':
            coordinate = 960 * 2
        if cla == 'four':
            coordinate = 960 * 3
        if cla == 'five':
            coordinate = 960 * 4
        if cla == 'six':
            coordinate = 960 * 5

        # 화면의 지정된 부분 캡처
        screenshot = pyautogui.screenshot(region=(posX1 + coordinate, posY1, posX2 - posX1, posY2 - posY1))

        # 이미지를 흑백으로 변환
        screenshot = screenshot.convert('L')

        # 이미지에서 텍스트 추출
        current_text = pytesseract.image_to_string(screenshot, config='--psm 6').strip()

        this_text = current_text

        print("this_text", this_text)

        ##
        return this_text
    except Exception as e:
        print(e)
        return 0

def text_check_get_black_white(posX1, posY1, posX2, posY2, cla):
    try:
        from PIL import ImageGrab
        from functools import partial
        import cv2
        import pytesseract
        import numpy
        import pyautogui

        ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

        coordinate = 0
        if cla == 'one':
            coordinate = 0
        if cla == 'two':
            coordinate = 960
        if cla == 'three':
            coordinate = 960 * 2
        if cla == 'four':
            coordinate = 960 * 3
        if cla == 'five':
            coordinate = 960 * 4
        if cla == 'six':
            coordinate = 960 * 5

        # 화면의 지정된 부분 캡처
        screenshot = pyautogui.screenshot(region=(posX1, posY1, posX2 - posX1, posY2 - posY1))

        # 이미지를 흑백으로 변환
        screenshot = screenshot.convert('L')

        # 이미지에서 텍스트 추출
        current_text = pytesseract.image_to_string(screenshot, config='--psm 6').strip()

        this_text = current_text

        print("this_text", this_text)

        ##
        return this_text
    except Exception as e:
        print(e)
        return 0

def text_check_get(posX1, posY1, posX2, posY2, cla):
    try:
        from PIL import ImageGrab
        from functools import partial
        import cv2
        import pytesseract
        import numpy
        import pyautogui

        ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

        coordinate = 0
        if cla == 'one':
            coordinate = 0
        if cla == 'two':
            coordinate = 960
        if cla == 'three':
            coordinate = 960 * 2
        if cla == 'four':
            coordinate = 960 * 3
        if cla == 'five':
            coordinate = 960 * 4
        if cla == 'six':
            coordinate = 960 * 5
        pos = (posX1 + coordinate, posY1, posX2 - posX1, posY2 - posY1)
        pyautogui.screenshot("asd.png", region=pos)
        pic = cv2.imread("asd.png", cv2.IMREAD_COLOR)  # 사진을 컬러로 읽어오기
        cv2.imwrite("asd.png", pic)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        pic_ = numpy.array(pic)
        result = pytesseract.image_to_string(pic_, lang='kor+eng')

        ##
        return result
    except Exception as e:
        print(e)
        return 0


def text_check_get_reg(posX1, posY1, posX2, posY2):
    try:
        from PIL import ImageGrab
        from functools import partial
        import cv2
        import pytesseract
        import numpy
        import pyautogui

        ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

        coordinate = 0
        pos = (posX1 + coordinate, posY1, posX2 - posX1, posY2 - posY1)
        pyautogui.screenshot("asd.png", region=pos)
        pic = cv2.imread("asd.png", cv2.IMREAD_COLOR)  # 사진을 컬러로 읽어오기
        cv2.imwrite("asd.png", pic)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        pic_ = numpy.array(pic)
        result = pytesseract.image_to_string(pic_, lang='kor+eng')

        ##
        return result
    except Exception as e:
        print(e)
        return 0


def text_check_get_num(posX1, posY1, posX2, posY2, cla):
    try:
        from PIL import ImageGrab
        from functools import partial
        import cv2
        import pytesseract
        import numpy
        from PIL import Image
        import pyautogui
        # color change
        coordinate = 0
        if cla == 'one':
            coordinate = 0
        if cla == 'two':
            coordinate = 960
        if cla == 'three':
            coordinate = 960 * 2
        if cla == 'four':
            coordinate = 960 * 3
        if cla == 'five':
            coordinate = 960 * 4
        if cla == 'six':
            coordinate = 960 * 5
        pos = (posX1 + coordinate, posY1, posX2 - posX1, posY2 - posY1)
        pyautogui.screenshot("asd.png", region=pos)
        pic = cv2.imread("asd.png", cv2.IMREAD_COLOR)  # 사진을 컬러로 읽어오기
        cv2.imwrite("asd.png", pic)
        ##
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        # path = Image.open(r'asd.png')
        pic_ = numpy.array(pic)
        rgb_image = cv2.cvtColor(pic_, cv2.COLOR_BGR2RGB)
        result = pytesseract.image_to_string(rgb_image, config='--psm 6')

        ##
        return result
    except Exception as e:
        print(e)
        return 0


def text_check_get_reg_num(posX1, posY1, posX2, posY2):
    try:
        from PIL import Image
        from PIL import ImageGrab
        from functools import partial
        import cv2
        import pytesseract
        import numpy
        import pyautogui

        ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

        coordinate = 0
        pos = (posX1 + coordinate, posY1, posX2 - posX1, posY2 - posY1)
        pyautogui.screenshot("asd.png", region=pos)
        pic = cv2.imread("asd.png", cv2.IMREAD_COLOR)  # 사진을 컬러로 읽어오기
        cv2.imwrite("asd.png", pic)
        ##
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        # path = Image.open(r'asd.png')
        pic_ = numpy.array(pic)
        rgb_image = cv2.cvtColor(pic_, cv2.COLOR_BGR2RGB)
        result = pytesseract.image_to_string(rgb_image, config='--psm 6')

        ##
        return result
    except Exception as e:
        print(e)
        return 0
    except Exception as e:
        print(e)
        return 0


def text_check_get_2(posX1, posY1, posX2, posY2, cla):
    try:
        from PIL import ImageGrab
        from functools import partial
        import cv2
        import pytesseract
        import numpy
        import pyautogui
        coordinate = 0
        if cla == 'one':
            coordinate = 0
        if cla == 'two':
            coordinate = 960
        if cla == 'three':
            coordinate = 960 * 2
        if cla == 'four':
            coordinate = 960 * 3
        if cla == 'five':
            coordinate = 960 * 4
        if cla == 'six':
            coordinate = 960 * 5
        isClick = False
        pos = (posX1 + coordinate, posY1, posX2 - posX1, posY2 - posY1)
        pyautogui.screenshot("asd.png", region=pos)
        pic = cv2.imread("asd.png", cv2.IMREAD_COLOR)  # 사진을 컬러로 읽어오기
        cv2.imwrite("asd.png", pic)
        ##
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        # path = Image.open(r'asd.png')
        pic_ = numpy.array(pic)
        rgb_image = cv2.cvtColor(pic_, cv2.COLOR_BGR2RGB)
        result = pytesseract.image_to_string(rgb_image, lang='kor+eng')

        ##
        return result
    except Exception as e:
        print(e)
        return 0


def text_check_get_3(posX1, posY1, posX2, posY2, color, cla):
    try:
        from PIL import ImageGrab
        from functools import partial
        import cv2
        import pytesseract
        import numpy
        from PIL import Image
        import pyautogui
        # color change
        coordinate = 0
        if cla == 'one':
            coordinate = 0
        if cla == 'two':
            coordinate = 960
        if cla == 'three':
            coordinate = 960 * 2
        if cla == 'four':
            coordinate = 960 * 3
        if cla == 'five':
            coordinate = 960 * 4
        if cla == 'six':
            coordinate = 960 * 5
        pos = (posX1 + coordinate, posY1, posX2 - posX1, posY2 - posY1)
        pyautogui.screenshot("asd.png", region=pos)
        pic = cv2.imread("asd.png", cv2.IMREAD_COLOR)  # 사진을 컬러로 읽어오기
        cv2.imwrite("asd.png", pic)
        ##
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        path = Image.open(r'asd.png')
        pic_ = numpy.array(pic)
        if color == 0:
            rgb_image = cv2.cvtColor(pic_, cv2.COLOR_BGR2RGB)
        if color == 1:
            rgb_image = cv2.cvtColor(pic_, cv2.COLOR_BGR2GRAY)
        if color == 2:
            rgb_image = cv2.cvtColor(pic_, cv2.COLOR_BGR2HSV)
        if color == 3:
            rgb_image = cv2.cvtColor(pic_, cv2.COLOR_BGR2YUV)
        if color == 4:
            rgb_image = cv2.cvtColor(pic_, cv2.COLOR_BGR2RGB)
        if color == 5:
            rgb_image = cv2.cvtColor(pic_, cv2.COLOR_BGR2RGB)
        if color == 6:
            rgb_image = cv2.cvtColor(pic_, cv2.COLOR_BGR2RGB)
        result = pytesseract.image_to_string(rgb_image, lang='kor+eng')

        ##
        return result
    except Exception as e:
        print(e)
        return 0


def text_check_get_4(posX1, posY1, posX2, posY2, color, cla):
    try:
        from PIL import ImageGrab
        from functools import partial
        import numpy as np
        import cv2
        import pytesseract
        import numpy
        import pyautogui
        # color change
        coordinate = 0
        if cla == 'one':
            coordinate = 0
        if cla == 'two':
            coordinate = 960
        if cla == 'three':
            coordinate = 960 * 2
        if cla == 'four':
            coordinate = 960 * 3
        if cla == 'five':
            coordinate = 960 * 4
        if cla == 'six':
            coordinate = 960 * 5
        pos = (posX1 + coordinate, posY1, posX2 - posX1, posY2 - posY1)
        pyautogui.screenshot("asd.png", region=pos)
        pic = cv2.imread("asd.png")
        cv2.imwrite("asd.png", pic)
        ##
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        # path = Image.open(r'asd.png')
        pic_ = numpy.array(pic)

        rgb_image_ = cv2.cvtColor(pic_, cv2.COLOR_BGR2HSV)

        lower_yellow = np.array([60, 100, 100])
        upper_yellow = np.array([90, 255, 255])

        lower_green = np.array([50, 100, 100])
        upper_green = np.array([70, 255, 255])

        lower_red = np.array([-10, 100, 100])
        upper_red = np.array([10, 255, 255])

        if color == 0:
            rgb_image_ready = cv2.inRange(rgb_image_, lower_yellow, upper_yellow)
            rgb_image = cv2.bitwise_and(pic, pic, mask=rgb_image_ready)
        if color == 1:
            rgb_image_ready = cv2.inRange(rgb_image_, lower_green, upper_green)
            rgb_image = cv2.bitwise_and(pic, pic, mask=rgb_image_ready)
        if color == 2:
            rgb_image_ready = cv2.inRange(rgb_image_, lower_red, upper_red)
            rgb_image = cv2.bitwise_and(pic, pic, mask=rgb_image_ready)
        result = pytesseract.image_to_string(rgb_image, lang='kor+eng')

        cv2.imshow('img_color', pic)

        ##
        return result
    except Exception as e:
        print(e)
        return 0


def how_many_pic(posX1, posY1, posX2, posY2, address, cla):
    try:
        from PIL import ImageGrab
        from functools import partial
        import cv2
        import pytesseract
        import numpy as np
        from PIL import Image
        import pyautogui

        ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

        coordinate = 0
        if cla == 'one':
            coordinate = 0
        if cla == 'two':
            coordinate = 960
        if cla == 'three':
            coordinate = 960 * 2
        if cla == 'four':
            coordinate = 960 * 3
        if cla == 'five':
            coordinate = 960 * 4
        if cla == 'six':
            coordinate = 960 * 5

        full_path = address  # '완료' 그림 갯수 파악
        img_array = np.fromfile(full_path, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        many = 0
        before = 0
        after = 0
        print("hihihihihi", coordinate)
        for list in pyautogui.locateAllOnScreen(img, region=(posX1 + coordinate, posY1, posX2 - posX1, posY2 - posY1),
                                                confidence=0.75):
            # print("list", list)
            after = list.top
            if before != after:
                before = after
                many += 1

        ##
        return many
    except Exception as e:
        print(e)
        return 0



