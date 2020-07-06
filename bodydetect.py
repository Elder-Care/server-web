import cv2 as cv
import numpy as np


confThreshold = 0.5
nmsThreshold = 0.4
inpWidth = 320
inpHeight = 320

classesFile = './model/coco.names'
classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

modelConfiguration = "./model/yolov3.cfg"
modelWeights = "./model/yolov3.weights"

net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)


def getOutputsNames(net):
    layersNames = net.getLayerNames()
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


# 绘制预测框
def drawPred(frame,classId, conf, left, top, right, bottom):
    # 绘制框体

    cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)

    label = '%.2f' % conf

    # 获取标签
    if classes:
        assert (classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    # 添加标签
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv.rectangle(frame, (left, top - round(1.5 * labelSize[1])), (left + round(1.5 * labelSize[0]), top + baseLine),
                 (255, 255, 255), cv.FILLED)
    cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)




# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawPred(frame,classIds[i], confidences[i], left, top, left + width, top + height)

    for i in classIds:
        if i == 1:
            return 1
        else:
            return 0




#winName = 'Yolodetect'

#cv.namedWindow(winName, cv.WINDOW_NORMAL)

def detect_fall(resource_path):
    cap = cv.VideoCapture(resource_path)

    fps = cap.get(cv.CAP_PROP_FPS)
    size = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))

    fallcount = 0

    while True:
        # get frame from the video
        hasFrame, frame = cap.read()
        # Stop the program if reached end of video
        if not hasFrame:
            print("处理完成")
            break
        # Create a 4D blob from a frame.
        blob = cv.dnn.blobFromImage(frame, 1 / 255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)

        # Sets the input to the network
        net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        outs = net.forward(getOutputsNames(net))

        # Remove the bounding boxes with low confidence
        fallcount = postprocess(frame, outs)

        # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the timings for each of the layers(in layersTimes)
        t, _ = net.getPerfProfile()
        label = 'Time Costs: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
        cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

        cv.imwrite('./result.jpg', frame)

        cv.waitKey(30)

    cap.release()
    cv.destroyAllWindows()
    return fallcount
