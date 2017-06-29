;; Auto-generated. Do not edit!


(when (boundp 'klt_tracker::target_coods)
  (if (not (find-package "KLT_TRACKER"))
    (make-package "KLT_TRACKER"))
  (shadow 'target_coods (find-package "KLT_TRACKER")))
(unless (find-package "KLT_TRACKER::TARGET_COODS")
  (make-package "KLT_TRACKER::TARGET_COODS"))

(in-package "ROS")
;;//! \htmlinclude target_coods.msg.html


(defclass klt_tracker::target_coods
  :super ros::object
  :slots (_xTar _yTar ))

(defmethod klt_tracker::target_coods
  (:init
   (&key
    ((:xTar __xTar) 0.0)
    ((:yTar __yTar) 0.0)
    )
   (send-super :init)
   (setq _xTar (float __xTar))
   (setq _yTar (float __yTar))
   self)
  (:xTar
   (&optional __xTar)
   (if __xTar (setq _xTar __xTar)) _xTar)
  (:yTar
   (&optional __yTar)
   (if __yTar (setq _yTar __yTar)) _yTar)
  (:serialization-length
   ()
   (+
    ;; float64 _xTar
    8
    ;; float64 _yTar
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _xTar
       (sys::poke _xTar (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _yTar
       (sys::poke _yTar (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _xTar
     (setq _xTar (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _yTar
     (setq _yTar (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get klt_tracker::target_coods :md5sum-) "3f304876c8960b3c74eda82366a1bf42")
(setf (get klt_tracker::target_coods :datatype-) "klt_tracker/target_coods")
(setf (get klt_tracker::target_coods :definition-)
      "float64 xTar
float64 yTar
")



(provide :klt_tracker/target_coods "3f304876c8960b3c74eda82366a1bf42")


