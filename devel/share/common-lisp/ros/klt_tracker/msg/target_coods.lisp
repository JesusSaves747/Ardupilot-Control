; Auto-generated. Do not edit!


(cl:in-package klt_tracker-msg)


;//! \htmlinclude target_coods.msg.html

(cl:defclass <target_coods> (roslisp-msg-protocol:ros-message)
  ((xTar
    :reader xTar
    :initarg :xTar
    :type cl:float
    :initform 0.0)
   (yTar
    :reader yTar
    :initarg :yTar
    :type cl:float
    :initform 0.0))
)

(cl:defclass target_coods (<target_coods>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <target_coods>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'target_coods)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name klt_tracker-msg:<target_coods> is deprecated: use klt_tracker-msg:target_coods instead.")))

(cl:ensure-generic-function 'xTar-val :lambda-list '(m))
(cl:defmethod xTar-val ((m <target_coods>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader klt_tracker-msg:xTar-val is deprecated.  Use klt_tracker-msg:xTar instead.")
  (xTar m))

(cl:ensure-generic-function 'yTar-val :lambda-list '(m))
(cl:defmethod yTar-val ((m <target_coods>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader klt_tracker-msg:yTar-val is deprecated.  Use klt_tracker-msg:yTar instead.")
  (yTar m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <target_coods>) ostream)
  "Serializes a message object of type '<target_coods>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'xTar))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'yTar))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <target_coods>) istream)
  "Deserializes a message object of type '<target_coods>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'xTar) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'yTar) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<target_coods>)))
  "Returns string type for a message object of type '<target_coods>"
  "klt_tracker/target_coods")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'target_coods)))
  "Returns string type for a message object of type 'target_coods"
  "klt_tracker/target_coods")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<target_coods>)))
  "Returns md5sum for a message object of type '<target_coods>"
  "3f304876c8960b3c74eda82366a1bf42")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'target_coods)))
  "Returns md5sum for a message object of type 'target_coods"
  "3f304876c8960b3c74eda82366a1bf42")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<target_coods>)))
  "Returns full string definition for message of type '<target_coods>"
  (cl:format cl:nil "float64 xTar~%float64 yTar~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'target_coods)))
  "Returns full string definition for message of type 'target_coods"
  (cl:format cl:nil "float64 xTar~%float64 yTar~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <target_coods>))
  (cl:+ 0
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <target_coods>))
  "Converts a ROS message object to a list"
  (cl:list 'target_coods
    (cl:cons ':xTar (xTar msg))
    (cl:cons ':yTar (yTar msg))
))
