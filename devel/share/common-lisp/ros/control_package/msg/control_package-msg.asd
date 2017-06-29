
(cl:in-package :asdf)

(defsystem "control_package-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "bBox" :depends-on ("_package_bBox"))
    (:file "_package_bBox" :depends-on ("_package"))
    (:file "target_coods" :depends-on ("_package_target_coods"))
    (:file "_package_target_coods" :depends-on ("_package"))
  ))