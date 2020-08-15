# import the main window object (mw) from aqt
import aqt
import aqt.editor
import aqt.gui_hooks
import anki.hooks
from PyQt5.QtWidgets import QApplication
from typing import List, Tuple
import sys

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

def hello_world():
    sys.stderr.write("hello world")

def editor_focus_notelist(editor: aqt.editor.Editor):
    #pass
    model = editor.note.model()
    sys.stderr.write(str(model))

def editor_focus_field(editor: aqt.editor.Editor, note_type, field_name):
    #sys.stderr.write("editor_focus_field")
    note_type_name = editor.note.model()['name']
    if note_type_name == note_type:
        field_index = 0
        for field in editor.note.model()['flds']:
            if field['name'] == field_name:
                break
            field_index += 1
        editor.web.setFocus()
        editor.web.eval("focusField(%d);" % int(field_index))

def editor_init_shortcuts(shortcuts: List[Tuple], editor: aqt.editor.Editor):
    config = aqt.mw.addonManager.getConfig(__name__)

    # shortcut to focus on the note list
    focus_note_list_shortcut = config['focus_note_list_shortcut']
    shortcut_entry = (focus_note_list_shortcut, lambda: editor_focus_notelist(editor), True)
    shortcuts.append(shortcut_entry)

    # shortcuts to focus on particular fields
    focus_field_shortcuts = config['focus_field_shortcuts']
    for shortcut in focus_field_shortcuts:
        shortcut_combination = shortcut['shortcut']
        note_type = shortcut['note_type']
        field_name = shortcut['field']
        shortcut_entry = (shortcut_combination, lambda: editor_focus_field(editor, note_type, field_name), True)
        shortcuts.append(shortcut_entry)

aqt.gui_hooks.editor_did_init_shortcuts.append(editor_init_shortcuts)