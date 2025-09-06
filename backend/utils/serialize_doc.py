from bson import ObjectId
def serialize_doc(doc):
    if hasattr(doc, "to_mongo"):  # Document or EmbeddedDocument
        d = doc.to_mongo().to_dict()
        return serialize_doc(d)  # recurse

    elif isinstance(doc, dict):
        out = {}
        for k, v in doc.items():
            if k == "_id":  # rename Mongo's _id
                out["id"] = str(v)
            else:
                out[k] = serialize_doc(v)
        return out

    elif isinstance(doc, list):
        return [serialize_doc(item) for item in doc]

    elif isinstance(doc, ObjectId):
        return str(doc)

    else:
        return doc