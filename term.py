import sys
import cmd2
from cmd2 import style
import os
import glob
import difflib

from . import rc
from . import model
from . import view

from .controller import (
    index,
    show,
    search,
    tex,
    add,
    stats
)

WELCOME_MESSAGE = style("Welcome to VON!\n", fg="red", bold=True, underline=True)
PROMPT = style("$> ", fg="green", bold=True)

def _complete_path(path):
    path = os.path.join(rc.VON_BASE_PATH, path)
    if os.path.isdir(path):
        return [model.shortenPath(g) for g in glob.glob(os.path.join(path, '*'))]
    else:
        return [model.shortenPath(g) for g in glob.glob(path + '*')]

def _complete_label(label):
    labels = list(model.VonIndex())
    return difflib.get_close_matches(label, labels, len(labels), 0)

def completeVonPath(self, text, line, start_idx, end_idx):
    return _complete_path(text)

def completeVonLabel(self, text, line, start_idx, end_idx):
    return _complete_label(text)


class VonTerm(cmd2.Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = PROMPT
        self.intro = WELCOME_MESSAGE
        self.debug = True

    def do_exit(self, *args):
        sys.exit()

    do_index = index.main
    do_show = show.main
    do_search = search.main
    do_tex = tex.main
    do_add = add.main
    do_stats = stats.main

    complete_show = completeVonLabel
    complete_tex = completeVonLabel
    complete_add = completeVonPath

