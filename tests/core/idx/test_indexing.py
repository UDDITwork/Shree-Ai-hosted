#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.11.23 19:00:00                  #
# ================================================== #

import os
import platform
from unittest.mock import MagicMock, patch, Mock
from llama_index.core import Document

from tests.mocks import mock_window
from pygpt_net.core.idx import Indexing


def test_get_online_loader(mock_window):
    """Test get online loader"""
    idx = Indexing(mock_window)
    loader = MagicMock()
    loaders = [
        {
            "ext": "pdf",
            "loader": loader,
        },
    ]
    mock_window.core.config.set("llama.hub.loaders", loaders)
    assert idx.get_online_loader("pdf") == loader


def test_get_documents(mock_window):
    """Test get documents"""
    idx = Indexing(mock_window)
    mock_window.core.filesystem.packer.is_archive = MagicMock(return_value=False)
    idx.get_online_loader = MagicMock(return_value=None)
    doc = Document()
    docs = [doc]
    reader = MagicMock()
    reader.load_data = MagicMock(return_value=docs)
    loaders = {
        "file": {
            "pdf": reader,
        }
    }
    idx.loaders = loaders
    with patch("os.path.isdir") as mock_isdir:
        mock_isdir.return_value = False
        documents = idx.get_documents("file.pdf")
    assert documents == docs


def test_index_files_single_file(mock_window):
    """Test index file"""
    index = MagicMock()
    path = "file.pdf"
    idx = Indexing(mock_window)
    doc = Document()
    doc.id_ = "test_id"
    docs = [doc]
    idx.get_documents = MagicMock(return_value=docs)
    idx.index_documents = MagicMock()
    idx.window.controller.idx = MagicMock()
    idx.window.controller.idx.is_stopped = MagicMock(return_value=False)
    with patch("os.path.isdir") as mock_isdir:
        mock_isdir.return_value = False
        with patch("os.path.isfile") as mock_isfile:
            mock_isfile.return_value = True
            indexed, errors = idx.index_files("base", index, path)
    assert indexed == {"file.pdf": "test_id"}
    assert errors == []


def test_index_files_in_directory(mock_window):
    """Test index directory"""
    index = MagicMock()
    idx = Indexing(mock_window)
    idx.window.controller.idx = MagicMock()
    idx.window.controller.idx.is_stopped = MagicMock(return_value=False)
    doc = Document()
    doc.id_ = "test_id"
    docs = [doc]
    idx.get_documents = MagicMock(return_value=docs)
    idx.index_documents = MagicMock()
    fake_path = '/fake/directory'
    fake_files = ['file1.txt', 'file2.txt', 'file3.txt']
    with patch('os.path.isdir') as mock_isdir, \
            patch('os.listdir') as mock_listdir, \
            patch('os.path.isfile') as mock_isfile:
        mock_isdir.return_value = True
        mock_listdir.return_value = fake_files
        mock_isfile.side_effect = lambda x: x in (os.path.join(fake_path, f) for f in fake_files)
        indexed, errors = idx.index_files("base", index, fake_path)

    if platform.system() == 'Windows':
        assert indexed == {
            '/fake/directory\\file1.txt': 'test_id',
            '/fake/directory\\file2.txt': 'test_id',
            '/fake/directory\\file3.txt': 'test_id'
        }
    else:
        assert indexed == {
            '/fake/directory/file1.txt': 'test_id',
            '/fake/directory/file2.txt': 'test_id',
            '/fake/directory/file3.txt': 'test_id'
        }
    assert errors == []


def test_get_db_data_from_ts(mock_window):
    """Test get db data from ts"""
    idx = Indexing(mock_window)
    updated_ts = 1234567890
    row1 = MagicMock()
    row1._asdict = MagicMock(
        return_value={"id": 123, "text": "User: user_input1; Assistant: assistant_output1", "input_ts": 0,
                      "meta_id": 123, "item_id": "test_id1"})
    row2 = MagicMock()
    row2._asdict = MagicMock(
        return_value={"id": 123, "text": "User: user_input2; Assistant: assistant_output2", "input_ts": 0,
                      "meta_id": 123, "item_id": "test_id1"})
    rows = [row1, row2]
    result = MagicMock()
    result.fetchall.return_value = rows
    conn = Mock()
    conn.execute.return_value = result
    with patch('pygpt_net.core.db.Database.get_db') as mock_get_db:
        mock_window.core.db.get_db = mock_get_db
        mock_get_db.return_value.connect.return_value.__enter__.return_value = conn
        documents = idx.get_db_data_from_ts(updated_ts)
    assert documents[0].text == 'User: user_input1; Assistant: assistant_output1'
    assert documents[1].text == 'User: user_input2; Assistant: assistant_output2'


def test_get_db_data_by_id(mock_window):
    """Test get db data by id"""
    idx = Indexing(mock_window)
    id = 123
    row1 = MagicMock()
    row1._asdict = MagicMock(return_value={"id": 123, "text": "User: user_input1; Assistant: assistant_output1", "input_ts": 0, "meta_id": 123, "item_id": "test_id1"})
    row2 = MagicMock()
    row2._asdict = MagicMock(return_value={"id": 123, "text": "User: user_input2; Assistant: assistant_output2", "input_ts": 0, "meta_id": 123, "item_id": "test_id1"})
    rows = [row1, row2]
    result = MagicMock()
    result.fetchall.return_value = rows
    conn = Mock()
    conn.execute.return_value = result
    with patch('pygpt_net.core.db.Database.get_db') as mock_get_db:
        mock_window.core.db.get_db = mock_get_db
        mock_get_db.return_value.connect.return_value.__enter__.return_value = conn
        documents = idx.get_db_data_by_id(id)
    assert documents[0].text == 'User: user_input1; Assistant: assistant_output1'
    assert documents[1].text == 'User: user_input2; Assistant: assistant_output2'


def test_index_db_by_meta_id(mock_window):
    """Test index db by meta id"""
    idx = Indexing(mock_window)
    idx.window.controller.idx = MagicMock()
    idx.window.controller.idx.is_stopped = MagicMock(return_value=False)
    doc = Document()
    doc.id_ = "test_id"
    docs = [doc]
    idx.get_db_data_by_id = MagicMock(return_value=docs)
    idx.index_documents = MagicMock()
    index = MagicMock()
    indexed, errors = idx.index_db_by_meta_id("base", index, 123)
    assert indexed == 1
    assert errors == []


def test_index_db_from_updated_ts(mock_window):
    """Test index db from updated ts"""
    idx = Indexing(mock_window)
    idx.window.controller.idx = MagicMock()
    idx.window.controller.idx.is_stopped = MagicMock(return_value=False)
    idx.index_db_by_meta_id = MagicMock(return_value=(1, []))
    idx.get_db_meta_ids_from_ts = MagicMock(return_value=[123])
    doc = Document()
    idx.index_documents = MagicMock()
    index = MagicMock()
    indexed, errors = idx.index_db_from_updated_ts("base", index, 123)
    assert indexed == 1
    assert errors == []
