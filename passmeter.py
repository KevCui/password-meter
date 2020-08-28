#!/usr/bin/python3
# -*- coding: utf-8 -*-
from getpass import getpass
from rich.console import Console
from rich.table import Table
from rich.text import Text
import sys
import os
import re
import math
import argparse


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--password', nargs=1, help='Password')
    parser.add_argument('-s', '--score-only',
                        action='store_true',
                        help='Only show score number as output'
                        )
    parser.add_argument('-c', '--complexity-only',
                        action='store_true',
                        help='Only show complexity text as output'
                        )
    return parser.parse_args()


def getPassword(arguments):
    if arguments.password:
        return arguments.password[0]
    else:
        try:
            return getpass()
        except KeyboardInterrupt:
            sys.exit(1)


def calcScore(dict):
    for k in dict.keys():
        if dict[k]["count"] > 0:
            if dict[k]["score"] == 0:
                dict[k]["score"] = dict[k]["count"] * dict[k]["mult"]


def printTable(dict):
    table = Table()
    table.add_column("", style="cyan")
    table.add_column("Rate", style="white")
    table.add_column("Count", justify="right", style="yellow")
    table.add_column("Bonus", justify="right", style="green")
    for k in dict.keys():
        table.add_row(
            dict[k]["text"],
            dict[k]["rate"],
            str(dict[k]["count"]),
            setBonuscolor(dict[k]['score'])
        )
    console = Console()
    console.print(table)


def printResult(dict, option):
    score = 0
    complexity = "unknown"
    for k in dict.keys():
        score += dict[k]["score"]

    if score < 20:
        score = max(0, score)
        complexity = "Very Weak"
    if score >= 20 and score < 40:
        complexity = "Weak"
    if score >= 40 and score < 60:
        complexity = "Good"
    if score >= 60 and score < 80:
        complexity = "Strong"
    if score >= 80:
        score = min(score, 100)
        complexity = "Very Strong"

    if option.score_only:
        print(score)
    elif option.complexity_only:
        print(complexity)
    else:
        print(complexity)
        print("Score: " + str(score) + "%")
        print("Complexity: " + complexity)
        printTable(dict)


def count(dict, password, key, pattern):
    tmp = ""
    arrPwd = list(password)
    for a in range(0, dict["length"]["count"]):
        if re.match(pattern, arrPwd[a]):
            if (key == "number" or key == "symbol") \
                    and a > 0 and a < (dict["length"]["count"] - 1):
                dict["midChar"]["count"] += 1
            if tmp != "":
                if (tmp + 1) == a:
                    consecKey = "consec" + key[:1].capitalize() + key[1:]
                    if consecKey in dict.keys():
                        dict[consecKey]["count"] += 1
            tmp = a
            dict[key]["count"] += 1

    if key == "alphaLC" or key == "alphaUC" or key == "number":
        if dict[key]["count"] > 0 \
                and dict[key]["count"] < dict["length"]["count"]:
            if key == "number":
                dict[key]["mult"] = 4
            else:
                dict[key]["mult"] = 2
                dict[key]["score"] = (dict["length"]["count"] - dict[key]["count"]) * dict[key]["mult"]


def countRepChar(dict, password):
    repInc = 0
    arrPwd = list(password)
    arrPwdLen = len(arrPwd)
    for a in range(0, arrPwdLen):
        charExists = False
        for b in range(0, arrPwdLen):
            if arrPwd[a] == arrPwd[b] and a != b:
                charExists = True
                repInc += abs(arrPwdLen/(b-a))
        if charExists:
            dict["repChar"]["count"] += 1
            nUnqChar = arrPwdLen - dict["repChar"]["count"]
            repInc = math.ceil(repInc/nUnqChar) if nUnqChar else math.ceil(repInc)
    dict["repChar"]["score"] = repInc * dict["repChar"]["mult"]


def countSeq(dict, password, key, pattern):
    for s in range(0, len(pattern) - 2):
        fwd = pattern[s: s+3]
        rev = fwd[:: -1]
        if password.lower().find(fwd) != -1 \
                or password.lower().find(rev) != -1:
            dict[key]["count"] += 1


def countAlphasOnly(dict):
    if max(dict["alphaLC"]["count"], dict["alphaUC"]["count"]) > 0 \
            and max(dict["symbol"]["count"], dict["number"]["count"]) == 0:
        dict["alphasOnly"]["count"] = dict["length"]["count"]


def countNumbersOnly(dict):
    if max(dict["alphaLC"]["count"], dict["alphaUC"]["count"], dict["symbol"]["count"]) == 0 \
            and dict["number"]["count"] > 0:
        dict["numbersOnly"]["count"] = dict["length"]["count"]


def countRequirements(dict):
    minReqChars = 4
    minPwdLen = 8
    arrChars = ["alphaUC", "alphaLC", "number", "symbol"]
    for c in arrChars:
        if dict[c]["count"] > 0:
            dict["requirements"]["count"] += 1
    if dict["length"]["count"] >= minPwdLen:
        dict["requirements"]["count"] += 1
        if dict["requirements"]["count"] >= minReqChars:
            dict["requirements"]["mult"] = 2


def setBonuscolor(score):
    if score > 0:
        return Text("+" + str(score), style="green")
    if score < 0:
        return Text(str(score), style="red")
    return Text("0", style="white")


def checkWeakPassword(password):
    passwordlist = "./commonpassword.list"
    if not os.path.isfile(passwordlist):
        return
    if any(password in s for s in open(passwordlist).readlines()):
        print("Common password in " + passwordlist)
        sys.exit(1)
    else:
        return


def main():
    pwd = getPassword(parseArgs())
    checkWeakPassword(pwd)

    dictRule = {
        "length": {"count": len(pwd), "mult": 4, "score": 0, "text": "Number of Characters", "rate": "+(n*4)"},
        "alphaUC": {"count": 0, "mult": 0, "score": 0, "text": "Uppercase Letters", "rate": "+((len-n)*2)"},
        "alphaLC": {"count": 0, "mult": 0, "score": 0, "text": "Lowercase Letters", "rate": "+((len-n)*2)"},
        "number": {"count": 0, "mult": 0, "score": 0, "text": "Numbers", "rate": "+(n*4)"},
        "symbol": {"count": 0, "mult": 6, "score": 0, "text": "Symbols", "rate": "+(n*6)"},
        "midChar": {"count": 0, "mult": 2, "score": 0, "text": "Middle Numbers of Symbols", "rate": "+(n*2)"},
        "requirements": {"count": 0, "mult": 0, "score": 0, "text": "Requirements", "rate": "+(n*2)"},
        "alphasOnly": {"count": 0, "mult": -1, "score": 0, "text": "Letters Only", "rate": "-n"},
        "numbersOnly": {"count": 0, "mult": -1, "score": 0, "text": "Numbers Only", "rate": "-n"},
        "repChar": {"count": 0, "mult": -1, "score": 0, "text": "Repeat Characters", "rate": "-?"},
        "consecAlphaUC": {"count": 0, "mult": -2, "score": 0, "text": "Consecutive Uppercase Letters", "rate": "-(n*2)"},
        "consecAlphaLC": {"count": 0, "mult": -2, "score": 0, "text": "Consecutive Lowercase Letters", "rate": "-(n*2)"},
        "consecNumber": {"count": 0, "mult": -2, "score": 0, "text": "Consecutive Numbers", "rate": "-(n*2)"},
        "seqAlpha": {"count": 0, "mult": -3, "score": 0, "text": "Sequential Letters (3+)", "rate": "-(n*3)"},
        "seqNumber": {"count": 0, "mult": -3, "score": 0, "text": "Sequential Numbers (3+)", "rate": "-(n*3)"},
        "seqSymbol": {"count": 0, "mult": -3, "score": 0, "text": "Sequential Symbols (3+)", "rate": "-(n*3)"}
    }

    count(dictRule, pwd, "alphaUC", r'[A-Z]')
    count(dictRule, pwd, "alphaLC", r'[a-z]')
    count(dictRule, pwd, "number", r'[0-9]')
    count(dictRule, pwd, "symbol", r'[^a-zA-Z0-9_]')
    countRequirements(dictRule)

    countAlphasOnly(dictRule)
    countNumbersOnly(dictRule)
    countRepChar(dictRule, pwd)
    countSeq(dictRule, pwd, "seqAlpha", "abcdefghijklmnopqrstuvwxyz")
    countSeq(dictRule, pwd, "seqNumber", "01234567890")
    countSeq(dictRule, pwd, "seqSymbol", ")!@#$%^&*()")

    calcScore(dictRule)
    printResult(dictRule, parseArgs())


if __name__ == '__main__':
    main()
