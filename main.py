# write a program that read a photo and convert it into pencil sketch
import cv2
import PySimpleGUI as sg

# set the overall theme
sg.theme("LightBrown1")

# set the specific text size in PySimpleGUI
sg.SetOptions(text_justification="center", font=("宋体", 15))


def process_photo_1(image):
    # convert the image to gray scale
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # invert the image
    inverted_img = 255 - gray_img

    # blur the image by gaussian function
    blurred_img = cv2.GaussianBlur(inverted_img, (21, 21), 0)

    # invert the blurred image
    inverted_blurred_img = 255 - blurred_img

    # create the pencil sketch image
    pencil_sketch_img = cv2.divide(gray_img, inverted_blurred_img, scale=256.0)

    return pencil_sketch_img


def process_photo_2(image):
    median = cv2.medianBlur(image, 3)
    r1 = cv2.Canny(median, thr1, thr2)
    # exchange the white and black
    r1 = 255 - r1

    return r1


layout = [
    [sg.Text("Please select a photo to convert to pencil sketch", size=(50, 1))],
    [sg.Text("Photo", size=(8, 1)), sg.Input(key="-FILE-"), sg.FileBrowse()],
    [sg.B("<<"), sg.B("<"), sg.T("清晰度", key="清晰度"), sg.B(">"), sg.B(">>")],
    [sg.B("--"), sg.B("-"), sg.T("对比度", key="对比度"), sg.B("+"), sg.B("++")],
    [sg.Button("Convert"), sg.Button("Exit")]
]

thr1=100
thr2=200

window = sg.Window("Photo to Pencil Sketch", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    elif event == "Convert":
        img = cv2.imread(values["-FILE-"])
        # show the image
        cv2.imshow("Original Image", img)
        cv2.imshow("Pencil Sketch of Image", process_photo_2(img))

    elif event in ("<<", "<", ">", ">>", "--", "-", "+", "++"):
        if event == "<<":
            thr1 -= 100
        elif event == "<":
            thr1 -= 10
        elif event == ">":
            thr1 += 10
        elif event == ">>":
            thr1 += 100
        elif event == "--":
            thr2 -= 100
        elif event == "-":
            thr2 -= 10
        elif event == "+":
            thr2 += 10
        elif event == "++":
            thr2 += 100

        window["对比度"].update("对比度: " + str(thr2))
        window["清晰度"].update("清晰度: " + str(thr1))
        cv2.imshow("Pencil Sketch of Image", process_photo_2(img))



window.close()


