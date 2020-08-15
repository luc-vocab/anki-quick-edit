# import the main window object (mw) from aqt
import aqt
import aqt.editor
import aqt.gui_hooks
from PyQt5.QtWidgets import QApplication
# import sys

# using this hook, copy the field we're interested in into the clipboard editor_did_load_note

def editor_loaded_note(editor: aqt.editor.Editor):
    # get addon configuration
    config = aqt.mw.addonManager.getConfig(__name__)
    # check the note type
    note_type_name = editor.note.model()['name']
    if note_type_name in config:
        field_name = config[note_type_name]
        field_data = editor.note[field_name]
        # copy to clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(field_data)


aqt.gui_hooks.editor_did_load_note.append(editor_loaded_note)
