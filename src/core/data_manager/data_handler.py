import typing as t
from copy import deepcopy

import numpy as np
import SimpleITK as sitk
from loguru import logger

from src.core.configs.static_params import USED_MODALITY_NAMES


class DataHandler:
    """Shares and controls ephemeral/lasting data between process steps"""

    def __init__(self):
        self._lasting_store = {
            'brain_mask_atlas_sitk': None,
            'brain_mask_atlas_ndarray': None,
            'seg_mask_atlas_sitk': None,
            'seg_mask_atlas_ndarray': None,
            'seg_mask_measure_volumes': None,
            'mac_donald_json': None,
            'mac_donald_base_image': None,
            'mac_donald_border_mask': None,
            'mac_donald_longest_line': None,
            'mac_donald_longest_cross_line': None,
        }

        self._ephemeral_results = deepcopy(self._lasting_store)
        self._ephemeral_input = {}
        self._ephemeral_output = {}
        self._case_name = None

        self.persistent = {}
        for modality in USED_MODALITY_NAMES:
            self.persistent[f'{modality}_sitk'] = None

        used_modality_names = USED_MODALITY_NAMES
        self._init_lasting_store(used_modality_names)
        self._init_ephemeral_results(used_modality_names)
        self._init_ephemerals(used_modality_names)
        logger.info(f'Init {self.__class__.__name__}')

    def __getitem__(self, key: str) -> t.Any:
        """Returns the value of a given key from the ephemeral input"""
        if key in self._ephemeral_input:
            return self._ephemeral_input.get(key, None)
        raise KeyError(f'key: "{key}" is not present in ephemeral input, None is returned')

    def __setitem__(self, key: str, value: t.Any) -> None:
        """Sets value for a given key  from the ephemeral output"""
        if key in self._ephemeral_output:
            self._ephemeral_output[key] = value
        else:
            raise KeyError(f'key: "{key}" is not present in ephemeral output')

    def __repr__(self) -> str:
        """Show data handler holdings"""
        column_1, column_2 = '45', '40'
        message = f'{"##### ephemerals #####":<{column_1}}{"input":<{column_2}}{"output"}'
        for key, value in self._ephemeral_input.items():
            message = (
                f'{message}\n{key:<{column_1}}{str(type(value)):<{column_2}}{str(type(self._ephemeral_output[key]))}'
            )
        message = f'{message}\n\n{"##### ephemeral results #####":<{column_1}}'
        for key, value in self._ephemeral_results.items():
            message = f'{message}\n{key:<{column_1}}{str(type(value))}'
        message = f'{message}\n\n{"##### lasting dict #####":<{column_1}}'
        for key, value in self._lasting_store.items():
            message = f'{message}\n{key:<{column_1}}{str(type(value))}'
        return message

    @property
    def case_name(self) -> str:
        """Returns case name"""
        return self._case_name

    @case_name.setter
    def case_name(self, value: t.Any) -> None:
        """Sets case name"""
        self._case_name = value

    def _init_lasting_store(self, modalities: list) -> None:
        """Init modalities in a compact way"""
        store_tags = [
            '_brain_mask_native_sitk',
            '_brain_mask_native_ndarray',
            '_seg_mask_native_sitk',
            '_seg_mask_native_ndarray',
            '_native_image_orientation',
            '_native_sitk',
            '_native_ndarray',
            '_native_meta',
            '_registration_sitk',
            '_registration_ndarray',
            '_registration_meta',
            '_registration_transformation',
            '_registration_inverse_transformation',
            '_registration_inverse_sitk',
            '_skull_strip_sitk',
            '_skull_strip_ndarray',
            '_skull_strip_meta',
            '_pyradiomics_feature',
        ]

        for modality in modalities:  # expand _store with store tags for every modality
            for store_tag in store_tags:
                self._lasting_store[f'{modality}{store_tag}'] = None

    def _init_ephemerals(self, modalities: list) -> None:
        """Init modalities in a compact way"""
        store_tags = [
            '_ephemeral_image_orientation',
            '_ephemeral_sitk',
            '_ephemeral_ndarray',
            '_ephemeral_meta',
            '_ephemeral_transformation',
            '_ephemeral_inverse_transformation',
            '_ephemeral_inverse_sitk',
            '_ephemeral_inverse_meta',
        ]

        for modality in modalities:  # expand _store with store tags for every modality
            for store_tag in store_tags:
                self._ephemeral_input[f'{modality}{store_tag}'] = None
                self._ephemeral_output[f'{modality}{store_tag}'] = None

    def _init_ephemeral_results(self, modalities: list) -> None:
        """Init modalities for ephemeral results in a compact way"""
        store_tags = [
            '_brain_mask_native_sitk',
            '_brain_mask_native_ndarray',
            '_seg_mask_native_sitk',
            '_seg_mask_native_ndarray',
            '_pyradiomics_feature',
        ]

        for modality in modalities:  # expand _store with store tags for every modality
            for store_tag in store_tags:
                self._ephemeral_results[f'{modality}{store_tag}'] = None

    def _reset_ephemeral_results(self) -> None:
        """After each state the ephemeral output gets copied to the ephemeral input and set to None afterwards"""
        for key in self._ephemeral_results:
            self._ephemeral_results[key] = None
        logger.debug('Ephemeral results reset done')

    def _ephemeral_transition(self) -> None:
        """After each state the ephemeral output gets copied to the ephemeral input and set to None afterwards"""
        for key in self._ephemeral_input:
            self._ephemeral_input[key] = deepcopy(self._ephemeral_output[key])
            self._ephemeral_output[key] = None
        logger.debug('Ephemeral transition done')

    def set_ephemeral_results(self, key: str, value: t.Any, new_key=False) -> None:
        """Sets ephemeral results"""
        if key in self._ephemeral_results or new_key:
            self._ephemeral_results[key] = value
            if new_key:
                self._lasting_store[key] = {}
        else:
            raise KeyError(f'key: "{key}" is not present in ephemeral results')

    def get_ephemeral_results(self, key: str) -> t.Any:
        """Sets ephemeral results"""
        if key in self._ephemeral_results:
            return deepcopy(self._ephemeral_results[key])
        raise KeyError(f'key: "{key}" is not present in ephemeral results')

    def reset(self) -> None:
        """Every value of ephemeral/enduring in the data base by setting them to None"""
        for data in [self._lasting_store, self._ephemeral_input, self._ephemeral_output, self._ephemeral_results]:
            for key in data.keys():
                data[key] = None
        logger.debug(f'Reset {self.__class__.__name__}')

    def get_from_lasting_store(self, key: str) -> t.Any:
        """Takes a lasting store key and returns the belonging value"""
        if key in self._lasting_store:
            return deepcopy(self._lasting_store[key])
        logger.warning(f'key: "{key}" is not present in lasting store, None is returned')
        return None

    def get_lasting_store(self) -> dict:
        """Returns the lasting store"""
        return deepcopy(self._lasting_store)

    def get_ephemeral_output(self, key: str) -> t.Any:
        """Returns the value of a given key from the ephemeral output, only used for gui update"""
        if key in self._ephemeral_output:
            return deepcopy(self._ephemeral_output.get(key, None))
        logger.warning(f'key: "{key}" is not present in ephemeral output, None is returned')
        return None

    def copy_ephemeral_to_lasting_store(self, state: str = 'native') -> None:
        """Deepcopy from ephemeral to lasting store for the given state without cleaning ephemeral store"""
        allowed_states = ['native', 'dockers']
        if state not in allowed_states:
            raise NotImplementedError('state tag is not supported')

        for eph_key, eph_value in self._ephemeral_output.items():  # copy ephemeral output to lasting
            lasting_key = eph_key.replace('ephemeral', state)
            if lasting_key in self._lasting_store:
                self._lasting_store[lasting_key] = deepcopy(eph_value)

        for eph_key, eph_value in self._ephemeral_results.items():  # copy results store to lasting
            if eph_key in self._lasting_store and eph_value is not None:
                self._lasting_store[eph_key] = deepcopy(eph_value)

        self._ephemeral_transition()
        self._reset_ephemeral_results()

    def check_ephemeral_input(self, modalities: list or None = None, extensions: list or None = None) -> bool:
        """Checks ephemeral input sitk store for certain modalities and extensions"""

        if modalities:
            if not isinstance(modalities, list):
                raise TypeError('modalities is not a list')
            if '_' in modalities:
                raise ValueError('modalities without _')
        else:
            raise ValueError('modalities must be specified')

        if extensions:
            if not isinstance(extensions, list):
                raise TypeError('extension is not a list')
            if '_' in extensions:
                raise ValueError('extensions without _')
        else:
            extensions = ['sitk', 'ndarray']

        check = True
        for modality in modalities:
            for extension in extensions:
                if self._ephemeral_input.get(f'{modality}_ephemeral_{extension}', None) is None:
                    check = False

        return check

    def copy_ephemeral_input_to_ephemeral_output(self) -> None:
        """Pass the ephemeral input to the ephemeral output, aka a pass through to keep the data in the pipeline.
        Used when a module does not modify any of the input images, like segmentation, analytics, etc"""
        for key, value in self._ephemeral_input.items():
            self._ephemeral_output[key] = value

    def get_segmentation_mask(self, extension: str = 'sitk', warning: bool = False) -> sitk.Image or np.ndarray:
        """Favours the lasting store over mask from persistent data"""
        if self._lasting_store.get(f'seg_mask_atlas_{extension}', None) is not None:  # from lasting store
            logger.trace('retrieved segmentation mask from lasting store')
            return deepcopy(self._lasting_store[f'seg_mask_atlas_{extension}'])
        if self.persistent.get('seg_mask_sitk', None) is not None:  # persistent store
            logger.trace('retrieved segmentation mask from persistent data')
            if extension == 'ndarray':
                return deepcopy(sitk.GetArrayFromImage(self.persistent.get('seg_mask_sitk', None)))
            return deepcopy(self.persistent.get('seg_mask_sitk', None))
        logger.trace('retrieved as None as segmentation mask')
        if warning:
            raise UserWarning('Segmentation mask not found')
        return None

    def get_active_modalities(self, key_name: str) -> list:
        """Returns a list of all modalities in the ephemeral input"""
        modalities = []
        for key, value in self._ephemeral_input.items():
            if key_name in key and value is not None:
                modalities.append(key.split('_')[0])
        return list(set(modalities))

    def get_image(self, modality_priorities: list or None = None, extension: str = 'sitk') -> sitk.Image or np.ndarray:
        """Returns first satisfied image from the priority list"""
        if modality_priorities:
            if not isinstance(modality_priorities, list):
                raise TypeError('modalities is not a list')
            if '_' in modality_priorities:
                raise ValueError('modalities without _')

        if not isinstance(extension, str):
            raise TypeError('extension has to be a string')

        for modality in modality_priorities:
            if self._ephemeral_input.get(f'{modality}_ephemeral_{extension}', None) is not None:
                logger.trace(f'returns ephemeral img: {modality} {extension}, priority list: {modality_priorities}')
                if extension == 'ndarray':
                    return deepcopy(self._ephemeral_input.get(f'{modality}_ephemeral_{extension}', None))
                return deepcopy(self._ephemeral_input.get(f'{modality}_ephemeral_{extension}', None))

            if self.persistent.get(f'{modality}_sitk', None) is not None:
                logger.trace(f'returns persistent img: {modality} {extension}, priority list: {modality_priorities}')
                if extension == 'ndarray':
                    return deepcopy(sitk.GetArrayFromImage(self.persistent[f'{modality}_sitk']))
                return deepcopy(self._ephemeral_input.get(f'{modality}_ephemeral_{extension}', None))

        logger.debug(f'Failed to retrieve {modality_priorities} {extension} from lasting store')
        return None

    def get_segmentation_mask_labels(self) -> list or None:
        """Returns a list of labels from the segmentation mask"""
        if self._lasting_store.get('seg_mask_atlas_sitk', None) is not None:
            labels = list(np.unique(sitk.GetArrayFromImage(self._lasting_store['seg_mask_atlas_sitk'])))
            labels = [int(i) for i in labels if i != 0]
            logger.trace(f'retrieved segmentation mask labels from lasting store -> {labels}')
            return labels
        if self.persistent.get('seg_mask_sitk', None) is not None:
            labels = list(np.unique(sitk.GetArrayFromImage(self.persistent['seg_mask_sitk'])))
            labels = [int(i) for i in labels if i != 0]
            logger.trace(f'retrieved segmentation mask labels from persistent store -> {labels}')
            return labels
        return None
