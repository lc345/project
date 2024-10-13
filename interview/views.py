# views.py

from django.shortcuts import render
from django.http import JsonResponse

from MonitorTypes.models import Resume
from interview.dingtalk import send
import settings.base as set_base


def upload_image(request):

    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']

        if image.size > set_base.MEDIA_MAX_SIZE:
            return JsonResponse({'error': '文件过大'})

        if image.name.split('.')[-1] not in set_base.MEDIA_ALLOWED_EXTENSIONS:
            return JsonResponse({'error': '文件类型不支持'})

        # 保存图片
        with open(set_base.MEDIA_ROOT + image.name, 'wb') as f:
            print(set_base.MEDIA_ROOT)
            for chunk in image.chunks():
                f.write(chunk)

        return JsonResponse({'success': '上传成功'})
    
    # id = request.path.split("/")[2]
    # resume_obj = Resume.objects.filter(id=id).first()
    # gesture = detect_image()
    # if gesture == "2":
    #     send("紧急报警")
    # elif gesture == "3":
    #     send("我爱你")
    # elif gesture == "4":
    #     send("赶紧跑")

    return render(request, 'upload_image.html')

# 手势识别
# import cv2
# import mediapipe as mp
# def detect_image():
#     # Load the image
#     image = cv2.imread('path/to/your/image.jpg')

#     # Initialize the MediaPipe hand detection and gesture recognition models
#     mp_hands = mp.solutions.hands
#     hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)
#     mp_drawing = mp.solutions.drawing_utils
#     mp_drawing_styles = mp.solutions.drawing_styles

#     # Detect hands in the image
#     results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

#     # Iterate over the detected hands
#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             # Visualize the hand landmarks
#             mp_drawing.draw_landmarks(
#                 image,
#                 hand_landmarks,
#                 mp_hands.HAND_CONNECTIONS,
#                 mp_drawing_styles.get_default_hand_landmarks_style(),
#                 mp_drawing_styles.get_default_hand_connections_style())

#             # Classify the hand gesture
#             gesture = classify_gesture(hand_landmarks)
#             print(f"Detected gesture: {gesture}")

#     # Display the annotated image
#     cv2.imshow('Hand Gesture Recognition', image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# def classify_gesture(hand_landmarks):
#     """
#     Classify the hand gesture based on the hand landmarks.
#     You'll need to implement your own logic here to recognize different gestures.
#     """
#     # Example logic: Detect a 'thumbs up' gesture
#     thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
#     index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
#     if thumb_tip.y < index_tip.y:
#         return "Thumbs up"
#     else:
#         return "Unknown"
