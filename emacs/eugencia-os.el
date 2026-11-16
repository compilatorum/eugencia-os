;;; eugencia-os.el --- Emacs Cockpit for Eugência OS & ValueCurator OS -*- lexical-binding: t; -*-
;;
;; Author: João Nitzsche (Compilatorum / ValueCurator)
;; Version: 1.0.0
;; Keywords: convenience, outlines, processes, tools
;; Description: Integração Híbrida Emacs/Org-mode <-> Eugência OS API & ProofGate

;;; Commentary:
;; Implementa o cockpit cognitivo Emacs/Org-mode descrito na Seção 8 e 11 de ~/eugencia.pdf:
;; - Captura rápida para o Flow Inbox sem interromper o estado de flow (`eugencia-capture-flow`)
;; - Sincronização bidirecional entre arquivos Org (`~/eugencia-os/org/*.org`) e o banco operacional
;; - Consulta de KPIs da Eugência (E = H + S + A + G, L, rho, MC, WIP <= 2) no minibuffer
;; - Abertura rápida dos arquivos Org do portfólio e do painel SCADA Web

;;; Code:

(require 'json)
(require 'url)
(require 'org)

(defgroup eugencia-os nil
  "Sistema Operacional de Carreira, Pesquisa e Ativos Digitais (Eugência OS)."
  :group 'applications
  :prefix "eugencia-")

(defcustom eugencia-os-root (expand-file-name "~/eugencia-os")
  "Diretório raiz do repositório Eugência OS."
  :type 'directory
  :group 'eugencia-os)

(defcustom eugencia-os-api-url "http://127.0.0.1:8765"
  "URL do servidor local FastAPI/HTTP do Eugência OS."
  :type 'string
  :group 'eugencia-os)

(defun eugencia-open-inbox ()
  "Abre o arquivo `inbox.org` (Flow Inbox: Divergência <-> Convergência)."
  (interactive)
  (find-file (expand-file-name "org/inbox.org" eugencia-os-root)))

(defun eugencia-open-portfolio ()
  "Abre o arquivo `portfolio.org` com os 72 repositórios e KPIs."
  (interactive)
  (find-file (expand-file-name "org/portfolio.org" eugencia-os-root)))

(defun eugencia-open-opportunities ()
  "Abre o arquivo `opportunities.org` (CRM de Oportunidades & Grant Stacking)."
  (interactive)
  (find-file (expand-file-name "org/opportunities.org" eugencia-os-root)))

(defun eugencia-open-experiments ()
  "Abre o arquivo `experiments.org` (Research & Experiment OS)."
  (interactive)
  (find-file (expand-file-name "org/experiments.org" eugencia-os-root)))

(defun eugencia-capture-flow (content)
  "Captura uma ideia, hipótese, oportunidade ou tarefa no Flow Inbox sem sair do flow."
  (interactive "s[Eugência Flow Inbox] Capturar ideia/oportunidade/tarefa: ")
  (let* ((cmd (format "python3 %s/scripts/eugencia_cli.py capture %s"
                      (shell-quote-argument eugencia-os-root)
                      (shell-quote-argument content)))
         (output (shell-command-to-string cmd)))
    (message "%s" (string-trim output))))

(defun eugencia-sync-org ()
  "Sincroniza bidirecionalmente os arquivos Org com o banco de dados do Eugência OS."
  (interactive)
  (let* ((cmd (format "python3 %s/scripts/eugencia_cli.py sync-org"
                      (shell-quote-argument eugencia-os-root)))
         (output (shell-command-to-string cmd)))
    (revert-buffer t t t)
    (message "[Eugência OS Sync] %s" (string-trim output))))

(defun eugencia-status-kpis ()
  "Exibe os KPIs em tempo real da Eugência no minibuffer."
  (interactive)
  (let* ((cmd (format "python3 %s/scripts/eugencia_cli.py kpis"
                      (shell-quote-argument eugencia-os-root)))
         (output (shell-command-to-string cmd)))
    (message "%s" (string-trim output))))

(defvar eugencia-os-mode-map
  (let ((map (make-sparse-keymap)))
    (define-key map (kbd "C-c e c") #'eugencia-capture-flow)
    (define-key map (kbd "C-c e s") #'eugencia-sync-org)
    (define-key map (kbd "C-c e k") #'eugencia-status-kpis)
    (define-key map (kbd "C-c e i") #'eugencia-open-inbox)
    (define-key map (kbd "C-c e p") #'eugencia-open-portfolio)
    (define-key map (kbd "C-c e o") #'eugencia-open-opportunities)
    (define-key map (kbd "C-c e x") #'eugencia-open-experiments)
    map)
  "Keymap para `eugencia-os-mode'.")

;;;###autoload
(define-minor-mode eugencia-os-mode
  "Modo menor para integração do Emacs/Org-mode com o Eugência OS."
  :lighter " 🧭Eugência"
  :keymap eugencia-os-mode-map
  :global t)

(provide 'eugencia-os)
;;; eugencia-os.el ends here
