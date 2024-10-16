# llm-repo

A RAG agent that uses Ollama which is running a Local LLM, the one that we use in this as driver is llama-3.1, specifically llama3-groq-tool-use variant of the llama-3.1 .
It has following features:
 * Since it uses llama3-groq-tool-use variant it is verry good at performing [function calling](https://platform.openai.com/docs/guides/function-calling), allowing it to connect to internet and perform specific task for you.
 * It as of right now able to utilize funcion calling for fetching current weather condition of a location. It connects to [Open Meteo](https://open-meteo.com/).
 * It utilizes [TTS](https://github.com/coqui-ai/TTS), giving every answer a voice.

Future Scope:
 * Add more **functions** in the arsenal, allowing it to perform task more adequate for a **Personal Assistant AI**.
 * Give it a beautiful front-end with help of Flet a UI framework in python.
 * Package it into a application and a self extracting package.
 * Optimize it for performance.
