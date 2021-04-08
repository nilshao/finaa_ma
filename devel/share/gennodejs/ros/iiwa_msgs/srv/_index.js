
"use strict";

let SetPTPCartesianSpeedLimits = require('./SetPTPCartesianSpeedLimits.js')
let SetEndpointFrame = require('./SetEndpointFrame.js')
let ConfigureControlMode = require('./ConfigureControlMode.js')
let SetWorkpiece = require('./SetWorkpiece.js')
let TimeToDestination = require('./TimeToDestination.js')
let SetSpeedOverride = require('./SetSpeedOverride.js')
let SetPTPJointSpeedLimits = require('./SetPTPJointSpeedLimits.js')
let SetSmartServoJointSpeedLimits = require('./SetSmartServoJointSpeedLimits.js')
let SetSmartServoLinSpeedLimits = require('./SetSmartServoLinSpeedLimits.js')

module.exports = {
  SetPTPCartesianSpeedLimits: SetPTPCartesianSpeedLimits,
  SetEndpointFrame: SetEndpointFrame,
  ConfigureControlMode: ConfigureControlMode,
  SetWorkpiece: SetWorkpiece,
  TimeToDestination: TimeToDestination,
  SetSpeedOverride: SetSpeedOverride,
  SetPTPJointSpeedLimits: SetPTPJointSpeedLimits,
  SetSmartServoJointSpeedLimits: SetSmartServoJointSpeedLimits,
  SetSmartServoLinSpeedLimits: SetSmartServoLinSpeedLimits,
};
