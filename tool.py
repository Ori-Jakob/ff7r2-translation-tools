import csv,os,subprocess,time
from gui import render

def read_csv(filename, read_jap=False, is_pretty=False) -> dict:
    temp = dict()
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if not is_pretty:
                key = "name" if row[1] == "ACTOR" else "text"
                if len(temp.get(row[0], [])) == 0:
                    temp[row[0]] = {key: row[2]}
                else:
                    temp[row[0]][key] = row[2]
            else:
                temp[row[0]] = {"id": row[0], "name": row[1], "text": row[2]}

    if(read_jap and not is_pretty):
        filename = filename.split("\\")[-1].split(".")[0] + "_jp.csv"
        with open(os.path.join('localizations', 'JP', filename), 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] != "ACTOR":
                    temp[row[0]]["text_jp"] = row[2]

        temp = dict(sorted(temp.items()))



    return temp

def read_orig_csv(filepath):
    temp = dict()
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return [row for row in reader]


def pretty_format(items: dict, filename: str):
    no_text = filename.split("-")[1][:6]
    if not os.path.exists("pretty_format"):
        os.mkdir("pretty_format")
    
    formatted = [[k, v.get('name', 'NPC'), v['text'] if v['text'] != "" else f"{no_text}__{i}",v['text_jp'] if v['text_jp'] != "" else f"{no_text}__{i}"] for i,(k,v) in enumerate(items.items())][:-2]

    with open(os.path.join("pretty_format", filename.split(".")[0] + "_pretty.csv"), "w", encoding='utf-8') as file:
        writer = csv.writer(file, lineterminator="\n")
        file.write("id,name,text,text_jp\n")
        writer.writerows(formatted)

    return

def copy_pretty_to_original(filename: str, debug=False):
    orig_name = os.path.join('localizations', 'US', "_".join(filename.split("_")[:2])+".csv")
    pretty_name = os.path.join('pretty_format', filename)

    print(f"Copying '{pretty_name}' to '{orig_name}'")
    original = read_orig_csv(orig_name)
    pretty = read_csv(pretty_name, is_pretty=True)

    for x in range(len(original)):
        if pretty.get(original[x][0], "") != "":
            if original[x][1] == "ACTOR":
                original[x][2] = pretty[original[x][0]]["name"]
            else:
                if debug:
                    original[x][2] = pretty[original[x][0]]["text"]
                else:
                    if pretty[original[x][0]]["text"].count("_") > 0:
                        original[x][2] = ""
                    else:
                        original[x][2] = pretty[original[x][0]]["text"]

    save_original(original, orig_name.split("\\")[-1], debug)


def save_original(items: list, filename: str, debug=False):
    path = os.path.join('localizations', 'US') if not debug else os.path.join('localizations', 'US', "Debug")
    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path, filename), 'w', encoding='utf-8') as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerows(items)


def fix_header(path):
    header = bytes([0x8C, 0x06, 0x00, 0x30, 0xDE, 0x88, 0x30, 0xDC, 0x0C, 0xF0])
    with open(path, 'r+b') as fs:
        fs.write(header)

def make_pak(debug=False):
    version = input("Enter version\n>> ")
    name = f"Faithful_ENG_Translation_v{version}_{"Debug_" if debug else ""}P.utoc"
    location = os.path.join("output", "Debug" if debug else "Release")
    command = [
        os.path.join('bin', 'UnrealReZen.exe'),
        "--content-path", location,
        "--compression-format", "Zlib",
        "--engine-version", "GAME_UE4_26",
        "--game-dir", r"D:\Steam\steamapps\common\FINAL FANTASY VII REBIRTH\End\Content\Paks",
        "--output-path", os.path.join("output", name)
    ]
    print(f"Packing mod as {name}.")
    result = subprocess.run(command, capture_output=True, text=True)

    if result.stderr:
        print("There was an error packaging mod:")
        print(result.stderr)
        return
    
    print("Fixing header...")
    fix_header(os.path.join("output", ".".join(name.split(".")[:-1])+".ucas"))
    


def import_csv_usasset(files: list, debug=False):
    output = os.path.join('output', 'Debug' if debug else 'Release', 'End', 'Content', 'Text', 'US')
    if not os.path.exists(output):
        os.makedirs(output)

    for x in files:
        print(f"Importing {x} to {x.split('.')[0] + '.uasset'}")
        command = [
        os.path.join('bin', 'ff7r-text-tool.exe'),
        os.path.join("localizations", "US", "Debug", x) if debug else os.path.join("localizations", "US", x),
        os.path.join("uassets", x.split(".")[0] + '.uasset'),
        "-o", output,
        "-f", "csv",
        "--mode", "import"
        ]
        subprocess.run(command, capture_output=True, text=True)

    print("Done!")
    time.sleep(1)

    options = ["Yes", "No"]

    match(render.start(options, "Package into mod?")):
        case 0:
            make_pak(debug)
        case 1:
            return



def do_pretty_format():
    return_option = "Return"
    render.reset()
    while(True):
        items = os.listdir(os.path.join('localizations', 'US')) + [return_option]
        if not len(items) > 1:
            print("No files are here to format!")
            time.sleep(1.5)
            return
        
        file = items[render.start(items , 'Select a file to pretty format:', reset=False)]
        if file == return_option: return
        temp = read_csv(os.path.join('localizations', 'US', file), read_jap=True)
        print(f"Pretty formatting {file}...")
        pretty_format(temp, file)

        print("Done!")
        time.sleep(1)

def do_pretty_copy():

    return_option = "Return"
    render.reset()
    while(True):

        items = os.listdir(os.path.join('.', 'pretty_format')) + [return_option]
        if not len(items) > 1:
            print("No files are here to copy!")
            time.sleep(1.5)
            return
        file = items[render.start(items, 'Select a pretty file to copy to the original:', reset=False)]
        if file == return_option: return
        
        options = ["Debug", "Release"]
        orig_pos = render.position
        match(render.start(options, "Select a release version")):
            case 0:
                copy_pretty_to_original(file, debug=True)
            case 1:
                copy_pretty_to_original(file)
        render.position = orig_pos


def do_import():
    options = ["Debug", "Release"]
    orig_pos = render.position
    files, path = list(), "\\".join(__file__.split("\\")[0:-1])

    match(render.start(options, "Select a release version")):
        case 0:
            path = os.path.join(path, "localizations", "US", "Debug")
            files = [x for x  in os.listdir(path) if os.path.isfile(os.path.join(path, x))]
            import_csv_usasset(files, debug=True)
        case 1:
            path = os.path.join(path, "localizations", "US")
            files = [x for x  in os.listdir(path) if os.path.isfile(os.path.join(path, x))]
            import_csv_usasset(files)

    print("Done!")
    time.sleep(1)


def perform_discrepancy(filename: str):
    orig_name = os.path.join('localizations', 'ORG', "_".join(filename.split("_")[:2])+".csv")
    pretty_name = os.path.join('pretty_format', filename)

    original = read_orig_csv(orig_name)
    pretty = read_csv(pretty_name, is_pretty=True)

    missed = dict()

    for x in range(2,len(original)):
        if original[x][2] != "" and pretty.get(original[x][0], "") == "":
            temp = "name" if original[x][1] == "ACTOR" else "text"
            if len(missed.get(original[x][0], [])) == 0:
                missed[original[x][0]] = {temp: original[x][2]}
            else:
                missed[original[x][0]][temp] = original[x][2] 

    missed = dict(sorted(missed.items()))
    final = list()

    for k,v in missed.items():
        final.append([k,v.get("name", "NPC"),v.get("text", "NONE")])

    if not os.path.exists("discrepancies"):
        os.mkdir("discrepancies")

    if len(final) != 0:
        with open(os.path.join("discrepancies", "_".join(filename.split('_')[:2]).split('.')[0] + "_d.csv"), "w", encoding="utf-8") as file:
            writer = csv.writer(file, lineterminator="\n")
            writer.writerows(final)
        print("Discrepancies done!")
    else:
        print("No discrepancies found.")




def do_descrepancy():
    return_option = "Return"
    render.reset()
    while(True):
        items = os.listdir(os.path.join('.', 'pretty_format')) + [return_option]
        if not len(items) > 1:
            print("No files are here to copy!")
            time.sleep(1.5)
            return
        
        file = items[render.start(items, 'Select a pretty file to peform discrepancy analysis on:', reset=False)]
        if file == return_option: return

        perform_discrepancy(file)
        
        print("Done!")
        time.sleep(1)


def tool():

    options = ["Pretty format CSV", "Copy pretty format to original CSV", "Create Discrepancy File", "Import to .uassets", "Return"]
    

    while(True):
        render.start(options, "Choose an option")
        match(render.position):
            case 0:
                do_pretty_format()
            case 1:
                do_pretty_copy()
            case 2:
                do_descrepancy()
            case 3:
                do_import()
            case 4:
                return
            
        
