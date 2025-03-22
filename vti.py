'''

VTI (Video To Images):
====================


Problem:    
            When an AI-ML beginner aspirant needs somewhat to 
            make easy its data collection regarding images for CNN model than that programmer spend its maximum time 
            to collect well labeled data for his project.

            

Solution:   
            By the usage of my current knowledge I made a smalland basic tool that helps to fetch a lot (hundreds or 
            thousands) of images in few seconds or minutes fromlive camera or the recoded videos.

            I named this tool VTI (Video To Images), that's easyto use (user friendly) and this tool is open-source.


            

Technologies used in this tool:

            - Python
            - Computer Vision (opencv-python)
            - Numeric Python (Numpy)
            - Tkinter [for GUI]
            - MTCNN [for human face detection]
            - other modules (os, datetime, webbrowser)


'''













# importing packages or required functions

import webbrowser 
import cv2 as cv

from mtcnn import MTCNN
from typing import Literal, Tuple
from time import sleep
from tkinter import *
from tkinter import messagebox, ttk 
from os import path, remove, walk
from os.path import exists
from datetime import datetime



# some variables
APP_NAME = "Video to Image (Beta version)"
logo_path = "vdo2img"
ENTRY_COMMON_WIDTH = 20
# declaring headings
xx_large = ('font',28)
x_large = ('font',23)
large = ('font',19)
medium = ('font',16)
small = ('font',13)
x_small = ('font',11)
xx_small = ('font',9)











class VideoToImageApp:




    # Assign default values
    EMPTY = ""
    DEFAULT_IMAGE_TYPE = ""
    DEFAULT_RECORD_TYPE = ""
    DEFAULT_NUMBER_OF_IMAGES = 100
    DEFAULT_IMAGES_PREFIX = "image"
    DEFAULT_RESIZE_VALUE = "auto"
    DEFAULT_VIDEO_MOTION = "normal"
    DEFAULT_EXTENSION = "png"
    DEFAULT_SHOW_WINDOW = 1
    DEFAULT_SHOW_INSTANT_UPDATES = 1







    # =================================== Starting Window ================================= #

    def __init__(self):

        root = Tk()
        root.geometry("800x600")
        root.title(APP_NAME)

        # adding navbar
        self.add_navbar(root)

        # App name
        APP_NAME_label = Label(root, text='Video to Image', font=xx_large)

        # single line description
        short_desc = "\n \
        Video to Image is a basic converter that helps to fetch images from recorded \n \
        videos or live with the camera. This tool mainly build for those persons whose \n \
        working in the AI-ML field (mainly deals with images or computer vision) and \n \
        needs a lot of images (thats a challenge for every AI-ML project), \n \
        and this tool will be  helpful for all of that."
        short_desc_label = Label(root, text=short_desc, font=small, justify='left')

        # Defining buttons
        # learn_more_btn = Button(root, text='Learn more', font=x_small, borderwidth=0)
        get_started_btn = Button(root, text='Get started', font=x_small, borderwidth=0, command=self.working_window)

        # plotting all them
        APP_NAME_label.grid(row=1, column=1, columnspan=3, pady=50)
        short_desc_label.grid(row=2, column=1, columnspan=3, padx=20)
        # learn_more_btn.grid(row=5, column=3, ipady=5, padx=5, pady=150)
        get_started_btn.grid(row=5, column=3, sticky='e', pady=150, ipady=5)

        root.mainloop()













    # ================================== Working window =================================== #

    def working_window(self) -> None:
        """ This is the main working window """



        # some settings of the current window
        window = Tk()
        window.geometry('1000x700')
        window.title(APP_NAME)
        
        # adding navbar
        self.add_navbar(window)

        # App name r-1
        APP_NAME_label = Label(window, text='Video to Image', font=large)

        # General instructions r-2
        general_ins_str = " \
        There are some general instructions: \n \
        1. All the field with astrick (*) sign must be filled up. \n \
        2. Some of these fields are optional so please active with them. \n \
        3. This app is not completely build yet so please cooperate with it."
        general_instructions_label = Label(window, text=general_ins_str, font=x_small, justify='left')

        
        # Setting some commonly used variables
        COMMON_INPUT_LABEL = x_small

        
        # -------------- Taking inputs ----------- #
        
        # Folder path r-3
        folder_path_lbl = Label(window, text='Folder path*', font=COMMON_INPUT_LABEL)
        self.folder_path_entry = Entry(window, width=ENTRY_COMMON_WIDTH, relief=FLAT)
        # self.folder_path_entry.insert(0, '/home/archit-elitebook/workarea/whole working/CV/understanding_and_exoloring_faces_img/data') # <<<<<<<<<<<<<<<<<<<<<<<<<<< Remove 

        # Image type 'entire image' or 'only human face' r-4
        img_type = Label(window, text='Image type*', font=COMMON_INPUT_LABEL)
        self.image_type_var = StringVar(window, value='entire image')
        self.image_type_opt_1 = Radiobutton(window, text='Only person face', variable=self.image_type_var, value='only human face', font=COMMON_INPUT_LABEL)
        self.image_type_opt_2 = Radiobutton(window, text='Entire image', variable=self.image_type_var, value='entire image', font=COMMON_INPUT_LABEL)

        # Record type r-5
        record_type_lbl = Label(window, text='Choose record type*', font=COMMON_INPUT_LABEL)
        self.record_type_var = StringVar(window, value='record live')
        self.record_type_radio_opt_1 = Radiobutton(window, text='Record live', variable=self.record_type_var, value='record live', font=COMMON_INPUT_LABEL)
        self.record_type_radio_opt_2 = Radiobutton(window, text='Recorded video', variable=self.record_type_var, value='recorded video', font=COMMON_INPUT_LABEL)

        # Video path r-6
        video_path_lbl = Label(window, text='Video path', font=COMMON_INPUT_LABEL)
        self.video_path_entry = Entry(window, width=ENTRY_COMMON_WIDTH, relief=FLAT)
        # self.video_path_entry.insert(0, "/home/archit-elitebook/workarea/whole working/CV/learning/sample_video.webm") # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Remove

        # Number of images to be fetched from video r-7
        no_imgs_lbl = Label(window, text='Number of images*', font=COMMON_INPUT_LABEL)
        self.no_imgs_entry = Entry(window, width=ENTRY_COMMON_WIDTH, relief=FLAT)
        self.no_imgs_entry.insert(0, 250)

        # Images prefix name r-8
        img_prefix_lbl = Label(window, text='Image prefix', font=COMMON_INPUT_LABEL)
        self.img_prefix_entry = Entry(window, width=ENTRY_COMMON_WIDTH, relief=FLAT)
        img_prefix_default_value = f"img_{str(datetime.today().date()).replace('-','_')}"
        self.img_prefix_entry.insert(0, img_prefix_default_value)

        # Resize r-9
        resize_lbl = Label(window, text='Fixed shape (rows x columns)', font=COMMON_INPUT_LABEL)
        self.resize_entry = Entry(window, width=ENTRY_COMMON_WIDTH, relief=FLAT)
        self.resize_entry.insert(0, 'auto')
    
        # adding separator
        separator = ttk.Separator(window, orient='vertical')
        separator.place(x=520, y=260, relwidth=1, relheight=0.5)
 

        # Video motion r-10
        video_motion_lbl = Label(window, text='Select video motion', font=COMMON_INPUT_LABEL)
        self.video_motion_var = StringVar(window, value='Normal')
        self.video_motion_values_data = {
            'Normal': None,
            'Little slow': 0.01,
            'Slow': 0.3,
            'Too Slow': 0.6
        }
        self.video_motion_options = self.video_motion_values_data.keys()
        self.video_motion_dropdown = OptionMenu(window, self.video_motion_var, *self.video_motion_options)

        # Image Extension r-11
        extension_lbl = Label(window, text='Choose image extension', font=COMMON_INPUT_LABEL)
        self.extension_var = StringVar(window, value='png')
        self.extension_options = ['png','jpeg','ppm','tiff','tif','jpg','pgm']
        self.extension_dropdown = OptionMenu(window, self.extension_var, *self.extension_options)

        
        # adding show working window
        self.show_window_checkbox_var = IntVar(window, value=1)
        self.show_window_checkbox = Checkbutton(window, text='Show working window', onvalue=1, offvalue=0, variable=self.show_window_checkbox_var)
        
        # adding show instant working window
        self.show_instant_status_checkbox_var = IntVar(window, value=1)
        self.show_instant_status_checkbox = Checkbutton(window, text='Show instant updates', onvalue=1, offvalue=0, variable=self.show_instant_status_checkbox_var)
        

        # Setting up buttons r-12
        self.proceed_btn = Button(window, text='Proceed', font=COMMON_INPUT_LABEL, width=ENTRY_COMMON_WIDTH, command=self.proceed_btn_action)
        # self.reset_btn = Button(window, text='Reset All', font=COMMON_INPUT_LABEL, width=ENTRY_COMMON_WIDTH, command=self.reset_all_fields)
        self.clear_folder_btn = Button(window, text='Clear folder', font=COMMON_INPUT_LABEL, width=ENTRY_COMMON_WIDTH, command=self.clear_folder_files)
        # self.paste_folder_path_btn = Button(window, text='Paste folder path', font=COMMON_INPUT_LABEL, width=ENTRY_COMMON_WIDTH)
        # self.paste_video_path_btn = Button(window, text='Paste video path', font=COMMON_INPUT_LABEL, width=ENTRY_COMMON_WIDTH)



        # instant instant_output_widget widget
        
        self.scrollbar = Scrollbar(window, width = 4)
        
        # Output Text
        self.instant_output_widget = Text(window, bg = 'white', fg = 'black', height = 12, width = 70, border = 1, wrap = 'word', yscrollcommand = self.scrollbar.set)
        self.instant_output_widget.configure( font = ('imprint mt shadow', 8))
        sn = '\n'
        self.instant_output_widget.insert(END, f'\t{sn*6}\tInstant updates will appear here...')
        self.instant_output_widget.config(state = DISABLED)
        self.instant_output_widget.yview('end')
        self.scrollbar.config( command = self.instant_output_widget.yview )




        
        # ------------- allocating widgets ------------- #
        
        # r-1
        APP_NAME_label.grid(row=1, column=1, columnspan=6, pady=20, padx=50)
        
        # r-2
        general_instructions_label.grid(row=2, column=1, columnspan=3, pady=50, padx=10)
        
        # r-3
        folder_path_lbl.grid(row=3, column=1, sticky='w', padx=50)
        self.folder_path_entry.grid(row=3, column=2, columnspan=3, sticky='w', ipadx=4, ipady=4)
        
        # r-4
        img_type.grid(row=4, column=1, sticky='w', padx=50, pady=10)
        self.image_type_opt_1.grid(row=4, column=2, columnspan=3, sticky='w')
        # r-5
        self.image_type_opt_2.grid(row=5, column=2, columnspan=3, sticky='w')

        # r-6
        record_type_lbl.grid(row=6, column=1, sticky='w', padx=50, pady=10)
        self.record_type_radio_opt_1.grid(row=6, column=2, columnspan=3, sticky='w')
        # r-7
        self.record_type_radio_opt_2.grid(row=7, column=2, columnspan=3, sticky='w')

        # r-8
        video_path_lbl.grid(row=8, column=1, sticky='w', padx=50)
        self.video_path_entry.grid(row=8, column=2, columnspan=3, sticky='w', pady=5, ipadx=4, ipady=4)

        # r-9
        no_imgs_lbl.grid(row=9, column=1, sticky='w', padx=50)
        self.no_imgs_entry.grid(row=9, column=2, columnspan=3, sticky='w', pady=5, ipadx=4, ipady=4)

        # r-10
        img_prefix_lbl.grid(row=10, column=1, sticky='w', padx=50)
        self.img_prefix_entry.grid(row=10, column=2, columnspan=3, sticky='w', pady=5, ipadx=4, ipady=4)

        # r-11
        resize_lbl.grid(row=11, column=1, sticky='w', padx=50)
        self.resize_entry.grid(row=11, column=2, sticky='w', pady=5, ipadx=4, ipady=4)

        # r-13
        video_motion_lbl.grid(row=3, column=6, sticky='w', padx=50)
        self.video_motion_dropdown.grid(row=3, column=7, columnspan=3, sticky='w')

        # r-14
        extension_lbl.grid(row=4, column=6, sticky='w', padx=50)
        self.extension_dropdown.grid(row=4, column=7, columnspan=3, sticky='w')

        # checkboxes
        self.show_window_checkbox.grid(row=6, column=6)
        self.show_instant_status_checkbox.grid(row=7, column=6)

        # r-15    
        self.proceed_btn.grid(row=10, column=6, ipady=3)
        # self.reset_btn.grid(row=11, column=6, ipady=3, sticky='e')
        self.clear_folder_btn.grid(row=11, column=6, ipady=3)
        # self.paste_folder_path_btn.grid(row=10, column=6, ipady=3, sticky='e')
        # self.paste_video_path_btn.grid(row=10, column=7, ipady=3, sticky='w')

        # display of instant instant_output_widget widget
        self.instant_output_widget.grid(row=1, column=6, rowspan=2, columnspan=2, ipadx=5, ipady=5, padx=20)
        
        
        

        window.mainloop()


    




    


    # ================================== About: window ==================== #

    def about_window(self) -> None:
        ''' This is the about window contains information for VTI '''

        # creating instance of Tk class for this about window
        window = Tk()
        window.geometry('900x700')
        window.title(APP_NAME)

        # addind common navbar
        self.add_navbar(window)

        # fetching the doc string 
        content: str = __doc__ 

        Label(window, text=content, font=x_small, justify='left').pack()















    # ===================================== Button action [Proceed] ========================== #



    def proceed_btn_action(self) -> None :
        """ This function call when user click on 'Proceed' button after filling required values """

        # --------------- Checking the values must be in proper format ---------- #
        
        # fetching folder path input
        self.folder_path_fetched = self.get_existed_folder_path(self.folder_path_entry)
        if self.folder_path_fetched is None:
            return None 
        # if self.folder_path_fetched == "":
        #     self.alert("You must be enter folder path for saving the images.")
        #     return 
        # if not exists(self.folder_path_fetched):
        #     self.alert(f"Invalid path directory: {self.folder_path_fetched}")
        #     return 
        

        # fetching image type
        image_type = str(self.image_type_var.get()).lower()
        only_human_face = True if image_type == 'only human face' else False
        

        # fetching record type
        record_type = str(self.record_type_var.get()).lower()
        live_record = True 
        video_path = None 
        if record_type == 'recorded video':
            live_record = False 
            # fetching video path
            video_path = str(self.video_path_entry.get()).strip()
            if video_path == "":
                self.alert("Please enter video path first.")
                return 
            if not exists(video_path):
                self.alert(f"Invalid video path: {video_path}")
                return 
            
        # self.alert(video_path)

        # fetching number of images
        try:
            number_of_imgs = str(self.no_imgs_entry.get()).strip()
            if number_of_imgs == "":
                self.alert("Please give a count of images (number of images) first.")
                return 
            number_of_imgs = int(number_of_imgs)
        except ValueError:
            self.alert(f"Enter a number instead of {number_of_imgs}")
            return
        except TypeError:
            self.alert(f"Something become None when fetching number of images.")
            return 
        except Exception as e:
            self.alert(f"Error occured: {e}")
            return
        

        # fetching image prefix
        image_prefix = str(self.img_prefix_entry.get()).strip()
        if image_prefix == "":
            self.alert("Must enter a prefix of image saving name.")
            return 
        

        # fetching resized shape
        resize_shape = str(self.resize_entry.get())
        if resize_shape == "":
            self.alert("Empty shape not valid.")
            return
        if resize_shape == 'auto':
            resize_shape = None 
        else:
            try:
                rows = int(resize_shape.split(',')[0])
                cols = int(resize_shape.split(',')[1])
                resize_shape = (rows, cols)
            except Exception as e:
                self.alert(f"Something went wrong with resize input. {e}")
                return
            

        # fetching slow motion
        slow_motion_user_input = str(self.video_motion_var.get())
        slow_motion_value = self.video_motion_values_data[slow_motion_user_input] # decoding to numerical values
        

        # fetching image extension
        extension = str(self.extension_var.get())


        # fetching show working window
        show_working_window = bool(int(self.show_window_checkbox_var.get()))

        # fetching show instant working status
        show_instant_working_status = bool(int(self.show_instant_status_checkbox_var.get()))

        
        if not messagebox.askokcancel(
            APP_NAME, f"You select {number_of_imgs} images to be fetched in the folder(...{self.folder_path_fetched.split('/')[-1]}), all images will be saved as {image_prefix}_1.{extension}"
            ):

            return


        # ----------- main working ----------- #
        
        try:
            self.save_live_images(
                save_dir = self.folder_path_fetched,
                resize = resize_shape,
                save_only_human_face = only_human_face,
                live_video = live_record,
                image_prefix = image_prefix,
                total_imgs = number_of_imgs,
                video_path = video_path,
                speed = slow_motion_value,
                extension = extension,
                show_working = show_working_window,
                show_instant_working_status = show_instant_working_status
            )
        except Exception as e:
            self.alert(e.with_traceback(None))
            return 

        
        











    # ====================================== update instant status ==================== #

    def update_instant_status(self, msg: str, verbose: bool = True) -> None :
        ''' This function will update the message in the update instant status/output '''
        
        if verbose:
            print(msg)

        # enable instant status widget for editing text
        self.instant_output_widget.config( state = NORMAL)

        # updating message to the
        self.instant_output_widget.insert(END, f' {msg}\n')

        # disable instant status widget
        self.instant_output_widget.config( state = NORMAL)

        self.instant_output_widget.yview('end')














    # ======================================= Main Script ==================== #


    def save_live_images(
        self, 
        save_dir: str,
        total_imgs: int = 5,
        verbose: bool = True,
        live_video: bool = True,
        resize: Tuple[int] = None,
        show_working: bool = True,
        label_img_count: bool = True,
        video_path: str | None = None,
        image_prefix: str | None = None,
        speed: float | int | None = None,         # range between 0 and 1 (0 for normal)
        starting_wait: float | None = None,
        save_only_human_face: bool = False,
        show_instant_working_status: bool = None,
        extension: Literal['png','jpeg','ppm','tiff','tif','jpg','pgm'] = 'png') -> None:

        """ This function will save the images [full frame] """


        # setting up is user choose live vdo or existing video
        capture_value = 0 if live_video and video_path is None else video_path
        capture = cv.VideoCapture(capture_value)

        # creating an instance for human face detection
        face_detector = MTCNN()

        if starting_wait:
            sleep(starting_wait)

        instant_msg = "" # it will store some messase that will prompt to the user
        count, iter = 0,0
        iter_count_diff = 0
        while True:
            if count == total_imgs :
                break
            if iter_count_diff == 10:
                instant_msg = "Face not detected from last 10 images that's why process stop."
                break
            ret,frame = capture.read()
            iter += 1  
            
            if not ret:
                break
        
            # controlling speed
            if speed:
                sleep(speed)

            # BGR to RGB
            cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            
            # dispay count if user want
            if label_img_count:
                cv.putText(frame, f"Img count: {count+1}", (10,25), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
            
            # save only human faces
            if save_only_human_face:
                face_detection_current_status = "not" # by default it means face not detected
                # detecting human faces
                faces = face_detector.detect_faces(frame)
                cropped_face = None
                if len(faces):
                    face = faces[0]
                    x,y,w,h = face['box']
                    # cropping face from image
                    cropped_face = frame[y:y+h, x:x+w].copy()
                    # plot rectangle
                    cv.rectangle(frame, (x,y), (x+w, y+h), (0,255,255),2)
                    face_detection_current_status = "" # it means face detected
                else: # face not detected
                    iter_count_diff += 1
                    
                # display current face detection status
                cv.putText(frame, f"Face {face_detection_current_status} detected !", (10,45), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 2)
                
                    
                    

            # showing video
            if show_working == False and video_path is not None:
                pass
            else:
                cv.imshow('current frame view',frame)
                # action perform when user press 'q'
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break

            # Image name
            if image_prefix is None:
                image_prefix = "image"


            # saving image
            try:
                full_img_path = f"{save_dir}/{image_prefix}_{count+1}.{extension}"
                if save_only_human_face:
                    if cropped_face is None:
                        if show_instant_working_status:
                            self.update_instant_status("Face not detected in the frame.", verbose)
                    else: # execute when face is detected and cropped from the frame
                        if resize:
                            cropped_face = cv.resize(cropped_face, resize, interpolation=cv.INTER_AREA)
                        cv.imwrite(full_img_path, cropped_face)
                        count += 1 # increasing count value after saving iterative image
                        iter_count_diff = 0
                        if show_instant_working_status:
                            self.update_instant_status(f"Image saved successfully: (...{full_img_path.split('/')[-1]})", verbose)
                else:
                    if resize:
                        frame = cv.resize(frame, resize, interpolation=cv.INTER_AREA)
                    cv.imwrite(full_img_path, frame)
                    count += 1 # increasing count value after saving iterative image
                    if show_instant_working_status:
                        self.update_instant_status(f"Image saved successfully: (...{full_img_path.split('/')[-1]})", verbose)

            except Exception as e:
                if show_instant_working_status:
                    self.update_instant_status(f"Something went wrong when try to save the image: (...{full_img_path})", verbose)
                return

            
            

        # releasing camera
        capture.release()
        cv.destroyAllWindows()
        if not (instant_msg == ""):
            self.alert(instant_msg)

        if count:
            self.alert(f'{count} images(s) saved successfully.')
        

















    # =================================== Get existed path ============================ #

    def get_existed_folder_path(self, folder_path_entry) -> str :
        ''' this function will return the real (existed) path (given by user) '''

        folder_path_fetched = str(folder_path_entry.get()).strip()
        if folder_path_fetched == "":
            self.alert("You must be provide a folder path in which all images will be saved.")
            return 
        if not exists(folder_path_fetched):
            self.alert(f"Invalid path directory: {folder_path_fetched}")
            return 
        
        return folder_path_fetched 


















    # ======================================= Remove all dir =================================== #

    def clear_folder_files(self) -> None :
        ''' This function will remove all files from the desired folder path (given by the user) '''
        
        # getting valid folder name
        folder_path = self.get_existed_folder_path(self.folder_path_entry)
        if folder_path is None:
            return None 
        
        # fetching folder name
        folder_name = folder_path.split('/')[-1]

        # calculating total number of files
        total_files_count = 0 # store how many files will be deleted
        for __, _, filenames in walk(folder_path):
            for filename in filenames:
                total_files_count += 1

        # if folder is already empty
        if not total_files_count:
            self.alert(f'Folder already empty.')
            return 
        
        # taking user perission
        if messagebox.askokcancel(APP_NAME, f"You will lost your {total_files_count} files in the {folder_name} folder."):
            # removing all files from folder 
            for dirname, _, filenames in walk(folder_path):
                for filename in filenames:
                    remove(path.join(dirname, filename))
                    self.update_instant_status(f"File deleted ({filename})")
            

            self.alert(f'{total_files_count} files(s) deleted successfully.')
                





        












    # ================================== Common navbar ==================================== #


    def add_navbar(self, window) -> None:
        # menu bar
        menubar = Menu(window) 
        common_font_for_navbar = x_small
        
        # link social accounts 
        social = Menu(menubar, tearoff = 0)
        # menubar.add_cascade(label ='Social', menu = social, font = common_font_for_navbar)
        social.add_command(label ='Github', font=common_font_for_navbar, command=lambda: webbrowser.open('https://github.com/a4archit'))
        social.add_command(label = 'LinkedIn', font=common_font_for_navbar, command=lambda: webbrowser.open('https://www.linkedin.com/in/archit-tyagi-191323296'))
        social.add_command(label = 'Portfolio', font=common_font_for_navbar, command=lambda: webbrowser.open('https://a4archit.github.io/portfolio'))
        social.add_command(label = 'Email', font=common_font_for_navbar, command=lambda: webbrowser.open('https://mailto:help.atd@gmail.com'))

        # Adding File Menu and commands 
        options = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label ='Menu', menu = options, font = common_font_for_navbar)
        options.add_command(label='About VTI',  font = common_font_for_navbar, command=self.about_window)
        options.add_cascade(label="Social",  font = common_font_for_navbar, menu=social)
        options.add_separator()
        options.add_command(label="Exit", font = common_font_for_navbar, command = window.destroy)
        
        
        window.config(menu = menubar)










    # ============================================ Alert Box =================================== #

    def alert(self, msg) -> None:
        """ This method will provide messageboxes (alternative of alert boxes in javascript) """
        messagebox.showinfo(APP_NAME, msg)

        







if __name__ == "__main__":

    VideoToImageApp()   

    # print(__doc__)
