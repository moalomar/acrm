# By Mohammad Alomar, 27 Feb 2025.
import csv, io, json, os, zipfile


ADMINS = ['127.0.0.1']
FILE_PATH = os.path.abspath(__file__)
PROJECT_PATH = os.path.dirname(FILE_PATH)
PROJECT_NAME = os.path.basename(PROJECT_PATH)
CRS_FILE = os.path.join(PROJECT_PATH, 'data/crs.json')
WHITELIST_FILE = os.path.join(PROJECT_PATH, 'data/whitelist.json')
GROUPS_NAMES = ['🚨 Follow Up', '🚫 Ignore', '🏁 Deployed']
CRID, TITLE, STATE, ASSIGNEE, EMAIL, GROUP, COMMENT = range(7)


def load(filename: str) -> list:
    if not os.path.exists(filename):
        return []
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def dump(obj: list, filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(obj, file, indent=4)


def is_allowed(user: str) -> bool:
    return user in ADMINS + get_whitelist()


def get_crs() -> list[list[str]]:
    return load(CRS_FILE)


# RETURNS: 'INVALID_VALUE', 'OK', 'NOT_FOUND'
def patch_group(crid: str, value: str) -> str:
    if value not in GROUPS_NAMES:
        return 'INVALID_VALUE'
    crs = get_crs()
    for i, cr in enumerate(crs):
        if cr[CRID] == crid:
            cr[GROUP] = value
            del crs[i]
            crs.insert(0, cr)
            dump(crs, CRS_FILE)
            return 'OK'
    return 'NOT_FOUND'


# RETURNS: 'OK', 'NOT_FOUND'
def patch_comment(crid: str, value: str) -> str:
    crs = get_crs()
    for i, cr in enumerate(crs):
        if cr[CRID] == crid:
            cr[COMMENT] = value
            del crs[i]
            crs.insert(0, cr)
            dump(crs, CRS_FILE)
            return 'OK'
    return 'NOT_FOUND'


def get_whitelist() -> list[str]:
    return load(WHITELIST_FILE)


def whitelist_append(value: str) -> list[str]:
    whitelist = get_whitelist()
    if value not in whitelist:
        whitelist.append(value)
        dump(whitelist, WHITELIST_FILE)
    return whitelist


def whitelist_remove(value: str) -> list[str]:
    whitelist = get_whitelist()
    if value in whitelist:
        whitelist.remove(value)
        dump(whitelist, WHITELIST_FILE)
    return whitelist


# RETURNS: 'OK'
def auto_group() -> str:
    crs = get_crs()
    for i, cr in enumerate(crs):
        if cr[STATE] == 'Deployed on Production' and cr[GROUP] != GROUPS_NAMES[-1]:
            cr[GROUP] = GROUPS_NAMES[-1]
            del crs[i]
            crs.insert(0, cr)
            dump(crs, CRS_FILE)
    return 'OK'


def export_project() -> io.BytesIO:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for folder, _, files in os.walk(PROJECT_PATH):
            if os.path.basename(folder) in (PROJECT_NAME, 'data', 'static', 'templates'):    
                for filename in files:
                    filepath = os.path.join(folder, filename)
                    filepath_in_zip = os.path.relpath(filepath, PROJECT_PATH)
                    zip_file.write(filepath, filepath_in_zip)
    buffer.seek(0)
    return buffer


# RETURNS: 'INVALID_FILE', 'OK'
def import_crs(file) -> str:
    try:
        file = io.BytesIO(file)
        file = file.getvalue()
        file = file.decode('utf-8-sig')
        file = file.splitlines()
        rows = csv.reader(file)
        if next(rows) != ['Work Item Type', 'ID', 'Title', 'State', 'Assigned To']:
            raise Exception
    except:
        return 'INVALID_FILE'
    crs = get_crs()
    for row in rows:
        _, crid, title, state, assignee = row
        email = assignee.split(' ')[-1][1:-1]
        assignee = ' '.join(assignee.split(' ')[:-1])
        group = GROUPS_NAMES[0]
        comment = 'New'
        imported = [crid, title, state, assignee, email, group, comment]
        found = False
        for i, cr in enumerate(crs):
            if cr[CRID] == imported[CRID]:
                found = True
                if cr[TITLE:GROUP] != imported[TITLE:GROUP]:
                    cr = imported[:GROUP] + cr[GROUP:]
                    del crs[i]
                    crs.insert(0, cr)
                break
        if not found:
            crs.insert(0, imported)
    dump(crs, CRS_FILE)
    return 'OK'
