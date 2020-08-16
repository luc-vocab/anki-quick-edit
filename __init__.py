# import the main window object (mw) from aqt
import aqt
import aqt.editor
import aqt.gui_hooks
import anki.hooks
from PyQt5.QtWidgets import QApplication
from typing import List, Tuple
import sys

current_status = {
    'modified': False,
    'monitor_field_changes': False,
    'tag_after_edit': None
}

def editor_switch_focus_field(editor: aqt.editor.Editor, note_type, field_name):
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
        shortcut_entry = (shortcut_combination, lambda: editor_switch_focus_field(editor, note_type, field_name), True)
        shortcuts.append(shortcut_entry)

def editor_focus_field(note: anki.notes.Note, current_field_idx: int):
    # by default, don't monitor
    current_status['monitor_field_changes'] = False
    current_status['modified'] = False
    current_status['tag_after_edit'] = None
    # gather information about the field which was focused
    current_note_type_name = note.model()['name']
    current_field_name = note.model()['flds'][current_field_idx]['name']

    # do we have quick focus access to this field in the config ?
    config = aqt.mw.addonManager.getConfig(__name__)
    focus_field_shortcuts = config['focus_field_shortcuts']
    for shortcut in focus_field_shortcuts:
        note_type = shortcut['note_type']
        field_name = shortcut['field']
        if current_note_type_name == note_type and current_field_name == field_name:
            # we do want to monitor this field for changes
            current_status['monitor_field_changes'] = True
            if 'tag_after_edit' in shortcut:
                current_status['tag_after_edit'] = shortcut['tag_after_edit']
            #sys.stderr.write("monitoring field changes")
            break
    

def editor_unfocus_field(changed: bool, note: anki.notes.Note, current_field_idx: int):
    if current_status['monitor_field_changes']:
        if current_status['modified']:
            #sys.sdterr.write(f"field was modified")
            # do we need to tag ?
            if current_status['tag_after_edit'] != None:
                tag_name = current_status['tag_after_edit']
                note.tags.append(tag_name)
                #sys.stderr.write(f"added tag {tag_name}")
                note.flush()
                #return True
    return False

def editor_typing_timer(note: anki.notes.Note):
    #sys.stderr.write(str(current_status))
    if current_status['monitor_field_changes']:
        current_status['modified'] = True
        #sys.stderr.write("typing detected")


# add shortcuts to quickly focus on a particular field
aqt.gui_hooks.editor_did_init_shortcuts.append(editor_init_shortcuts)
# monitor for field focus / typing
aqt.gui_hooks.editor_did_focus_field.append(editor_focus_field)
aqt.gui_hooks.editor_did_unfocus_field.append(editor_unfocus_field)
aqt.gui_hooks.editor_did_fire_typing_timer.append(editor_typing_timer)