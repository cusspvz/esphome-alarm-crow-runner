
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import alarm_control_panel
from esphome.core import coroutine_with_priority
from esphome.const import (
    CONF_ID,
    CONF_BINARY_SENSORS,
    CONF_INPUT,
    CONF_RESTORE_MODE,
)
from .. import crow_runner_ns


CODEOWNERS = ["@cusspvz"]


CrowRunnerAlarmControlPanel = crow_runner_ns.class_(
    "CrowRunnerAlarmControlPanel",
     alarm_control_panel.AlarmControlPanel, cg.Component
)

CROW_RUNNER_ALARM_CONTROL_PANEL_SCHEMA = (
    alarm_control_panel.ALARM_CONTROL_PANEL_SCHEMA.extend(
        {
            cv.GenerateID(): cv.declare_id(CrowRunnerAlarmControlPanel),
            cv.Optional("codes"): cv.ensure_list(cv.string_strict),
        }
    ).extend(cv.COMPONENT_SCHEMA)
)

def validate_config(config):

    return config

# Export configuration schema
CONFIG_SCHEMA = cv.All(
    CROW_RUNNER_ALARM_CONTROL_PANEL_SCHEMA,
    validate_config,
)

@coroutine_with_priority(100.0)
async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await alarm_control_panel.register_alarm_control_panel(var, config)

    if "codes" in config:
        for acode in config["codes"]:
            cg.add(var.add_code(acode))
