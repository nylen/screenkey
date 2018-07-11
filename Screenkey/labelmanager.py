# -*- coding: utf-8 -*-
# "screenkey" is distributed under GNU GPLv3+, WITHOUT ANY WARRANTY.
# Copyright(c) 2010-2012: Pablo Seminario <pabluk@gmail.com>
# Copyright(c) 2015-2016: wave++ "Yuri D'Elia" <wavexx@thregr.org>.

from __future__ import print_function, unicode_literals, absolute_import, generators

from .inputlistener import InputListener, InputType
import glib

from collections import namedtuple
from datetime import datetime

# Key replacement data:
#
# bk_stop: stops backspace processing in baked mode, but not full mode
#          these keys generally move the caret, and are also padded with a thin space
# silent:  always stops backspace processing (baked/full mode)
#          these keys generally do not emit output in the text and cannot be processed
# spaced:  strong spacing is required around the symbol

ReplData = namedtuple('ReplData', ['value', 'font', 'suffix'])
KeyRepl  = namedtuple('KeyRepl',  ['bk_stop', 'silent', 'spaced', 'repl'])
KeyData  = namedtuple('KeyData',  ['stamp', 'is_ctrl', 'bk_stop', 'silent', 'spaced', 'markup'])

REPLACE_SYMS = {
    # Regular keys
    'Escape':       KeyRepl(True,  True,  True,  _('Esc')),
    'Tab':          KeyRepl(True,  False, False, _('↹')),
    'ISO_Left_Tab': KeyRepl(True,  False, False, _('↹')),
    'Return':       KeyRepl(True,  False, False, _('⏎')),
    'space':        KeyRepl(False, False, False, _('␣')),
    'BackSpace':    KeyRepl(True,  True,  False, _('⌫')),
    'Caps_Lock':    KeyRepl(True,  True,  True,  _('Caps')),
    'F1':           KeyRepl(True,  True,  True,  _('F1')),
    'F2':           KeyRepl(True,  True,  True,  _('F2')),
    'F3':           KeyRepl(True,  True,  True,  _('F3')),
    'F4':           KeyRepl(True,  True,  True,  _('F4')),
    'F5':           KeyRepl(True,  True,  True,  _('F5')),
    'F6':           KeyRepl(True,  True,  True,  _('F6')),
    'F7':           KeyRepl(True,  True,  True,  _('F7')),
    'F8':           KeyRepl(True,  True,  True,  _('F8')),
    'F9':           KeyRepl(True,  True,  True,  _('F9')),
    'F10':          KeyRepl(True,  True,  True,  _('F10')),
    'F11':          KeyRepl(True,  True,  True,  _('F11')),
    'F12':          KeyRepl(True,  True,  True,  _('F12')),
    'Up':           KeyRepl(True,  True,  False, _('↑')),
    'Left':         KeyRepl(True,  True,  False, _('←')),
    'Right':        KeyRepl(True,  True,  False, _('→')),
    'Down':         KeyRepl(True,  True,  False, _('↓')),
    'Prior':        KeyRepl(True,  True,  True,  _('PgUp')),
    'Next':         KeyRepl(True,  True,  True,  _('PgDn')),
    'Home':         KeyRepl(True,  True,  True,  _('Home')),
    'End':          KeyRepl(True,  True,  True,  _('End')),
    'Insert':       KeyRepl(False, True,  True,  _('Ins')),
    'Delete':       KeyRepl(True,  False, True,  _('Del')),
    'KP_End':       KeyRepl(False, False, True,  _('(1)')),
    'KP_Down':      KeyRepl(False, False, True,  _('(2)')),
    'KP_Next':      KeyRepl(False, False, True,  _('(3)')),
    'KP_Left':      KeyRepl(False, False, True,  _('(4)')),
    'KP_Begin':     KeyRepl(False, False, True,  _('(5)')),
    'KP_Right':     KeyRepl(False, False, True,  _('(6)')),
    'KP_Home':      KeyRepl(False, False, True,  _('(7)')),
    'KP_Up':        KeyRepl(False, False, True,  _('(8)')),
    'KP_Prior':     KeyRepl(False, False, True,  _('(9)')),
    'KP_Insert':    KeyRepl(False, False, True,  _('(0)')),
    'KP_Delete':    KeyRepl(False, False, True,  _('(.)')),
    'KP_Add':       KeyRepl(False, False, True,  _('(+)')),
    'KP_Subtract':  KeyRepl(False, False, True,  _('(-)')),
    'KP_Multiply':  KeyRepl(False, False, True,  _('(*)')),
    'KP_Divide':    KeyRepl(False, False, True,  _('(/)')),
    'KP_Enter':     KeyRepl(True,  False, False, _('⏎')),
    'Num_Lock':     KeyRepl(False, True,  True,  _('NumLck')),
    'Scroll_Lock':  KeyRepl(False, True,  True,  _('ScrLck')),
    'Pause':        KeyRepl(False, True,  True,  _('Pause')),
    'Break':        KeyRepl(False, True,  True,  _('Break')),
    'Print':        KeyRepl(False, True,  True,  _('Print')),
    'Multi_key':    KeyRepl(False, True,  True,  _('Compose')),

    # Multimedia keys
    'XF86AudioMute':         KeyRepl(True, True, True, [ReplData(_('\uf026'),  'FontAwesome', None),
                                                        ReplData(_('Mute'),    None,          None)]),
    'XF86AudioMicMute':      KeyRepl(True, True, True, [ReplData(_('\uf131'),  'FontAwesome', None),
                                                        ReplData(_('Rec'),     None,          None)]),
    'XF86AudioRaiseVolume':  KeyRepl(True, True, True, [ReplData(_('\uf028'),  'FontAwesome', None),
                                                        ReplData(_('Vol'),     None,          '+')]),
    'XF86AudioLowerVolume':  KeyRepl(True, True, True, [ReplData(_('\uf027'),  'FontAwesome', None),
                                                        ReplData(_('Vol'),     None,          '-')]),
    'XF86AudioPrev':         KeyRepl(True, True, True, [ReplData(_('\uf048'),  'FontAwesome', None),
                                                        ReplData(_('Prev'),    None,          None)]),
    'XF86AudioNext':         KeyRepl(True, True, True, [ReplData(_('\uf051'),  'FontAwesome', None),
                                                        ReplData(_('Next'),    None,          None)]),
    'XF86AudioPlay':         KeyRepl(True, True, True, [ReplData(_('\uf04b'),  'FontAwesome', None),
                                                        ReplData(_('▶'),       None,          None)]),
    'XF86AudioStop':         KeyRepl(True, True, True, [ReplData(_('\uf04d'),  'FontAwesome', None),
                                                        ReplData(_('⬛'),       None,          None)]),
    'XF86Eject':             KeyRepl(True, True, True, [ReplData(_('\uf052'),  'FontAwesome', None),
                                                        ReplData(_('Eject'),   None,          None)]),
    'XF86MonBrightnessDown': KeyRepl(True, True, True, [ReplData(_('\uf185'),  'FontAwesome', '-'),
                                                        ReplData(_('Bright'),  None,          '-')]),
    'XF86MonBrightnessUp':   KeyRepl(True, True, True, [ReplData(_('\uf185'),  'FontAwesome', '+'),
                                                        ReplData(_('Bright'),  None,          '+')]),
    'XF86Display':           KeyRepl(True, True, True, [ReplData(_('\uf108'),  'FontAwesome', None),
                                                        ReplData(_('Display'), None,          None)]),
    'XF86WLAN':              KeyRepl(True, True, True, [ReplData(_('\uf1eb'),  'FontAwesome', None),
                                                        ReplData(_('WLAN'),    None,          None)]),
    'XF86Search':            KeyRepl(True, True, True, [ReplData(_('\uf002'),  'FontAwesome', None),
                                                        ReplData(_('Search'),  None,          None)]),
}

WHITESPACE_SYMS = {'Tab', 'ISO_Left_Tab', 'Return', 'space', 'KP_Enter'}

MODS_SYMS = {
    'shift':  {'Shift_L', 'Shift_R'},
    'ctrl':   {'Control_L', 'Control_R'},
    'alt':    {'Alt_L', 'Alt_R', 'Meta_L', 'Meta_R'},
    'super':  {'Super_L', 'Super_R'},
    'hyper':  {'Hyper_L', 'Hyper_R'},
    'alt_gr': {'ISO_Level3_Shift'},
}

REPLACE_MODS = {
    'shift':  {'normal': _('Shift+'), 'emacs': 'S-', 'mac': _('⇧+')},
    'ctrl':   {'normal': _('Ctrl+'),  'emacs': 'C-', 'mac': _('⌘+')},
    'alt':    {'normal': _('Alt+'),   'emacs': 'M-', 'mac': _('⌥+')},
    'super':  {'normal': _('Super+'), 'emacs': 's-',
               'win': [ReplData(_('\uf17a'), 'FontAwesome', '+'),
                       ReplData(_('Win'),    None,          '+')],
               'tux': [ReplData(_('\uf17c'), 'FontAwesome', '+'),
                       ReplData(_('Super'),  None,          '+')]},
    'hyper':  {'normal': _('Hyper+'), 'emacs': 'H-'},
    'alt_gr': {'normal': _('AltGr+'), 'emacs': 'AltGr-'},
}


def keysym_to_mod(keysym):
    for k, v in MODS_SYMS.items():
        if keysym in v:
            return k
    return None


class LabelManager(object):
    def __init__(self, listener, logger, key_mode, bak_mode, mods_mode, mods_only,
                 multiline, vis_shift, vis_space, recent_thr, compr_cnt, ignore, pango_ctx):
        self.key_mode = key_mode
        self.bak_mode = bak_mode
        self.mods_mode = mods_mode
        self.logger = logger
        self.listener = listener
        self.data = []
        self.key_count = 0
        self.enabled = True
        self.mods_only = mods_only
        self.multiline = multiline
        self.vis_shift = vis_shift
        self.vis_space = vis_space
        self.recent_thr = recent_thr
        self.compr_cnt = compr_cnt
        self.ignore = ignore
        self.kl = None
        self.font_families = {x.get_name() for x in pango_ctx.list_families()}
        self.update_replacement_map()


    def __del__(self):
        self.stop()


    def start(self):
        self.stop()
        compose = (self.key_mode == 'composed')
        translate = (self.key_mode in ['composed', 'translated'])
        self.kl = InputListener(self.key_press, InputType.keyboard, compose, translate)
        self.kl.start()
        self.logger.debug("Thread started.")


    def stop(self):
        if self.kl:
            self.kl.stop()
            self.logger.debug("Thread stopped.")
            self.kl.join()
            self.kl = None


    def clear(self):
        self.data = []


    def get_repl_markup(self, repl):
        if type(repl) != list:
            repl = [repl]
        for c in repl:
            # no replacement data
            if type(c) != ReplData:
                return unicode(glib.markup_escape_text(c))

            # plain suffix
            if c.suffix is None:
                sfx = ''
            else:
                sfx = unicode(glib.markup_escape_text(c.suffix))

            if c.font is None:
                # regular font
                return unicode(glib.markup_escape_text(c.value)) + sfx;
            elif c.font in self.font_families:
                # custom symbol
                return '<span font_family="' + c.font + '" font_weight="regular">' + \
                    unicode(glib.markup_escape_text(c.value)) + '</span>' + sfx;


    def update_replacement_map(self):
        self.replace_syms = {}
        for k, v in REPLACE_SYMS.items():
            markup = self.get_repl_markup(v.repl)
            self.replace_syms[k] = KeyRepl(v.bk_stop, v.silent, v.spaced, markup)

        self.replace_mods = {}
        for k, v in REPLACE_MODS.items():
            data = v.get(self.mods_mode, v['normal'])
            self.replace_mods[k] = self.get_repl_markup(data)


    def update_text(self):
        markup = ""
        recent = False
        stamp = datetime.now()
        repeats = 0
        for i, key in enumerate(self.data):
            if i != 0:
                markup += ' '
            markup += key.markup
        self.logger.debug("Label updated: %s." % repr(markup))
        if markup == '':
            self.key_count = 0
        self.listener(markup, self.key_count)


    def key_press(self, event):
        is_pressed = True
        if event is None:
            self.logger.debug("inputlistener failure: {}".format(str(self.kl.error)))
            self.listener(None)
            return
        if event.pressed == False:
            self.logger.debug("Key released {:5}(ks): {}".format(event.keysym, event.symbol))
            is_pressed = False
        if event.symbol in self.ignore:
            self.logger.debug("Key ignored  {:5}(ks): {}".format(event.keysym, event.symbol))
            return
        if event.filtered:
            self.logger.debug("Key filtered {:5}(ks): {}".format(event.keysym, event.symbol))
        else:
            state = "repeated" if event.repeated else "pressed"
            string = repr(event.string)
            self.logger.debug("Key {:8} {:5}(ks): {} ({}, mask: {:08b})".format
                              (state, event.keysym, string, event.symbol, event.mods_mask))

        # Modifiers only
        if keysym_to_mod(event.symbol) is None:
            if len(self.data) and is_pressed:
                self.key_count += 1
                self.update_text()
                return True
            else:
                return False

        if self.key_keysyms_mode(event, is_pressed):
            self.update_text()


    def key_normal_mode(self, event):
        # Visible modifiers
        mod = ''
        for cap in ['ctrl', 'alt', 'super', 'hyper']:
            if event.modifiers[cap]:
                mod = mod + self.replace_mods[cap]

        # Backspace handling
        if event.symbol == 'BackSpace' and not self.mods_only and \
           mod == '' and not event.modifiers['shift']:
            key_repl = self.replace_syms.get(event.symbol)
            if self.bak_mode == 'normal':
                self.data.append(KeyData(datetime.now(), False, *key_repl))
                return True
            else:
                if not len(self.data):
                    pop = False
                else:
                    last = self.data[-1]
                    if last.is_ctrl:
                        pop = False
                    elif self.bak_mode == 'baked':
                        pop = not last.bk_stop
                    else:
                        pop = not last.silent
                if pop:
                    self.data.pop()
                else:
                    self.data.append(KeyData(datetime.now(), False, *key_repl))
                return True

        # Regular keys
        key_repl = self.replace_syms.get(event.symbol)
        replaced = key_repl is not None
        if key_repl is None:
            if keysym_to_mod(event.symbol):
                return False
            else:
                repl = event.string or event.symbol
                markup = unicode(glib.markup_escape_text(repl))
                key_repl = KeyRepl(False, False, len(repl) > 1, markup)

        if event.modifiers['shift'] and \
           (replaced or (mod != '' and \
                         self.vis_shift and \
                         self.mods_mode != 'emacs')):
            # add back shift for translated keys
            mod = mod + self.replace_mods['shift']

        # Whitespace handling
        if not self.vis_space and mod == '' and event.symbol in WHITESPACE_SYMS:
            if event.symbol not in ['Return', 'KP_Enter']:
                repl = event.string
            elif self.multiline:
                repl = ''
            else:
                repl = key_repl.repl
            key_repl = KeyRepl(key_repl.bk_stop, key_repl.silent, key_repl.spaced, repl)

        # Multiline
        if event.symbol in ['Return', 'KP_Enter'] and self.multiline == True:
            key_repl = KeyRepl(key_repl.bk_stop, key_repl.silent,
                               key_repl.spaced, key_repl.repl + '\n')

        if mod == '':
            if not self.mods_only:
                repl = key_repl.repl

                # switches
                if event.symbol in ['Caps_Lock', 'Num_Lock']:
                    state = event.modifiers[event.symbol.lower()]
                    repl += '(%s)' % (_('off') if state else _('on'))

                self.data.append(KeyData(datetime.now(), False, key_repl.bk_stop,
                                         key_repl.silent, key_repl.spaced, repl))
                return True
        else:
            if self.mods_mode == 'emacs' or key_repl.repl[0] != mod[-1]:
                repl = mod + key_repl.repl
            else:
                repl = mod + '‟' + key_repl.repl + '”'
            self.data.append(KeyData(datetime.now(), True, key_repl.bk_stop,
                                     key_repl.silent, key_repl.spaced, repl))
            return True

        return False


    def key_raw_mode(self, event):
        # modifiers
        mod = ''
        for cap in REPLACE_MODS.keys():
            if event.modifiers[cap]:
                mod = mod + self.replace_mods[cap]

        # keycaps
        key_repl = self.replace_syms.get(event.symbol)
        if key_repl is None:
            if keysym_to_mod(event.symbol):
                return False
            else:
                repl = event.string.upper() if event.string else event.symbol
                markup = unicode(glib.markup_escape_text(repl))
                key_repl = KeyRepl(False, False, len(repl) > 1, markup)

        if mod == '':
            repl = key_repl.repl

            # switches
            if event.symbol in ['Caps_Lock', 'Num_Lock']:
                state = event.modifiers[event.symbol.lower()]
                repl += '(%s)' % (_('off') if state else _('on'))

            self.data.append(KeyData(datetime.now(), False, key_repl.bk_stop,
                                     key_repl.silent, key_repl.spaced, repl))
        else:
            if self.mods_mode == 'emacs' or key_repl.repl[0] != mod[-1]:
                repl = mod + key_repl.repl
            else:
                repl = mod + '‟' + key_repl.repl + '”'
            self.data.append(KeyData(datetime.now(), True, key_repl.bk_stop,
                                     key_repl.silent, key_repl.spaced, repl))
        return True


    def key_keysyms_mode(self, event, is_pressed):
        if event.symbol in REPLACE_SYMS:
            value = event.symbol
        else:
            value = event.string or event.symbol

        old_len = len(self.data)
        self.data = [key for key in self.data if key.markup != value]
        if is_pressed:
            self.data.append(KeyData(datetime.now(), True, True, True, True, value))
        return len(self.data) != old_len
