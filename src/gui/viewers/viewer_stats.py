import numpy as np
import qimage2ndarray
from loguru import logger
from PyQt5 import QtGui


class ViewerStats:
    def __init__(self, path_master_manager, config_file_handler):
        self.path_master = path_master_manager

        logger.debug(f'Run {self.__class__.__name__}')
        self._title = ''
        self.qlabel_viewer = None
        self.docked_widget = None
        self.float_widget = None
        self.pixmap_viewer = QtGui.QPixmap(qimage2ndarray.array2qimage(np.zeros((10, 10))))  # only for init

        self._img_data = np.zeros((10, 10, 10), dtype=int)
        self._seg_data = None
        self.view_plane_name = None
        self.view_modality_name = None
        self.base_resolution = None

        self._img_index = 5
        self._img_index_min = 0
        self._img_index_max = 10
        self._img_opacity = 100
        self._img_intensity_max_origin = 1e6
        self._img_intensity_min_origin = 0
        self._img_intensity_max_temp = 1e6
        self._img_intensity_min_temp = 0

        self._intensity_max_origin = None
        self._intensity_min_origin = None
        self._intensity_max_temp = None
        self._intensity_min_temp = None

        self._zoom_factor = 1
        self.zoom_pos = (0, 0)
        self.zoom_rect = (0, 0, 240, 240)

        self._linking = False
        self._activated = False
        self.zero_cut_store = []

        self.segmentation_color_map = [
            QtGui.qRgba(label[0], label[1], label[2], label[3])
            for label in config_file_handler.get_conf('meta_gui', 'segmentation_label_color', optional=[[0, 0, 0, 0]])
        ]

    @property
    def img_opacity(self):
        return self._img_opacity

    @img_opacity.setter
    def img_opacity(self, opacity):
        if 100 > opacity >= 0:
            self._img_opacity = opacity

    @property
    def img_index(self):
        if self._img_index_min > self._img_index:
            tmp_index = self._img_index_min
        elif self._img_index_max <= self._img_index:
            tmp_index = self._img_index_max
        else:
            tmp_index = self._img_index
        return tmp_index

    @img_index.setter
    def img_index(self, index):
        if self._img_index_max > index >= self._img_index_min:
            self._img_index = index

    @property
    def img_index_max(self):
        return self._img_index_max

    @img_index_max.setter
    def img_index_max(self, index_max):
        self._img_index_max = index_max

    @property
    def img_index_min(self):
        return self._img_index_min

    @img_index_min.setter
    def img_index_min(self, index_min):
        self._img_index_min = index_min

    @property
    def img_data(self):
        return self._img_data

    @img_data.setter
    @logger.catch
    def img_data(self, img):
        if img is not None:
            self._activated = True
            self._img_data = img
            self._get_img_intensity()
            self._img_index_max = np.shape(img)[0]
            self._img_index = int((self._img_index_max - self._img_index_min) / 2)
        else:
            self._img_data = np.zeros((10, 10, 10), dtype=int)
            self._activated = False

    @property
    def seg_data(self):
        return self._seg_data

    @seg_data.setter
    def seg_data(self, seg):
        self._seg_data = seg

    @property
    def current_seg_slice(self):
        return self._seg_data[self._img_index]

    @property
    def title(self):
        return self._title

    @title.setter
    @logger.catch
    def title(self, text):
        self._title = text
        if self.docked_widget is not None:
            self.docked_widget.set_title(text)

    @property
    def linking(self):
        return self._linking

    @linking.setter
    def linking(self, value):
        self._linking = value

    @property
    def activated(self):
        return self._activated

    @activated.setter
    def activated(self, value):
        if self._img_index_min < value < self._img_index_max:
            self._activated = value

    @property
    def zoom_factor(self):
        return self._zoom_factor

    @zoom_factor.setter
    def zoom_factor(self, factor):
        if factor > 0:
            self._zoom_factor = factor

    def reset(self):
        self.seg_data = None
        self.view_plane_name = None
        self.activated = True

    @logger.catch
    def load(self, img_data, title, orientation, linking, activated=True, reset=True):
        if reset:
            self.reset()
        self._activated = activated
        self.img_data = img_data
        self._title = title
        self._linking = linking
        self.view_plane_name = orientation
        if orientation == 'transverse':
            self.set_transverse_orientation()
        elif orientation == 'sagittal':
            self.set_sagittal_orientation()
        elif orientation == 'coronal':
            self.set_coronal_orientation()
        else:
            self.view_plane_name = None
            self.activated = False

    @logger.catch
    def set_transverse_orientation(self):
        if self._img_data is not None:
            self.view_plane_name = 'transverse'
            self._img_index_max = np.shape(self._img_data)[0]
            self._img_index = int((self._img_index_max - self._img_index_min) / 2)

    @logger.catch
    def set_sagittal_orientation(self):
        if self._img_data is not None:
            self.view_plane_name = 'sagittal'
            self._img_data = np.rot90(self._img_data, 1, axes=(1, 0))
            self._img_data = np.rot90(self._img_data, 3, axes=(2, 0))
            self._img_index_max = np.shape(self._img_data)[0]
            self._img_index = int((self._img_index_max - self._img_index_min) / 2)
        if self._seg_data is not None:
            self._seg_data = np.rot90(self._seg_data, 1, axes=(1, 0))
            self._seg_data = np.rot90(self._seg_data, 3, axes=(2, 0))

    @logger.catch
    def set_coronal_orientation(self):
        if self._img_data is not None:
            self.view_plane_name = 'coronal'
            self._img_data = np.rot90(self._img_data, 1, axes=(1, 0))
            self._img_index_max = np.shape(self._img_data)[0]
            self._img_index = int((self._img_index_max - self._img_index_min) / 2)
        if self._seg_data is not None:
            self._seg_data = np.rot90(self._seg_data, 1, axes=(1, 0))

    @logger.catch
    def _get_img_intensity(self):
        try:
            self._intensity_max_origin = np.max(self._img_data)
            self._intensity_min_origin = np.min(self._img_data)
            self._intensity_max_temp = np.max(self._img_data)
            self._intensity_min_temp = np.min(self._img_data)
        except:
            self._intensity_max_origin = None
            self._intensity_min_origin = None
            self._intensity_max_temp = None
            self._intensity_min_temp = None
