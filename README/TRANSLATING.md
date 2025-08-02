# Guide for Localizing Porn Fetch into Your Language
Thank you for your interest in translating Porn Fetch! Your contribution to localizing the application is highly valued.


# The Easy Way
The easy way of translating Porn Fetch directly from your browser from anywhere is by using
crowdin. 

Here's the Project URL ->: https://de.crowdin.com/project/pornfetch/

You need to make a free account on crowdin (takes 1 minute).
For reference, watch this very short and easy tutorial how to do it.

Link: https://youtu.be/0N-kLGT1nJQ

> [!IMPORTANT]
> You DO NOT have to translate these big weird HTML like texts.


# The Hard way
The hard way is easier if you are tech savy and I would recommend it if you know what
I am talking about ;) 

## Getting Started with Qt Linguist

Qt Linguist is the recommended tool for translation. You can find installation instructions online – it's straightforward to set up.

## Setting Up Your Environment

1. **Fork the Repository**: It's strongly advised to fork the repository for easier contribution. If you're familiar with Pull Requests, please use them for submission.
   - Clone the repository using: `$ git clone https://github.com/EchterAlsFake/Porn_Fetch`
   - Alternatively, fork it and use your fork for later Pull Requests.
2. **Install Qt Linguist**: Look up online guides for installing Qt Linguist. It's a simple process.

## Translation Process

1. **Open Qt Linguist**: Launch the program, navigate to "File" > "Open", and locate the `en.ts` file in `Porn_Fetch/src/translations/`.
2. **Configure Language Settings**: In the dialog, set 'English' as the source language and 'United States' as the region. Then, choose your target language and region.
3. **Translate Strings**: The application contains approximately 110 strings. Select each string and provide your translation in the box below.
4. **Save Your Work**: After translating, save your progress with `CTRL + S`.

**Note**: You don’t need to worry about converting the translations into `.qm` format or embedding them into the resource file. I will handle that part. 

## Submitting Your Translations

You can submit the `.ts` file through:
- A Pull Request on GitHub.
- Opening an Issue on the repository.
- Discord: echteralsfake

**Tips for Translators**:
- If unsure about a translation, feel free to skip it.
- The use of formal or informal language is at your discretion.

## Video Tutorial

For a visual guide on the translation process, please watch the tutorial video I’ve created.

- [Translation Process Video](https://youtu.be/X2h1SG-xLOg)
