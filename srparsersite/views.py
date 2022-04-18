from django.shortcuts import render
from srparsersite.Scripts.Formatter import formatJson, formatString
from srparsersite.Scripts.SRParser import SRParser


def index(request):
    return render(request, 'index.html', {})


def result(request):
    req = request.POST["req"]
    String = request.POST["string"]

    req = formatJson(req)

    # print(req)

    parser = SRParser(req["CFG"], req["Terminals"], req["NonTerminals"], req["Start"])
    res = parser.parse(String)
    res = formatString(res)

    return render(request, 'result.html', {"data": res})
