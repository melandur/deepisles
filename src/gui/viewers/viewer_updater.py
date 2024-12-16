# pylint: disable=too-many-locals

import numpy as np
import qimage2ndarray
from loguru import logger
from PyQt5 import QtCore, QtGui, QtWidgets


class ViewerUpdater(QtWidgets.QMainWindow):
    """Updates the viewers (qlabel) by setting the pixmap with data from the viewerstats"""

    def __init__(self, mw, core):
        super().__init__()
        self.mw = mw
        self.core = core

    @staticmethod
    def get_pixmap(viewer_stats):
        """Get pixmap from viewer stats"""
        return viewer_stats.pixmap_viewer

    @logger.catch
    def refresh_sse_viewer(self):
        """Refresh smart segmentation editor"""
        self.refresh(self.core.viewer_stats.sse_viewer)

    @staticmethod
    def most_frequent(indexes):
        """Get most frequent index"""
        return max(set(indexes), key=indexes.count)

    @logger.catch
    def refresh_viewers(self):
        """Refresh all viewers"""
        if self.core.viewer_stats.viewer_1.linking:
            viewers_img_index = []
            if self.core.viewer_stats.viewer_1.qlabel_viewer is not None:
                if self.core.viewer_stats.viewer_1.activated:
                    viewers_img_index.append(self.core.viewer_stats.viewer_1.img_index)

            if self.core.viewer_stats.viewer_2.qlabel_viewer is not None:
                if self.core.viewer_stats.viewer_2.activated:
                    viewers_img_index.append(self.core.viewer_stats.viewer_2.img_index)

            if self.core.viewer_stats.viewer_3.qlabel_viewer is not None:
                if self.core.viewer_stats.viewer_3.activated:
                    viewers_img_index.append(self.core.viewer_stats.viewer_3.img_index)

            if self.core.viewer_stats.viewer_4.qlabel_viewer is not None:
                if self.core.viewer_stats.viewer_4.activated:
                    viewers_img_index.append(self.core.viewer_stats.viewer_4.img_index)

            if self.core.viewer_stats.viewer_5.qlabel_viewer is not None:
                if self.core.viewer_stats.viewer_5.activated:
                    viewers_img_index.append(self.core.viewer_stats.viewer_5.img_index)

            if self.core.viewer_stats.viewer_6.qlabel_viewer is not None:
                if self.core.viewer_stats.viewer_6.activated:
                    viewers_img_index.append(self.core.viewer_stats.viewer_6.img_index)

            if self.core.viewer_stats.viewer_7.qlabel_viewer is not None:
                if self.core.viewer_stats.viewer_7.activated:
                    viewers_img_index.append(self.core.viewer_stats.viewer_7.img_index)

            if self.core.viewer_stats.viewer_8.qlabel_viewer is not None:
                if self.core.viewer_stats.viewer_8.activated:
                    viewers_img_index.append(self.core.viewer_stats.viewer_8.img_index)

            try:
                most_frequent_index = self.most_frequent(viewers_img_index)
                viewers_img_index = [x for x in viewers_img_index if x != most_frequent_index][0]
                self.core.viewer_stats.viewer_1.img_index = viewers_img_index
                self.core.viewer_stats.viewer_2.img_index = viewers_img_index
                self.core.viewer_stats.viewer_3.img_index = viewers_img_index
                self.core.viewer_stats.viewer_4.img_index = viewers_img_index
                self.core.viewer_stats.viewer_5.img_index = viewers_img_index
                self.core.viewer_stats.viewer_6.img_index = viewers_img_index
                self.core.viewer_stats.viewer_7.img_index = viewers_img_index
                self.core.viewer_stats.viewer_8.img_index = viewers_img_index
            except:
                pass

            viewers_img_opacity = [
                self.core.viewer_stats.viewer_1.img_opacity,
                self.core.viewer_stats.viewer_2.img_opacity,
                self.core.viewer_stats.viewer_3.img_opacity,
                self.core.viewer_stats.viewer_4.img_opacity,
                self.core.viewer_stats.viewer_5.img_opacity,
                self.core.viewer_stats.viewer_6.img_opacity,
                self.core.viewer_stats.viewer_7.img_opacity,
                self.core.viewer_stats.viewer_8.img_opacity,
            ]
            most_frequent_opacity = self.most_frequent(viewers_img_opacity)
            try:
                viewers_img_opacity = [x for x in viewers_img_opacity if x != most_frequent_opacity][0]
                self.core.viewer_stats.viewer_1.img_opacity = viewers_img_opacity
                self.core.viewer_stats.viewer_2.img_opacity = viewers_img_opacity
                self.core.viewer_stats.viewer_3.img_opacity = viewers_img_opacity
                self.core.viewer_stats.viewer_4.img_opacity = viewers_img_opacity
                self.core.viewer_stats.viewer_5.img_opacity = viewers_img_opacity
                self.core.viewer_stats.viewer_6.img_opacity = viewers_img_opacity
                self.core.viewer_stats.viewer_7.img_opacity = viewers_img_opacity
                self.core.viewer_stats.viewer_8.img_opacity = viewers_img_opacity
            except:
                pass

            viewers_zoom_pos = [
                self.core.viewer_stats.viewer_1.zoom_pos,
                self.core.viewer_stats.viewer_2.zoom_pos,
                self.core.viewer_stats.viewer_3.zoom_pos,
                self.core.viewer_stats.viewer_4.zoom_pos,
                self.core.viewer_stats.viewer_5.zoom_pos,
                self.core.viewer_stats.viewer_6.zoom_pos,
                self.core.viewer_stats.viewer_7.zoom_pos,
                self.core.viewer_stats.viewer_8.zoom_pos,
            ]
            most_frequent_zoom_pos = self.most_frequent(viewers_zoom_pos)
            try:
                viewers_zoom_pos = [x for x in viewers_zoom_pos if x != most_frequent_zoom_pos][0]
                self.core.viewer_stats.viewer_1.zoom_pos = viewers_zoom_pos
                self.core.viewer_stats.viewer_2.zoom_pos = viewers_zoom_pos
                self.core.viewer_stats.viewer_3.zoom_pos = viewers_zoom_pos
                self.core.viewer_stats.viewer_4.zoom_pos = viewers_zoom_pos
                self.core.viewer_stats.viewer_5.zoom_pos = viewers_zoom_pos
                self.core.viewer_stats.viewer_6.zoom_pos = viewers_zoom_pos
                self.core.viewer_stats.viewer_7.zoom_pos = viewers_zoom_pos
                self.core.viewer_stats.viewer_8.zoom_pos = viewers_zoom_pos
            except:
                pass

            viewers_zoom_factor = [
                self.core.viewer_stats.viewer_1.zoom_factor,
                self.core.viewer_stats.viewer_2.zoom_factor,
                self.core.viewer_stats.viewer_3.zoom_factor,
                self.core.viewer_stats.viewer_4.zoom_factor,
                self.core.viewer_stats.viewer_5.zoom_factor,
                self.core.viewer_stats.viewer_6.zoom_factor,
                self.core.viewer_stats.viewer_7.zoom_factor,
                self.core.viewer_stats.viewer_8.zoom_factor,
            ]
            most_frequent_zoom_factor = self.most_frequent(viewers_zoom_factor)
            try:
                viewers_zoom_factor = [x for x in viewers_zoom_factor if x != most_frequent_zoom_factor][0]
                self.core.viewer_stats.viewer_1.zoom_factor = viewers_zoom_factor
                self.core.viewer_stats.viewer_2.zoom_factor = viewers_zoom_factor
                self.core.viewer_stats.viewer_3.zoom_factor = viewers_zoom_factor
                self.core.viewer_stats.viewer_4.zoom_factor = viewers_zoom_factor
                self.core.viewer_stats.viewer_5.zoom_factor = viewers_zoom_factor
                self.core.viewer_stats.viewer_6.zoom_factor = viewers_zoom_factor
                self.core.viewer_stats.viewer_7.zoom_factor = viewers_zoom_factor
                self.core.viewer_stats.viewer_8.zoom_factor = viewers_zoom_factor
            except:
                pass

        if self.core.viewer_stats.viewer_1.qlabel_viewer is not None:
            self.refresh(self.core.viewer_stats.viewer_1)
        if self.core.viewer_stats.viewer_2.qlabel_viewer is not None:
            self.refresh(self.core.viewer_stats.viewer_2)
        if self.core.viewer_stats.viewer_3.qlabel_viewer is not None:
            self.refresh(self.core.viewer_stats.viewer_3)
        if self.core.viewer_stats.viewer_4.qlabel_viewer is not None:
            self.refresh(self.core.viewer_stats.viewer_4)
        if self.core.viewer_stats.viewer_5.qlabel_viewer is not None:
            self.refresh(self.core.viewer_stats.viewer_5)
        if self.core.viewer_stats.viewer_6.qlabel_viewer is not None:
            self.refresh(self.core.viewer_stats.viewer_6)
        if self.core.viewer_stats.viewer_7.qlabel_viewer is not None:
            self.refresh(self.core.viewer_stats.viewer_7)
        if self.core.viewer_stats.viewer_8.qlabel_viewer is not None:
            self.refresh(self.core.viewer_stats.viewer_8)

    @staticmethod
    @logger.catch
    def opacity_adjuster(viewer_stats):
        """Adjusts the opacity of the segmentation mask dependent on the mouse wheel event delta"""
        if viewer_stats.activated and viewer_stats.img_data is not None:
            img_data = viewer_stats.img_data
            img_base = img_data[viewer_stats.img_index, :, :]
            # img_base = img_base.clip(self.get_img_intensity_min_temp, self.img_intensity_max_temp)
            # img_base = exposure.adjust_gamma(img_base, self.img_intensity_max_temp)
            img_base = qimage2ndarray.array2qimage(img_base)

            # Change opacity of segmentation
            seg_data = np.zeros(np.shape(viewer_stats.img_data))
            seg_overlay = seg_data[viewer_stats.img_index, :, :]
            try:
                # Triggered while scrolling with different image sizes by the segmentation mask
                if viewer_stats.seg_data is not None:
                    seg_overlay = viewer_stats.seg_data[viewer_stats.img_index, :, :]
                seg_overlay = QtGui.QImage(qimage2ndarray.gray2qimage(np.uint8(seg_overlay), normalize=False))
                seg_overlay.setColorTable(viewer_stats.segmentation_color_map)
                seg_overlay = seg_overlay.convertToFormat(QtGui.QImage.Format_ARGB32)
                painter = QtGui.QPainter()
                painter.begin(img_base)
                painter.setOpacity(viewer_stats.img_opacity * 0.01)
                painter.drawImage(0, 0, seg_overlay)
                painter.end()
            except Exception:
                pass
        else:
            img_base = qimage2ndarray.array2qimage(np.zeros((10, 10), dtype=int))
            viewer_stats.view_plane_name = None
        return img_base

    @staticmethod
    @logger.catch
    def zoom_function(viewer_stats, img_base):
        """Applies a crop window and rescales everything inside"""
        if viewer_stats.zoom_factor == 1.0 and viewer_stats.img_data is not None:
            img_base = img_base.scaled(
                viewer_stats.qlabel_viewer.geometry().width(),
                viewer_stats.qlabel_viewer.geometry().height(),
                QtCore.Qt.KeepAspectRatio,
            )
            viewer_stats.zoom_rect = (0, 0, viewer_stats.img_data.shape[2], viewer_stats.img_data.shape[1])
        elif viewer_stats.img_data is not None:
            # update zoomed image
            # get needed variables
            factor = viewer_stats.zoom_factor
            rect = viewer_stats.zoom_rect
            img_width = viewer_stats.img_data.shape[2]
            img_height = viewer_stats.img_data.shape[1]

            min_val = 1e-6
            max_val = 1e6
            x = viewer_stats.zoom_pos[0]
            if viewer_stats.qlabel_viewer.pixmap() is not None:
                xd = (
                    viewer_stats.qlabel_viewer.rect().width() - viewer_stats.qlabel_viewer.pixmap().rect().width()
                ) / 2
                win_pos_x = x - xd

                y = viewer_stats.zoom_pos[1]
                yd = (
                    viewer_stats.qlabel_viewer.rect().height() - viewer_stats.qlabel_viewer.pixmap().rect().height()
                ) / 2
                win_pos_y = y - yd

                if rect is None:
                    rect = QtCore.QRect(0, 0, img_width, img_height)

                pixmap_width = viewer_stats.qlabel_viewer.pixmap().rect().width()
                pixmap_height = viewer_stats.qlabel_viewer.pixmap().rect().height()

                crop_width = np.divide(img_width, np.clip(factor, a_min=min_val, a_max=max_val))
                crop_height = np.divide(img_height, np.clip(factor, a_min=min_val, a_max=max_val))
                # make sure crop width not larger than img
                crop_width = min(crop_width, img_width)
                crop_height = min(crop_height, img_height)

                # proportional distance from top/left
                x_factor = np.divide(win_pos_x, np.clip(pixmap_width, a_min=min_val, a_max=max_val))
                y_factor = np.divide(win_pos_y, np.clip(pixmap_height, a_min=min_val, a_max=max_val))

                # absolute position within old crop
                dx = np.multiply(x_factor, rect[2])
                dy = np.multiply(y_factor, rect[3])

                # position within new crop, keep ratio with factors
                dx_new = np.multiply(crop_width, x_factor)
                dy_new = np.multiply(crop_height, y_factor)

                # absolute position within image
                img_pos_x = rect[0] + dx
                img_pos_y = rect[1] + dy

                # left/top start position of new crop
                xs = img_pos_x - dx_new
                ys = img_pos_y - dy_new

                # make sure the crop is not outside image (no paddin done, smaller crop then)
                if xs < 0:
                    crop_width = crop_width + xs
                    xs = 0

                elif img_width - crop_width - xs < 0:
                    crop_width = img_width - xs

                if ys < 0:
                    crop_height = crop_height + ys
                    ys = 0

                elif img_height - crop_height - ys < 0:
                    crop_height = img_height - ys

                # left, top, width, height of new crop

                xs = 0 if np.isnan(xs) else xs
                ys = 0 if np.isnan(ys) else ys
                crop_width = 0 if np.isnan(crop_width) else crop_width
                crop_height = 0 if np.isnan(crop_height) else crop_height

                xs = 0 if np.isinf(xs) else xs
                ys = 0 if np.isinf(ys) else ys
                crop_width = 0 if np.isinf(crop_width) else crop_width
                crop_height = 0 if np.isinf(crop_height) else crop_height

                rect = QtCore.QRect(np.int32(xs), np.int32(ys), np.int32(crop_width), np.int32(crop_height))
                # set new crop
                img_base = img_base.copy(rect)
                viewer_stats.zoom_rect = (xs, ys, crop_width, crop_height)
                img_base = img_base.scaled(
                    viewer_stats.qlabel_viewer.geometry().width(),
                    viewer_stats.qlabel_viewer.geometry().height(),
                    QtCore.Qt.KeepAspectRatioByExpanding,
                    QtCore.Qt.FastTransformation,
                )
        return img_base

    @logger.catch
    def refresh(self, viewer_stats):
        """Sets the modified pixel to the qlabel"""
        if not all(np.shape(viewer_stats.img_data)):
            viewer_stats.img_data = np.zeros((10, 10, 10), dtype=int)

        img_base = self.opacity_adjuster(viewer_stats)
        img_base = self.zoom_function(viewer_stats, img_base)
        img_base = QtGui.QPixmap(img_base)
        viewer_stats.qlabel_viewer.setPixmap(img_base)

        if viewer_stats.activated and viewer_stats.docked_widget is not None:
            viewer_stats.docked_widget.set_slice_number()
        elif not viewer_stats.activated and viewer_stats.docked_widget is not None:
            viewer_stats.docked_widget.set_slice_number(text='')
