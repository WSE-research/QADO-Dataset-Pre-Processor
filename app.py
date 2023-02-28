from flask import Flask, request, jsonify
from requests import get

app = Flask(__name__)


def process_cwq(data: str, language: str) -> list[dict[str, str]]:
    dataset = []

    for i, line in enumerate(data.split('\n')):
        if line == '':
            break

        question = line.split('IN: ')[-1].split('OUT: ')[0]
        query = line.split('OUT: ')[1]

        dataset.append({
            'question': question,
            'query': query,
            'lang': language,
            'id': i
        })

    return dataset


@app.post('/process/compositional_wikidata')
def handle_cwq_processing():
    payload = request.get_json()

    if not ('fetch_url' in payload and 'language' in payload):
        return 'Missing parameter "fetch_url" or "language"', 400

    base_dataset_response = get(payload['fetch_url'])
    language = payload['language']

    if not base_dataset_response.ok:
        return f'Fetching dataset failed: "{base_dataset_response.text}"'

    dataset = base_dataset_response.text

    return jsonify(process_cwq(dataset, language))


if __name__ == '__main__':
    app.run()
