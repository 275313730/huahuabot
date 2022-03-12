from src.plugins.tree_hole.crud import crud


def trans_note_to_str(note: dict) -> str:
    """将小纸条dict转化为字符串"""

    nickname = crud.user.get_nickname(note[1])
    return str(f"来自'{nickname}'的小纸条(编号:{note[0]})："
               f"\n{note[2]}")


def trans_notes_to_str(notes: list) -> str:
    """将小纸条list转化为字符串"""

    notes_str = ""
    num = len(notes)
    for i in range(num):
        if i < num - 1:
            notes_str += f"{trans_note_to_str(notes[i])}\n\n"
        else:
            notes_str += f"{trans_note_to_str(notes[i])}"
    return notes_str

