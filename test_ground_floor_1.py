import os
import tensorflow as tf
from inferenceutils import *
import cv2
import pyodbc
import time
import datetime


# #connect database
# connect = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=DESKTOP-K5R79Q9; DATABASE=com_vision_smart_she; UID=sa; PWD=123456")
# cursor = connect.cursor()

labelmap_path='C:/Users/PTF/models/research/object_detection/data/mscoco_label_map.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(labelmap_path, use_display_name=True)
tf.keras.backend.clear_session()
model = tf.saved_model.load(f"C:/Users/PTF/she_objectdetection/deploy_com_vision_she/model")

list_ip = [
"192.168.1.55"
]

location = {
"192.168.1.55" : "Ground Floor 1"
}

def _lineNotify(payload,file=None):
    import requests
    url = 'https://notify-api.line.me/api/notify'
    token = 'L6EXQTUrlZT0Bz7D9LV5HLwDTiG4BkQ1FI6yvnVJdSa'	#กลุ่มตรวจสอบวัตถุดิบ
    # token = "EVPO0TRxPKQO8QtoIkX2p1uQFVuumR2FEUccTjYDoOY" #กลุ่มเทส she
    # token = '8edczGWSP1hnMeLXKfXseH8Ck1CATRTvLRL5CFSb3PW'	#she
    headers = {'Authorization':'Bearer '+token}
    return requests.post(url, headers=headers , data = payload, files=file)


def notifyFile(filename, person):
    file = {'imageFile':open(filename,'rb')}
    payload = {'message':'แจ้งเตือน ตรวจพบบุคคลในที่อับอากาศ\nLocation : ตึกผลิต ชั้นใต้ดิน\nจำนวนคน : {} คน'.format(person)}
    return _lineNotify(payload,file)

# path_img_before = "C:/Users/PTF/deploy_com_vision_she/img_before.png"
path_img_before = "C:/Users/PTF/she_objectdetection/deploy_com_vision_she/g1/g1_2022-02-23_09-16-25.png"

path_img_after = "C:/Users/PTF/she_objectdetection/deploy_com_vision_she/img_after.jpg"
# path_img_after = "C:/Users/PTF/deploy_com_vision_she/img_after.png"



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
    groundtruth_box_visualization_color='black',
    skip_labels=False,
    skip_scores=True,
    min_score_thresh=0.9,
    line_thickness=2)

count_len = 0
count_person = 0
for i in output_dict['detection_scores']:
    print(i)
for i in (output_dict['detection_classes']):
    if i == 1:
        values_person = output_dict['detection_scores'][count_len] >= 0.9
        if values_person == True:
            count_person += 1
    count_len += 1
image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
img_show = image_np.copy()
img_show = cv2.resize(img_show, (1280, 720))
cv2.imwrite(path_img_after, image_np)
# if count_person >= 1:
notifyFile(path_img_after, count_person)
    # cursor.execute("update detect_risk_area SET location='%s', create_at = getdate(), status='%s' WHERE id = 1" % (location[i_ip], 1))
    # cursor.commit()
cv2.imshow("test", img_show)
cv2.waitKey(1000)
  


