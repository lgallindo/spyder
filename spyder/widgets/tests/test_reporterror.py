# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
#

"""Tests for report error dialog."""

# 3rd party imports
import pytest
from qtpy.QtCore import Qt

# Local imports
from spyder.widgets.reporterror import MIN_CHARS, SpyderErrorDialog


@pytest.fixture
def setup_dialog(qtbot):
    """Set up dialog."""
    widget = SpyderErrorDialog(None)
    qtbot.addWidget(widget)
    return widget


def test_dialog(qtbot):
    """Run dialog tests."""
    dlg = setup_dialog(qtbot)
    text = "1" * MIN_CHARS

    # Assert Submit button is disabled at first
    assert not dlg.submit_btn.isEnabled()

    # Introduce 15 chars to input_description
    qtbot.keyClicks(dlg.input_description, text)

    # Assert Submit button is now enabled
    assert dlg.submit_btn.isEnabled()

    # Assert cut leaves the header
    dlg.input_description.selectAll()
    dlg.input_description.cut()
    assert dlg.input_description.toPlainText() == dlg.input_description.header

    # Assert delete leaves the header
    qtbot.keyClicks(dlg.input_description, text)
    dlg.input_description.selectAll()
    qtbot.keyPress(dlg.input_description, Qt.Key_Delete)
    assert dlg.input_description.toPlainText() == dlg.input_description.header

    # Assert backspace works as expected
    qtbot.keyClicks(dlg.input_description, text)
    qtbot.keyPress(dlg.input_description, Qt.Key_Backspace)
    assert not dlg.submit_btn.isEnabled()

    dlg.input_description.selectAll()
    qtbot.keyPress(dlg.input_description, Qt.Key_Backspace)
    assert dlg.input_description.toPlainText() == dlg.input_description.header

    # Assert chars label works as expected
    assert dlg.chars_label.text() == '{} more characters to go...'.format(MIN_CHARS)
    qtbot.keyClicks(dlg.input_description, text)
    assert dlg.chars_label.text() == 'Ready to submit! Thanks!'


if __name__ == "__main__":
    pytest.main()
