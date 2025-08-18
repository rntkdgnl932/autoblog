import time

# 로그인

# 메인화면

# 글쓰기 화면
# https://cafe.naver.com/ca-fe/cafes/27960969/articles/write?boardType=L
write_url = "https://cafe.naver.com/ca-fe/cafes/27960969/articles/write?boardType=L"
# 75%

def naver_cafe_upload_main_in():
    import numpy as np
    import cv2
    from function_game import imgs_set_
    try:
        print("naver_upload_main_in")

        is_main = False

        full_path = r"c:\\my_games\\auto_blog\\data_basic\imgs\\naver_cafe_upload\\main_img.PNG"
        img_array = np.fromfile(full_path, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        imgs_ = imgs_set_(500, 100, 900, 400, "one", img, 0.7)
        if imgs_ is not None and imgs_ != False:
            print("main_img", imgs_)
            is_main = True
        else:
            full_path = r"c:\\my_games\\auto_blog\\data_basic\imgs\\naver_cafe_upload\\main_img2.PNG"
            img_array = np.fromfile(full_path, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            imgs_ = imgs_set_(500, 100, 900, 400, "one", img, 0.7)
            if imgs_ is not None and imgs_ != False:
                print("main_im2222222", imgs_)
                is_main = True



        if is_main == True:
           naver_cafe_write_ready()

        return is_main

    except Exception as e:
        return e


def naver_cafe_write_ready():
    import numpy as np
    import cv2
    from function_game import imgs_set_, click_pos_reg
    try:
        print("naver_upload_main_in")

        for i in range(4):

            full_path = r"c:\\my_games\\auto_blog\\data_basic\imgs\\naver_cafe_upload\\write_title.PNG"
            img_array = np.fromfile(full_path, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            imgs_ = imgs_set_(50, 350, 200, 450, "one", img, 0.7)
            if imgs_ is not None and imgs_ != False:
                print("write_title", imgs_)
                break
            else:
                full_path = r"c:\\my_games\\auto_blog\\data_basic\imgs\\naver_cafe_upload\\write_btn.PNG"
                img_array = np.fromfile(full_path, np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                imgs_ = imgs_set_(50, 500, 250, 600, "one", img, 0.7)
                if imgs_ is not None and imgs_ != False:
                    print("write_btn", imgs_)
                    click_pos_reg(imgs_.x, imgs_.y, "one")
            time.time(0.5)

    except Exception as e:
        return e