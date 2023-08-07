import openai
from dotenv import load_dotenv
import os

load_dotenv()

def chatgpt(words_size):
    try:
        openai.api_key = os.getenv("OPENAI_KEY")
        system_text = """
    These data were extracted from a sequence of screens (screenshots) from a cell phone (mobile) in the following format: (word, x position, y position,width,height). The data is in a large array and each screen in the flow in an array inside. The screens are in order of execution. Identify the language of the screens and make sure that your analysis should be in the language you identified on the screens. You don't need to inform of the language, just write your analysis in the language you identified on the screens.
    Try to identify what the app is, analyze each screen, the flow of the screens, and suggest what is being done. If a screen does not have text and / or is empty, do not talk about it, or cite it. Consider the sizes and distances between the words in your analysis to understand how they should be positioned on the screen and how this influences the final result. At the end of your analysis, answer: What is the final result of the sequence of screens?

    Data:
    
        """
        system_text_pt = """
    Esses dados foram extraidos de uma sequencia de telas (screenshots) de um celular (mobile) no seguinte formato: (word, x position, y position, width, height). Os dados estão em um grande array e cada tela do fluxo em um array dentro. As telas estão em ordem de execução. Identifique o idioma das telas e a sua analise deve ser no idioma que você identificou nas telas. Não precisa me informar o idioma, apenas escreva a sua analise no idioma que você identificou nas telas.
    Tente identificar qual é o app, analise cada tela, o fluxo das telas, e sugira o que está sendo feito. Se uma tela não possuir texto e/ou estiver vazia não fale sobre ela, nem cite. Considere os tamanhos e distancias entre as palavras na sua análise para entender como elas devem estar posicionadas na tela e como isso influencia no resultado final. Ao final da sua análise responda: Qual o resultado final da sequencia de telas?

    Dados:

        """
        response_openai = openai.ChatCompletion.create(
            model='gpt-4',
            # model='gpt-3.5-turbo-16k',
            # model='gpt-4-32k', 
            messages=[{"role": "user", "content": system_text + words_size}], 
        )
        response_message = response_openai.choices[0].message.content
    except Exception as e:
        # print("Error: ", e)
        response_message = "Error: " + str(e)
    return response_message