# import the main window object (mw) from aqt
import aqt
import aqt.editor
import aqt.gui_hooks
import anki.hooks
from PyQt5.QtWidgets import QApplication
from typing import List, Tuple
import sys


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

    # shortcuts to focus on particular fields
    focus_field_shortcuts = config['focus_field_shortcuts']
    for shortcut in focus_field_shortcuts:
        shortcut_combination = shortcut['shortcut']
        note_type = shortcut['note_type']
        field_name = shortcut['field']
        shortcut_entry = (shortcut_combination, lambda: editor_focus_field(editor, note_type, field_name), True)
        shortcuts.append(shortcut_entry)

aqt.gui_hooks.editor_did_init_shortcuts.append(editor_init_shortcuts)