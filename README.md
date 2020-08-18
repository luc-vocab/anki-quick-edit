# Anki Quick Field Focus
Quickly focus on a particular field in the card browser. When trying to populate a particular field for many notes at once, it's helpful to have a shortcut which jumps direcly to a particular field from within the browser.

## Installation
to be completed

## Configuration

You do need to configure the addon to tell it which field in your for a given note type needs to be focused. After installing the addon, select it in the Anki addon manager, then click **Config**

For each shortcut that you need, add an entry which contains the note type, the keyboard shortcut, and the name of the field to focus on

`
{
    "focus_field_shortcuts" : [
        {
            "note_type": "Chinese-Words",
            "shortcut": "Ctrl+T",
            "field": "Example"
        }
    ]
}
`

