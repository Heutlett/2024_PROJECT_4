from flask import Flask, request, jsonify
from google.cloud import language_v1

app = Flask(__name__)

def analyze_text(text):
    if isinstance(text, str) and len(text) > 5:
        client = language_v1.LanguageServiceClient()

        # The text to analyze
        document = language_v1.types.Document(
            content=text, type_=language_v1.types.Document.Type.PLAIN_TEXT
        )

        # Detects the sentiment of the text
        sentiment = client.analyze_sentiment(
            request={"document": document}
        ).document_sentiment

        return sentiment
    else:
        return 1

# Function to interpret sentiment score
def interpret_sentiment(score):
    if score < -0.25:
        return "Negative"
    elif score > 0.25:
        return "Positive"
    else:
        return "Neutral"

def generateAnswer(kind):
    responses = {
        'Negative': "I'm sorry to hear that. We will try to improve our service.",
        'Neutral': "I understand. Thank you for sharing.",
        'Positive': "That's wonderful to hear! We're glad you enjoyed your experience."
    }
    return responses.get(kind, "Unable to determine sentiment.")

@app.route('/feedback-chatbot', methods=['GET', 'OPTIONS'])
def feedback_chatbot():
    if request.method == 'OPTIONS':
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }
        return ('', 204, headers)
    
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
    }

    request_args = request.args
    path = request.path

    if path == "/feedback-chatbot" and request.method == 'GET':
        if request_args and "texto" in request_args:
            text = request_args["texto"]
            sentiment = analyze_text(text)

            if sentiment != 1:
                kind = interpret_sentiment(sentiment.score)

                answer = {
                    "status_code": 200,
                    "message": "OK",
                    "data": generateAnswer(kind)
                }
            
                return jsonify(answer), 200, headers
            else:
                answer = {
                    "status_code": 400,
                    "message": "Bad Request",
                    "data": "Texto debe tener al menos 5 caracteres"
                }
                return jsonify(answer), 400, headers
        else:
            answer = {
                "status_code": 400,
                "message": "Bad Request",
                "data": "Texto no encontrado"
            }
            return jsonify(answer), 400, headers
    else:
        answer = {
            "status_code": 404,
            "message": "Not Found",
            "data": "Ruta no encontrada"
        }
        return jsonify(answer), 404, headers

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001,debug=True)