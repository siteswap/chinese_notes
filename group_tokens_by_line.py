
from google.cloud import language_v1
from google.cloud import translate_v2 as translate

translate_client = translate.Client()
language_client = language_v1.LanguageServiceClient()


def all_tokens(doc):
    document = {"content": doc, "type_": language_v1.Document.Type.PLAIN_TEXT, "language": "zh"}
    encoding_type = language_v1.EncodingType.UTF8  # Available values: NONE, UTF8, UTF16, UTF32
    syntax_response = language_client.analyze_syntax(request={'document': document, 'encoding_type': encoding_type})
    segmented_doc = list(token.text.content for token in syntax_response.tokens)
    return segmented_doc

doc = "here is some 正文文章\r\r\rAnd some 问题\rdone"
tokens = all_tokens(doc)
# ['here', 'is', 'some', '正文', '文章', 'And', 'some', '问题', 'done']

lines = []
current_line = []

while len(doc) > 0:
    head_token = tokens[0]
    if doc.startswith(head_token):
        print("Adding:", head_token)
        current_line.append(head_token)
        doc = doc[len(head_token):]
        tokens.pop(0)
    elif doc.startswith('\r'):
        print("Creating new line")
        lines.append(current_line)
        current_line = []
        doc = doc[1:]
    else:
        doc = doc[1:]




# bytes(string, 'utf-8')
