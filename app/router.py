from semantic_router import Route
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.index import LocalIndex
from semantic_router.routers import SemanticRouter

encoder = HuggingFaceEncoder(
    name = "sentence-transformers/all-MiniLM-L6-v2"
)

faq = Route(
    name="faq",
    utterances=[
        "What is the return policy?",
        "How can I return a product?",
        "Can I return an item?",
        "I want to return my order",

        "How can I track my order?",
        "Where is my order?",
        "Can I check my order status?",
        "How do I track my package?",

        "What payment methods do you accept?",
        "How can I pay for my order?",
        "Do you accept credit cards?",
        "Can I pay using cash on delivery?",

        "How long does a refund take?",
        "When will I receive my refund?",
        "How long does it take to get my money back?",

        "Do you offer international shipping?",
        "Can you ship internationally?",
        "Do you deliver outside the country?",

        "I received a damaged product",
        "My product arrived damaged",
        "I received a defective item",
        "What should I do if my product is defective?"
    ]
)

small_talk = Route(
    name="small_talk",
    utterances=[
        "How are you?",
        "How are you doing?",
        "How are you today?",
        "How have you been?",
        "How is it going?",
        "How's it going?",
        "Are you doing well?",
        "How are things?",
        "What are you up to?",

        "What is your name?",
        "What's your name?",
        "Who are you?",
        "Are you a robot?",
        "Are you an AI?",
        "What are you?",
        "What do you do?",
        "What can you do?"
    ]
)


sql = Route(
    name='sql',
    utterances=[
        'What shoes do you have in stock?',
        'Which running shoes are available?',
        'Show me all Nike shoes',
        'Do you have Adidas shoes?',
        'What is the price of the Nike Air Max?',
        'How much do these shoes cost?',
        'Which shoes are under $100?',
        'Show me shoes between $50 and $100',
        'Do you have size 9 available?',
        'Which shoes are available in size 10?',
        'Do you have black shoes in stock?',
        'Show me all black running shoes',
        'Which shoes are available in white?',
        'Which sneakers have the highest price?',
        'What is the cheapest pair of shoes?',
        'How many pairs of Nike shoes are in stock?',
        'Which shoes have the most inventory?',
        'Are there any shoes on sale?',
        'Show me discounted shoes',
        'Which running shoes are available under $120?',
        'Do you have sneakers for men?',
        'Show me women’s shoes',
        'What men’s sneakers do you have?',
        'Which shoes are available in size 8 and black?',
        'Show me Nike shoes under $150',
        'How many shoes are currently in stock?',
    ]
)

router = SemanticRouter(
    routes=[faq,sql,small_talk],
    encoder=encoder,
    auto_sync='local',
    index=LocalIndex()
)

if __name__ == '__main__':
    print(router("What is your name?").name)
    print(router("What shoes do you have in stock?").name)
    print(router("What is the return policy?").name)