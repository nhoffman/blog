(load-file "bin/common.el")

(require-option "post" args)
(require-option "html-body" args)

;; save the current directory; find-file seems to change it
(setq cwd default-directory)

;; copy file containing the post to a tempfile
(setq body-temp (make-temp-name "temp-body-"))
(copy-file (gethash "post" args) body-temp t)
(find-file body-temp)
(org-mode)

;; read some metadata from the post
(setq titlestring (org-entry-get nil "title" 1))
(setq datestring (org-entry-get nil "date" 1))
(setq tagstring (org-entry-get nil "tags" 1))

;; compile and save body only
(setq org-export-with-toc nil)
(org-export-as-html 3 ;; levels of TOC 
		    nil ;; EXT-PLIST 
		    "string" ;; TO-BUFFER 
		    t ;; BODY-ONLY
		    )

(write-file (gethash "html-body" args))
(setq default-directory cwd)

(delete-file body-temp)

