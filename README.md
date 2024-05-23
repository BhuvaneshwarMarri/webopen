# WebOpen

WebOpen is a python command to open urls through command line.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install webopen.

```bash
pip install webopen
```

## Usage

```bash
webopen -link link_name
```
<link_name>:The name or identifier of the link you want to open.

```bash
webopen add
```
This command prompts user for website name,username in that website, and password used in that website and store it in local sqllite database.

```bash
webopen search
```
This command prompts user for a website, if the website is in database, it prints out the credentials used in the website.

## Example

```bash
webopen -link github.com
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)