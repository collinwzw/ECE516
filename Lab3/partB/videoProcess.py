import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import heartpy as hp
from scipy.signal import find_peaks
from moviepy.editor import *
def proces_video(video_name):
    cap = cv2.VideoCapture(video_name)
    cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    df = read_ecg_data("try.csv")
    count = 0
    out = cv2.VideoWriter('output.mp4', -1, 60.0, (1920, 1080))
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        imS = cv2.resize(frame, (1920, 1080))
        if count%120 == 0:
            added_numeral_img = generate_osc_plot(df,int(count/120))
        # for row in range(len(imS)):
        #     for column in range(len(imS[0])):
        #         if added_numeral_img[row][column].sum() != 0:
        #             final_image[row][column] =  added_numeral_img[row][column]


        #cv2.imshow('frame',cv2.add(imS, added_numeral_img))
        out.write(cv2.add(imS, added_numeral_img))
        count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print(count)
    cap.release()
    cv2.destroyAllWindows()

def concat_image():
    pass

def generate_Numerals(left_numeral,middle_numeral, right_numeral):
    img_left = cv2.imread("numeral/" + str(left_numeral) + ".jpg")
    img_middle = cv2.imread("numeral/" + str(middle_numeral) + ".jpg")
    img_right = cv2.imread("numeral/" + str(right_numeral) + ".jpg")
    size = img_left.shape[:2]
    top_offset = 600
    left_img_left_offset = 1500
    left_img_right_offset = 1920 - left_img_left_offset - size[1]

    middle_img_left_offset = left_img_left_offset + size[1]
    middle_img_right_offset = 1920 - middle_img_left_offset - size[1]

    right_img_left_offset = middle_img_left_offset +  size[1]
    right_img_right_offset = 1920 - right_img_left_offset - size[1]

    botttom_offset = 1080 - top_offset - size[0]
    new_img_left = cv2.copyMakeBorder(img_left, top_offset, botttom_offset, left_img_left_offset, left_img_right_offset, cv2.BORDER_CONSTANT)
    new_img_middle = cv2.copyMakeBorder(img_middle, top_offset, botttom_offset, middle_img_left_offset, middle_img_right_offset, cv2.BORDER_CONSTANT)
    new_img_right = cv2.copyMakeBorder(img_right, top_offset, botttom_offset, right_img_left_offset, right_img_right_offset, cv2.BORDER_CONSTANT)
    final_img = new_img_left + new_img_middle +  new_img_right

    return final_img

def read_ecg_data(filename):
    #around 269 data points per second
    # 37 seconds for 10000 data pointes

    dataset = pd.read_csv(filename, names=['hr'])
    return dataset

def plot_ecg_data(data):
    fig = plt.figure()
    fig.set_facecolor('black')
    fig.set_alpha(0.6)
    ax = fig.add_subplot(111)

    ax.set_facecolor("black")
    plt.plot(data, color = (0,0.3,0),linewidth = 16)
    plt.plot(data, color = (0,0.5,0),linewidth = 4)
    plt.plot(data, color = (0,0.8,0),linewidth = 1)
    plt.plot(data, color = (0,1,0),linewidth = 0.25)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    fig.savefig('temp.jpg')


def generate_osc_plot(df,initial_time):
    initial_time = initial_time * 2 + 10
    time_duration = 2 #in seconds
    data_point_per_second = 269
    peaks = find_peaks(df['hr'][initial_time*data_point_per_second:(initial_time + time_duration) * data_point_per_second], distance=150)[0]
    plot_ecg_data(df['hr'][initial_time*data_point_per_second :(initial_time + time_duration) * data_point_per_second])
    osc_plot = cv2.imread("temp.jpg")
    size = osc_plot.shape[:2]
    top_offset = 500
    left_offset = 100
    right_offset = 1920 - left_offset - size[1]
    botttom_offset = 1080 - top_offset - size[0]
    newosc_plot = cv2.copyMakeBorder(osc_plot, top_offset, botttom_offset, left_offset, right_offset,
                                      cv2.BORDER_CONSTANT)
    heart_rate = (len(peaks) / time_duration) * 60

    last_digit = int(heart_rate % 10)
    heart_rate /= 10
    second_digit = int(heart_rate % 10)
    heart_rate /= 10
    first_digit = int(heart_rate % 10)


    img_numeral = generate_Numerals(first_digit, second_digit, last_digit)
    added_numeral_img = newosc_plot + img_numeral



    return added_numeral_img
# img = generate_Numerals(1, 0)
# cv2.imshow("window", img)
# cv2.waitKey(0)
if __name__ == '__main__':
    video_filename = 'DJI_0131.mp4'
    proces_video(video_filename)
    videoclip = VideoFileClip(video_filename)
    # Extract Audio from Video
    audioclip = videoclip.audio
    # Save the Audio file (.mp3)
    audioclip.write_audiofile("Audio_fetched.mp3")

    videoclip = VideoFileClip("output.mp4")
    audioclip = AudioFileClip("Audio_fetched.mp3")

    videoclip = videoclip.set_audio(audioclip)
    videoclip.write_videofile("new_filename.mp4")




    # new_img = cv2.copyMakeBorder(p, 700, 1080 - 700, 100, 1920 - 100, cv2.BORDER_CONSTANT)







