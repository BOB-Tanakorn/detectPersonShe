import os
import tensorflow as tf
from inferenceutils import *
import cv2
import pyodbc
import time
import datetime


#connect database
connect = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=DESKTOP-K5R79Q9; DATABASE=com_vision_smart_she; UID=sa; PWD=123456")
cursor = connect.cursor()

labelmap_path='C:/Users/PTF/deploy_com_vision_she/models/research/object_detection/data/mscoco_label_map.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(labelmap_path, use_display_name=True)
tf.keras.backend.clear_session()
model = tf.saved_model.load(f"C:/Users/PTF/deploy_com_vision_she/model")

list_ip = [
"192.168.1.56"
]

location = {
"192.168.1.56" : "Ground Floor 2"
}

def _lineNotify(payload,file=None):
    import requests
    url = 'https://notify-api.line.me/api/notify'
    token = 'L6EXQTUrlZT0Bz7D9LV5HLwDTiG4BkQ1FI6yvnVJdSa'	#กลุ่มตรวจสอบวัตถุดิบ
    # token = '8edczGWSP1hnMeLXKfXseH8Ck1CATRTvLRL5CFSb3PW'	#she
    headers = {'Authorization':'Bearer '+token}
    return requests.post(url, headers=headers , data = payload, files=file)


def notifyFile(filename, person):
    file = {'imageFile':open(filename,'rb')}
    payload = {'message':'แจ้งเตือน ตรวจพบบุคคลในที่อับอากาศ\nLocation : ตึกผลิต ชั้นใต้ดิน\nจำนวนคน : {} คน'.format(person)}
    return _lineNotify(payload,file)

path_img_before = "C:/Users/PTF/deploy_com_vision_she/img_before.png"
# path_img_before = "C:/Users/PTF/she_objectdetection/deploy_com_vision_she/15586933715581.jpg"
path_img_after = "C:/Users/PTF/deploy_com_vision_she/img_after.png"

for i_ip in list_ip:
    try:
        os.remove(path_img_before)
    except:
        pass

    try:
        os.remove(path_img_after)
    except:
        pass

    save_picture_success = False
    path_camera = "rtsp://admin:999999999@{}:10554/tcp/av0_0".format(i_ip)
    time_strf = time.strftime("%d-" "%m-" "%Y"" " "%H." "%M." "%S")

    try:
        cap = cv2.VideoCapture(path_camera)
        while True:
            _, frame = cap.read()
            cv2.imwrite(path_img_before, frame)
            save_picture_success = True
            break
    except:
        print("type error ; can not connect camera ip {}, location = {}".format(i_ip, location[i_ip]))
        pass

    if save_picture_success == True:
        image_name = path_img_before
        image_np = load_image_into_numpy_array(image_name)
        output_dict = run_inference_for_single_image(model, image_np)
        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            output_dict['detection_boxes'],
            output_dict['detection_classes'],
            output_dict['detection_scores'],
            category_index,
            instance_masks=output_dict.get('detection_masks_reframed', None),
            use_normalized_coordinates=True,
            skip_labels=False,
            skip_scores=True,
            min_score_thresh=0.9,
            line_thickness=2)

        count_len = 0
        count_person = 0
        for i in (output_dict['detection_classes']):
            if i == 1:
                values_person = output_dict['detection_scores'][count_len] >= 0.9
                if values_person == True:
                    count_person += 1
            count_len += 1
        print("location = {}".format(location["{}".format(i_ip)]))
        print("ip {}".format(i_ip))
        print("person = ", count_person)
        
        image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        cv2.imwrite(path_img_after, image_np)
        if count_person >= 1:
            notifyFile(path_img_after, count_person)
            cursor.execute("update detect_risk_area SET location='%s', create_at = getdate(), status='%s' WHERE id = 2" % (location[i_ip], 1))
            cursor.commit()
            pass
        
    try:
        cap.release()
        cv2.destroyAllWindows()
    except:
        pass
    print("------------------------------------------------------------------------")

    # time.sleep(30)


