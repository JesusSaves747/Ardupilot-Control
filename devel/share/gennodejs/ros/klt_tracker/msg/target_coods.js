// Auto-generated. Do not edit!

// (in-package klt_tracker.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class target_coods {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.xTar = null;
      this.yTar = null;
    }
    else {
      if (initObj.hasOwnProperty('xTar')) {
        this.xTar = initObj.xTar
      }
      else {
        this.xTar = 0.0;
      }
      if (initObj.hasOwnProperty('yTar')) {
        this.yTar = initObj.yTar
      }
      else {
        this.yTar = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type target_coods
    // Serialize message field [xTar]
    bufferOffset = _serializer.float64(obj.xTar, buffer, bufferOffset);
    // Serialize message field [yTar]
    bufferOffset = _serializer.float64(obj.yTar, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type target_coods
    let len;
    let data = new target_coods(null);
    // Deserialize message field [xTar]
    data.xTar = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [yTar]
    data.yTar = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 16;
  }

  static datatype() {
    // Returns string type for a message object
    return 'klt_tracker/target_coods';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '3f304876c8960b3c74eda82366a1bf42';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64 xTar
    float64 yTar
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new target_coods(null);
    if (msg.xTar !== undefined) {
      resolved.xTar = msg.xTar;
    }
    else {
      resolved.xTar = 0.0
    }

    if (msg.yTar !== undefined) {
      resolved.yTar = msg.yTar;
    }
    else {
      resolved.yTar = 0.0
    }

    return resolved;
    }
};

module.exports = target_coods;
