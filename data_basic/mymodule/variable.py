# 현재실행중인 클라우드
now_cla = 'none'

# 아두이노 관련
now_arduino = "none"

# 해당 게임 관련
wd_id = "none"
wd_pw = "none"
domain_adress = "none"
api_key = "none"
keyword = "none"
my_category = "none"
my_prompt = "none"
my_topic = "none"
my_google_custom_id = "none"
my_google_custom_api = "none"
my_topic_system = "none"
my_topic_user = "none"
my_gas_key = "none"

# 게임 및 폴더 관련
this_game = "auto_blog"
game_folder = "auto_blog"
data_folder = "data_basic"
notification_count = 0
# 버젼

dir_path = "C:\\my_games\\" + str(game_folder) + "\\" + str(data_folder)
file_path = dir_path + "\\mymodule\\version.txt"
file_path2 = "C:\\my_games\\mouse\\port.txt"

with open(file_path, "r", encoding='utf-8-sig') as file:
    version_ = file.read()
    print("version???", version_)

with open(file_path2, "r", encoding='utf-8-sig') as file:
    read_port = file.read().splitlines()
    COM_ = read_port[0]
    speed_ = int(read_port[1])
    print("COM???", COM_)
    print("speed_???", speed_)




# 강제로 돈벌기
forcee_not_sub = False
force_sub_quest = False
# 수집(아레스에서는 다크디멘션으로 대체)


# 마우스 관련
mouse_speed = 20
mouse_pm = 3
mouse_move_count = 300