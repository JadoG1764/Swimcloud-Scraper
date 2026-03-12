# app/context_processors.py

def divisions_context(request):
    divisions = ["CCCAA", "CCS", "Big8"]
    return {
        "divisions": divisions,
    }
