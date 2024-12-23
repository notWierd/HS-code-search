# # import google.generativeai as genai

# # genai.configure(api_key="AIzaSyD-s-ZXFiLtbcFP-s8sGSNfAy1JfZJ6GIQ")
# # model = genai.GenerativeModel("gemini-1.5-flash")
# # query = "stainless steel kitchen knife"
# # response = model.generate_content("Give me WCO HS codes for" + query)
# # print(response.text)



# # import google.generativeai as genai
# # import typing_extensions as typing

# # genai.configure(api_key="AIzaSyD-s-ZXFiLtbcFP-s8sGSNfAy1JfZJ6GIQ")

# # class HScodes(typing.TypedDict):
# #     hs_codes: str
# #     descriptions: list[str]

# # query = "stainless steel knife"
# # model = genai.GenerativeModel("gemini-1.5-pro-latest")
# # result = model.generate_content(
# #     "List a few HS codes for"+ query,
# #     generation_config=genai.GenerationConfig(
# #         response_mime_type="application/json", response_schema=list[HScodes]
# #     ),
# # )
# # print(result)



# import json
# import google.generativeai as genai
# import typing_extensions as typing

# # Configure the generative AI API
# genai.configure(api_key="AIzaSyD-s-ZXFiLtbcFP-s8sGSNfAy1JfZJ6GIQ")

# # Define a TypedDict for the expected output
# class HScodes(typing.TypedDict):
#     hs_codes: str
#     descriptions: list[str]

# # Query for the HS codes
# query = "commercial car"
# model = genai.GenerativeModel("gemini-1.5-pro-latest")
# result = model.generate_content(
#     "List a few HS codes for " + query,
#     generation_config=genai.GenerationConfig(
#         response_mime_type="application/json", 
#         response_schema=list[HScodes]
#     ),
# )

# # Extract and parse the JSON from the response
# try:
#     # Access the first candidate's content
#     candidates = result.candidates
#     if candidates:
#         raw_json = candidates[0].content.parts[0].text
#         # Parse the JSON string into a Python object
#         structured_data = json.loads(raw_json)
        
#         # Display the structured HS codes
#         print("\nStructured HS Codes and Descriptions:\n")
#         for item in structured_data:
#             print(f"HS Codes: {item['hs_codes']}")
#             print("Descriptions:")
#             for description in item['descriptions']:
#                 print(f"  - {description}")
#             print()
#     else:
#         print("No candidates found in the response.")

# except AttributeError as e:
#     print(f"AttributeError: {e}")
# except KeyError as e:
#     print(f"KeyError: Missing expected key {e}")
# except json.JSONDecodeError as e:
#     print(f"JSONDecodeError: {e}")


# from flask import Flask, request, jsonify, render_template
# import json
# import google.generativeai as genai
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# @app.route('/')
# def home():
#     return render_template('index.html')  # Ensure `index.html` is in the correct templates folder


# # Configure the generative AI API
# genai.configure(api_key="AIzaSyD-s-ZXFiLtbcFP-s8sGSNfAy1JfZJ6GIQ")

# @app.route('/get_hs_codes', methods=['POST'])
# def get_hs_codes():
#     data = request.json
#     query = data.get('query', '')

#     try:
#         model = genai.GenerativeModel("gemini-1.5-pro-latest")
#         result = model.generate_content(
#             "Provide HS codes for products related to [query] in a JSON format.",
#             generation_config=genai.GenerationConfig(
#                 response_mime_type="application/json"
#             ),
#         )
#         candidates = result.candidates
#         if candidates:
#             raw_json = candidates[0].content.parts[0].text
#             structured_data = json.loads(raw_json)
#             return jsonify({"success": True, "data": structured_data})
#         else:
#             return jsonify({"success": False, "error": "No candidates found"})
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)})


# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify, render_template
import json
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')  # Ensure `index.html` is in the correct templates folder


# Configure the generative AI API
genai.configure(api_key="AIzaSyD-s-ZXFiLtbcFP-s8sGSNfAy1JfZJ6GIQ")

@app.route('/get_hs_codes', methods=['POST'])
def get_hs_codes():
    data = request.json
    query = data.get('query', '')  # Get the query from the request

    try:
        # Ensure the actual query is used in the prompt
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        result = model.generate_content(
            f"Provide HS codes for products related to {query} in a JSON format.",  # Inject query dynamically
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            ),
        )
        candidates = result.candidates
        if candidates:
            raw_json = candidates[0].content.parts[0].text
            structured_data = json.loads(raw_json)
            return jsonify({"success": True, "data": structured_data})
        else:
            return jsonify({"success": False, "error": "No candidates found"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})



if __name__ == '__main__':
    app.run(debug=True)
