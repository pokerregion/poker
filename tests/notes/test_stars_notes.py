from pathlib import Path
from datetime import datetime
from pytz import UTC
import pytest
from poker.room.pokerstars import Notes, _Note, _Label, NoteNotFoundError


@pytest.fixture
def notes():
    filedir = Path(__file__).parent
    return Notes.from_file(filedir / "notes.W2lkm2n.xml")


def test_from_str_no_problem():
    filedir = Path(__file__).parent
    notes_unicode = (filedir / "notes.W2lkm2n.xml").open().read()
    Notes(notes_unicode)


def test_players(notes):
    assert notes.players == (
        "regplayer",
        "sharkplayer",
        "fishplayer",
        '"htmlchar"',
        "$dollarsign",
        "nonoteforplayer",
        "-=strangename=-",
        "//ÄMGS",
        "0bullmarket0",
        "CarlGardner",
        "µ (x+t)",
    )


def test_find_note_text_for_player(notes):
    assert notes.get_note_text("regplayer") == "river big bet 99"


def test_find_note_for_player(notes):
    note = notes.get_note("regplayer")
    assert note.text == "river big bet 99"
    assert note.player == "regplayer"
    assert note.label == "FISH"
    assert note.update == datetime(2013, 12, 13, 17, 6, 35, tzinfo=UTC)


def test_find_not_existing_note(notes):
    with pytest.raises(NoteNotFoundError):
        assert notes.get_note("Nosuchnote")


def test_all_notes(notes):
    assert notes.notes == (
        _Note(
            player="regplayer",
            label="FISH",
            text="river big bet 99",
            update=datetime(2013, 12, 13, 17, 6, 35, tzinfo=UTC),
        ),
        _Note(
            player="sharkplayer",
            label="SHARK",
            text="plays GTO",
            update=datetime(2014, 9, 14, 19, 20, 49, tzinfo=UTC),
        ),
        _Note(
            player="fishplayer",
            label="REG",
            text="4-way check-miniraise draw",
            update=datetime(2013, 12, 13, 17, 23, 6, tzinfo=UTC),
        ),
        _Note(
            player='"htmlchar"',
            label="GENERAL",
            text="UTG limp AA",
            update=datetime(2013, 8, 14, 15, 14, 49, tzinfo=UTC),
        ),
        _Note(
            player="$dollarsign",
            label="REG",
            text="not very good",
            update=datetime(2013, 2, 7, 18, 35, 39, tzinfo=UTC),
        ),
        _Note(
            player="nonoteforplayer",
            label=None,
            text="not note",
            update=datetime(2013, 2, 7, 18, 35, 39, tzinfo=UTC),
        ),
        _Note(
            player="-=strangename=-",
            label=None,
            text="DONK-CALL TP",
            update=datetime(2010, 9, 15, 15, 56, 20, tzinfo=UTC),
        ),
        _Note(
            player="//ÄMGS",
            label=None,
            text="unicode chars in name",
            update=datetime(2011, 6, 26, 13, 14, 58, tzinfo=UTC),
        ),
        _Note(
            player="0bullmarket0",
            label=None,
            text="multiple\nlines\nin the\nnote",
            update=datetime(2010, 3, 23, 2, 36, 50, tzinfo=UTC),
        ),
        _Note(
            player="CarlGardner",
            label=None,
            text="contains invalid character: 3B 57s ",
            update=datetime(2010, 8, 15, 10, 59, 15, tzinfo=UTC),
        ),
        _Note(
            player="µ (x+t)",
            label=None,
            text="µ (x+t): strange chars everywhere",
            update=datetime(2010, 3, 24, 5, 34, 14, tzinfo=UTC),
        ),
    )


def test_add_note(notes):
    notes.add_note("Walkman", "is a big fish", label="FISH")

    assert "Walkman" in notes.players
    note = notes.get_note("Walkman")
    assert isinstance(note, _Note)
    assert note.player == "Walkman"
    assert note.label == "FISH"
    assert isinstance(note.update, datetime)
    assert note.text == "is a big fish"


def test_append_note(notes):
    notes.append_note("regplayer", "\n3bet 87s preflop")
    assert notes.get_note_text("regplayer") == "river big bet 99\n3bet 87s preflop"


def test_prepend_and_append_note(notes):
    notes.prepend_note("regplayer", "flop and ")
    notes.append_note("regplayer", ",66")
    assert notes.get_note_text("regplayer") == "flop and river big bet 99,66"


def test_replace_note_text(notes):
    notes.replace_note("regplayer", "he is actually a fish not a reg")
    assert notes.get_note_text("regplayer") == "he is actually a fish not a reg"


def test_change_note_label(notes):
    assert notes.get_note("nonoteforplayer").label is None
    notes.change_note_label("nonoteforplayer", "FISH")
    assert notes.get_note("nonoteforplayer").label == "FISH"


def test_delete_note(notes):
    assert "$dollarsign" in notes.players
    notes.del_note("$dollarsign")
    assert "$dollarsign" not in notes.players


def test_find_player_with_html_quotes(notes):
    assert notes.get_note('"htmlchar"') == _Note(
        player='"htmlchar"',
        label="GENERAL",
        update=datetime(2013, 8, 14, 15, 14, 49, tzinfo=UTC),
        text="UTG limp AA",
    )

    with pytest.raises(NoteNotFoundError):
        assert notes.get_note("&quot;htmlchar&quot;")


def test_label_names(notes):
    assert notes.label_names == ("FISH", "SHARK", "REG", "GENERAL")


def test_all_labels(notes):
    assert notes.labels == (
        _Label(id="0", color="30DBFF", name="FISH"),
        _Label(id="1", color="30FF97", name="SHARK"),
        _Label(id="2", color="E1FF80", name="REG"),
        _Label(id="3", color="E1FF80", name="GENERAL"),
    )


def test_add_label(notes):
    notes.add_label("YETI", "FF0000")
    assert notes.labels == (
        _Label(id="0", color="30DBFF", name="FISH"),
        _Label(id="1", color="30FF97", name="SHARK"),
        _Label(id="2", color="E1FF80", name="REG"),
        _Label(id="3", color="E1FF80", name="GENERAL"),
        _Label(id="4", color="FF0000", name="YETI"),
    )


def test_delete_label(notes):
    notes.del_label("REG")
    assert notes.labels == (
        _Label(id="0", color="30DBFF", name="FISH"),
        _Label(id="1", color="30FF97", name="SHARK"),
        _Label(id="3", color="E1FF80", name="GENERAL"),
    )
