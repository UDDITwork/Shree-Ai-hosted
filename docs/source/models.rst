Models
======

Built-in models
---------------

PyGPT has built-in support for models (as of 2024-11-27):

* ``bielik-11b-v2.2-instruct:Q4_K_M``
* ``chatgpt-4o-latest``
* ``claude-3-5-sonnet-20240620``
* ``claude-3-opus-20240229``
* ``codellama``
* ``dall-e-2``
* ``dall-e-3``
* ``gemini-1.5-flash``
* ``gemini-1.5-pro``
* ``gpt-3.5-turbo``
* ``gpt-3.5-turbo-1106``
* ``gpt-3.5-turbo-16k``
* ``gpt-3.5-turbo-instruct``
* ``gpt-4``
* ``gpt-4-0125-preview``
* ``gpt-4-1106-preview``
* ``gpt-4-32k``
* ``gpt-4-turbo``
* ``gpt-4-turbo-2024-04-09``
* ``gpt-4-turbo-preview``
* ``gpt-4-vision-preview``
* ``gpt-4o``
* ``gpt-4o-2024-11-20``
* ``gpt-4o-audio-preview``
* ``gpt-4o-mini``
* ``llama2-uncensored``
* ``llama3.1``
* ``llama3.1:405b``
* ``llama3.1:70b``
* ``mistral``
* ``mistral-large``
* ``o1-mini``
* ``o1-preview``

All models are specified in the configuration file ``models.json``, which you can customize. 
This file is located in your working directory. You can add new models provided directly by ``OpenAI API``
and those supported by ``LlamaIndex`` or ``LangChain`` to this file. Configuration for LangChain wrapper is placed in ``langchain`` key, configuration for LlamaIndex in ``llama_index`` key.

Adding a custom model
---------------------

You can add your own models. See the section ``Extending PyGPT / Adding a new model`` for more info.

There is built-in support for those LLM providers:

* ``OpenAI`` (openai)
* ``Azure OpenAI`` (azure_openai)
* ``Google`` (google)
* ``HuggingFace API`` (huggingface_api)
* ``Anthropic`` (anthropic)
* ``Ollama`` (ollama)

How to use local or non-GPT models
----------------------------------

Llama 3, Mistral, and other local models
````````````````````````````````````````

How to use locally installed Llama 3 or Mistral models:

1) Choose a working mode: ``Chat with Files`` or ``LangChain``.

2) On the models list - select, edit, or add a new model (with ``ollama`` provider). You can edit the model settings through the menu ``Config -> Models``, then configure the model parameters in the ``advanced`` section.

3) Download and install Ollama from here: https://github.com/ollama/ollama

For example, on Linux:

.. code-block:: sh

    $ curl -fsSL https://ollama.com/install.sh | sh

4) Run the model (e.g. Llama 3) locally on your machine. For example, on Linux:

.. code-block:: sh

    $ ollama run llama3.1

5) Return to PyGPT and select the correct model from models list to chat with selected model using Ollama running locally.

**Example available models:**

- ``llama3.1``
- ``codellama``
- ``mistral``
- ``llama2-uncensored``

You can add more models by editing the models list.

**List of all models supported by Ollama:**

https://ollama.com/library

https://github.com/ollama/ollama

**IMPORTANT:** Remember to define the correct model name in the **kwargs list in the model settings.

Using local embeddings
```````````````````````
Refer to: https://docs.llamaindex.ai/en/stable/examples/embeddings/ollama_embedding/

You can use an Ollama instance for embeddings. Simply select the ``ollama`` provider in:

.. code-block:: sh

    Config -> Settings -> Indexes (LlamaIndex) -> Embeddings -> Embeddings provider

Define parameters like model name and Ollama base URL in the Embeddings provider **kwargs list, e.g.:

- name: ``model_name``, value: ``llama3.1``, type: ``str``

- name: ``base_url``, value: ``http://localhost:11434``, type: ``str``


Google Gemini and Anthropic Claude
``````````````````````````````````
To use ``Gemini`` or ``Claude`` models, select the ``Chat with Files`` mode in PyGPT and select a predefined model.
Remember to configure the required parameters like API keys in the model ENV config fields.

**Google Gemini**

Required ENV:

- GOOGLE_API_KEY

Required **kwargs:

- model

**Anthropic Claude**

Required ENV:

- ANTHROPIC_API_KEY

Required **kwargs:

- model
