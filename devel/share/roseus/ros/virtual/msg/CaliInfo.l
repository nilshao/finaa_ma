;; Auto-generated. Do not edit!


(when (boundp 'virtual::CaliInfo)
  (if (not (find-package "VIRTUAL"))
    (make-package "VIRTUAL"))
  (shadow 'CaliInfo (find-package "VIRTUAL")))
(unless (find-package "VIRTUAL::CALIINFO")
  (make-package "VIRTUAL::CALIINFO"))

(in-package "ROS")
;;//! \htmlinclude CaliInfo.msg.html


(defclass virtual::CaliInfo
  :super ros::object
  :slots (_marker _markerincamera_measure _markerincamera_truth _eeinbase _baseincamera _markerinee ))

(defmethod virtual::CaliInfo
  (:init
   (&key
    ((:marker __marker) 0)
    ((:markerincamera_measure __markerincamera_measure) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:markerincamera_truth __markerincamera_truth) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:eeinbase __eeinbase) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:baseincamera __baseincamera) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:markerinee __markerinee) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _marker (round __marker))
   (setq _markerincamera_measure __markerincamera_measure)
   (setq _markerincamera_truth __markerincamera_truth)
   (setq _eeinbase __eeinbase)
   (setq _baseincamera __baseincamera)
   (setq _markerinee __markerinee)
   self)
  (:marker
   (&optional __marker)
   (if __marker (setq _marker __marker)) _marker)
  (:markerincamera_measure
   (&optional __markerincamera_measure)
   (if __markerincamera_measure (setq _markerincamera_measure __markerincamera_measure)) _markerincamera_measure)
  (:markerincamera_truth
   (&optional __markerincamera_truth)
   (if __markerincamera_truth (setq _markerincamera_truth __markerincamera_truth)) _markerincamera_truth)
  (:eeinbase
   (&optional __eeinbase)
   (if __eeinbase (setq _eeinbase __eeinbase)) _eeinbase)
  (:baseincamera
   (&optional __baseincamera)
   (if __baseincamera (setq _baseincamera __baseincamera)) _baseincamera)
  (:markerinee
   (&optional __markerinee)
   (if __markerinee (setq _markerinee __markerinee)) _markerinee)
  (:serialization-length
   ()
   (+
    ;; int64 _marker
    8
    ;; float64[] _markerincamera_measure
    (* 8    (length _markerincamera_measure)) 4
    ;; float64[] _markerincamera_truth
    (* 8    (length _markerincamera_truth)) 4
    ;; float64[] _eeinbase
    (* 8    (length _eeinbase)) 4
    ;; float64[] _baseincamera
    (* 8    (length _baseincamera)) 4
    ;; float64[] _markerinee
    (* 8    (length _markerinee)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int64 _marker
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _marker (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _marker) (= (length (_marker . bv)) 2)) ;; bignum
              (write-long (ash (elt (_marker . bv) 0) 0) s)
              (write-long (ash (elt (_marker . bv) 1) -1) s))
             ((and (class _marker) (= (length (_marker . bv)) 1)) ;; big1
              (write-long (elt (_marker . bv) 0) s)
              (write-long (if (>= _marker 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _marker s)(write-long (if (>= _marker 0) 0 #xffffffff) s)))
     ;; float64[] _markerincamera_measure
     (write-long (length _markerincamera_measure) s)
     (dotimes (i (length _markerincamera_measure))
       (sys::poke (elt _markerincamera_measure i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _markerincamera_truth
     (write-long (length _markerincamera_truth) s)
     (dotimes (i (length _markerincamera_truth))
       (sys::poke (elt _markerincamera_truth i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _eeinbase
     (write-long (length _eeinbase) s)
     (dotimes (i (length _eeinbase))
       (sys::poke (elt _eeinbase i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _baseincamera
     (write-long (length _baseincamera) s)
     (dotimes (i (length _baseincamera))
       (sys::poke (elt _baseincamera i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _markerinee
     (write-long (length _markerinee) s)
     (dotimes (i (length _markerinee))
       (sys::poke (elt _markerinee i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int64 _marker
#+(or :alpha :irix6 :x86_64)
      (setf _marker (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _marker (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; float64[] _markerincamera_measure
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _markerincamera_measure (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _markerincamera_measure i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _markerincamera_truth
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _markerincamera_truth (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _markerincamera_truth i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _eeinbase
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _eeinbase (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _eeinbase i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _baseincamera
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _baseincamera (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _baseincamera i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _markerinee
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _markerinee (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _markerinee i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(setf (get virtual::CaliInfo :md5sum-) "aa331633c72b6e8b9017db2e4147569d")
(setf (get virtual::CaliInfo :datatype-) "virtual/CaliInfo")
(setf (get virtual::CaliInfo :definition-)
      "int64 marker
float64[] markerincamera_measure
float64[] markerincamera_truth
float64[] eeinbase
float64[] baseincamera
float64[] markerinee

")



(provide :virtual/CaliInfo "aa331633c72b6e8b9017db2e4147569d")


