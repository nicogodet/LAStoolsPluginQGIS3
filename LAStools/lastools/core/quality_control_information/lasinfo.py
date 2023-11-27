# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasinfo.py
    ---------------------
    Date                 : November 2023
    Copyright            : (C) 2023 by rapidlasso GmbH
    Email                : info near rapidlasso point de
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'rapidlasso'
__date__ = 'September 2023'
__copyright__ = '(C) 2023, rapidlasso GmbH'

import os

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterNumber, QgsProcessingParameterEnum

from ..utils import LastoolsUtils, descript_quality_control_information as descript_info, paths
from ..algo import LastoolsAlgorithm


class LasInfo(LastoolsAlgorithm):
    TOOL_INFO = ('lasinfo', 'LasInfo')
    COMPUTE_DENSITY = "COMPUTE_DENSITY"
    REPAIR_BB = "REPAIR_BB"
    REPAIR_COUNTERS = "REPAIR_COUNTERS"
    HISTO1 = "HISTO1"
    HISTO2 = "HISTO2"
    HISTO3 = "HISTO3"
    HISTOGRAM = ["---", "x", "y", "z", "intensity", "classification", "scan_angle", "user_data", "point_source",
                 "gps_time", "X", "Y", "Z", "attribute0", "attribute1", "attribute2"]
    HISTO1_BIN = "HISTO1_BIN"
    HISTO2_BIN = "HISTO2_BIN"
    HISTO3_BIN = "HISTO3_BIN"

    def initAlgorithm(self, config=None):
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterBoolean(LasInfo.COMPUTE_DENSITY, "compute density", False))
        self.addParameter(QgsProcessingParameterBoolean(LasInfo.REPAIR_BB, "repair bounding box", False))
        self.addParameter(QgsProcessingParameterBoolean(LasInfo.REPAIR_COUNTERS, "repair counters", False))
        self.addParameter(QgsProcessingParameterEnum(LasInfo.HISTO1, "histogram", LasInfo.HISTOGRAM, False, 0))
        self.addParameter(QgsProcessingParameterNumber(
            LasInfo.HISTO1_BIN, "bin size", QgsProcessingParameterNumber.Double, 1.0, False, 0
        ))
        self.addParameter(QgsProcessingParameterEnum(LasInfo.HISTO2, "histogram", LasInfo.HISTOGRAM, False, 0))
        self.addParameter(QgsProcessingParameterNumber(
            LasInfo.HISTO2_BIN, "bin size", QgsProcessingParameterNumber.Double, 1.0, False, 0
        ))
        self.addParameter(QgsProcessingParameterEnum(LasInfo.HISTO3, "histogram", LasInfo.HISTOGRAM, False, 0))
        self.addParameter(QgsProcessingParameterNumber(
            LasInfo.HISTO3_BIN, "bin size", QgsProcessingParameterNumber.Double, 1.0, False, 0
        ))
        self.add_parameters_generic_output_gui("Output ASCII file", "txt", True)
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        if LastoolsUtils.has_wine():
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasinfo.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasinfo")]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, LasInfo.COMPUTE_DENSITY, context):
            commands.append("-cd")
        if self.parameterAsBool(parameters, LasInfo.REPAIR_BB, context):
            commands.append("-repair_bb")
        if self.parameterAsBool(parameters, LasInfo.REPAIR_COUNTERS, context):
            commands.append("-repair_counters")
        histo = self.parameterAsInt(parameters, LasInfo.HISTO1, context)
        if histo != 0:
            commands.append("-histo")
            commands.append(LasInfo.HISTOGRAM[histo])
            commands.append(str(self.parameterAsDouble(parameters, LasInfo.HISTO1_BIN, context)))
        histo = self.parameterAsInt(parameters, LasInfo.HISTO2, context)
        if histo != 0:
            commands.append("-histo")
            commands.append(LasInfo.HISTOGRAM[histo])
            commands.append(str(self.parameterAsDouble(parameters, LasInfo.HISTO2_BIN, context)))
        histo = self.parameterAsInt(parameters, LasInfo.HISTO3, context)
        if histo != 0:
            commands.append("-histo")
            commands.append(LasInfo.HISTOGRAM[histo])
            commands.append(str(self.parameterAsDouble(parameters, LasInfo.HISTO3_BIN, context)))
        self.add_parameters_generic_output_commands(parameters, context, commands, "-o")
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasInfo()

    def name(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["name"]

    def displayName(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["display_name"]

    def group(self):
        return descript_info["info"]["group"]

    def groupId(self):
        return descript_info["info"]["group_id"]

    def helpUrl(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["url_path"]

    def shortHelpString(self):
        return self.tr(descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["short_help_string"])

    def shortDescription(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["short_description"]

    def icon(self):
        licence_icon_path = descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["licence_icon_path"]
        return QIcon(f"{paths['img']}{licence_icon_path}")


class LasInfoPro(LastoolsAlgorithm):
    TOOL_INFO = ('lasinfo', 'LasInfoPro')
    COMPUTE_DENSITY = "COMPUTE_DENSITY"
    REPAIR_BB = "REPAIR_BB"
    REPAIR_COUNTERS = "REPAIR_COUNTERS"
    HISTO1 = "HISTO1"
    HISTO2 = "HISTO2"
    HISTO3 = "HISTO3"
    HISTOGRAM = ["---", "x", "y", "z", "intensity", "classification", "scan_angle", "user_data", "point_source",
                 "gps_time", "X", "Y", "Z", "attribute0", "attribute1", "attribute2"]
    HISTO1_BIN = "HISTO1_BIN"
    HISTO2_BIN = "HISTO2_BIN"
    HISTO3_BIN = "HISTO3_BIN"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.addParameter(QgsProcessingParameterBoolean(LasInfoPro.COMPUTE_DENSITY, "compute density", False))
        self.addParameter(QgsProcessingParameterBoolean(LasInfoPro.REPAIR_BB, "repair bounding box", False))
        self.addParameter(QgsProcessingParameterBoolean(LasInfoPro.REPAIR_COUNTERS, "repair counters", False))
        self.addParameter(QgsProcessingParameterEnum(LasInfoPro.HISTO1, "histogram", LasInfoPro.HISTOGRAM, False, 0))
        self.addParameter(QgsProcessingParameterNumber(
            LasInfoPro.HISTO1_BIN, "bin size", QgsProcessingParameterNumber.Double, 1.0, False, 0
        ))
        self.addParameter(QgsProcessingParameterEnum(LasInfoPro.HISTO2, "histogram", LasInfoPro.HISTOGRAM, False, 0))
        self.addParameter(QgsProcessingParameterNumber(
            LasInfoPro.HISTO2_BIN, "bin size", QgsProcessingParameterNumber.Double, 1.0, False, 0
        ))
        self.addParameter(QgsProcessingParameterEnum(LasInfoPro.HISTO3, "histogram", LasInfoPro.HISTOGRAM, False, 0))
        self.addParameter(QgsProcessingParameterNumber(
            LasInfoPro.HISTO3_BIN, "bin size", QgsProcessingParameterNumber.Double, 1.0, False, 0
        ))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()

    def processAlgorithm(self, parameters, context, feedback):
        if LastoolsUtils.has_wine():
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasinfo.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasinfo")]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, LasInfoPro.COMPUTE_DENSITY, context):
            commands.append("-cd")
        if self.parameterAsBool(parameters, LasInfoPro.REPAIR_BB, context):
            commands.append("-repair_bb")
        if self.parameterAsBool(parameters, LasInfoPro.REPAIR_COUNTERS, context):
            commands.append("-repair_counters")
        histo = self.parameterAsInt(parameters, LasInfoPro.HISTO1, context)
        if histo != 0:
            commands.append("-histo")
            commands.append(LasInfoPro.HISTOGRAM[histo])
            commands.append(str(self.parameterAsDouble(parameters, LasInfoPro.HISTO1_BIN, context)))
        histo = self.parameterAsInt(parameters, LasInfoPro.HISTO2, context)
        if histo != 0:
            commands.append("-histo")
            commands.append(LasInfoPro.HISTOGRAM[histo])
            commands.append(str(self.parameterAsDouble(parameters, LasInfoPro.HISTO2_BIN, context)))
        histo = self.parameterAsInt(parameters, LasInfoPro.HISTO3, context)
        if histo != 0:
            commands.append("-histo")
            commands.append(LasInfoPro.HISTOGRAM[histo])
            commands.append(str(self.parameterAsDouble(parameters, LasInfoPro.HISTO3_BIN, context)))
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        commands.append("-otxt")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasInfoPro()

    def name(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["name"]

    def displayName(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["display_name"]

    def group(self):
        return descript_info["info"]["group"]

    def groupId(self):
        return descript_info["info"]["group_id"]

    def helpUrl(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["url_path"]

    def shortHelpString(self):
        return self.tr(descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["short_help_string"])

    def shortDescription(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["short_description"]

    def icon(self):
        licence_icon_path = descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["licence_icon_path"]
        return QIcon(f"{paths['img']}{licence_icon_path}")
