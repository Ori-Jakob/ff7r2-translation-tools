# ff7r2-translation-tools


## Introduction

These are a set of tools that I developed to aid in my attempt to translate the Japanese subtitles for FINAL FANTASY VII REBIRTH.

The project can be found on Nexus Mods: [More Faithful English Translation for Japanese Dub](https://www.nexusmods.com/finalfantasy7rebirth/mods/775)

Why does this project exist? Well, for one, the English localization does not remain faithful to what was said in the Japanese in a lot of cases. As someone who prefers to play the game in the Japanese Dub, there is a lot of mismatch between what is said in the Japanese, and what the English localized subtitles read. I also feel personally that there is a big difference between the characters personalities in the Japanese and English. Because of this, there are things that the characters just wouldn't say, or just are plain inaccurate to what the original writers (the Japanese) intended.



## Folder Structure

`./bin`: The binaries require to build the CSV files into the a mod

`./localizations`: Contains several other folders `JP` the Japanese subtitles, `ORG` the original English localization, and `US` the Japanese translation (the mod). There is also `Debug` inside of `US` which has debug subtitles to pinpoint Japanese speech which did not have subtitles for it

`./pretty_format`: This is the folder which you will mainly use. It contains CSV files for all the region that contain the **id, speaker, translation, and Japanese text** for each spoken line. ***This is the file that you will be working in***. If you wish to make any text changes do them in these file.

`./uassets`: This folder will contain the files for the subtitles of the game. ***These files are not provided in this repository and need to be extracted yourselves*** (see *How to Use* section) as they are the property of **SQUARE ENIX**. If you would like to build this mod yourself with this tool, then these files will be needed.



## How to Use

You will need [Python](https://python.org)

First, clone the repository with the method of your choice:

1.  Using the git command-line (requires git) `git clone %repository-link%`

2.  Click the green "Code" button dropdown, and select **Download .zip**

#### External Tools

These tools rely on external tools. In order to have my tools be able to automatically build the CSV files into a mod, you will need the following binaries:

1. [UnrealReZen](https://github.com/rm-NoobInCoding/UnrealReZen/releases): Download the release, and put all contents in the ***bin*** folder of ff7r2-translation-tools
   
2. [ff7r-text-tool](https://github.com/matyamod/ff7r-text-tool/releases): Download the release, and put **ff7r-text-tool.exe** into the ***bin*** folder of ff7r2-translation-tools. **GUI.exe, gui_definition.json, and LISENCE** are not needed.
   
3. [FModel](https://fmodel.app/): This is used to extract the uassets from the game. These are needed as **ff7r-text-tool** needs to be able to import the CSV into them before the building can take place

**NOTE**: I have not provided these files in this repository as they are property of their respective authors

#### Making Text Changes

As stated earlier, all text changes should be done on the CSV files contained within the `pretty_format` folder. 

**IMPORTAT: Keep in mind that the changes need to conform with how CSVs are parsed:**
1. `,` is a delimiter in CSV denoting the end of a column, if your text contains any `,`, you need to make sure the whole text is surround by double-quotes -> `"Currently, Midgar is facing an unprecedented crisis."

2. To *wrap* text in double-quotes, two sets are needed and the whole text needs to be wrapped in double-quotes -> `"Say ""Thanks for the food."""`

3. If you want to use *italics* then html tags are needed -> `<i>Time is running out.</i>`

**If you don't follow these, then things will either not build, or you will have major errors when text is rendered**

I will now explain how you know which subtitles are in which file. if you haven't figured it out each of the files has subtitles that are associated with the region (i.e. MIDGR -> Midgar, GRASE -> Grasslands, etc.). For flashbacks, the case is the same. For instance, in Cloud's reciting of his memories at the beginning of the game,  these memories take place in *Nibelheim*, so the dialog for that will be found in the corresponding file.

###### Guidelines for Text

There are several guidelines to follow for consistency's sake. **Make sure you have read the important note about CSV parsing:**

1. All quotes must be done in double quotes -> `"...the anti-Shinra group ""Avalanche"""`

2. Nested quotations are to use double-quotes than single-quotes -> `"""I won’t forgive unscientific terms like 'weird power'..."""`

3. Contractions that use an apostrophe are to use the unicode `’` and not `'` -> `It’s` not `It's`

4. If you are going to shorten words to add character "flare" use `‘` and not `'` -> them would become `‘em`  and not `'em`

5. If you are going to use an em dash, make sure to use the Unicode one — and not -

6. Any eclipses being used need to be connect on both sides to text (no white space) -> `"You...You said that?!"` **and not** `"You... You said that?!"`

#### Building the Mod

This requires the `External Tools to be installed`

1. Run `main.py`

2. Select `CSV Tools` in GUI

3. Select `Copy pretty format to original csv`

4. Select the file(s) that you modified and let them copy

5. When done, `Return`

6. Select `Import to .uassets`

7. Select `Release` version

8. Once done importing, it will ask if you would like to build into a mod. Select `Yes`

9. Enter a version number

10. Done! It should be in `./output` now


## Contributions

Contributions are allowed. There are two ways to help:

1. Create an issue and **state the exact text spoken, who said it and what region of the game you are in**
2. Fork the project, create a new branch with your changes, and submit a PR. I will review it and merge it into the repository.

**If you choose to fork, make sure you have read the `Making Text Changes` and `Guildlines for Text` thouroughly to understand what is required**
