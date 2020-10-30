#!/usr/bin/env python
# coding: utf8
#
# Copyright (c) 2020 Centre National d'Etudes Spatiales (CNES).
#
# This file is part of PANDORA
#
#     https://github.com/CNES/Pandora_pandora
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
This module contains functions to test the configuration
"""

import unittest

import json_checker
from transitions import MachineError

import pandora.json_checker as JSON_checker
from pandora.state_machine import PandoraMachine


class TestConfig(unittest.TestCase):
    """
    TestConfig class allows to test the configuration
    """

    def setUp(self):
        """
        Method called to prepare the test fixture

        """

    @staticmethod
    def test_check_input_section():
        """
        Test the method check_input_section
        """

        # Test configuration with left disparity grids and right disparity = none
        cfg = {
            'input': {
                'img_left': 'tests/pandora/left.png',
                'img_right': 'tests/pandora/right.png',
                'disp_min': 'tests/pandora/disp_min_grid.tif',
                'disp_max': 'tests/pandora/disp_max_grid.tif'
            }
        }
        cfg_return = JSON_checker.check_input_section(cfg)
        if (cfg_return['input']['disp_min_right'] is not None) and (cfg_return['input']['disp_max_right'] is not None):
            raise AssertionError

        # Test configuration with left disparity as integer
        cfg = {
            'input': {
                'img_left': 'tests/pandora/left.png',
                'img_right': 'tests/pandora/right.png',
                'disp_min': -60,
                'disp_max': 0
            }
        }
        cfg_return = JSON_checker.check_input_section(cfg)

        # Test configuration with left and right disparity grids
        cfg = {
            'input': {
                'img_left': 'tests/pandora/left.png',
                'img_right': 'tests/pandora/right.png',
                'disp_min': 'tests/pandora/disp_min_grid.tif',
                'disp_max': 'tests/pandora/disp_max_grid.tif',
                'disp_min_right': 'tests/pandora/disp_min_grid.tif',
                'disp_max_right': 'tests/pandora/disp_max_grid.tif'
            }
        }
        cfg_return = JSON_checker.check_input_section(cfg)
        if (cfg_return['input']['disp_min_right'] != 'tests/pandora/disp_min_grid.tif') and \
                (cfg_return['input']['disp_max_right'] != 'tests/pandora/disp_max_grid.tif'):
            raise AssertionError

    def test_check_input_section_with_error(self):
        """
        Test the method check_input_section that must raise an error
        """
        # Test configuration with left disparity min as grids and left disparity max as integer
        cfg = {
            'input': {
                'img_left': 'tests/pandora/left.png',
                'img_right': 'tests/pandora/right.png',
                'disp_min': 'tests/pandora/disp_min_grid.tif',
                'disp_max': 45,
            }
        }
        # Json checker must raise an error
        self.assertRaises(json_checker.core.exceptions.DictCheckerError, JSON_checker.check_input_section, cfg)

        # Test configuration with left disparity grids and right disparity max as integer
        cfg = {
            'input': {
                'img_left': 'tests/pandora/left.png',
                'img_right': 'tests/pandora/right.png',
                'disp_min': 'tests/pandora/disp_min_grid.tif',
                'disp_max': 'tests/pandora/disp_max_grid.tif',
                'disp_max_right': -4
            }
        }
        # Json checker must raise an error
        self.assertRaises(json_checker.core.exceptions.DictCheckerError, JSON_checker.check_input_section, cfg)

        # Test configuration with left disparity grids and right disparity max as integer
        cfg = {
            'input': {
                'img_left': 'tests/pandora/left.png',
                'img_right': 'tests/pandora/right.png',
                'disp_min': 'tests/pandora/disp_min_grid.tif',
                'disp_max': 'tests/pandora/disp_max_grid.tif',
                'disp_max_right': -4,
                'disp_min_right': 'tests/pandora/disp_max_grid.tif'
            }
        }
        # Json checker must raise an error
        self.assertRaises(json_checker.core.exceptions.DictCheckerError, JSON_checker.check_input_section, cfg)

        # Test configuration with left disparity grids and right disparity min as integer
        cfg = {
            'input': {
                'img_left': 'tests/pandora/left.png',
                'img_right': 'tests/pandora/right.png',
                'disp_min': 'tests/pandora/disp_min_grid.tif',
                'disp_max': 'tests/pandora/disp_max_grid.tif',
                'disp_min_right': -4
            }
        }
        # Json checker must raise an error
        self.assertRaises(json_checker.core.exceptions.DictCheckerError, JSON_checker.check_input_section, cfg)

        # Test configuration with left disparity grids and right disparities as integer
        cfg = {
            'input': {
                'img_left': 'tests/pandora/left.png',
                'img_right': 'tests/pandora/right.png',
                'disp_min': 'tests/pandora/disp_min_grid.tif',
                'disp_max': 'tests/pandora/disp_max_grid.tif',
                'disp_min_right': -4,
                'disp_max_right': 0
            }
        }
        # Json checker must raise an error
        self.assertRaises(json_checker.core.exceptions.DictCheckerError, JSON_checker.check_input_section, cfg)

    def test_check_conf(self):
        """
        Test the method check_conf
        """

        # Check the configuration returned with left disparity grids

        pandora_machine = PandoraMachine()
        cfg = {
            'input': {
                'img_left': 'tests/pandora/left.png',
                'img_right': 'tests/pandora/right.png',
                'disp_min': 'tests/pandora/disp_min_grid.tif',
                'disp_max': 'tests/pandora/disp_max_grid.tif'
            },
            'pipeline': {
                'stereo': {
                    'stereo_method': 'zncc',
                    'window_size': 5,
                    'subpix': 2
                },
                'disparity': {
                    'disparity_method': 'wta'
                }
            }
        }

        cfg_return = JSON_checker.check_conf(cfg, pandora_machine)
        cfg_gt = {
            'image': {
                'nodata1': 0,
                'nodata2': 0,
                'valid_pixels': 0,
                'no_data': 1
            },
            'input': {
                'left_mask': None,
                'right_mask': None,
                'disp_min_right': None,
                'disp_max_right': None,
                'img_left': 'tests/pandora/left.png',
                'img_right': 'tests/pandora/right.png',
                'disp_min': 'tests/pandora/disp_min_grid.tif',
                'disp_max': 'tests/pandora/disp_max_grid.tif'
            },

            'pipeline': {
                'right_disp_map': {
                    'method': 'none'
                },
                'stereo': {
                    'stereo_method': 'zncc',
                    'window_size': 5,
                    'subpix': 2
                },
                'disparity': {
                    'disparity_method': 'wta',
                    'invalid_disparity': -9999
                }
            }

        }
        assert cfg_return == cfg_gt

        # Check the configuration returned with left and right disparity grids
        cfg = {
            'input': {
                'img_left': 'tests/pandora/left.png',
                'img_right': 'tests/pandora/right.png',
                'disp_min': 'tests/pandora/disp_min_grid.tif',
                'disp_max': 'tests/pandora/disp_max_grid.tif',
                'disp_min_right': 'tests/pandora/disp_min_grid.tif',
                'disp_max_right': 'tests/pandora/disp_max_grid.tif'
            },
            'pipeline': {
                'stereo': {
                    'stereo_method': 'zncc',
                    'window_size': 5,
                    'subpix': 2
                },
                'disparity': {
                    'disparity_method': 'wta'
                }
            }

        }
        cfg_return = JSON_checker.check_conf(cfg, pandora_machine)
        cfg_gt = {
            'image': {
                'nodata1': 0,
                'nodata2': 0,
                'valid_pixels': 0,
                'no_data': 1
            },
            'input': {
                'left_mask': None,
                'right_mask': None,
                'disp_min_right': 'tests/pandora/disp_min_grid.tif',
                'disp_max_right': 'tests/pandora/disp_max_grid.tif',
                'img_left': 'tests/pandora/left.png',
                'img_right': 'tests/pandora/right.png',
                'disp_min': 'tests/pandora/disp_min_grid.tif',
                'disp_max': 'tests/pandora/disp_max_grid.tif'
            },

            'pipeline':
                {
                    'right_disp_map': {
                        'method': 'none'
                    },
                    'stereo': {
                        'stereo_method': 'zncc',
                        'window_size': 5,
                        'subpix': 2
                    },
                    'disparity': {
                        'disparity_method': 'wta',
                        'invalid_disparity': -9999
                    }
                }

        }

        assert cfg_return == cfg_gt

        # Check the configuration returned with left disparity grids and cross checking method
        cfg = {
            'input': {
                'img_left': 'tests/pandora/left.png',
                'img_right': 'tests/pandora/right.png',
                'disp_min': 'tests/pandora/disp_min_grid.tif',
                'disp_max': 'tests/pandora/disp_max_grid.tif'
            },
            'pipeline':
                {
                    'right_disp_map': {
                        'method': 'accurate'
                    },
                    'stereo': {
                        'stereo_method': 'zncc',
                        'window_size': 5,
                        'subpix': 2
                    },
                    'disparity': {
                        'disparity_method': 'wta'
                    },
                    'validation': {
                        'validation_method': 'cross_checking'
                    }
                }
        }

        # When left disparities are grids and right are none, cross checking method cannot be used : the program exits
        self.assertRaises(SystemExit, JSON_checker.check_conf, cfg, pandora_machine)

        # Check the configuration returned with left and right disparity grids and cross checking method
        cfg = {
            'input': {
                'img_left': 'tests/pandora/left.png',
                'img_right': 'tests/pandora/right.png',
                'disp_min': 'tests/pandora/disp_min_grid.tif',
                'disp_max': 'tests/pandora/disp_max_grid.tif',
                'disp_min_right': 'tests/pandora/disp_min_grid.tif',
                'disp_max_right': 'tests/pandora/disp_max_grid.tif',
            },
            'pipeline': {
                'right_disp_map': {
                    'method': 'accurate'
                },
                'stereo': {
                    'stereo_method': 'zncc',
                    'window_size': 5,
                    'subpix': 2
                },
                'disparity': {
                    'disparity_method': 'wta',
                    'invalid_disparity': -9999
                },
                'validation': {
                    'validation_method': 'cross_checking'
                }
            }

        }
        # When left and right disparities are grids, cross checking method can be used
        cfg_return = JSON_checker.check_conf(cfg, pandora_machine)
        cfg_gt = {
            'image': {
                'nodata1': 0,
                'nodata2': 0,
                'valid_pixels': 0,
                'no_data': 1
            },
            'input': {
                'left_mask': None,
                'right_mask': None,
                'disp_min_right': 'tests/pandora/disp_min_grid.tif',
                'disp_max_right': 'tests/pandora/disp_max_grid.tif',
                'img_left': 'tests/pandora/left.png',
                'img_right': 'tests/pandora/right.png',
                'disp_min': 'tests/pandora/disp_min_grid.tif',
                'disp_max': 'tests/pandora/disp_max_grid.tif'
            },
            'pipeline': {
                'right_disp_map': {
                    'method': 'accurate'
                },
                'stereo': {
                    'stereo_method': 'zncc',
                    'window_size': 5,
                    'subpix': 2
                },
                'disparity': {
                    'disparity_method': 'wta',
                    'invalid_disparity': -9999
                },
                'validation': {
                    'validation_method': 'cross_checking',
                    'cross_checking_threshold': 1.0,
                    'right_left_mode': 'accurate'
                }
            }

        }

        assert cfg_return == cfg_gt

    def test_check_pipeline_section_with_error(self):
        """
        Test the method check_input_section that must raise an error from PandoraMachine
        """

        cfg_pipeline = {
            'pipeline': {
                'right_disp_map': {
                    'method': 'accurate'
                },
                'stereo': {
                    'stereo_method': 'zncc',
                    'window_size': 5,
                    'subpix': 2
                },
                'filter': {
                    'filter_method': 'median'
                },
                'disparity': {
                    'disparity_method': 'wta',
                    'invalid_disparity': -9999
                },
                'validation': {
                    'validation_method': 'cross_checking'
                }
            }
        }

        pandora_machine = PandoraMachine()

        self.assertRaises(MachineError, JSON_checker.check_pipeline_section, cfg_pipeline, pandora_machine)


if __name__ == '__main__':
    unittest.main()
