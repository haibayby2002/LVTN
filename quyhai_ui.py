import customtkinter
import os
import cv2 as cv
from PIL import Image
from tkinter import filedialog as fd
from tkinter import messagebox
from polyroi import Shape
import numpy as np
# import pandas as pd
import csv
from utils import Utils


class AppConfig(object):
    __slots__ = ()
    # app_dir = os.path.dirname(os.path.realpath(__file__)
    title = "Traffic Congestion GUI"
    geometry = "700x450"
    author = "Nguyen Quy Hai"
    organization = "BKU HCMUT"
    logo = "bku_logo.jpg"  # CustomTkinter_logo_single.png
    icon = {"video": "video-file-icon-28.png", "csv": "csv_icon.jpg"}
    video_type = [("video", "avi"), ("video", "mp4")]
    csv_type = [("Comma Separated Value", "csv")]

conf = AppConfig()



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # region Properties
        self.prop_import_file = ""
        self.prop_export_file = ""
        self.dens = ""
        self.mqtt_url = ""

        self.cap = self.first_cap = ""
        self.roi = ""
        # self.csv_frame_file_label = ""
        # endregion

        # self.title("image_example.py")
        self.title(conf.title)
        self.geometry(conf.geometry)

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # region load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.initial_path = os.path.dirname(os.path.realpath(__file__))
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, conf.logo)), size=(26, 26))
        self.image_preview = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")),
                                                    size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")),
                                                       size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                                                 size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
                                                 size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        self.video_icon = customtkinter.CTkImage(Image.open((os.path.join(image_path, conf.icon["video"]))))
        self.csv_icon = customtkinter.CTkImage(Image.open((os.path.join(image_path, conf.icon["csv"]))))
        # endregion

        # region create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  " + conf.organization,
                                                             image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.export_csv_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                         border_spacing=10, text="Export CSV",
                                                         fg_color="transparent", text_color=("gray10", "gray90"),
                                                         hover_color=("gray70", "gray30"),
                                                         image=self.chat_image, anchor="w",
                                                         command=self.export_csv_button_event)
        self.export_csv_button.grid(row=2, column=0, sticky="ew")

        self.pub_mqtt_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                       border_spacing=10, text="Publish MQTT",
                                                       fg_color="transparent", text_color=("gray10", "gray90"),
                                                       hover_color=("gray70", "gray30"),
                                                       image=self.add_user_image, anchor="w",
                                                       command=self.pub_mqtt_button_event)
        self.pub_mqtt_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                                values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")
        # endregion

        # region create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_image_preview = customtkinter.CTkLabel(self.home_frame, text="", image=self.image_preview)
        self.home_frame_image_preview.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_button_open = customtkinter.CTkButton(self.home_frame, text="", image=self.video_icon,
                                                              command=self.button_video_open_event)
        self.home_frame_button_open.grid(row=1, column=0, padx=20, pady=10)

        self.home_frame_poly_checkbox = customtkinter.CTkCheckBox(self.home_frame, text="Cut Polygon")
        self.home_frame_poly_checkbox.grid(row=2, column=0, padx=20, pady=10)

        self.home_frame_file_label = customtkinter.CTkLabel(self.home_frame, text=self.prop_import_file, compound="right")
        self.home_frame_file_label.grid(row=3, column=0, padx=20, pady=10)

        self.home_frame_button_open = customtkinter.CTkButton(self.home_frame, text="Preview",
                                                              command=self.button_preview_event)
        self.home_frame_button_open.grid(row=4, column=0, padx=20, pady=10)
        # endregion

        # region create csv frame
        self.export_csv_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.export_csv_frame.grid_columnconfigure(0, weight=1)

        self.csv_name_entry = customtkinter.CTkEntry(self.export_csv_frame, placeholder_text="Name the file")
        self.csv_name_entry.grid(row=0, column=0, padx=20, pady=(100, 15))

        self.csv_frame_button_open = customtkinter.CTkButton(self.export_csv_frame, text="Open Output Directory",
                                                              command=self.csv_frame_open_event)
        self.csv_frame_button_open.grid(row=1, column=0, padx=20, pady=10)

        self.csv_frame_file_label = customtkinter.CTkLabel(self.export_csv_frame, text=self.prop_export_file, compound="right")
        self.csv_frame_file_label.grid(row=2, column=0, padx=20, pady=10)

        self.longtitude_entry = customtkinter.CTkEntry(self.export_csv_frame, width=200, placeholder_text="Longtitude")
        self.longtitude_entry.grid(row=3, column=0, padx=20, pady=(15, 15))
        self.lattitude_entry = customtkinter.CTkEntry(self.export_csv_frame, width=200, placeholder_text="Lattitude")
        self.lattitude_entry.grid(row=4, column=0, padx=20, pady=(0, 15))
        self.export_csv_button = customtkinter.CTkButton(self.export_csv_frame, text="Export CSV", command=self.export_csv_event)
        self.export_csv_button.grid(row=5, column=0, padx=20, pady=(15, 15))
        # endregion

        # region create publish mqtt frame
        self.pub_mqtt_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.pub_mqtt_frame.grid_columnconfigure(0, weight=1)
        self.pub_mqtt_frame_button_open = customtkinter.CTkButton(self.pub_mqtt_frame, text="Open CSV File", image=self.csv_icon,
                                                              command=self.button_csv_open_event)
        self.pub_mqtt_frame_button_open.grid(row=0, column=0, padx=20, pady=(150,15))

        self.mqtt_frame_file_label = customtkinter.CTkLabel(self.pub_mqtt_frame, text=self.prop_import_file,
                                                            compound="right")
        self.mqtt_frame_file_label.grid(row=1, column=0, padx=20, pady=10)

        self.broker_entry = customtkinter.CTkEntry(self.pub_mqtt_frame, width=200, placeholder_text="Broker Entry")
        self.broker_entry.grid(row=2, column=0, padx=20, pady=(15, 15))

        self.topic_entry = customtkinter.CTkEntry(self.pub_mqtt_frame, width=200, show="*", placeholder_text="Topic")
        self.topic_entry.grid(row=3, column=0, padx=20, pady=(0, 15))

        self.publish_button = customtkinter.CTkButton(self.pub_mqtt_frame, text="Publish",
                                                         command=self.publish_mqtt_event, width=200)
        self.publish_button.grid(row=4, column=0, padx=20, pady=(15, 15))
        # endregion

        # select default frame
        self.select_frame_by_name("home")

    # region Nav
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.export_csv_button.configure(fg_color=("gray75", "gray25") if name == "export_csv" else "transparent")
        self.pub_mqtt_button.configure(fg_color=("gray75", "gray25") if name == "pub_mqtt" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "export_csv":
            self.export_csv_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.export_csv_frame.grid_forget()
        if name == "pub_mqtt":
            self.pub_mqtt_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.pub_mqtt_frame.grid_forget()


    def home_button_event(self):
        self.select_frame_by_name("home")

    def export_csv_button_event(self):
        self.select_frame_by_name("export_csv")

    def pub_mqtt_button_event(self):
        self.select_frame_by_name("pub_mqtt")


    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # endregion

    # region Home frame event
    def button_video_open_event(self):
        try:
            temp = fd.askopenfile(
                initialdir=self.initial_path + '/test_videos',
                filetypes=conf.video_type
            )
            self.prop_import_file = temp.name
            self.home_frame_file_label.configure(text=self.prop_import_file)
        except:
            pass
        finally:
            if self.prop_import_file != "":
                self.select_roi()

        print(self.prop_import_file)

    def select_roi(self):
        self.cap = cv.VideoCapture(self.prop_import_file)
        _, img = self.cap.read()

        """Polygon"""
        if self.home_frame_poly_checkbox.get():
            shape = Shape.get_roi(img)

            roi = self.roi= Utils.point2arr(shape.points)
            # Todo: numpy, calculate area, mass with image
            # area = Utils.calculates_area(shape.points)
            area = Utils.calculates_area(roi)
            print(area)
            self.dens = DensityManagement(self.cap, roi, is_poly=True)
            # dens.analyze()

        else:  # Rectangle
            roi = self.roi= cv.selectROI(img)
            img = img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

            self.dens = DensityManagement(self.cap, roi)

        self.home_frame_image_preview.configure(image=self.image_preview)   # This line is form PIL

    def button_preview_event(self):
        if self.home_frame_poly_checkbox.get() == 0:
            self.dens.analyze()
        else:
            # Todo: work from here
            self.dens.analyze_polygon()
            pass
    # endregion

    # region CSV event
    def get_longitude_and_latitude(self):
        try:
            long = float(self.longtitude_entry.get())
            lat = float(self.lattitude_entry.get())
        except:
            messagebox.showerror("Unverified", "Please fill in the longitude and latitude in number or decimal format")
            return (-np.inf, -np.inf)

        return long, lat

    def csv_frame_open_event(self):
        try:
            temp = fd.askdirectory(initialdir='./test_output')
            name = self.csv_name_entry.get()
            if name == "":
                messagebox.showerror("Lack of name", "Please type in csv name field before select folder")
                return
            if name[:-4] != ".csv":
                name = name + ".csv"
            self.prop_export_file = temp + "/" + name
            self.csv_frame_file_label.configure(text=self.prop_export_file)
            print(self.prop_export_file)
        except:
            pass

    def export_csv_event(self):
        print(self.prop_export_file)
        long, lat = self.get_longitude_and_latitude()
        print(long, lat)
        if long == -np.inf:
            return

        # Rectangle
        if self.home_frame_poly_checkbox.get() == 0:
            self.dens.write_csv(self.prop_export_file, long=long, lat=lat, frame_interval=30)
        else:
            # Polygon
            self.dens.write_csv_polygon(self.prop_export_file, long=long, lat=lat, frame_interval=30)
            pass



    # endregion

    # region MQTT event
    def button_csv_open_event(self):
        try:
            temp = fd.askopenfile(
                initialdir=self.initial_path + '/test_output',
                filetypes=conf.csv_type
            )
            self.prop_export_file = temp.name
            self.home_frame_file_label.configure(text=self.prop_import_file)
        except:
            pass
        finally:
            pass

        print(self.prop_import_file)

    def publish_mqtt_event(self):
        pass

    def publish_csv(self, csv_file_name, broker_url, topic):
        pass


    # endregion

class DensityManagement:
    def __init__(self, cap, roi, is_poly=False):
        # self.path = path
        self.area = 0
        self.roi = roi
        if is_poly:
            self.area = Utils.calculates_area(roi)
            print(self.area)
        self.params = cv.SimpleBlobDetector_Params()
        self.params.filterByInertia = False
        self.params.filterByConvexity = False
        self.params.filterByCircularity = True
        self.params.minCircularity = 0.1

        self.threshold = 150
        self.bg_sub_MOG2 = cv.createBackgroundSubtractorMOG2()
        self.bg_sub_KNN = cv.createBackgroundSubtractorKNN()
        # self.cap = cv.VideoCapture(path)
        self.cap = cap
        self.frame_index = 0
        self.fields = ['frame', 'knn', 'knn mor', 'mog2']
        self.val = []

    # region Preview Analyze
    def analyze(self, frame_interval = 30):

        while self.cap.isOpened():
            self.frame_index = self.frame_index + 1
            row = [self.frame_index]
            ret, frame = self.cap.read()
            if ret == False:
                self.frame_index = 0
                cv.VideoCapture.set(self.cap, cv.CAP_PROP_POS_AVI_RATIO, 0)
                break
            frame = Utils.crop_img(frame, self.roi)
            cv.imshow('Video', frame)

            # region Get background using KNN
            kernel = np.ones((5, 5), np.uint8)
            bg_mask = self.get_foreground_KNN(frame)
            knn_val = self.calculate_density(bg_mask)
            label_mask = cv.putText(
                img=bg_mask,
                text=str(knn_val),
                org=(20, bg_mask.shape[0] - 20),
                fontFace=cv.FONT_HERSHEY_COMPLEX,
                fontScale=1,
                color=(255, 255, 255),
                thickness=2)
            cv.imshow('KNN', label_mask)
            row.append(round(knn_val, 2))
            # endregion

            # region KNN morph
            bg_mask = self.get_foreground_KNN(frame)
            bg_mask = cv.morphologyEx(bg_mask, cv.MORPH_CLOSE, kernel)
            knn_morph = self.calculate_density(bg_mask)
            label2_mask = cv.putText(
                img=bg_mask,
                text=str(knn_morph),
                org=(20, bg_mask.shape[0] - 20),
                fontFace=cv.FONT_HERSHEY_COMPLEX,
                fontScale=1,
                color=(255, 255, 255),
                thickness=2)
            cv.imshow('Extend', label2_mask)
            row.append(round(knn_morph, 2))
            # endregion

            #region Mog2 Morph
            bg_mask = self.get_foreground_MOG2(frame)
            mog2_val = self.calculate_density(bg_mask)
            label_mask = cv.putText(
                img=bg_mask,
                text=str(mog2_val),
                org=(20, 20),
                fontFace=cv.QT_FONT_BLACK,
                fontScale=1,
                color=(255, 255, 255),
                thickness=2)
            cv.imshow('MOG2', label_mask)
            row.append(round(mog2_val, 2))
            #endregion



            # print('white: ', np.sum(bg_mask == 255))
            # print('black: ', np.sum(bg_mask == 0))

            # self.val.append(row)
            if self.frame_index % frame_interval == 0:
                print(row)
            if cv.waitKey(25) & 0xFF == ord('q'):
                self.frame_index = 0
                cv.VideoCapture.set(self.cap, cv.CAP_PROP_POS_AVI_RATIO, 0)
                break
        # print(self.val)
        # self.cap.release()
        # cv.destroyAllWindows()
        # self.cap.release()

    def analyze_polygon(self, frame_interval = 30):
        # print("analyze polygon")
        # print(self.roi)
        while self.cap.isOpened():

            self.frame_index = self.frame_index + 1
            row = [self.frame_index]
            ret, frame = self.cap.read()
            if ret == False:
                self.frame_index = 0
                cv.VideoCapture.set(self.cap, cv.CAP_PROP_POS_AVI_RATIO, 0)
                break
            frame = Utils.mask_img(frame, self.roi)
            cv.imshow('Video', frame)
            area = Utils.calculates_area(self.roi)


            # region Get background using KNN
            kernel = np.ones((5, 5), np.uint8)
            bg_mask = self.get_foreground_KNN(frame)
            knn_val = self.calculate_density(bg_mask, is_polygon=True)
            label_mask = cv.putText(
                img=bg_mask,
                text=str(knn_val),
                org=(20, bg_mask.shape[0] - 20),
                fontFace=cv.FONT_HERSHEY_COMPLEX,
                fontScale=1,
                color=(255, 255, 255),
                thickness=2)
            cv.imshow('KNN', label_mask)
            row.append(round(knn_val, 2))
            # endregion

            # region KNN morph
            bg_mask = self.get_foreground_KNN(frame)
            bg_mask = cv.morphologyEx(bg_mask, cv.MORPH_CLOSE, kernel)
            knn_morph = self.calculate_density(bg_mask, is_polygon=True)
            label2_mask = cv.putText(
                img=bg_mask,
                text=str(knn_morph),
                org=(20, bg_mask.shape[0] - 20),
                fontFace=cv.FONT_HERSHEY_COMPLEX,
                fontScale=1,
                color=(255, 255, 255),
                thickness=2)
            cv.imshow('Extend', label2_mask)
            row.append(round(knn_morph, 2))
            # endregion

            #region Mog2 Morph
            bg_mask = self.get_foreground_MOG2(frame)
            mog2_val = self.calculate_density(bg_mask, is_polygon=True)
            label_mask = cv.putText(
                img=bg_mask,
                text=str(mog2_val),
                org=(20, 20),
                fontFace=cv.QT_FONT_BLACK,
                fontScale=1,
                color=(255, 255, 255),
                thickness=2)
            cv.imshow('MOG2', label_mask)
            row.append(round(mog2_val, 2))
            #endregion

            if self.frame_index % frame_interval == 0:
                print(row)
            if cv.waitKey(25) & 0xFF == ord('q'):
                self.frame_index = 0
                cv.VideoCapture.set(self.cap, cv.CAP_PROP_POS_AVI_RATIO, 0)
                break
        # self.cap.release()
    # endregion

    # region Write CSV method
    def write_csv(self, path, long=0, lat=0, frame_interval=30):
        print("write csv rectangle")
        with open(path, 'w') as csvfile:
            # Create a writer object
            csvwriter = csv.writer(csvfile)
            # Write the fields and rows to the file
            csvwriter.writerow([long, lat])
            csvwriter.writerow(self.fields)

            while self.cap.isOpened():
                self.frame_index = self.frame_index + 1
                row = [self.frame_index]
                ret, frame = self.cap.read()
                if ret == False:
                    self.frame_index = 0
                    cv.VideoCapture.set(self.cap, cv.CAP_PROP_POS_AVI_RATIO, 0)
                    return
                frame = Utils.crop_img(frame, self.roi)
                # cv.imshow('Video', frame)

                # region Get background using KNN
                kernel = np.ones((5, 5), np.uint8)
                bg_mask = self.get_foreground_KNN(frame)
                knn_val = self.calculate_density(bg_mask)
                # cv.imshow('KNN', label_mask)
                row.append(round(knn_val, 2))
                # endregion

                # region KNN morph
                bg_mask = self.get_foreground_KNN(frame)
                bg_mask = cv.morphologyEx(bg_mask, cv.MORPH_CLOSE, kernel)
                knn_morph = self.calculate_density(bg_mask)
                # cv.imshow('Extend', label2_mask)
                row.append(round(knn_morph, 2))
                # endregion

                # region Mog2 Morph
                bg_mask = self.get_foreground_MOG2(frame)
                mog2_val = self.calculate_density(bg_mask)
                # cv.imshow('MOG2', label_mask)
                row.append(round(mog2_val, 2))
                # endregion

                # self.val.append(row)
                if self.frame_index % frame_interval == 0:
                    csvwriter.writerow(row)

            # self.cap.release()

    def write_csv_polygon(self, path, long=0, lat=0, frame_interval=30):
        print("write csv polygon")
        with open(path, 'w') as csvfile:
            # Create a writer object
            csvwriter = csv.writer(csvfile)
            # Write the fields and rows to the file
            csvwriter.writerow([long, lat])
            csvwriter.writerow(self.fields)
            while self.cap.isOpened():

                self.frame_index = self.frame_index + 1
                row = [self.frame_index]
                ret, frame = self.cap.read()
                if ret == False:
                    self.frame_index = 0
                    cv.VideoCapture.set(self.cap, cv.CAP_PROP_POS_AVI_RATIO, 0)
                    break
                frame = Utils.mask_img(frame, self.roi)
                area = Utils.calculates_area(self.roi)

                # region Get background using KNN
                kernel = np.ones((5, 5), np.uint8)
                bg_mask = self.get_foreground_KNN(frame)
                knn_val = self.calculate_density(bg_mask, is_polygon=True)
                row.append(round(knn_val, 2))
                # endregion

                # region KNN morph
                bg_mask = self.get_foreground_KNN(frame)
                bg_mask = cv.morphologyEx(bg_mask, cv.MORPH_CLOSE, kernel)
                knn_morph = self.calculate_density(bg_mask, is_polygon=True)
                row.append(round(knn_morph, 2))
                # endregion

                # region Mog2 Morph
                bg_mask = self.get_foreground_MOG2(frame)
                mog2_val = self.calculate_density(bg_mask, is_polygon=True)
                row.append(round(mog2_val, 2))
                # endregion

                if self.frame_index % frame_interval == 0:
                    csvwriter.writerow(row)
            # self.cap.release()
    # endregion

    # region Calculate
    def get_foreground_MOG2(self, frame):
        background = cv.GaussianBlur(frame, (7, 7), 0)
        return self.bg_sub_MOG2.apply(background)

    def get_foreground_KNN(self, frame):
        background = cv.GaussianBlur(frame, (7, 7), 0)
        return self.bg_sub_KNN.apply(background)

    def calculate_density(self, frame, is_polygon = False):
        if not is_polygon:
            white = np.sum(frame != 0)
            black = np.sum(frame == 0)
            return white / (black + white)
        else:
            # print("Yolo")
            white = np.sum(frame != 0)
            # return ("white: ", white, " area: ", self.area)
            return white / self.area
    #endregion

if __name__ == "__main__":
    app = App()
    app.mainloop()
