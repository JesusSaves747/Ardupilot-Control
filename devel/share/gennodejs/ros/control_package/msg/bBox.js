// Auto-generated. Do not edit!

// (in-package control_package.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class bBox {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.top_left_x = null;
      this.top_left_y = null;
      this.width = null;
      this.height = null;
    }
    else {
      if (initObj.hasOwnProperty('top_left_x')) {
        this.top_left_x = initObj.top_left_x
      }
      else {
        this.top_left_x = 0.0;
      }
      if (initObj.hasOwnProperty('top_left_y')) {
        this.top_left_y = initObj.top_left_y
      }
      else {
        this.top_left_y = 0.0;
      }
      if (initObj.hasOwnProperty('width')) {
        this.width = initObj.width
      }
      else {
        this.width = 0.0;
      }
      if (initObj.hasOwnProperty('height')) {
        this.height = initObj.height
      }
      else {
        this.height = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type bBox
    // Serialize message field [top_left_x]
    bufferOffset = _serializer.float64(obj.top_left_x, buffer, bufferOffset);
    // Serialize message field [top_left_y]
    bufferOffset = _serializer.float64(obj.top_left_y, buffer, bufferOffset);
    // Serialize message field [width]
    bufferOffset = _serializer.float64(obj.width, buffer, bufferOffset);
    // Serialize message field [height]
    bufferOffset = _serializer.float64(obj.height, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type bBox
    let len;
    let data = new bBox(null);
    // Deserialize message field [top_left_x]
    data.top_left_x = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [top_left_y]
    data.top_left_y = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [width]
    data.width = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [height]
    data.height = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 32;
  }

  static datatype() {
    // Returns string type for a message object
    return 'control_package/bBox';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '6fed9585f6e4fe60118eae6528781f7c';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64 top_left_x
    float64 top_left_y
    float64 width
    float64 height
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new bBox(null);
    if (msg.top_left_x !== undefined) {
      resolved.top_left_x = msg.top_left_x;
    }
    else {
      resolved.top_left_x = 0.0
    }

    if (msg.top_left_y !== undefined) {
      resolved.top_left_y = msg.top_left_y;
    }
    else {
      resolved.top_left_y = 0.0
    }

    if (msg.width !== undefined) {
      resolved.width = msg.width;
    }
    else {
      resolved.width = 0.0
    }

    if (msg.height !== undefined) {
      resolved.height = msg.height;
    }
    else {
      resolved.height = 0.0
    }

    return resolved;
    }
};

module.exports = bBox;
