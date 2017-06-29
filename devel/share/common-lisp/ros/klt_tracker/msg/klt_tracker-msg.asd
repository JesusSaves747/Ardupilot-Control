
(cl:in-package :asdf)

(defsystem "klt_tracker-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "target_coods" :depends-on ("_package_target_coods"))
    (:file "_package_target_coods" :depends-on ("_package"))
  ))