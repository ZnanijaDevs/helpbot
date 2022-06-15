# pylint: disable=line-too-long

import os


channels = {
    'TO_DELETE': os.environ['CHANNEL_TO_DELETE_ID'],
    'ANTISPAMERS': os.environ['CHANNEL_ANTISPAMERS_ID'],
    'HELP': os.environ['CHANNEL_HELP_ID'],
    'MODERATORS': os.environ['CHANNEL_MODERATORS_ID']
}

admins = [
    'U3FHTMNQY',
    'U2PS59CC8',
    'U2NSN0X26',
    'U018Q2S3KFA',
    'U3VMF71PU',
    'U35GJA25B',
    'U03C8Q4L2CR',
    'U03BL66ABD4',
    'U03BV5V60Q4',
    'U03FYLKRE9Y'
]

DANGER_REACTIONS_REGEX = r"check|2020|completed|peacock|reasonable|mary_cheek|^(bug|canc_noj)$"

TASK_ID_REGEX = r"(?<=\/task\/)\d+(?=\||>|\?)"
PROFILE_LINK_REGEX = r"(?<=<)[A-Za-z:\/]+znanija\.com\/((app\/profile\/)|(profil\/\w+-)|(users\/(user_content|redirect_user)\/))\d+"
DELETE_REASON_REGEX = r"(?<=\|)[А-Яа-я0-9]+|.+(?=<)|(?<=>)(.|\n)+?[А-Яа-я0-9\s]+"
