import sys
import os
import time

import variable as v_
from PyQt5.QtTest import *
sys.path.append('C:/my_games/' + str(v_.game_folder) + '/' + str(v_.data_folder) + '/mymodule')

# def game_start_screen(cla, character_id):
#     import numpy as np
#     import cv2
#
#     from function_moon import imgs_set_, click_pos_reg
#
#
#
#     try:
#
#         # 실수로 새 캐릭터 클릭시...
#         full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\game_start\\job_select_title.PNG"
#         img_array = np.fromfile(full_path, np.uint8)
#         img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#         imgs_ = imgs_set_(20, 30, 150, 100, cla, img, 0.8)
#         if imgs_ is not None and imgs_ != False:
#             # 이건 잘못 클릭시 나가기
#             click_pos_reg(imgs_.x, imgs_.y, cla)
#             print("job_select_title", imgs_)
#
#             for i in range(10):
#                 full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\game_start\\character_select_title.PNG"
#                 img_array = np.fromfile(full_path, np.uint8)
#                 img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#                 imgs_ = imgs_set_(20, 30, 150, 100, cla, img, 0.8)
#                 if imgs_ is not None and imgs_ != False:
#                     break
#                 time.sleep(0.5)
#
#         # 캐릭터 선택 화면
#         full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\game_start\\character_select_title.PNG"
#         img_array = np.fromfile(full_path, np.uint8)
#         img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#         imgs_ = imgs_set_(20, 30, 150, 100, cla, img, 0.8)
#         if imgs_ is not None and imgs_ != False:
#
#             character_change(cla, character_id)
#
#         else:
#             dir_path = "C:\\my_games\\" + str(v_.game_folder) + ""
#             if cla == 'one':
#                 file_path = dir_path + "\\mysettings\\myschedule\\one_now_id.txt"
#             if cla == 'two':
#                 file_path = dir_path + "\\mysettings\\myschedule\\two_now_id.txt"
#             if cla == 'three':
#                 file_path = dir_path + "\\mysettings\\myschedule\\three_now_id.txt"
#             if cla == 'four':
#                 file_path = dir_path + "\\mysettings\\myschedule\\four_now_id.txt"
#             if cla == 'five':
#                 file_path = dir_path + "\\mysettings\\myschedule\\five_now_id.txt"
#             if cla == 'six':
#                 file_path = dir_path + "\\mysettings\\myschedule\\six_now_id.txt"
#
#             same = False
#
#             if os.path.isfile(file_path) == True:
#                 with open(file_path, "r", encoding='utf-8-sig') as file:
#                     read_id = file.read()
#                     if str(character_id) == str(read_id):
#                         # 메뉴 안 열어도 됨
#                         same = True
#             if same == False:
#                 character_change(cla, character_id)
#
#
#     except Exception as e:
#         print(e)
#
# def character_change(cla, character_id):
#     import numpy as np
#     import cv2
#
#     from function_moon import imgs_set_, click_pos_reg, click_pos_2
#
#     from action_moon import loading, clean_screen, out_check, menu_open
#     from get_item import get_event, get_event_sub
#     from repair_moon import repair_start
#     from chango_moon import chango_action
#     from potion_moon import maul_potion_small_only
#     from dead import dead_die
#
#     from massenger import line_to_me
#     try:
#
#
#
#         print(str(character_id), "번으로 캐릭터 체인지")
#
#
#         cha_select = False
#         cha_select_count = 0
#         while cha_select is False:
#             cha_select_count += 1
#             if cha_select_count > 10:
#                 cha_select = True
#                 line_to_me(cla, "처음 스타트 화면에 문제가 있다.")
#
#             # 실수로 새 캐릭터 클릭시...
#             full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\game_start\\job_select_title.PNG"
#             img_array = np.fromfile(full_path, np.uint8)
#             img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#             imgs_ = imgs_set_(20, 30, 150, 100, cla, img, 0.8)
#             if imgs_ is not None and imgs_ != False:
#                 # 이건 잘못 클릭시 나가기
#                 click_pos_reg(imgs_.x, imgs_.y, cla)
#                 print("job_select_title", imgs_)
#
#                 for i in range(10):
#                     full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\game_start\\character_select_title.PNG"
#                     img_array = np.fromfile(full_path, np.uint8)
#                     img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#                     imgs_ = imgs_set_(20, 30, 150, 100, cla, img, 0.8)
#                     if imgs_ is not None and imgs_ != False:
#                         break
#                     time.sleep(0.5)
#
#             # 저장된 캐릭 번호 불러오기
#             dir_path = "C:\\my_games\\" + str(v_.game_folder) + ""
#             if cla == 'one':
#                 file_path = dir_path + "\\mysettings\\myschedule\\one_now_id.txt"
#             if cla == 'two':
#                 file_path = dir_path + "\\mysettings\\myschedule\\two_now_id.txt"
#             if cla == 'three':
#                 file_path = dir_path + "\\mysettings\\myschedule\\three_now_id.txt"
#             if cla == 'four':
#                 file_path = dir_path + "\\mysettings\\myschedule\\four_now_id.txt"
#             if cla == 'five':
#                 file_path = dir_path + "\\mysettings\\myschedule\\five_now_id.txt"
#             if cla == 'six':
#                 file_path = dir_path + "\\mysettings\\myschedule\\six_now_id.txt"
#
#             # 캐릭터 선택 화면
#
#             full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\game_start\\character_select_title.PNG"
#             img_array = np.fromfile(full_path, np.uint8)
#             img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#             imgs_ = imgs_set_(20, 30, 150, 100, cla, img, 0.8)
#             if imgs_ is not None and imgs_ != False:
#                 full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\game_start\\game_start_button.PNG"
#                 img_array = np.fromfile(full_path, np.uint8)
#                 img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#                 imgs_ = imgs_set_(740, 970, 900, 1040, cla, img, 0.8)
#                 if imgs_ is not None and imgs_ != False:
#
#                     x_reg = imgs_.x
#                     y_reg = imgs_.y
#
#                     # select 1 (730, 360)
#                     # select 2 (730, 435)
#                     if int(character_id) == 1:
#                         click_pos_2(730, 360, cla)
#                         time.sleep(0.1)
#                         click_pos_2(730, 360, cla)
#                         time.sleep(0.1)
#                     elif int(character_id) == 2:
#                         click_pos_2(730, 440, cla)
#                         time.sleep(0.1)
#                         click_pos_2(730, 440, cla)
#                         time.sleep(0.1)
#                     elif int(character_id) == 3:
#                         click_pos_2(730, 510, cla)
#                         time.sleep(0.1)
#                         click_pos_2(730, 510, cla)
#                         time.sleep(0.1)
#                     elif int(character_id) == 4:
#                         click_pos_2(730, 580, cla)
#                         time.sleep(0.1)
#                         click_pos_2(730, 580, cla)
#                         time.sleep(0.1)
#                     time.sleep(0.5)
#                     click_pos_reg(x_reg, y_reg, cla)
#                     time.sleep(0.1)
#
#                     #진입 버튼 누르면서 캐릭번호 저장하기
#                     save = False
#                     save_count = 0
#                     while save is False:
#                         save_count += 1
#                         if save_count > 15:
#                             save = True
#                         if os.path.isfile(file_path) == True:
#                             with open(file_path, "r", encoding='utf-8-sig') as file:
#                                 read_id = file.read()
#                                 if str(character_id) == str(read_id):
#                                     save = True
#                                 else:
#                                     with open(file_path, "w", encoding='utf-8-sig') as file:
#                                         file.write(str(character_id))
#                                 time.sleep(0.3)
#                         else:
#                             with open(file_path, "w", encoding='utf-8-sig') as file:
#                                 file.write(str(character_id))
#
#                     # 대기 화면 있는지 확인하면서 진입확인하기
#                     joined = False
#                     joined_count = 0
#                     while joined is False:
#                         joined_count += 1
#                         if joined_count > 15:
#                             joined = True
#
#                         result_out = out_check(cla)
#                         if result_out == True:
#                             joined = True
#                             cha_select = True
#
#                             print("게임 접속 끝")
#                             time.sleep(0.1)
#
#                             # 1번 캐릭은 이벤트 받기
#                             full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\get_items\\event_title.PNG"
#                             img_array = np.fromfile(full_path, np.uint8)
#                             img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#                             imgs_ = imgs_set_(400, 300, 545, 345, cla, img, 0.8)
#                             if imgs_ is not None and imgs_ != False:
#
#                                 if int(character_id) == 1:
#                                     get_event(cla)
#
#                                 else:
#                                     get_event_sub(cla)
#                             dead_die(cla, "start")
#                             chango_action(cla, "jangbi_out")
#                             repair_start(cla)
#
#                         else:
#                             # 로딩중 확인
#                             full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\action\\loding_1.PNG"
#                             img_array = np.fromfile(full_path, np.uint8)
#                             img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#                             imgs_ = imgs_set_(250, 920, 650, 1040, cla, img, 0.8)
#                             if imgs_ is not None and imgs_ != False:
#                                 loading(cla)
#                             else:
#                                 # 게임대기화면 확인
#                                 game_ready(cla)
#                         time.sleep(1)
#             else:
#                 # 캐릭 번호와 체인지 하려는 번호 비교하기
#
#                 same = False
#
#                 if os.path.isfile(file_path) == True:
#                     with open(file_path, "r", encoding='utf-8-sig') as file:
#                         read_id = file.read()
#                         if str(character_id) == str(read_id):
#                             # 메뉴 안 열어도 됨
#                             same = True
#                             cha_select = True
#                 if same == False:
#
#                     # 포션만 채우기(수집 분해도 함)
#                     maul_potion_small_only(cla)
#
#                     # 장비 빼기
#                     chango_action(cla, "jangbi_in")
#
#                     # 메뉴 열기
#                     menu_open(cla)
#                     full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\action\\menu_character_select.PNG"
#                     img_array = np.fromfile(full_path, np.uint8)
#                     img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#                     imgs_ = imgs_set_(670, 470, 960, 670, cla, img, 0.8)
#                     if imgs_ is not None and imgs_ != False:
#                         click_pos_reg(imgs_.x, imgs_.y, cla)
#                         for i in range(10):
#                             # 로딩중 확인
#                             full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\action\\loding_1.PNG"
#                             img_array = np.fromfile(full_path, np.uint8)
#                             img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#                             imgs_ = imgs_set_(250, 920, 650, 1040, cla, img, 0.8)
#                             if imgs_ is not None and imgs_ != False:
#                                 loading(cla)
#                             else:
#                                 full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\game_start\\character_select_title.PNG"
#                                 img_array = np.fromfile(full_path, np.uint8)
#                                 img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#                                 imgs_ = imgs_set_(20, 30, 150, 100, cla, img, 0.8)
#                                 if imgs_ is not None and imgs_ != False:
#                                     break
#                             time.sleep(1)
#                 else:
#                     print("같은 번호의 캐릭이라서 체인지 안함")
#
#     except Exception as e:
#         print(e)
#
# def game_ready(cla):
#     import numpy as np
#     import cv2
#
#     from function_moon import imgs_set_
#     from action_moon import loading, out_check
#
#
#     try:
#
#         # 접속대기일 경우 기다리기
#         full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\check\\moon_game_ready.PNG"
#         img_array = np.fromfile(full_path, np.uint8)
#         img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#         imgs_ = imgs_set_(400, 500, 600, 700, cla, img, 0.8)
#         if imgs_ is not None and imgs_ != False:
#             game_ready = True
#             game_ready_count = 0
#             game_play_count = 0
#             while game_ready is True:
#
#                 game_ready_count += 1
#
#                 full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\check\\moon_game_ready.PNG"
#                 img_array = np.fromfile(full_path, np.uint8)
#                 img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#                 imgs_ = imgs_set_(400, 500, 600, 700, cla, img, 0.8)
#                 if imgs_ is not None and imgs_ != False:
#                     game_ready_count = 0
#                     print("기다리는중", game_ready_count, "초")
#                 else:
#                     # 로딩중 확인
#                     full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\action\\loding_1.PNG"
#                     img_array = np.fromfile(full_path, np.uint8)
#                     img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#                     imgs_ = imgs_set_(250, 920, 650, 1040, cla, img, 0.8)
#                     if imgs_ is not None and imgs_ != False:
#                         loading(cla)
#
#                     else:
#                         result_out = out_check(cla)
#                         if result_out == False:
#                             game_ready = True
#
#                         else:
#                             game_play_count += 1
#                             print("게임 3초 대기", game_ready_count)
#                             if game_play_count > 2:
#                                 game_ready = False
#                 time.sleep(1)
#
#
#
#     except Exception as e:
#         print(e)