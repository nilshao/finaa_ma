// Auto-generated. Do not edit!

// (in-package virtual.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class CaliInfo {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.marker = null;
      this.markerincamera_measure = null;
      this.markerincamera_truth = null;
      this.eeinbase = null;
      this.baseincamera = null;
      this.markerinee = null;
    }
    else {
      if (initObj.hasOwnProperty('marker')) {
        this.marker = initObj.marker
      }
      else {
        this.marker = 0;
      }
      if (initObj.hasOwnProperty('markerincamera_measure')) {
        this.markerincamera_measure = initObj.markerincamera_measure
      }
      else {
        this.markerincamera_measure = [];
      }
      if (initObj.hasOwnProperty('markerincamera_truth')) {
        this.markerincamera_truth = initObj.markerincamera_truth
      }
      else {
        this.markerincamera_truth = [];
      }
      if (initObj.hasOwnProperty('eeinbase')) {
        this.eeinbase = initObj.eeinbase
      }
      else {
        this.eeinbase = [];
      }
      if (initObj.hasOwnProperty('baseincamera')) {
        this.baseincamera = initObj.baseincamera
      }
      else {
        this.baseincamera = [];
      }
      if (initObj.hasOwnProperty('markerinee')) {
        this.markerinee = initObj.markerinee
      }
      else {
        this.markerinee = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type CaliInfo
    // Serialize message field [marker]
    bufferOffset = _serializer.int64(obj.marker, buffer, bufferOffset);
    // Serialize message field [markerincamera_measure]
    bufferOffset = _arraySerializer.float64(obj.markerincamera_measure, buffer, bufferOffset, null);
    // Serialize message field [markerincamera_truth]
    bufferOffset = _arraySerializer.float64(obj.markerincamera_truth, buffer, bufferOffset, null);
    // Serialize message field [eeinbase]
    bufferOffset = _arraySerializer.float64(obj.eeinbase, buffer, bufferOffset, null);
    // Serialize message field [baseincamera]
    bufferOffset = _arraySerializer.float64(obj.baseincamera, buffer, bufferOffset, null);
    // Serialize message field [markerinee]
    bufferOffset = _arraySerializer.float64(obj.markerinee, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type CaliInfo
    let len;
    let data = new CaliInfo(null);
    // Deserialize message field [marker]
    data.marker = _deserializer.int64(buffer, bufferOffset);
    // Deserialize message field [markerincamera_measure]
    data.markerincamera_measure = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [markerincamera_truth]
    data.markerincamera_truth = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [eeinbase]
    data.eeinbase = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [baseincamera]
    data.baseincamera = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [markerinee]
    data.markerinee = _arrayDeserializer.float64(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.markerincamera_measure.length;
    length += 8 * object.markerincamera_truth.length;
    length += 8 * object.eeinbase.length;
    length += 8 * object.baseincamera.length;
    length += 8 * object.markerinee.length;
    return length + 28;
  }

  static datatype() {
    // Returns string type for a message object
    return 'virtual/CaliInfo';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'aa331633c72b6e8b9017db2e4147569d';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int64 marker
    float64[] markerincamera_measure
    float64[] markerincamera_truth
    float64[] eeinbase
    float64[] baseincamera
    float64[] markerinee
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new CaliInfo(null);
    if (msg.marker !== undefined) {
      resolved.marker = msg.marker;
    }
    else {
      resolved.marker = 0
    }

    if (msg.markerincamera_measure !== undefined) {
      resolved.markerincamera_measure = msg.markerincamera_measure;
    }
    else {
      resolved.markerincamera_measure = []
    }

    if (msg.markerincamera_truth !== undefined) {
      resolved.markerincamera_truth = msg.markerincamera_truth;
    }
    else {
      resolved.markerincamera_truth = []
    }

    if (msg.eeinbase !== undefined) {
      resolved.eeinbase = msg.eeinbase;
    }
    else {
      resolved.eeinbase = []
    }

    if (msg.baseincamera !== undefined) {
      resolved.baseincamera = msg.baseincamera;
    }
    else {
      resolved.baseincamera = []
    }

    if (msg.markerinee !== undefined) {
      resolved.markerinee = msg.markerinee;
    }
    else {
      resolved.markerinee = []
    }

    return resolved;
    }
};

module.exports = CaliInfo;
