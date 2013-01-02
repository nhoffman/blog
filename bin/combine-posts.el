(load-file "bin/common.el")

(require-option "org-src" args)
(require-option "html" args)

;; save the current directory; find-file seems to change it
(setq cwd default-directory)

;; copy file containing the post to a tempfile
(setq index-temp (make-temp-name "temp-index-"))
(copy-file (gethash "org-src" args) index-temp t)
(find-file index-temp)
(org-mode)

;; compile
;; (setq org-export-with-toc nil)
(org-export-as-html 1 ;; levels of TOC 
		    nil ;; EXT-PLIST 
		    "string" ;; TO-BUFFER 
		    )

(write-file (gethash "html" args))
(setq default-directory cwd)

(delete-file index-temp)

