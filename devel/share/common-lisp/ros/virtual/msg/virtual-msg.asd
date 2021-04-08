
(cl:in-package :asdf)

(defsystem "virtual-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "CaliInfo" :depends-on ("_package_CaliInfo"))
    (:file "_package_CaliInfo" :depends-on ("_package"))
  ))