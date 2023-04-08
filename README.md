# Github Readme file for Hervis Crawler

This is a Python script that crawls the [Hervis website](https://www.hervis.ro/) to extract metadata from the website's pages. 

The script uses the following packages:

- `BeautifulSoup` for parsing HTML content
- `pandas` for creating and manipulating dataframes
- `pathlib` for checking and creating files
- `tqdm` for progress bars
- `playwright` for controlling Chromium-based browsers and extracting dynamic content
- `re` for regular expressions

## Getting Started

### Installation

To install the required packages, run the following command in your terminal:

```sh
pip install -r requirements.txt
```

### Usage

The script is run from the command line and takes a CSV file with a list of URLs as input. For example:

```sh
python main.py url_list.csv
```

The script crawls each URL in the list and extracts the following metadata:

- Meta Title
- H1
- Tip Pagina (Page type)
- Cuvinte Descriere (Description word count)
- Linkuri Interne Descriere (Description internal links count)
- Exista FAQ (FAQ exists)
- Numar Produse (Product count)
- URL
- URL Cannonical (Canonical URL)
- breadcrumbs (Breadcrumb text)
- Facets (Facets)

The extracted data is saved to a tab-separated CSV file named `hervis/hervis.csv`. If the file already exists, the data is appended to the end of the file.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
