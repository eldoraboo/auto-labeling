<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/eldoraboo/auto-labeling">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Auto Labeling Pipeline</h3>

  <p align="center">
    Built with Doccano, spaCy & FastAPI
    <br />
    <a href="https://github.com/eldoraboo/auto-labeling"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/eldoraboo/auto-labeling">View Demo</a>
    ·
    <a href="https://github.com/eldoraboo/auto-labeling/issues">Report Bug</a>
    ·
    <a href="https://github.com/eldoraboo/auto-labeling/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#desktop_computer-about-the-project">About The Project</a>
      <ul>
        <li><a href="#hammer_and_wrench-built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#computer-getting-started">Getting Started</a>
      <ul>
        <li><a href="#gear-set-up-a-virtual-environment">Set Up A Virtual Environment</a></li>
        <li><a href="#book-requirements">Requirements</a></li>
        <li><a href="#seal-start-doccano-server-with-fastapi">Start Doccano Server With FastAPI</a></li>
      </ul>
    </li>
    <li>
      <a href="#robot-auto-labeling-setup">Auto Labeling Setup</a>
      <ul>
        <li><a href="#memo-named-entity-recognition">Named Entity Recognition</a></li>
        <li><a href="#file_folder-text-classification">Text Classification</a></li>
      </ul>
    </li>
    <li>
      <a href="#syringe-few-shot-learning-models">Auto Labeling Setup</a>
      <ul>
        <li><a href="#blue_book-concise-concepts-ner">Concise Concepts (NER)</a></li>
        <li><a href="#dancer-classy-classification-tc">Classy Classification (TC)</a></li>
        <li><a href="#dog-petipet-tc-in-progress-construction"> PET/iPET (TC) [In Progress 🚧]</a></li>
        <li><a href="#lotus_position-taichi-tc-in-progress-construction">TaiChi (TC) [In Progress 🚧]</a></li>
      </ul>
    </li>
    <li><a href="#car-roadmap">Roadmap</a></li>
    <li><a href="#busts_in_silhouette-contributing">Contributing</a></li>
    <li><a href="#phone-contact">Contact</a></li>
    <li><a href="#toolbox-acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## :desktop_computer: About The Project

[![doccano-screenshot]](http://doccano.herokuapp.com/)

doccano can perform different types of labeling tasks with many data formats and spaCy is an industrial-strength NLP tool. Utilising these two, we are able to built an auto labeling pipeline for Named Entity Recognition as well as Test Classification.

![GitHub](https://img.shields.io/github/license/eldoraboo/auto-labeling?style=for-the-badge) ![GitHub issues](https://img.shields.io/github/issues/eldoraboo/auto-labeling?style=for-the-badge) ![GitHub pull requests](https://img.shields.io/github/issues-pr/eldoraboo/auto-labeling?style=for-the-badge) ![GitHub last commit](https://img.shields.io/github/last-commit/eldoraboo/auto-labeling?style=for-the-badge) ![Maintenance](https://img.shields.io/maintenance/yes/2022?style=for-the-badge)


<p align="right">(<a href="#top">back to top</a>)</p>



### 	:hammer_and_wrench: Built With

* [![doccano]][doccano-url]
* [![spacy]][spacy-url]
* [![fastapi]][fastapi-url]
* [![gcp]][gcp-url]
* [![python]][python-url]

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## :computer: Getting Started

This is an example of how you can set up your project on GCP.

### :gear: Set Up A Virtual Environment

Set up a new conda environment: `mydoccano`
```sh
# Python 3.9 works best for this auto labeling project
conda create -n mydoccano python=3.9

conda activate mydoccano

conda deactivate
```

### :book: Requirements

* Download all packages in requirements.txt 
```sh
pip3 install -r requirements.txt
```

* Download spacy libraries
```sh
python3 -m spacy download en_core_web_sm
python3 -m spacy download en_core_web_md
python3 -m spacy download en_core_web_lg
```

### :seal: Start Doccano Server With FastAPI

1. Initialize doccano
   ```sh
   doccano init
   ```
2. Create superuser (admin)
   ```sh
   doccano createuser --username {USERNAME} --password {PASSWORD}
   ```
3. Run doccano on port 8000
   ```sh
   doccano webserver --port 8000
   ```
4. Start task queue
   ```sh
   # In another terminal, run the following command:
   doccano task
   ```
5. Deploy API on port 8888
   ```sh
   # Also in another terminal, run the following command:
   python3 -m uvicorn ner:app --reload --port 8888 --host {INTERNAL_IP_ADDRESS}
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- AUTO LABELING SETUP -->
## :robot: Auto Labeling Setup
Ensure the API returns the request in doccano's format before setting up Auto Labeling
```sh
Sequence Labeling/Named Entity Recognition
[{ "label": "Cat", "start_offset": 0, "end_offset": 5 }, ...]

Text Classification 
[{ "label": "Cat" }, ...]

Sequence to Sequence
[{ "text": "Cat" }, ...]
```

### :memo: Named Entity Recognition 
##### 1. Select a Template
* Task Name: `SequenceLabeling`
* Config Template: `Custom REST Request`

##### 2. Set Parameters
* URL: `http://{EXTERNAL_IP_ADDRESS}:8888/ner_spacy_trf`
* Method: `POST`
* Params: `Key: text, Value: {{ text }}`

##### 3. Set a Template
* Mapping Template:
  ```sh
  [
      {% for entity in input %}
          {
              "start_offset": {{ entity.start_offset }},
              "end_offset": {{ entity.end_offset}},
              "label": "{{ entity.label }}"
          }{% if not loop.last %},{% endif %}
      {% endfor %}
  ]
  ```

##### 4. Set Mappings
* Label Mapping: `{}`

### :file_folder: Text Classification 
##### 1. Select a Template
* Task Name: `DocumentClassification`
* Config Template: `Custom REST Request`

##### 2. Set Parameters
* URL: `http://{EXTERNAL_IP_ADDRESS}:8888/textcat_fewshot`
* Method: `POST`
* Params: `Key: text, Value: {{ text }}`

##### 3. Set a Template
* Mapping Template:
  ```sh
  [
      {% for entity in input %}
          {
              "label": "{{ entity.label }}"
          }{% if not loop.last %},{% endif %}
      {% endfor %}
  ]
  ```

##### 4. Set Mappings
* Label Mapping: `{}`

_For more examples, please refer to the [Auto Labeling Settings](https://doccano.github.io/doccano/advanced/auto_labelling_config/)_

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- Few-Shot Learning Models -->
## :syringe: Few-Shot Learning Models

### :blue_book: Concise Concepts (NER)
```python
# Import packages and libraries
import spacy 
import spacy_transformers
from spacy import displacy
import concise_concepts
import gensim.downloader as api
import json
import csv

# Load training data
with open('train.json') as json_file:
    data = json.load(json_file)

# Load en_core_web_trf pre-trained model
# & fasttext-wiki-news-subwords-300 word embeddings
nlp = spacy.load("en_core_web_trf")
model_path = "fasttext-wiki-news-subwords-300"
nlp.add_pipe("concise_concepts", config={
             "data": data, "ent_score": True
             ,"model_path": model_path
             })

# Open CSV file and read lines into list
with open('test.csv', newline='') as f:
    reader = csv.reader(f)
    texts = [row[0] for row in reader]

# Parse testing data into few-shot model
for text in texts:
    doc = nlp(text)
    ents = doc.ents
    for ent in ents:
        new_label = f"{ent.label_}"
        ent.label_ = new_label
    doc.ents = ents

    displacy.render(doc, style="ent")
```
![concise-screenshot]

### :dancer: Classy Classification (TC)
```python
# Import packages and libraries
import spacy
import classy_classification
import csv
import pandas as pd

# Load training data
df = pd.read_csv("train.csv")
data = {}
sample_size = 10
candidate_labels = df['{CLASS_COLUMN}'].unique().tolist()
for label in candidate_labels:
    candidate_values = df.query(f"`{CLASS_COLUMN}` == '{label}'").sample(n=sample_size)['{TEXT_COLUMN}'].values.tolist()
    data[label] = candidate_values

# Load blank spaCy model
# & sentence-transformers/all-mpnet-base-v2
nlp = spacy.blank("en")
nlp.add_pipe(
    "text_categorizer",
    config={
        "data": data,
        "model": "sentence-transformers/all-mpnet-base-v2",
        "device": "gpu"
    }
)

# Open CSV file and read lines into dict
reader = csv.DictReader(open('test.csv'))

# Parse testing data into few-shot model
for row in reader:
    doc = row['{TEXT_COLUMN}']
    categories = nlp(doc)._.cats
    max_category = max(categories, key=categories.get)
    print(f"\033[97m{doc}")
    print(f"\033[94mClass: \033[92m{max_category}")
    print()
```
![classy-screenshot]

### :dog: PET/iPET (TC) [In Progress :construction:]
* Use AG's News format
* Numbers in `train.csv` and `test.csv` are mapped to `classes.txt`

### :lotus_position: TaiChi (TC) [In Progress :construction:]
* Find a way to create Out-Of-Sample (OOS) data
* Must have 4 files, `ood_test.csv`, `ood_train.csv`, `test.csv` and `train.csv`

<p align="right">(<a href="#top">back to top</a>)</p>




<!-- ROADMAP -->
## :car: Roadmap

- [x] Create VM instance with GPU
- [x] Set Up Doccano Interface
- [x] Set Up FastAPI
- [x] Named Entity Recognition
    - [x] concise-concepts
- [ ] Text Classification
    - [x] classy-classification
    - [ ] pet
    - [ ] TaiChi

See the [open issues](https://github.com/eldoraboo/auto-labeling/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## :busts_in_silhouette: Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit your Changes (`git commit -m 'Add some NewFeature'`)
4. Push to the Branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## :phone: Contact

[![gmail]][gmail-url] [![linkedin]][linkedin-url] [![website]][website-url]
Project Link: [https://github.com/eldoraboo/auto-labeling](https://github.com/eldoraboo/auto-labeling) 

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGEMENTS -->
## :toolbox: Acknowledgements

* [doccano/doccano](https://github.com/doccano/doccano/)
* [spaCy](https://spacy.io/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Create a VM with attached GPUs](https://cloud.google.com/compute/docs/gpus/create-vm-with-gpus)
* [Pandora-Intelligence/concise-concepts](https://github.com/pandora-intelligence/concise-concepts)
* [Pandora-Intelligence/classy-classification](https://github.com/Pandora-Intelligence/classy-classification)
* [timoschick/pet](https://github.com/timoschick/pet)
* [salesforce/TaiChi](https://github.com/salesforce/TaiChi)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[doccano-screenshot]: images/doccano_1.png
[concise-screenshot]: images/concise_1.png
[classy-screenshot]: images/classy_1.png
[doccano]: https://img.shields.io/badge/Doccano-6376ab?style=for-the-badge&logo=doccano&logoColor=white
[doccano-url]: http://doccano.herokuapp.com/
[spacy]: https://img.shields.io/badge/spacy-09a3d5?style=for-the-badge&logo=spacy&logoColor=white
[spacy-url]: https://spacy.io/
[fastapi]: https://img.shields.io/badge/fastapi-019486?style=for-the-badge&logo=fastapi&logoColor=white
[fastapi-url]: https://fastapi.tiangolo.com/
[gcp]: https://img.shields.io/badge/Google_Cloud_Platform-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white
[gcp-url]: https://cloud.google.com/gcp
[python]: https://img.shields.io/badge/Python-3.9-14354C?style=for-the-badge&logo=python&logoColor=white
[python-url]: https://www.python.org/downloads/release/python-390/
[linkedin]: https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white
[linkedin-url]: https://www.linkedin.com/in/eldoraboo/
[gmail]: https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white
[gmail-url]: mailto:eldoraboo.mby@gmail.com
[website]: https://img.shields.io/badge/website-FF69B4?style=for-the-badge&logo=About.me&logoColor=white
[website-url]: https://eldoraboo.github.io/