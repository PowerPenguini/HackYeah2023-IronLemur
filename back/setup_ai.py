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
        
        template = """Extract from this text up to 3 recommedations of universities and give names of them in json list format without white spaces. Use exact names which are used in context.

        text:
        {text}
        """
        prompt_template = PromptTemplate(input_variables=["text"], template=template)
        self.recommendation_chain = LLMChain(llm=llm_recommendation, prompt=prompt_template)

        # Prompt 
        prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(
                    '''Your name is Agama, You are a truthful career coach and you have to help me choose university based only on data in provided context. Every response should end with 3 recommendations of universities. You are allowed only to talk about universities and use data from context. If You do not know, just say "Nie wiem jak odpowiedzieć na to pytanie". Be concise. Answear in Polish.
                    context###
Uniwersytet Warszawski
W Warszawie
Wydziały: Prawo, Matematyka, Informatyka, Nauki Humanistyczne
Kierunki: Prawo, Informatyka, Filozofia, Psychologia
Poziomy: licencjackie, magisterskie, doktoranckie
Przedmioty na maturze: różne; dla informatyki - matematyka, dla prawa - język polski i historia
Wiele kierunków, międzynarodowe badania

Uniwersytet Jagielloński
W Krakowie
Wydziały: Medycyna, Prawo, Filozofia, Nauki Ścisłe
Kierunki: Medycyna, Prawo, Filozofia, Matematyka
Poziomy: licencjackie, magisterskie, doktoranckie
Przedmioty na maturze: różne; dla medycyny - chemia, biologia, dla prawa - język polski i historia
Topowi wykładowcy, Międzynarodowe badania

Politechnika Warszawska
W Warszawie
Wydziały: Elektroniki, Inżynierii Lądowej, Mechaniki
Kierunki: Inżynieria Lądowa, Elektronika, Automatyka i Robotyka
Poziomy: inżynierskie, magisterskie
Przedmioty na maturze: matematyka, fizyka
Współpraca z przemysłem, Innowacje

Akademia Górniczo-Hutnicza
W Krakowie
Wydziały: Geologia, Informatyka, Mechanika
Kierunki: Geologia, Informatyka, Mechanika i Budowa Maszyn
Poziomy: inżynierskie, magisterskie
Przedmioty na maturze: matematyka, fizyka
Innowacje, Współpraca z przemysłem

Uniwersytet Wrocławski
We Wrocławiu
Wydziały: Prawo, Biotechnologia, Nauki Humanistyczne
Kierunki: Prawo, Biotechnologia, Filologia Angielska
Poziomy: licencjackie, magisterskie, doktoranckie
Przedmioty na maturze: różne; dla biotechnologii - chemia, biologia
Topowi wykładowcy

Uniwersytet Gdański
W Gdańsku
Wydziały: Oceanografia, Prawo, Filologia
Kierunki: Oceanografia, Prawo, Filologia Angielska
Poziomy: licencjackie, magisterskie
Przedmioty na maturze: różne; dla oceanografii - biologia, chemia
Wiele kierunków, Innowacje

Uniwersytet Poznański
W Poznaniu
Wydziały: Ekonomia, Nauki Humanistyczne, Prawo
Kierunki: Ekonomia, Socjologia, Prawo
Poziomy: licencjackie, magisterskie
Przedmioty na maturze: różne; dla ekonomii - matematyka
Wiele kierunków

Politechnika Wrocławska
We Wrocławiu
Wydziały: Architektura, Elektronika, Inżynieria Środowiska
Kierunki: Architektura, Elektronika, Inżynieria Środowiska
Poziomy: inżynierskie, magisterskie
Przedmioty na maturze: matematyka, fizyka


Uniwersytet Łódzki
W Łodzi
Wydziały: Filologia, Prawo, Nauki Humanistyczne
Kierunki: Filologia Polska, Prawo, Historia
Poziomy: licencjackie, magisterskie
Przedmioty na maturze: różne; dla filologii - język obcy
Wiele kierunków, Międzynarodowe badania

Katolicki Uniwersytet Lubelski Jana Pawła II
W Lublinie
Wydziały: Teologia, Prawo, Filozofia
Kierunki: Teologia, Prawo, Filozofia
Poziomy: licencjackie, magisterskie
Przedmioty na maturze: różne; dla teologii - wiedza religijna, dla prawa - język polski i historia
Długa historia

Punkty ECTS (European Credit Transfer and Accumulation System) to system kredytów stworzony w celu ułatwienia międzynarodowej wymiany studentów i uznawania ich osiągnięć edukacyjnych w Europie. Punkty ECTS są powszechnie używane w krajach europejskich, zwłaszcza w ramach programu Erasmus i innych programów wymiany studenckiej.


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
        self.json_data = self.load_json_db()
        
    def ask(self, last_msg):
        response = self.conversation({"question": last_msg})
        recommendations = json.loads(self.recommendation_chain.run(response['text']))
        complete_dataset = []
        for r in recommendations:
            try:
                uni = [uni for uni in self.json_data if uni.get("name") == r][0]
                complete_dataset.append(uni)
            except IndexError:
                continue
            

        response["recommendations"] = complete_dataset
        return response
    
    def load_json_db(self):
        with open('data.json', 'r') as file:
            data = file.read()
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            print(f"Błąd parsowania JSON: {e}")