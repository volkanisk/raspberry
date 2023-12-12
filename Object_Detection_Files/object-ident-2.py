import cv2
from picamera2 import Picamera2

#thres = 0.45 # Threshold to detect object

classNames = []
classFile = "/home/volkan/Desktop/code/raspberry/Object_Detection_Files/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "/home/pi/Desktop/code/raspberry/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/home/pi/Desktop/code/raspberry/Object_Detection_Files/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    return img,objectInfo


if __name__ == "__main__":

    # cap = cv2.VideoCapture(0)
    # cap.set(3,640)
    # cap.set(4,480)
    # #cap.set(10,70)
    piCam = Picamera2()
    piCam.preview_configuration.main.size = (640, 480)  # setting the size
    piCam.preview_configuration.main.format = ("RGB888")  # turning to BRG as cv2 uses
    piCam.preview_configuration.align()  # for non-formal size --> normal size automatically
    piCam.configure("preview")  # add the configurations
    piCam.start()


    while True:
        # success, img = cap.read()
        img = piCam.capture_array()  # get the frame and let cv2 do its magic
        result, objectInfo = getObjects(img,0.45,0.2, objects=['potted plant'])
        #print(objectInfo)
        cv2.imshow("Output",img)
        cv2.waitKey(1)
