#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.11.26 19:00:00                  #
# ================================================== #

from unittest.mock import MagicMock, patch

from tests.mocks import mock_window
from pygpt_net.controller.chat.input import Input
from pygpt_net.core.bridge.context import BridgeContext, MultimodalContext
from pygpt_net.item.ctx import CtxItem


def test_send_input(mock_window):
    """Test send input"""
    input = Input(mock_window)
    input.send = MagicMock()
    message = 'test'

    mock_window.controller.ctx.extra.is_editing = MagicMock(return_value=False)
    mock_window.ui.nodes['input'].toPlainText = MagicMock(return_value=message)

    input.send_input()
    mock_window.dispatch.assert_called()  # must dispatch event: user.send


def test_send_input_stop(mock_window):
    """Test send input with stop command"""
    input = Input(mock_window)
    input.send = MagicMock()
    input.generating = True
    message = 'stop'
    mock_window.controller.agent.common.is_infinity_loop = MagicMock(return_value=False)
    mock_window.controller.ctx.extra.is_editing = MagicMock(return_value=False)
    mock_window.ui.nodes['input'].toPlainText = MagicMock(return_value=message)

    input.send_input()
    mock_window.controller.kernel.stop.assert_called_once()
    mock_window.dispatch.assert_called()
    input.send.assert_not_called()


def test_send(mock_window):
    """Test send"""
    mock_window.controller.kernel.stopped = MagicMock(return_value=False)
    input = Input(mock_window)
    input.execute = MagicMock()
    context = BridgeContext()
    context.multimodal_ctx = MultimodalContext()
    context.prompt = "xxx"
    context.ctx = None
    extra = {}

    input.send(context, extra)
    input.execute.assert_called_once_with(
        text="xxx",
        force=False,
        reply=False,
        internal=False,
        prev_ctx=None,
        parent_id=None,
        multimodal_ctx=context.multimodal_ctx,
    )


def test_execute_text(mock_window):
    """Test execute for text"""
    input = Input(mock_window)
    input.locked = False
    mock_window.core.config.data['mode'] = 'chat'
    mock_window.core.config.data['attachments_send_clear'] = True
    mock_window.core.config.data['send_clear'] = True
    mock_window.controller.chat.common.check_api_key = MagicMock(return_value=True)  # api key OK
    mock_window.core.ctx.count_meta = MagicMock(return_value=1)  # ctx exists

    ctx = CtxItem()
    mock_window.controller.chat.text.send = MagicMock(return_value=ctx)  # send text to API and get ctx

    with patch('PySide6.QtWidgets.QApplication.processEvents') as mock_process_events:
        input.execute('test')

        # assert input.generating is False
        # assert input.stop is False

        mock_window.controller.chat.text.send.assert_called_once_with(
            text='test',
            reply=False,
            internal=False,
            prev_ctx=None,
            parent_id=None,
            multimodal_ctx=None,
        )
        # mock_window.controller.ui.update_tokens.assert_called_once()

        # attachments clear should be called
        #mock_window.controller.attachment.clear.assert_called_once()
        # mock_window.controller.attachment.update.assert_called_once()

        # input clear should be called
        mock_window.dispatch.assert_called()

        # handle allowed should be called
        mock_window.controller.ctx.handle_allowed.assert_called_once()


def test_execute_image(mock_window):
    """Test execute for image"""
    input = Input(mock_window)
    input.locked = False
    mock_window.core.config.data['mode'] = 'img'
    mock_window.core.config.data['attachments_send_clear'] = False
    mock_window.core.config.data['send_clear'] = False
    mock_window.controller.chat.common.check_api_key = MagicMock(return_value=True)  # api key OK
    mock_window.core.ctx.count_meta = MagicMock(return_value=1)  # ctx exists

    ctx = CtxItem()
    mock_window.controller.chat.text.send = MagicMock(return_value=ctx)  # send text to API and get ctx

    with patch('PySide6.QtWidgets.QApplication.processEvents') as mock_process_events:
        input.execute('test')

        assert input.stop is False

        mock_window.controller.chat.image.send.assert_called_once_with(text='test', prev_ctx=None, parent_id=None)
        # mock_window.controller.ui.update_tokens.assert_called_once()

        # attachments clear should not be called
        # mock_window.controller.attachment.clear.assert_not_called()
        # mock_window.controller.attachment.update.assert_not_called()

        # input clear should not be called
        mock_window.controller.chat.render.clear_input.assert_not_called()

        # handle allowed should be called
        mock_window.controller.ctx.handle_allowed.assert_called_once()


def test_execute_no_ctx(mock_window):
    """Test execute for text without ctx"""
    input = Input(mock_window)
    input.locked = False
    mock_window.core.config.data['mode'] = 'chat'
    mock_window.core.config.data['attachments_send_clear'] = True
    mock_window.core.config.data['send_clear'] = True
    mock_window.controller.chat.common.check_api_key = MagicMock(return_value=True)  # api key OK
    mock_window.core.ctx.count_meta = MagicMock(return_value=0)  # no ctx

    ctx = CtxItem()
    mock_window.controller.chat.text.send = MagicMock(return_value=ctx)  # send text to API and get ctx

    with patch('PySide6.QtWidgets.QApplication.processEvents') as mock_process_events:
        input.execute('test')

        mock_window.controller.chat.text.send.assert_called_once_with(
            text='test',
            reply=False,
            internal=False,
            prev_ctx=None,
            parent_id=None,
            multimodal_ctx=None,
        )
        # mock_window.controller.ui.update_tokens.assert_called_once()

        # attachments clear should be called
        # mock_window.controller.attachment.clear.assert_called_once()
        # mock_window.controller.attachment.update.assert_called_once()

        # input clear should be called
        mock_window.dispatch.assert_called()

        # handle allowed should not be called
        mock_window.controller.ctx.handle_allowed.assert_not_called()

        # new ctx should be created and saved
        mock_window.core.ctx.new.assert_called_once()
        mock_window.controller.ctx.update.assert_called_once()


def test_execute_empty_assistant(mock_window):
    """Test execute for text with empty assistant"""
    input = Input(mock_window)
    input.locked = False
    mock_window.core.config.data['mode'] = 'assistant'
    mock_window.core.config.data['assistant'] = None  # empty assistant
    mock_window.core.config.data['attachments_send_clear'] = True
    mock_window.core.config.data['send_clear'] = True
    mock_window.controller.chat.common.check_api_key = MagicMock(return_value=True)  # api key OK
    mock_window.core.ctx.count_meta = MagicMock(return_value=1)  # ctx exists

    ctx = CtxItem()
    mock_window.controller.chat.text.send = MagicMock(return_value=ctx)  # send text to API and get ctx

    with patch('PySide6.QtWidgets.QApplication.processEvents') as mock_process_events:
        input.execute('test')
        mock_window.ui.dialogs.alert.assert_called_once()
        mock_window.controller.chat.text.assert_not_called()


def test_execute_vision_mode(mock_window):
    """Test execute for vision mode"""
    input = Input(mock_window)
    input.locked = False
    mock_window.core.config.data['mode'] = 'vision'
    mock_window.core.config.data['attachments_send_clear'] = True
    mock_window.core.config.data['send_clear'] = True
    mock_window.controller.chat.common.check_api_key = MagicMock(return_value=True)  # api key OK
    mock_window.core.ctx.count_meta = MagicMock(return_value=1)  # ctx exists
    mock_window.controller.camera.is_enabled = MagicMock(return_value=True)
    mock_window.controller.camera.is_auto = MagicMock(return_value=True)
    mock_window.controller.ui.vision.has_vision = MagicMock(return_value=True)

    ctx = CtxItem()
    mock_window.controller.chat.text.send = MagicMock(return_value=ctx)  # send text to API and get ctx

    with patch('PySide6.QtWidgets.QApplication.processEvents') as mock_process_events:
        input.execute('test')

        mock_window.controller.chat.text.send.assert_called_once_with(
            text='test',
            reply=False,
            internal=False,
            prev_ctx=None,
            parent_id=None,
            multimodal_ctx=None,
        )
        # mock_window.controller.ui.update_tokens.assert_called_once()

        # attachments clear should be called
        # mock_window.controller.attachment.clear.assert_called_once()
        # mock_window.controller.attachment.update.assert_called_once()

        # input clear should be called
        mock_window.dispatch.assert_called()

        # handle allowed should be called
        mock_window.controller.ctx.handle_allowed.assert_called_once()

        # vision: capture frame should be called
        mock_window.controller.camera.handle_auto_capture()


def test_execute_vision_plugin(mock_window):
    """Test execute for inline vision mode by plugin"""
    input = Input(mock_window)
    input.locked = False
    mock_window.core.config.data['mode'] = 'chat'
    mock_window.core.config.data['attachments_send_clear'] = True
    mock_window.core.config.data['send_clear'] = True
    mock_window.controller.chat.common.check_api_key = MagicMock(return_value=True)  # api key OK
    mock_window.core.ctx.count_meta = MagicMock(return_value=1)  # ctx exists
    mock_window.controller.camera.is_enabled = MagicMock(return_value=True)
    mock_window.controller.camera.is_auto = MagicMock(return_value=True)
    mock_window.controller.ui.vision.has_vision = MagicMock(return_value=True)

    # plugin enabled for vision mode
    mock_window.controller.plugins.is_type_enabled = MagicMock(return_value=True)

    ctx = CtxItem()
    mock_window.controller.chat.text.send = MagicMock(return_value=ctx)  # send text to API and get ctx

    with patch('PySide6.QtWidgets.QApplication.processEvents') as mock_process_events:
        input.execute('test')

        mock_window.controller.chat.text.send.assert_called_once_with(
            text='test',
            reply=False,
            internal=False,
            prev_ctx=None,
            parent_id=None,
            multimodal_ctx=None,
        )
        # mock_window.controller.ui.update_tokens.assert_called_once()

        # attachments clear should be called
        # mock_window.controller.attachment.clear.assert_called_once()
        # mock_window.controller.attachment.update.assert_called_once()

        # input clear should be called
        mock_window.dispatch.assert_called()

        # handle allowed should be called
        mock_window.controller.ctx.handle_allowed.assert_called_once()

        # vision: capture frame should be called
        mock_window.controller.camera.handle_auto_capture()
