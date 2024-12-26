#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.08.22 17:00:00                  #
# ================================================== #

from langchain_openai import OpenAI  # <--- Import OpenAI provider for Langchain (completion)
from langchain_openai import ChatOpenAI  # <--- Import ChatOpenAI provider for Langchain (chat)

from llama_index.core.llms.llm import BaseLLM as LlamaBaseLLM
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.llms.openai import OpenAI as LlamaOpenAI  # <--- Import OpenAI provider for Llama-Index
from llama_index.embeddings.openai import OpenAIEmbedding  # <--- Import OpenAI embeddings for Llama-Index

from pygpt_net.provider.llms.base import BaseLLM  # <--- provider must inherit from BaseLLM class
from pygpt_net.item.model import ModelItem  # <--- ModelItem class with selected model config


class ExampleLlm(BaseLLM):
    def __init__(self, *args, **kwargs):
        super(ExampleLlm, self).__init__(*args, **kwargs)

        # Define provider ID and modes handled by the provider:

        self.id = "example_llm"  # <--- ID of the provider, must be unique in the app
        self.type = ["langchain", "llama_index"]  # <--- List with modes handled by the provider

        # You can handle Langchain and Chat with files (llama-index) modes in the same provider
        # Methods defined in this class will be used for each use case.

    def completion(self, window, model: ModelItem, stream: bool = False):
        """
        Return Langchain LLM provider instance for completion mode.

        This method is used for Langchain mode when getting provider to handle completion.
        It must return an instance of the Langchain LLM provider for completion mode.
        Instance returned by this method must provide methods for completion mode:

            - `invoke(message)` - method for completion
            - `stream(message)` - method for completion in stream mode

        See: `pygpt_net.core.chain.completion` for more details how it is handled internally.

        In this example, the method returns OpenAI provider instance.
        Keyword arguments for the Langchain provider are parsed from the model config instance and can be
        configured in 'Models' settings dialog (or manually, in '%workdir%/models.json' config file).

        :param window: window instance
        :param model: model instance - current model
        :param stream: stream mode - True if stream mode is enabled
        :return: Langchain LLM provider instance
        """
        print("Using example provider (completion)...")
        print("Using model:", model.id)
        print("Model config:", model)

        # arguments parser is provided by BaseLLM class
        args = self.parse_args(model.langchain)  # <--- config for Langchain is stored in `model.langchain` dict
        print("Keyword arguments for the example provider:", args)

        # return OpenAI provider instance
        return OpenAI(**args)  # <--- pass all parsed args from model config to the provider

    def chat(self, window, model: ModelItem, stream: bool = False):
        """
        Return Langchain LLM provider instance for chat mode.

        This method is used for Langchain mode when getting provider to handle chat.
        It must return an instance of the Langchain LLM provider for chat mode.
        Instance returned by this method must provide methods for chat mode:

            - `invoke(messages)` - method for chat
            - `stream(messages)` - method for chat in stream mode

        See: `pygpt_net.core.chain.chat` for more details how it is handled internally.

        In this example, the method returns ChatOpenAI provider instance.
        Keyword arguments for the Langchain provider are parsed from the model config instance and can be
        configured in 'Models' settings dialog (or manually, in '%workdir%/models.json' config file).

        :param window: window instance
        :param model: model instance - current model
        :param stream: stream mode - True if stream mode is enabled
        :return: Langchain LLM provider instance
        """
        print("Using example provider (chat)...")
        print("Using model:", model.id)
        print("Model config:", model)

        # arguments parser is provided by BaseLLM class
        args = self.parse_args(model.langchain)  # <--- config for Langchain is stored in `model.langchain` dict
        print("Keyword arguments for the example provider:", args)

        # return ChatOpenAI provider instance
        return ChatOpenAI(**args)  # <--- pass all parsed args from model config to the provider

    def llama(self, window, model: ModelItem, stream: bool = False) -> LlamaBaseLLM:
        """
        Return LlamaIndex LLM provider instance for 'Chat with Files' (llama_index) mode.

        This method is used for Llama-Index mode when getting provider to handle chat with files.
        It must return an instance of the Llama-Index LLM which will be used in service context.

        See how it is handled internally for more details:
            - `pygpt_net.core.idx.llm.get`
            - `pygpt_net.core.idx.llm.get_service_context`

        In this example, the method returns LlamaOpenAI provider instance.
        Keyword arguments for the Llama-Index provider are parsed from the model config instance and can be
        configured in 'Models' settings dialog (or manually, in '%workdir%/models.json' config file).

        :param window: window instance
        :param model: model instance - current model
        :param stream: stream mode - True if stream mode is enabled
        :return: LLM provider instance
        """
        print("Using example provider (llama-index)...")
        print("Using model:", model.id)
        print("Model config:", model)

        # arguments parser is provided by BaseLLM class
        args = self.parse_args(model.llama_index)  # <--- config for Llama-index is stored in `model.llama_index` dict
        print("Keyword arguments for the example provider:", args)

        # return OpenAI provider instance
        return LlamaOpenAI(**args)  # <--- pass all parsed args from model config to the provider

    def get_embeddings_model(self, window, config: list = None) -> BaseEmbedding:
        """
        Return provider instance for embeddings

        This method is used to get provider instance for embeddings.
        It must return an instance of the Embedding provider which will be used for embeddings in Llama-Index.

        See how it is handled internally for more details:
            - `pygpt_net.core.idx.llm.get_embeddings_provider`

        In this example, the method returns OpenAIEmbedding provider instance.
        Keyword arguments for the Embedding provider are parsed from the global config and can be
        configured in 'Config -> Indexes (Llama-index) -> Embeddings -> Embeddings provider **kwargs' option.

        :param window: window instance
        :param config: config keyword arguments list
        :return: Embedding provider instance
        """
        print("Using example embeddings provider (llama-index)...")
        print("Using config:", config)

        # arguments parser is provided by BaseLLM class
        args = {}
        if config is not None:
            args = self.parse_args({  # <--- config for embeddings is passed as a list of keyword arguments from the global config
                "args": config,
            })
        return OpenAIEmbedding(**args)  # <--- pass all parsed args from model config to the provider
