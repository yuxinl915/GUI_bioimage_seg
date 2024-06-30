import napari
from qtpy.QtWidgets import QWidget, QGridLayout
from skimage.io import imread
import os
import time
import threading


IMG_FILEPATH = "test_colorized_annotation_1.png"
IMG_STEM = "original_img"

SEG1_FILEPATH = "mask_1.png"
SEG1_STEM = "original_img_seg_1"
SEG2_FILEPATH = "mask_2.tif"
SEG2_STEM = "original_img_seg_2"

class NapariWindow(QWidget):
    '''Napari Window Widget object.
    Opens the napari image viewer to view and fix the labeles.
    '''

    def __init__(self):
        super().__init__()
        self.setWindowTitle("napari viewer")

        # Set the viewer
        self.viewer = napari.Viewer(show=False)
        
        # whenever the user switches between layers update cur_selected_seg
        self.cur_selected_seg = True
        # add the images to the viewer
        # img = imread(IMG_FILEPATH)
        # seg1 = imread(SEG1_FILEPATH)
        # seg2 = imread(SEG2_FILEPATH)
        # print(img.shape, seg1.shape, seg2.shape)
        # self.viewer.add_image(img, name=IMG_STEM)
        # self.viewer.add_labels(seg1, name=SEG1_STEM)
        # self.viewer.add_labels(seg2, name=SEG2_STEM)
        # self.viewer.layers.selection.events.changed.connect(self.on_seg_channel_changed)

        # when the user uploads the image, get the image and add it to the viewer
        self.user_file_path = None
        self.viewer.layers.selection.events.changed.connect(self.on_seg_channel_changed)

        # print(self.viewer.layers[-1])
        # print()

        main_window = self.viewer.window._qt_window
        layout = QGridLayout()
        layout.addWidget(main_window, 0, 0, 1, 4)
        
        '''
        add other stuff
        '''
        self.setLayout(layout)
        self.show()

    # get the image the user just uploaded
    def on_seg_channel_changed(self, event):
        if (act := self.viewer.layers.selection.active) is not None and not self.user_file_path:
        #     self.cur_selected_seg = act.name
            self.user_file_path = act.source.path 
            print(self.viewer.layers.selection.active)
            print(self.viewer.layers.selection.active.name)
            print(self.viewer.layers.selection.active.data.shape)
            # add the image to the viewer
            # self.viewer.add_image(
            #     self.viewer.layers.selection.active.data,
            #     name=self.viewer.layers.selection.active.name
            # )
            # run another python script with user_file_path as an argument (should be in a separate thread)
            thread_seg_algo = threading.Thread(target=self.call_seg_algo,
                                               args=(self.user_file_path,)
            )
            # worker_seg_algo = napari.qt.threading.create_worker(
            #     self.call_seg_algo,
            #     (self.user_file_path,),
            #     _progress={'total':5}
            # )
            # os.system(f"python mock_seg_algo.py {self.user_file_path}")

            # check whether the output image is created every 10 seconds
            # record the start time
            start_time = time.time()
            thread_seg_algo.start()
            while True:
                if os.path.exists("working_dir/output_img.png"):
                    print("output image is created!")
                    print(f"Time elapsed: {time.time() - start_time} seconds")
                    break
                else:
                    print("output image is not created yet!")
                    time.sleep(10)
            thread_seg_algo.join()
            # if the output image is created, add it to the viewer
            output_img = imread("working_dir/output_img.png")
            self.viewer.add_labels(output_img, name="output_img")
            if os.path.exists("working_dir"):
                os.system("rmdir working_dir")

    def call_seg_algo(self, input_path):
        os.system(f"python mock_seg_algo.py {input_path}")

    def load_img(self):
        output_img = imread("working_dir/output_img.png")
        self.viewer.add_labels(output_img, name="output_img")
        if os.path.exists("working_dir"):
            os.system("rmdir working_dir")


if __name__=="__main__":
    import sys
    from qtpy.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = NapariWindow()
    sys.exit(app.exec())