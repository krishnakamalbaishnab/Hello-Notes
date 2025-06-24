# converting mongo object to pythonic dictionary

def noteEntity(item) -> dict:
    return {
        "id" : str(item["_id"]),
        "title" : item["title"],
        "description":item["desc"],
        "important" : item["important"]
    }


def notesEntity(items)->list:
    return [notesEntity(item) for item in items]