from openai import AzureOpenAI


class GptClient:

    gpt = AzureOpenAI(
            azure_endpoint="https://momoopenai.openai.azure.com/",
            api_version="2024-08-01-preview",
            api_key="46935c341fc74abbbb64d1dd68ded6cf",
            azure_deployment="MomoGpt4o"
            )

    @staticmethod
    def query(msg: str) -> str:
        payload = [
                    {
                        "role": "user",
                        "content": msg
                        }
                ]

        response = GptClient.gpt.chat.completions.create(
                messages=payload,
                model="MomoGpt4o",
                )

        first_response = response.choices[0].message
        return first_response.content
