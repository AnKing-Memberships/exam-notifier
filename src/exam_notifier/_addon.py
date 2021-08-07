# -*- coding: utf-8 -*-

# Exam Notifier Add-on for Anki
#
# Copyright (C) 2019-2021  Aristotelis P. <https://glutanimate.com/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the license file that accompanied this program.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# NOTE: This program is subject to certain additional terms pursuant to
# Section 7 of the GNU Affero General Public License.  You should have
# received a copy of these additional terms immediately following the
# terms and conditions of the GNU Affero General Public License that
# accompanied this program.
#
# If not, please request a copy through one of the means of contact
# listed here: <https://glutanimate.com/contact/>.
#
# Any modifications to this file must keep this entire header intact.

from typing import Final, TYPE_CHECKING

from aqt import mw
from aqt.gui_hooks import reviewer_did_show_question

from ._version import __version__  # noqa: F401
from .consts import ADDON
from .deck_options_legacy import (
    DeckConfigDialogPatcher,
    DeckConfigDialogService,
    ExamConfigTab,
)
from .libaddon.consts import set_addon_properties
from .notifications import NotificationService
from .reviewer import ReviewService
from .deck_config import DeckConfigService

if TYPE_CHECKING:
    assert mw is not None

# Constants ####

EXAM_SETTINGS_KEY: Final = "exam_settings"

set_addon_properties(ADDON)

# Deck options dialog ####

# Qt (Anki <= 2.1.44 and any Anki with V1 scheduler)

deck_config_dialog_service = DeckConfigDialogService(
    settings_key=EXAM_SETTINGS_KEY, deck_config_tab_factory=ExamConfigTab
)
deck_config_dialog_patcher = DeckConfigDialogPatcher(deck_config_dialog_service)
deck_config_dialog_patcher.patch()

# Web (new) TODO

# Deck config access ####

deck_config_service = DeckConfigService(main_window=mw, settings_key=EXAM_SETTINGS_KEY)

# Notifications ####

notification_service = NotificationService()

# Reviewer ####

review_service = ReviewService(
    main_window=mw,
    deck_config_service=deck_config_service,
    notification_service=notification_service,
)

reviewer_did_show_question.append(review_service.on_reviewer_did_show_question)