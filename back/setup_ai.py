from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain import LLMChain
from langchain.prompts import PromptTemplate
import json

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain

class Ai: 
    def __init__(self):
        llm_chat = ChatOpenAI(openai_api_key="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")
        llm_recommendation = OpenAI(openai_api_key="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")
        

        template = """Extract from this text 3 recommedations of universities and give names of them in json list format without white spaces

        text:
        {text}
        """
        prompt_template = PromptTemplate(input_variables=["text"], template=template)
        self.recommendation_chain = LLMChain(llm=llm_recommendation, prompt=prompt_template)



        # Prompt 
        prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(
                    '''You are truthful, concise a career coach and you have to help me choose university based only on data in provided documents. Every response should end with 3 recommendations of universities. If You do not know, just say "I don't know."
                    context###
                        Uniwersytet Warszawski. Założony w 1816 roku, Uniwersytet Warszawski jest największą uczelnią wyższą w Polsce. Oferuje szeroki zakres kursów na poziomie licencjackim, magisterskim i podyplomowym.

                    ###'''
                ),
                # The `variable_name` here is what must align with memory
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}")
            ]
        )

        # Notice that we `return_messages=True` to fit into the MessagesPlaceholder
        # Notice that `"chat_history"` aligns with the MessagesPlaceholder name
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.conversation = LLMChain(
            llm=llm_chat,
            prompt=prompt,
            verbose=False,
            memory=memory
        )
        
    def ask(self, last_msg):
        response = self.conversation({"question": last_msg})
        response['recomendations'] = json.loads(self.recommendation_chain.run(response['text']))
        return response