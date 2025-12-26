from __future__ import annotations

from PySide6 import QtWidgets, QtCore
from storage import db
from storage import utils as storage_utils
from pathlib import Path
import os
from ai.client import AIClient
import threading


class SettingsDialog(QtWidgets.QDialog):
    test_result = QtCore.Signal(object)
    """Settings dialog scaffold with Connection and Rewrite Modes tabs.

    This is a lightweight scaffold. UI wiring to storage and runtime APIs
    will be implemented in subsequent tasks.
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(700, 500)

        layout = QtWidgets.QVBoxLayout(self)
        tabs = QtWidgets.QTabWidget()
        layout.addWidget(tabs)

        # Connection tab
        conn_widget = QtWidgets.QWidget()
        conn_layout = QtWidgets.QFormLayout(conn_widget)

        self.endpoint_input = QtWidgets.QLineEdit()
        self.deployment_input = QtWidgets.QLineEdit()
        self.api_version_input = QtWidgets.QLineEdit()
        self.timeout_input = QtWidgets.QSpinBox()
        self.timeout_input.setRange(1, 120)
        self.timeout_input.setValue(6)

        self.api_key_input = QtWidgets.QLineEdit()
        self.api_key_input.setEchoMode(QtWidgets.QLineEdit.Password)

        conn_layout.addRow("Endpoint:", self.endpoint_input)
        conn_layout.addRow("Deployment ID:", self.deployment_input)
        conn_layout.addRow("API Version:", self.api_version_input)
        conn_layout.addRow("Timeout (s):", self.timeout_input)
        conn_layout.addRow("API Key:", self.api_key_input)

        test_btn = QtWidgets.QPushButton("Test Connection")
        conn_layout.addRow(test_btn)

        tabs.addTab(conn_widget, "Connection")

        # Rewrite Modes tab (scaffold)
        modes_widget = QtWidgets.QWidget()
        modes_layout = QtWidgets.QVBoxLayout(modes_widget)

        # Reorderable list widget that persists order after internal moves
        class ReorderableList(QtWidgets.QListWidget):
            def __init__(self, parent=None, on_reorder=None):
                super().__init__(parent)
                self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
                self.setDragEnabled(True)
                self.setAcceptDrops(True)
                self.setDropIndicatorShown(True)
                self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
                self.on_reorder = on_reorder

            def dropEvent(self, event):
                super().dropEvent(event)
                # after the internal move, persist the new order
                if callable(self.on_reorder):
                    try:
                        self.on_reorder()
                    except Exception:
                        pass

        self.modes_list = ReorderableList(self, on_reorder=lambda: self._persist_modes_order())
        modes_layout.addWidget(self.modes_list)

        btn_row = QtWidgets.QHBoxLayout()
        self.add_btn = QtWidgets.QPushButton("Add New")
        self.dup_btn = QtWidgets.QPushButton("Duplicate")
        self.del_btn = QtWidgets.QPushButton("Delete")
        self.edit_btn = QtWidgets.QPushButton("Edit")
        self.up_btn = QtWidgets.QPushButton("Move Up")
        self.down_btn = QtWidgets.QPushButton("Move Down")
        btn_row.addWidget(self.add_btn)
        btn_row.addWidget(self.dup_btn)
        btn_row.addWidget(self.edit_btn)
        btn_row.addWidget(self.del_btn)
        btn_row.addWidget(self.up_btn)
        btn_row.addWidget(self.down_btn)
        btn_row.addStretch()
        modes_layout.addLayout(btn_row)

        tabs.addTab(modes_widget, "Rewrite Modes")

        # Dialog buttons
        dlg_buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel
        )
        dlg_buttons.accepted.connect(self.accept)
        dlg_buttons.rejected.connect(self.reject)
        layout.addWidget(dlg_buttons)

        # Connect signals for wiring
        test_btn.clicked.connect(self._on_test_clicked)
        dlg_buttons.accepted.disconnect()
        dlg_buttons.accepted.connect(self._on_save)

        # Load current persisted connection settings if present
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM connection_settings WHERE id=1")
            row = cur.fetchone()
            if row:
                self.endpoint_input.setText(row['endpoint'] or "")
                self.deployment_input.setText(row['deployment_id'] or "")
                if row['api_version']:
                    self.api_version_input.setText(row['api_version'])
                if row['timeout']:
                    try:
                        self.timeout_input.setValue(int(row['timeout']))
                    except Exception:
                        pass
        except Exception:
            # ignore DB load errors for now
            pass

        # AI client for test connection
        self._ai_client = AIClient()

        # Load rewrite modes into list
        self._load_modes()

        # Wire mode buttons
        self.add_btn.clicked.connect(self._on_add_mode)
        self.dup_btn.clicked.connect(self._on_duplicate_mode)
        self.del_btn.clicked.connect(self._on_delete_mode)
        self.edit_btn.clicked.connect(self._on_edit_mode)
        self.up_btn.clicked.connect(self._on_move_up)
        self.down_btn.clicked.connect(self._on_move_down)
        self.modes_list.itemDoubleClicked.connect(self._on_item_double_clicked)
        # enable/disable mode buttons depending on selection
        self.modes_list.currentItemChanged.connect(self._on_mode_selection_changed)
        self._on_mode_selection_changed()

        # Context menu for modes list
        self.modes_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.modes_list.customContextMenuRequested.connect(self._on_modes_context_menu)

        # Test connection result signal
        self.test_result.connect(self._on_test_result)

    def _on_test_clicked(self) -> None:
        # Run test_connection in background thread and emit result via signal
        self._set_status("Testing connection...")

        def worker():
            try:
                res = self._ai_client.test_connection()
            except Exception as e:
                res = {"ok": False, "status": "other", "details": str(e)}
            self.test_result.emit(res)

        threading.Thread(target=worker, daemon=True).start()

    def _on_test_result(self, res: dict) -> None:
        ok = res.get("ok", False)
        status = res.get("status", "other")
        details = res.get("details", "")
        if ok:
            self._set_status("Connection OK")
            QtWidgets.QMessageBox.information(self, "Test Connection", f"OK — {details}")
        else:
            self._set_status(f"Connection: {status}")
            QtWidgets.QMessageBox.warning(self, "Test Connection", f"Status: {status}\nDetails: {details}")

    def _set_status(self, text: str) -> None:
        # lightweight status feedback in window title temporarily
        self.setWindowTitle(f"Settings — {text}")
        QtCore.QTimer.singleShot(3000, lambda: self.setWindowTitle("Settings"))

    def _on_save(self) -> None:
        # Persist connection settings and optionally store API key securely
        endpoint = self.endpoint_input.text().strip()
        deployment = self.deployment_input.text().strip()
        api_version = self.api_version_input.text().strip() or None
        timeout = int(self.timeout_input.value())
        api_key = self.api_key_input.text().strip()

        if not endpoint or not deployment:
            QtWidgets.QMessageBox.warning(self, "Save Settings", "Endpoint and Deployment ID are required.")
            return

        # Save non-secret settings to DB
        try:
            conn = db.get_connection()
            cs = db.ConnectionSettings(endpoint=endpoint, deployment_id=deployment, api_version=api_version, timeout=timeout)
            db.save_connection_settings(conn, cs)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Save Settings", f"Failed to save settings: {e}")
            return

        # Handle API key storage
        if api_key:
            if storage_utils.keyring_available():
                storage_utils.store_api_key("ai_notepad", "default", api_key)
                QtWidgets.QMessageBox.information(self, "Save Settings", "API key stored in OS keyring.")
            else:
                # Ask for user consent to store locally encrypted
                resp = QtWidgets.QMessageBox.question(
                    self,
                    "Store API Key",
                    "OS keyring not available. Store API key locally encrypted? This will store an encrypted file on disk.",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                )
                if resp == QtWidgets.QMessageBox.Yes:
                    # Prompt for passphrase
                    pwd, ok = QtWidgets.QInputDialog.getText(self, "Passphrase", "Enter a passphrase to protect the API key:", QtWidgets.QLineEdit.Password)
                    if ok and pwd:
                        fallback_dir = Path.home().joinpath('.local', 'share', 'ai_notepad')
                        fallback_dir.mkdir(parents=True, exist_ok=True)
                        fallback_path = fallback_dir.joinpath('api_key.json')
                        try:
                            storage_utils.store_api_key("ai_notepad", "default", api_key, fallback_path, passphrase=pwd)
                            QtWidgets.QMessageBox.information(self, "Save Settings", f"API key stored encrypted at {fallback_path}")
                        except Exception as e:
                            QtWidgets.QMessageBox.critical(self, "Save Settings", f"Failed to store API key: {e}")
                    else:
                        QtWidgets.QMessageBox.information(self, "Save Settings", "Passphrase not provided; API key not stored.")

        self.accept()

    def _load_modes(self) -> None:
        try:
            conn = db.get_connection()
            modes = db.list_rewrite_modes(conn)
            self.modes_list.clear()
            for m in modes:
                item = QtWidgets.QListWidgetItem(f"{m.order}. {m.name}")
                item.setData(QtCore.Qt.UserRole, m)
                self.modes_list.addItem(item)
        except Exception:
            pass

    def _on_item_double_clicked(self, item: QtWidgets.QListWidgetItem) -> None:
        # ensure selection and launch editor
        self.modes_list.setCurrentItem(item)
        self._on_edit_mode()

    def _persist_modes_order(self) -> None:
        try:
            conn = db.get_connection()
            # iterate items and assign order sequentially
            for idx in range(self.modes_list.count()):
                it = self.modes_list.item(idx)
                m = it.data(QtCore.Qt.UserRole)
                if m:
                    m.order = idx + 1
                    db.save_rewrite_mode(conn, m)
        except Exception:
            pass
    def _on_add_mode(self) -> None:
        dlg = ModeEditor(self)
        if dlg.exec() == QtWidgets.QDialog.Accepted:
            mode = dlg.get_mode()
            try:
                conn = db.get_connection()
                # set order to end
                existing = db.list_rewrite_modes(conn)
                mode.order = (max([m.order for m in existing]) + 1) if existing else 1
                db.save_rewrite_mode(conn, mode)
                self._load_modes()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Rewrite Modes", f"Failed to add mode: {e}")

    def _get_selected_mode(self):
        it = self.modes_list.currentItem()
        if not it:
            return None
        return it.data(QtCore.Qt.UserRole)

    def _on_mode_selection_changed(self, *args) -> None:
        sel = self._get_selected_mode()
        enabled = sel is not None
        self.edit_btn.setEnabled(enabled and not (sel and sel.builtin))
        self.del_btn.setEnabled(enabled and not (sel and sel.builtin))
        self.dup_btn.setEnabled(enabled)
        self.up_btn.setEnabled(enabled)
        self.down_btn.setEnabled(enabled)

    def _on_modes_context_menu(self, pos) -> None:
        item = self.modes_list.itemAt(pos)
        if not item:
            return
        self.modes_list.setCurrentItem(item)
        menu = QtWidgets.QMenu(self)
        edit_act = menu.addAction("Edit")
        dup_act = menu.addAction("Duplicate")
        del_act = menu.addAction("Delete")
        menu.addSeparator()
        up_act = menu.addAction("Move Up")
        down_act = menu.addAction("Move Down")
        act = menu.exec(self.modes_list.mapToGlobal(pos))
        if act == edit_act:
            self._on_edit_mode()
        elif act == dup_act:
            self._on_duplicate_mode()
        elif act == del_act:
            self._on_delete_mode()
        elif act == up_act:
            self._on_move_up()
        elif act == down_act:
            self._on_move_down()

    def _on_duplicate_mode(self) -> None:
        sel = self._get_selected_mode()
        if not sel:
            return
        new = db.RewriteMode(id=None, name=sel.name + " (copy)", instruction_template=sel.instruction_template, enabled=sel.enabled, order=sel.order + 1, applies_to=sel.applies_to, builtin=False, advanced_settings=sel.advanced_settings)
        try:
            conn = db.get_connection()
            db.save_rewrite_mode(conn, new)
            self._load_modes()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Rewrite Modes", f"Failed to duplicate mode: {e}")

    def _on_edit_mode(self) -> None:
        sel = self._get_selected_mode()
        if not sel:
            return
        if sel.builtin:
            QtWidgets.QMessageBox.information(self, "Rewrite Modes", "Built-in modes cannot be edited.")
            return
        dlg = ModeEditor(self, mode=sel)
        if dlg.exec() == QtWidgets.QDialog.Accepted:
            updated = dlg.get_mode()
            try:
                conn = db.get_connection()
                db.save_rewrite_mode(conn, updated)
                self._load_modes()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Rewrite Modes", f"Failed to save mode: {e}")

    def _on_delete_mode(self) -> None:
        sel = self._get_selected_mode()
        if not sel:
            return
        if sel.builtin:
            QtWidgets.QMessageBox.information(self, "Rewrite Modes", "Built-in modes cannot be deleted.")
            return
        resp = QtWidgets.QMessageBox.question(self, "Delete Mode", f"Delete mode '{sel.name}'?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if resp != QtWidgets.QMessageBox.Yes:
            return
        try:
            conn = db.get_connection()
            db.delete_rewrite_mode(conn, sel.id)
            self._load_modes()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Rewrite Modes", f"Failed to delete mode: {e}")

    def _on_move_up(self) -> None:
        sel = self._get_selected_mode()
        if not sel:
            return
        try:
            conn = db.get_connection()
            modes = db.list_rewrite_modes(conn)
            idx = next((i for i, m in enumerate(modes) if m.id == sel.id), None)
            if idx is None or idx == 0:
                return
            # swap orders
            modes[idx].order, modes[idx-1].order = modes[idx-1].order, modes[idx].order
            for m in modes:
                db.save_rewrite_mode(conn, m)
            self._load_modes()
        except Exception:
            pass

    def _on_move_down(self) -> None:
        sel = self._get_selected_mode()
        if not sel:
            return
        try:
            conn = db.get_connection()
            modes = db.list_rewrite_modes(conn)
            idx = next((i for i, m in enumerate(modes) if m.id == sel.id), None)
            if idx is None or idx >= len(modes)-1:
                return
            modes[idx].order, modes[idx+1].order = modes[idx+1].order, modes[idx].order
            for m in modes:
                db.save_rewrite_mode(conn, m)
            self._load_modes()
        except Exception:
            pass


class ModeEditor(QtWidgets.QDialog):
    def __init__(self, parent=None, mode: db.RewriteMode | None = None):
        super().__init__(parent)
        self.setWindowTitle("Edit Rewrite Mode" if mode else "Add Rewrite Mode")
        self.resize(500, 300)
        self._mode = mode

        layout = QtWidgets.QFormLayout(self)
        self.name_in = QtWidgets.QLineEdit()
        self.template_in = QtWidgets.QPlainTextEdit()
        self.enabled_cb = QtWidgets.QCheckBox()
        self.applies_combo = QtWidgets.QComboBox()
        self.applies_combo.addItems(["selection-only", "whole-note-default"])

        layout.addRow("Name:", self.name_in)
        layout.addRow("Instruction Template:", self.template_in)
        # Advanced settings collapsed by default
        self.adv_toggle = QtWidgets.QCheckBox("Show Advanced Settings")
        self.adv_toggle.setChecked(False)
        layout.addRow(self.adv_toggle)

        self.adv_widget = QtWidgets.QWidget()
        adv_layout = QtWidgets.QFormLayout(self.adv_widget)
        self.adv_field = QtWidgets.QLineEdit()
        adv_layout.addRow("Advanced Option:", self.adv_field)
        self.adv_widget.setVisible(False)
        layout.addRow(self.adv_widget)

        def _on_toggle_changed(checked):
            self.adv_widget.setVisible(self.adv_toggle.isChecked())

        self.adv_toggle.stateChanged.connect(_on_toggle_changed)
        layout.addRow("Enabled:", self.enabled_cb)
        layout.addRow("Applies To:", self.applies_combo)

        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addRow(btns)

        if mode:
            self.name_in.setText(mode.name)
            self.template_in.setPlainText(mode.instruction_template)
            self.enabled_cb.setChecked(bool(mode.enabled))
            idx = 0 if mode.applies_to == 'selection-only' else 1
            self.applies_combo.setCurrentIndex(idx)

    def get_mode(self) -> db.RewriteMode:
        name = self.name_in.text().strip()
        template = self.template_in.toPlainText().strip()
        enabled = bool(self.enabled_cb.isChecked())
        applies = self.applies_combo.currentText()
        if self._mode:
            adv = self._mode.advanced_settings or {}
            if self.adv_toggle.isChecked():
                adv['advanced_option'] = self.adv_field.text().strip()
            return db.RewriteMode(id=self._mode.id, name=name, instruction_template=template, enabled=enabled, order=self._mode.order, applies_to=applies, builtin=self._mode.builtin, advanced_settings=adv)
        return db.RewriteMode(id=None, name=name, instruction_template=template, enabled=enabled, order=0, applies_to=applies, builtin=False, advanced_settings=None)
    
