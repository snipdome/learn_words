# learn_words

## Description
`learn_words` is a command-line tool designed to help you learn new words in any language. By using a vocabulary list, as the ones provided by wortschatz.uni-leipzig.de, you can practice and memorize new words in an interactive way.

The program is written in Python. It saves the words to which you have been exposed, given that you have provided any input, for example its translation or any other information as type of word and gender.

If the downloaded vocabulary list has a "sentences" file, the program will also provide you with sentences in which the word is used.

## Usage
1. Download the repository:
    ```shell
    git clone git@github.com:snipdome/learn_words.git
    ```

2. Download the vocabulary list from [ wortschatz.uni-leipzig.de:](https://wortschatz.uni-leipzig.de/en/download)
    Unzip the file and place it in the `language_pack` folder.

3. Modify the `learn_mylanguage.py` file to specify the language_pack folder. Even better, a copy of the `learn_mylanguage.py` file can be created and modified to specify the language_pack folder.

2. Run the `learn_mylanguage.py` command

3. Follow the on-screen instructions. The Enter key can be used to exit from loops. By pressing first Esc and then Enter, the program will go back to the outer loops.

## Contributing
Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- [wortschatz.uni-leipzig.de](https://wortschatz.uni-leipzig.de/en/download) for providing vocabulary lists.

