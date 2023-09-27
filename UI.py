from tkinter import *
import tkinter.messagebox
import customtkinter
import cv2
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("/home/isaac/Downloads/card-system/theme.json")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()


        # configure window
        self.title("WmScanner")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        sidebar_frame.grid_rowconfigure(4, weight=1)

        logo_label = customtkinter.CTkLabel(sidebar_frame, text="WmScanner", font=customtkinter.CTkFont(size=20, weight="bold"))
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        sidebar_button_1 = customtkinter.CTkButton(sidebar_frame, command=self.open_camera, text="Enable Camera")
        sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        sidebar_button_2 = customtkinter.CTkButton(sidebar_frame, command=self.sidebar_button_event, text="Disable")
        sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        manual_input = customtkinter.CTkButton(sidebar_frame, command=self.manual_input, text="Manual Input")
        manual_input.grid(row=3, column=0, padx=20, pady=(10, 10))

        # appearance text
       # appearance_text = customtkinter.CTkLabel(sidebar_frame, text="Appearance Mode:", anchor="w") 
        #appearance_text.grid(row=5, column=0, padx=20, pady=(10, 0)) 

        # appearance selector
        appearance_select = customtkinter.CTkOptionMenu(sidebar_frame, values=["Light", "Dark", "System"], command=self.appearance_select) 
        appearance_select.grid(row=6, column=0, padx=20, pady=(10, 10))

        # scaling text
        scaling_text = customtkinter.CTkLabel(sidebar_frame, text="UI Scaling:", anchor="w")
        scaling_text.grid(row=7, column=0, padx=20, pady=(10, 0))

        # scaling selector
        scaling_select = customtkinter.CTkOptionMenu(sidebar_frame, values=["80%", "90%", "100%", "110%", "120%","130%","140%","150%","160%","170%","180%","190%","200%","250%","300%"],command=self.scaling_select)
        scaling_select.grid(row=8, column=0, padx=20, pady=(10, 20))

        # command entry bar
        self.command_entry = customtkinter.CTkEntry(self, placeholder_text="Enter a command...")
        self.command_entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # command sending button
        command_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Send Command", command=self.command_button)
        command_button.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create logs
        self.console = customtkinter.CTkTextbox(self, width=250)
        self.console.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create tabview
        tabview = customtkinter.CTkTabview(self, width=250)
        tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        tabview.add("CTkTabview")
        tabview.add("Tab 2")
        tabview.add("Tab 3")
        tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)
        tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        optionmenu_1 = customtkinter.CTkOptionMenu(tabview.tab("CTkTabview"), dynamic_resizing=False,
                                                  values=["Value 1", "Value 2", "Value Long Long Long"])
        optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        combobox_1 = customtkinter.CTkComboBox(tabview.tab("CTkTabview"),
                                              values=["Value 1", "Value 2", "Value Long....."])
        combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))

        label_tab_2 = customtkinter.CTkLabel(tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # create radiobutton frame
        radiobutton_frame = customtkinter.CTkFrame(self)
        radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        radio_var = tkinter.IntVar(value=0)
        label_radio_group = customtkinter.CTkLabel(master=radiobutton_frame, text="CTkRadioButton Group:")
        label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        radio_button_1 = customtkinter.CTkRadioButton(master=radiobutton_frame, variable=radio_var, value=0)
        radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        radio_button_2 = customtkinter.CTkRadioButton(master=radiobutton_frame, variable=radio_var, value=1)
        radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        radio_button_3 = customtkinter.CTkRadioButton(master=radiobutton_frame, variable=radio_var, value=2)
        radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        # Create slider and progressbar frame
        outer_camera_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        outer_camera_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        outer_camera_frame.grid_columnconfigure(0, weight=1)
        outer_camera_frame.grid_rowconfigure(4, weight=1)

        # Create a frame to hold the camera feed with a border
        camera_frame = customtkinter.CTkFrame(outer_camera_frame, border_width=5, border_color="#AA1122")
        camera_frame.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="nsew")

        # Configure the weights for rows and columns of outer_camera_frame
        outer_camera_frame.grid_rowconfigure(0, weight=1)  # Allow vertical expansion
        outer_camera_frame.grid_columnconfigure(0, weight=1)  # Allow horizontal expansion

        # Create the camera label (or canvas) with the specified width and height
        self.camera = customtkinter.CTkLabel(camera_frame, text="")
        self.camera.grid(row=0, column=0)

        # Make the camera_frame span multiple rows and columns
        camera_frame.grid_rowconfigure(0, weight=1)  # Allow vertical expansion within camera_frame
        camera_frame.grid_columnconfigure(0, weight=1)  # Allow horizontal expansion within camera_frame


        #seg_button_1 = customtkinter.CTkSegmentedButton(slider_progressbar_frame)
        #seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        #progressbar_1 = customtkinter.CTkProgressBar(slider_progressbar_frame)
        #progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        #progressbar_2 = customtkinter.CTkProgressBar(slider_progressbar_frame)
        #progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        #slider_1 = customtkinter.CTkSlider(slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
       # slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        #slider_2 = customtkinter.CTkSlider(slider_progressbar_frame, orientation="vertical")
       # slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
       ## progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")

        # create checkbox and switch frame
        checkbox_slider_frame = customtkinter.CTkFrame(self)
        checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        checkbox_1 = customtkinter.CTkCheckBox(master=checkbox_slider_frame)
        checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        checkbox_2 = customtkinter.CTkCheckBox(master=checkbox_slider_frame)
        checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        checkbox_3 = customtkinter.CTkCheckBox(master=checkbox_slider_frame)
        checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

        # set default values
        # sidebar_button_3.configure(state="disabled", text="Disabled CTkButton") # DISABLE
        checkbox_3.configure(state="disabled")  # DISABLE
        checkbox_1.select()  # ENABLE
        radio_button_3.configure(state="disabled")  # DISABLE

        appearance_select.set("Dark")  # MAKE DARK
        scaling_select.set("100%")  # SET SCALE TO 100

        optionmenu_1.set("CTkOptionmenu")
        combobox_1.set("CTkComboBox")
       # slider_1.configure(command=progressbar_2.set)
        #slider_2.configure(command=progressbar_3.set)
        #progressbar_1.configure(mode="indeterminnate")
       # progressbar_1.start()
        #self.console.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
       # seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
       # seg_button_1.set("Value 2")

    global cap
    
    cameraPort = 2

    cameraWidth, cameraHeight = 720, 720
  
    def open_camera(self):
        try:
            cap = cv2.VideoCapture(self.cameraPort)
            if not cap.isOpened():
                raise Exception("Can't open camera by index")
            


            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cameraWidth)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cameraHeight)

            def update_camera_frame():
                ret, frame = cap.read()
                if ret:
                    # Resize the frame to your desired dimensions (e.g., 400x400)
                    frame = cv2.resize(frame, (400, 400))

                    # Convert the OpenCV frame to a PhotoImage
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(image)
                    photo_image = ImageTk.PhotoImage(image=image)

                    # Update the CTKLabel widget with the new image
                    self.camera.configure(image=photo_image)
                    self.camera.image = photo_image  # Prevent garbage collection

                    # Schedule the next frame update
                    self.after(10, update_camera_frame)

            update_camera_frame()

        except cv2.error as e:
            error_message = f"OpenCV Error: {e}"
            self.console.insert("0.0", error_message)
            self.console.insert("0.0", "\n")

        except Exception as e:
            error_message = str(e)
            self.console.insert("0.0", error_message)
            self.console.insert("0.0", "\n")



    def manual_input(self):
        dialog = customtkinter.CTkInputDialog(text="Enter your full QR Code: FIRSTNAME_LASTNAME_ID", title="Manual Attendance")
        print("CTkInputDialog:", dialog.get_input())

    def command_button(self):
        text = self.command_entry.get().strip()  # Get the entered text and remove leading/trailing whitespace
        if not text:
            return  # No text entered, do nothing

        # Split the text into a command and its arguments, assuming a space separates them
        command, *args = text.split()

        if command.lower() == "cameraport":
            try:
                # Try to convert the argument to an integer and set it as the cameraPort variable
                self.cameraPort = int(args[0])
                # Now you can use the cameraPort variable in your camera-related code
                self.console.insert("0.0", f"Camera port set to {self.cameraPort}")
                self.console.insert("0.0", "\n")
            except ValueError:
                self.console.insert("0.0", "Invalid camera port value. Please enter a valid integer.")
                self.console.insert("0.0", "\n")

        elif command.lower() == "stop":
               self.console.insert("0.0", "\n")
               self.destroy()
               
        elif command.lower() == "cameraheight":
               self.cameraHeight = int(args[0])
               self.console.insert("0.0", "The camera height is now set to: " + str(self.cameraHeight) + "px")
               self.console.insert("0.0", "\n")

        elif command.lower() == "camerawidth":
               self.camerawidth = int(args[0])
               self.console.insert("0.0", "The camera width is now set to: " + str(self.camerawidth) + "px")
               self.console.insert("0.0", "\n")

        elif command.lower() == "clear":
            self.console.delete("0.0", "e")

        elif command.lower() == "help":
                self.console.insert("0.0", "\n")
                self.console.insert("0.0", """Available commands to run:
            
                Changes the port of the webcam:
                        cameraport [NEW PORT]
                                    
                Lists all the commands the are available
                        help [NULL]
                                    
                Stops and instantly kills the program
                        stop [NULL]
                                    
                Changes the camera height resolution
                        cameraheight [PX]
                                    
                Changes the camera width resolution
                        camerawidth [PX]
                                    
                Erases the text in the console
                        clear [NULL]
                                    
                                    """)
                self.console.insert("0.0", "\n")
    
        # Add more commands here as needed
        # Example: elif command.lower() == "another_command":
        #            do_something_with_args(args)

        # Clear the command entry after processing
        self.command_entry.delete(0, "end")



    def appearance_select(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def scaling_select(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()