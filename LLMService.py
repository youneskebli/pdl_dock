# structureService.py
import openai
import json
from vectorStore import llm_differentiation as llm_diff_vectorstore
# from vectorStore import llm_differentiation as llm_diff_vectorstore

def llm_differentiation(doc):
    openai.api_key = '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'

    print(doc)

    # Call the llm_differentiation function from VectorStore.py
    category = llm_diff_vectorstore(doc)

    message = {
        'role': 'system',
        'content': f"""Given the context provided in this PaddleOCR Processed document:

        {doc}

        The document belongs to the category: {category}

        Now, extract the patient's first name, last name, age, and the date from the document and return the data as a JavaScript object called results, inside of it should be 2 attributes one called category which will be a string mentioning the category and second should be an array called cells, in that array there should be objects with the attributes: title, value, normalRange and unit.
        The object should look like this:
        results: {{
            "patient": {{
                "firstName": "Extracted first name",
                "lastName": "Extracted last name",
                "age": "Extracted age",
            }},
            "date": "Extracted date",
            "category": "{category}",
            "cells": [
                {{
                    "title": "Glucose",
                    "value": "9",
                    "normalRange": "8 - 11",
                    "unit": "mg"
                }}
            ]
        }}
        Remember this is only an example so make sure to modify it based on the provided document as long as it displays results in the same manner.
        Use only the measurable data provided in the document and only the test results and their respective values, avoid personal information such as names and phone numbers. 
        The cells array is an array of objects containing those tests results, meaning there will be as many objects in it as there are test results.
        If the context isn't enough respond with: The context provided in the document isn't enough for an accurate type determination"""
    }

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[message]
    )


    generated_text = response['choices'][0]['message']['content']

    return generated_text
