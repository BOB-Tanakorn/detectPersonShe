import os
import tensorflow as tf
from inferenceutils import *
import cv2
import pyodbc
import datetime

path = os.getcwd().replace('\\', '/')

#baseLocal
connect = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost; DATABASE=projectComputerVision; UID=sa; PWD=123456")
cursor = connect.cursor()

labelmap_path = path + '/mscoco_label_map.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(labelmap_path, use_display_name=True)
tf.keras.backend.clear_session()
model = tf.saved_model.load(path + "/model")

list_ip = [
"192.168.1.55"
]

location = {
"192.168.1.55" : "groundFloorMixer"
}

def _lineNotify(payload,file=None):
    import requests
    url = 'https://notify-api.line.me/api/notify'
    token = 'yYoPiS4TyW2bHja3HvlWrD5iccYefS09VcIBhCzcW1H'	#token ส่วนตัว
    # token = "EVPO0TRxPKQO8QtoIkX2p1uQFVuumR2FEUccTjYDoOY" #กลุ่มเทส she
    # token = '8edczGWSP1hnMeLXKfXseH8Ck1CATRTvLRL5CFSb3PW'	#she
    headers = {'Authorization':'Bearer '+token}
    return requests.post(url, headers=headers , data = payload, files=file)


def notifyFile(filename, person):
    file = {'imageFile':open(filename,'rb')}
    payload = {'message':'แจ้งเตือน ตรวจพบบุคคลในที่อับอากาศ\nLocation : ตึกผลิต ชั้นใต้ดิน\nจำนวนคน : {} คน'.format(person)}
    return _lineNotify(payload,file)

try:
    os.remove(path + '/imgBefore.png')
    print('{} >>> remove imgBefore.png success'.datetime.datetime.now())
except:
    pass

try:
    os.remove(path + '/imgAfter.png')
    print('{} >>> remove imgAfter.png success'.format(datetime.datetime.now()))
except:
    pass

cap = cv2.VideoCapture('rtsp://admin:999999999@192.168.1.55:10554/tcp/av0_0')
while True:
    try:
        _, frame = cap.read()
        cv2.imwrite(path + '/imgBefore.png', frame)
        print('{} >>> save picture for process success'.format(datetime.datetime.now()))
        saveImg = True
    except:
        print('{} >>> can not save image for process plase check connecttion camera'.format(datetime.datetime.now()))
        saveImg = False
    break
if saveImg == True:
    image_np = load_image_into_numpy_array(path + '/imgBefore.png')
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

    countLen = 0
    countPerson = 0
    for i in output_dict['detection_scores']:
        # print(i)
        pass
    for i in (output_dict['detection_classes']):
        if i == 1:
            valuesPerson = output_dict['detection_scores'][countLen] >= 0.9
            if valuesPerson == True:
                countPerson += 1
        countLen += 1
    image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    img_show = image_np.copy()
    cv2.imwrite(path + '/imgAfter.png', image_np)
    
    location = 'groundFloorMixer'
    location = location.replace("'", "")

    if countPerson >= 1:
        notifyFile(path + '/imgAfter.png', countPerson)
        statusPerson = True
        cursor = cursor.execute('UPDATE detectPersonShe SET statusPerson=? WHERE location=?', (True, location))
        cursor.commit()

    else:
        statusPerson = False
        cursor = cursor.execute('UPDATE detectPersonShe SET statusPerson=? WHERE location=?', (False, location))
        cursor.commit()
        notifyFile(path + '/imgAfter.png', countPerson)

