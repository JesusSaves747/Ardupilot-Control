;; Auto-generated. Do not edit!


(when (boundp 'control_package::bBox)
  (if (not (find-package "CONTROL_PACKAGE"))
    (make-package "CONTROL_PACKAGE"))
  (shadow 'bBox (find-package "CONTROL_PACKAGE")))
(unless (find-package "CONTROL_PACKAGE::BBOX")
  (make-package "CONTROL_PACKAGE::BBOX"))

(in-package "ROS")
;;//! \htmlinclude bBox.msg.html


(defclass control_package::bBox
  :super ros::object
  :slots (_top_left_x _top_left_y _width _height ))

(defmethod control_package::bBox
  (:init
   (&key
    ((:top_left_x __top_left_x) 0.0)
    ((:top_left_y __top_left_y) 0.0)
    ((:width __width) 0.0)
    ((:height __height) 0.0)
    )
   (send-super :init)
   (setq _top_left_x (float __top_left_x))
   (setq _top_left_y (float __top_left_y))
   (setq _width (float __width))
   (setq _height (float __height))
   self)
  (:top_left_x
   (&optional __top_left_x)
   (if __top_left_x (setq _top_left_x __top_left_x)) _top_left_x)
  (:top_left_y
   (&optional __top_left_y)
   (if __top_left_y (setq _top_left_y __top_left_y)) _top_left_y)
  (:width
   (&optional __width)
   (if __width (setq _width __width)) _width)
  (:height
   (&optional __height)
   (if __height (setq _height __height)) _height)
  (:serialization-length
   ()
   (+
    ;; float64 _top_left_x
    8
    ;; float64 _top_left_y
    8
    ;; float64 _width
    8
    ;; float64 _height
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _top_left_x
       (sys::poke _top_left_x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _top_left_y
       (sys::poke _top_left_y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _width
       (sys::poke _width (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _height
       (sys::poke _height (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _top_left_x
     (setq _top_left_x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _top_left_y
     (setq _top_left_y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _width
     (setq _width (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _height
     (setq _height (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get control_package::bBox :md5sum-) "6fed9585f6e4fe60118eae6528781f7c")
(setf (get control_package::bBox :datatype-) "control_package/bBox")
(setf (get control_package::bBox :definition-)
      "float64 top_left_x
float64 top_left_y
float64 width
float64 height

")



(provide :control_package/bBox "6fed9585f6e4fe60118eae6528781f7c")


